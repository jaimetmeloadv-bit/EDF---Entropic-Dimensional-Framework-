#!/usr/bin/env python3
"""
scripts/generate_results_v2.py

Gera um JSON 'v2' compatível com o pipeline de limpeza/analise,
incorporando critérios de saturação e mapeamento de probabilidades 3D.

Uso:
  python scripts/generate_results_v2.py --input data/results.json --out data/results_v2.json
  python scripts/generate_results_v2.py --input data/results.json data/results_clean_serializable.json --out data/results_v2.json --saturation-threshold 1e-8 --prob3d-bins 32

Saída:
  - data/results_v2.json  (JSON pronto para conversão/limpeza)
  - logs/generate_results_v2_YYYYMMDDTHHMMSSZ.log (registro)
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import datetime
import traceback
import numpy as np

def ISO_TS():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# -------------------------
# Utilitários
# -------------------------
def atomic_write(path: Path, data: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.replace(tmp, str(path))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

def safe_load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# Estatísticas e mapeamentos
# -------------------------
def compute_spacings(evals):
    ev = np.array(evals, dtype=float)
    if ev.size == 0:
        return None, None
    ev_sorted = np.sort(ev)
    if ev_sorted.size < 2:
        return None, None
    spacings = np.diff(ev_sorted)
    mean_first10 = float(np.mean(spacings[:min(10, spacings.size)])) if spacings.size>0 else None
    return spacings, mean_first10

def detect_degeneracies(spacings, deg_thresh=1e-12, tiny_thresh=1e-8):
    if spacings is None or spacings.size == 0:
        return 0, 0
    degeneracies = int(np.sum(spacings < deg_thresh))
    tiny_gaps = int(np.sum((spacings >= deg_thresh) & (spacings < tiny_thresh)))
    return degeneracies, tiny_gaps

def map_prob3d_from_evecs(evecs_array, bins=32):
    try:
        arr = np.asarray(evecs_array, dtype=np.complex128)
        dens = np.abs(arr)**2
        dens_sum = dens.sum()
        if dens_sum == 0:
            hist = np.zeros(bins, dtype=float)
        else:
            dens_flat = dens.ravel()
            maxv = float(dens_flat.max()) if dens_flat.size>0 and dens_flat.max()>0 else 1.0
            hist, _ = np.histogram(dens_flat, bins=bins, range=(0.0, maxv))
            hist = hist.astype(float)
            if hist.sum() > 0:
                hist /= hist.sum()
        nonzero = hist[hist > 0]
        entropy = float(-np.sum(nonzero * np.log(nonzero))) if nonzero.size>0 else 0.0
        return hist.tolist(), entropy
    except Exception:
        return None, None

def apply_saturation_criterion(spacings, saturation_threshold):
    if spacings is None or spacings.size == 0:
        return True, 0.0
    large = np.sum(spacings > saturation_threshold)
    frac = float(large) / float(spacings.size)
    saturated = frac < 0.05
    return bool(saturated), float(frac)

# -------------------------
# Processamento de bloco
# -------------------------
def process_block(key: str, block: dict, params: dict, logger) -> dict:
    out = {}
    try:
        evals = block.get("evals") or block.get("eigenvalues") or []
        out["N_eigs"] = int(len(evals))
        spacings, mean_first10 = compute_spacings(evals)
        out["mean_first10"] = mean_first10
        if spacings is not None:
            out["spacings_summary"] = {
                "min": float(np.min(spacings)),
                "max": float(np.max(spacings)),
                "median": float(np.median(spacings))
            }
        else:
            out["spacings_summary"] = None
        deg, tiny = detect_degeneracies(spacings, params["deg_thresh"], params["tiny_thresh"])
        out["degeneracies"] = deg
        out["tiny_gaps"] = tiny
        saturated, frac_large = apply_saturation_criterion(spacings, params["saturation_threshold"])
        out["saturated"] = saturated
        out["saturation_fraction_large_spacings"] = frac_large

        evecs_info = []
        evecs = block.get("evecs") or block.get("eigenvectors") or []
        if isinstance(evecs, dict):
            items = list(evecs.items())
        elif isinstance(evecs, list):
            items = list(enumerate(evecs))
        else:
            items = []

        max_proc = params.get("max_evecs_process", 8)
        for idx, vec in items[:max_proc]:
            arr = None
            if isinstance(vec, dict) and vec.get("__qobj__") is True:
                if "data" in vec:
                    try:
                        arr = np.array(vec["data"], dtype=np.complex128)
                    except Exception:
                        arr = None
                elif "array" in vec:
                    try:
                        arr = np.array(vec["array"], dtype=np.complex128)
                    except Exception:
                        arr = None
                elif "repr" in vec:
                    s = vec.get("repr","")
                    nums = []
                    for token in s.replace(",", " ").split():
                        try:
                            nums.append(float(token))
                        except Exception:
                            pass
                    if len(nums) > 0:
                        arr = np.array(nums, dtype=float)
            elif isinstance(vec, (list, tuple, np.ndarray)):
                try:
                    arr = np.array(vec, dtype=np.complex128)
                except Exception:
                    arr = None

            if arr is not None:
                hist, entropy = map_prob3d_from_evecs(arr, bins=params["prob3d_bins"])
                evecs_info.append({
                    "idx": int(idx),
                    "has_array": True,
                    "prob3d_histogram": hist,
                    "prob3d_entropy": entropy
                })
            else:
                evecs_info.append({
                    "idx": int(idx),
                    "has_array": False,
                    "prob3d_histogram": None,
                    "prob3d_entropy": None
                })
        out["evecs_summary"] = evecs_info
        out["meta"] = {
            "source_key": key,
            "processed_at": ISO_TS(),
            "orig_meta": block.get("meta", {})
        }
    except Exception as e:
        logger.append(f"Error processing block {key}: {repr(e)}")
        logger.append(traceback.format_exc())
        out["error"] = str(e)
    return out

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Gerar results_v2 JSON com saturação e prob3D")
    parser.add_argument("--input", "-i", nargs="+", required=True, help="Arquivos JSON de entrada (originais)")
    parser.add_argument("--out", "-o", default="data/results_v2.json", help="Caminho do JSON de saída (v2)")
    parser.add_argument("--saturation-threshold", type=float, default=1e-8, help="Limiar para considerar espaçamentos significativos")
    parser.add_argument("--deg-thresh", type=float, default=1e-12, help="Limiar para degenerescência numérica")
    parser.add_argument("--tiny-thresh", type=float, default=1e-8, help="Limiar para tiny gaps")
    parser.add_argument("--prob3d-bins", type=int, default=32, help="Número de bins para histogram prob3D")
    parser.add_argument("--max-evecs-process", type=int, default=8, help="Máximo de autovetores a processar por bloco")
    parser.add_argument("--force", action="store_true", help="Sobrescrever saída existente")
    args = parser.parse_args()

    out_path = Path(args.out)
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"generate_results_v2_{ISO_TS().replace(':','')}.log"

    logger = []
    try:
        logger.append(f"Start generate_results_v2 at {ISO_TS()}")
        logger.append(f"Inputs: {args.input}")
        logger.append(f"Output: {out_path}")
        params = {
            "saturation_threshold": args.saturation_threshold,
            "deg_thresh": args.deg_thresh,
            "tiny_thresh": args.tiny_thresh,
            "prob3d_bins": args.prob3d_bins,
            "max_evecs_process": args.max_evecs_process
        }
        logger.append(f"Params: {params}")

        merged = {}
        for p in args.input:
            pth = Path(p)
            if not pth.exists():
                logger.append(f"Input not found: {pth}")
                continue
            try:
                data = safe_load_json(pth)
                if isinstance(data, dict) and "blocks" in data and isinstance(data["blocks"], dict):
                    for k, v in data["blocks"].items():
                        merged.setdefault(k, {}).update(v if isinstance(v, dict) else {"value": v})
                else:
                    for k, v in data.items():
                        if k == "meta":
                            merged.setdefault("_global_meta", {})["meta_from_"+pth.name] = v
                        else:
                            if isinstance(v, dict):
                                merged.setdefault(k, {}).update(v)
                            else:
                                merged.setdefault(k, {})["value"] = v
            except Exception as e:
                logger.append(f"Failed to load {pth}: {repr(e)}")
                logger.append(traceback.format_exc())

        logger.append(f"Merged {len(merged)} blocks")

        results_v2 = {"meta": {"generated_at": ISO_TS(), "source_files": args.input, "params": params}, "blocks": {}}
        for key, block in merged.items():
            if key == "_global_meta":
                results_v2["meta"]["global_meta"] = block
                continue
            processed = process_block(key, block, params, logger)
            results_v2["blocks"][key] = processed

        if out_path.exists() and not args.force:
            logger.append(f"Output {out_path} exists. Use --force to overwrite.")
            atomic_write(log_path, "\n".join(logger))
            print(f"Output exists: {out_path}. Use --force to overwrite. Log: {log_path}")
            return

        atomic_write(out_path, json.dumps(results_v2, indent=2, ensure_ascii=False))
        logger.append(f"Wrote output to {out_path}")

    except Exception as e:
        logger.append(f"Fatal error: {repr(e)}")
        logger.append(traceback.format_exc())
        atomic_write(log_path, "\n".join(logger))
        raise
    finally:
        atomic_write(log_path, "\n".join(logger))
        print(f"Log gravado em: {log_path}")
        print(f"Saída gerada em: {out_path}")

if __name__ == "__main__":
    main()
