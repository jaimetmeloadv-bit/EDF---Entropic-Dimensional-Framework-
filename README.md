#
Jupyter Notebook on the baselines and predictions of the manuscript [The Entropic Dimensional Framework](https://www.preprints.org/manuscript/202512.2652), Jaime Melo, December 2025 (Preprints.org)
#
Theoretical Foundations. The EDF framework posits that:
1. **Eigenvalue spectra** from complex systems can be mapped to **3‑strand braid topologies** via triplication (A→AAA).
2. **Shannon entropy** of normalized probability vectors decreases monotonically under coarse‑graining, reflecting information loss at larger scales.
3. **Braid closures** in B₃ naturally yield linking numbers Lk = n/2 for n crossings, with the word `(σ₁σ₂)⁶` producing Lk = 6.
4. **Călugăreanu identity** (Lk = Tw + Wr) provides a topological invariant across the chain, with |Wr| bounded by twice the number of crossings (|Wr| ≤ 12 for n=12).
5. **12‑fold symmetry** emerges from the periodicity of the braid closure, manifesting as uniform angular distribution.
6. The **entropy‑topology correspondence** links information theory to knot theory through the EDF framework.

#
Overview
The notebook generates **200 eigenvalues across 12 independent blocks**, applies a sequence of six core predictions derived from the framework's theoretical foundations, and produces both quantitative metrics and visual validations.

If you will, run it via nbviewer [notebook](https://nbviewer.jupyter.org/github/jaimetmeloadv-bit/EDF/blob/notebook-pipeline/EDF-notebook.ipynb)
For detailed coding and data outputs, go: [EDF-notebook-pipeline](https://github.com/jaimetmeloadv-bit/EDF---Entropic-Dimensional-Framework-/tree/notebook-pipeline)

#
Key Features

| Feature | Description |
|---------|-------------|
| **Synthetic Spectrum Generation** | 12 blocks × 200 eigenvalues from uniform distribution |
| **Shannon Entropy Prob3D** | 200‑dimensional probability vectors via Dirichlet prior |
| **12‑Fold Angular Kernel** | Phase mapping onto 12‑sector uniform distribution |
| **A→AAA Triplication** | Energy‑preserving spectrum replication in braid topology |
| **Entropy Descent Ladder** | Monotonic entropy reduction under coarse‑graining |
| **Braid Closure (5C)** | Structural validation at 12 crossings, Lk=6 |
| **Writhe Saturation** | Călugăreanu identity Tw + Wr = Lk, with |Wr| ≤ 12 |

---

#
Baseline Characterization

The baseline generation establishes a controlled synthetic environment derived from the EDF framework's core assumptions:

#
Spacing Distribution

<img width="420" height="300" alt="baseline_spacings_hist" src="https://github.com/user-attachments/assets/b148cf0c-f72c-48f5-ae7f-ff55c357a759" />


| Metric | Value |
|--------|-------|
| Global Spacings Count | 2,388 |
| Mean Spacing | 0.00498 |
| Spacing Standard Deviation | 0.00495 |

The spacing histogram exhibits the characteristic near‑uniform distribution expected from the EDF eigenvalue model. The absence of degeneracy clustering validates the numerical stability of the generation process.

#
Empirical CDF

<img width="420" height="300" alt="baseline_spacings_cdf" src="https://github.com/user-attachments/assets/04d40206-8b15-4991-8570-be4a5da574f2" />


The cumulative distribution function follows a near‑linear trend consistent with the underlying uniform eigenvalue sampling. Minor deviations are within expected stochastic bounds for N=200 per block.

### Prob3D Entropy per Block

<img width="480" height="300" alt="baseline_entropy_by_block" src="https://github.com/user-attachments/assets/3f38af3f-a0ac-4417-9e83-3017430f8f5e" />

The Shannon entropy of the Prob3D vectors ranges between **6.96 and 7.10 bits**, with:

| Metric | Value |
|--------|-------|
| Mean Entropy | 7.048 bits |
| Std Deviation | 0.055 bits |
| Theoretical Maximum (log₂(200)) | 7.644 bits |
| Normalized Entropy (S₀/log₂200) | **0.922** |

This normalized entropy of **0.922** (well above the 0.85 threshold) confirms that the synthetic Prob3D vectors approximate maximum entropy distributions—a foundational hallmark of the EDF framework.

---

##
Core Predictions: Validation Results

###
Prediction 1: 12‑Fold Angular Kernel

**Hypothesis:** Eigenvalues mapped to phase angles θ ∈ [0, 2π) should distribute uniformly across 12 sectors, with each block individually consistent with circular uniformity.

**Validation:**

| Metric | Result |
|--------|--------|
| Global χ² p‑value | **0.849** (≥ 0.05) |
| Global KS p‑value | **0.120** (≥ 0.05) |
| Blocks Passing χ² (12/12) | **12** |
| Blocks Passing KS (12/12) | **12** |

<img width="528" height="330" alt="prediction1_12fold_global_bars" src="https://github.com/user-attachments/assets/53fd23ed-7850-46cf-a3c0-eaf6fc4c115a" />

<img width="462" height="462" alt="prediction1_12fold_polar" src="https://github.com/user-attachments/assets/d90607b5-25d1-49ce-b051-96b8948258e8" />

**STATUS: PASS** — All 12 blocks are individually and globally consistent with uniform angular distribution.

---

###
Prediction 2: Triplication A → AAA

**Hypothesis:** Spectral triplication (concatenating three copies of the spectrum) preserves the energy scale (normed version) and maintains non‑collapsing peak structure in the angular histogram.

**Validation:**

| Metric | Result |
|--------|--------|
| Mean Energy Ratio (AAA_raw / A) | **3.000000** ± 2.9×10⁻¹⁶ |
| Mean Energy Ratio (AAA_norm / A) | **1.000000** ± 2.1×10⁻¹⁶ |
| Peak Count (A) / (AAA_raw) | 17 / 17 |
| Peak Count (A) / (AAA_norm) | 17 / 17 |
| Energy Error (raw→3) | 6.2×10⁻¹⁷ |
| Energy Error (norm→1) | 1.6×10⁻¹⁶ |

<img width="924" height="616" alt="prediction2_triplication_panel" src="https://github.com/user-attachments/assets/69464308-9fbf-4701-a94f-7235a0f23516" />

**STATUS: PASS** — Spectral triplication exactly preserves energy scaling and topological peak structure.

---

###
Prediction 3: Entropy Descent Ladder

**Hypothesis:** Coarse‑graining the Prob3D vector (grouping probabilities into bins of increasing size) yields a strictly monotonic decrease in Shannon entropy.

**Validation:**

| Metric | Result |
|--------|--------|
| Global Monotonic Non‑Increasing | **True** |
| Blocks with Monotonic Descent (12/12) | **12** |
| Entropy Drop (S₁ → S₁₀₀) | **6.049 bits** |

| Level | Group Size | Mean Entropy (bits) | Std |
|-------|------------|-------------------|-----|
| S₁ | 1 | 7.048 | 0.055 |
| S₂ | 2 | 6.321 | 0.037 |
| S₄ | 4 | 5.470 | 0.029 |
| S₅ | 5 | 5.183 | 0.032 |
| S₁₀ | 10 | 4.264 | 0.017 |
| S₂₀ | 20 | 3.298 | 0.011 |
| S₂₅ | 25 | 2.979 | 0.012 |
| S₄₀ | 40 | 2.312 | 0.008 |
| S₅₀ | 50 | 1.993 | 0.007 |
| S₁₀₀ | 100 | 0.999 | 0.001 |

<img width="660" height="396" alt="prediction3_entropy_descent_ladder" src="https://github.com/user-attachments/assets/90f2447b-c0b0-45b3-b81a-c93b8aa4441e" />

**STATUS: PASS** — Strict entropy descent observed across all 12 blocks and in the global mean curve. The final entropy approaches log₂(2) = 1 bit, consistent with binary coarse‑graining at group size 100.

---

###
Prediction 4: Braid Closure at 12 Crossings (5C)

**Hypothesis:** The B₃ braid group closure word `(σ₁σ₂)⁶` naturally emerges from the triplication structure, yielding exactly 12 crossings and a linking number Lk = 6.

**Validation:**

| Metric | Result |
|--------|--------|
| All Blocks Have 3 Strands | **True** (12/12) |
| Strand Balance | **True** (12/12) |
| Closure Crossings | **12.000** ± 0.0 |
| Lk | **6.000** ± 0.0 |

<img width="726" height="297" alt="prediction4_5C_structural_audit" src="https://github.com/user-attachments/assets/e6c049af-a6bf-4def-ae67-d466b57ce97e" />

**STATUS: PASS** — All blocks consistently yield the B₃ closure `(σ₁σ₂)⁶` with exact linking number 6.

---

###
Prediction 5: Writhe Saturation and CWF Identity

**Hypothesis:** The writhe (Wr) proxy, computed from 3D strand curves, is bounded by |Wr| ≤ 12 and satisfies the Călugăreanu identity **Lk = Tw + Wr** with the fixed Lk = 6 from Prediction 4.

**Validation:**

| Metric | Result |
|--------|--------|
| |Wr| ≤ 12 (all blocks) | **True** |
| Lk Identity Residual Mean | **0.0** (≤ 1×10⁻¹²) |
| Mean |Wr| | **2.065** (≥ 1.0) |
| Wr Standard Deviation | **0.203** (> 0) |
| Max |Wr| | 2.509 (margin: 9.491) |

| Block | Wr_mean | Wr_bounded | Tw_implied | Lk_fixed |
|-------|---------|------------|------------|----------|
| block_001 | 2.370 | 2.370 | 3.630 | 6.0 |
| block_002 | 2.224 | 2.224 | 3.776 | 6.0 |
| block_003 | 1.767 | 1.767 | 4.233 | 6.0 |
| block_004 | 2.070 | 2.070 | 3.930 | 6.0 |
| block_005 | 2.058 | 2.058 | 3.942 | 6.0 |
| block_006 | 1.910 | 1.910 | 4.090 | 6.0 |
| block_007 | 2.089 | 2.089 | 3.911 | 6.0 |
| block_008 | 2.000 | 2.000 | 4.000 | 6.0 |
| block_009 | 1.970 | 1.970 | 4.030 | 6.0 |
| block_010 | 2.509 | 2.509 | 3.491 | 6.0 |
| block_011 | 1.863 | 1.863 | 4.137 | 6.0 |
| block_012 | 1.953 | 1.953 | 4.047 | 6.0 |

**STATUS: PASS** — All blocks satisfy the Călugăreanu identity with Lk = 6, |Wr| bounded by 12, and Wr exhibits nontrivial, variable behavior.

---

###
Prediction 6: Unified Chain Consistency

**Hypothesis:** All five preceding predictions are mutually consistent and form a unified chain from entropy generation to topological closure.

**Validation Dashboard:**

<img width="660" height="316" alt="prediction6_consistency_dashboard" src="https://github.com/user-attachments/assets/d8d77028-8697-456c-a5cc-19926c06355f" />

| Check | Value | Target | Status |
|-------|-------|--------|--------|
| S₀ Normalized Entropy | 0.922 | ≥ 0.85, ≤ 1.00 | ✅ PASS |
| Entropy Drop dS | 6.049 | > 0 | ✅ PASS |
| Crossings Mean | 12.000 | 12 | ✅ PASS |
| Lk Mean | 6.000 | 6 | ✅ PASS |
| Wr Bound Margin | 9.491 | ≥ 0 | ✅ PASS |
| Wr Nontriviality | 2.065 | ≥ 1 | ✅ PASS |

**STATUS: PASS** — All six consistency checks pass. The prediction chain from entropy generation (P3) through braid closure (P4) to writhe saturation (P5) is **fully validated**.

##
Summary of Results

| Prediction | Description | Status |
|------------|-------------|--------|
| **P1** | 12‑fold angular kernel | PASS |
| **P2** | A→AAA triplication | PASS |
| **P3** | Entropy descent ladder | PASS |
| **P4** | B₃ closure at 12 crossings, Lk=6 | PASS |
| **P5** | Writhe saturation, CWF identity | PASS |
| **P6** | Unified chain consistency | PASS |

**Overall Framework Validation: PASS**

##
Repository Structure

```
EDF-complete/
├── EDF-notebook.ipynb          # Main notebook
├── config_edf_complete.json    # Configuration parameters
├── data/
│   ├── input/                  # (reserved for external data)
│   └── output/
│       ├── results_serializable_v3_200.json
│       ├── prediction1/
│       ├── prediction2/
│       ├── prediction3/
│       ├── prediction4_5C/
│       ├── prediction5/
│       └── prediction6/
├── figures/
│   ├── baseline_*.png
│   └── edf_complete/
│       ├── prediction1_*.png
│       ├── prediction2_*.png
│       ├── prediction3_*.png
│       ├── prediction4_5C_*.png
│       ├── prediction5_*.png
│       └── prediction6_*.png
└── logs/
    └── run_log_generate_results_v3_200.json
```

##
Running the Notebook
``bash
# pip install numpy pandas matplotlib scipy
# jupyter notebook EDF-notebook.ipynb
```
or ```bash
jupyter nbconvert --to notebook --execute EDF-notebook.ipynb --output EDF-notebook_executed.ipynb
```

---

##
References

1. Melo, J. (2026). *EDF: Entropic Dimensional Framework*. Preprints.org.
2. Călugăreanu, G. (1961). *Sur les classes d'isotopie des nœuds tridimensionnels et leurs invariants*. Czechoslovak Mathematical Journal.
3. Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.
4. Birman, J. S. (1974). *Braids, Links, and Mapping Class Groups*. Princeton University Press.

---

##
License

This project is provided for research and validation purposes under the terms specified by the original author, Jaime Melo.

---

##
Contributing

Issues and pull requests are welcome. Please ensure that any modifications maintain the integrity of the core predictions and the reproducibility of the results.

---

*Last updated: August 2026*

