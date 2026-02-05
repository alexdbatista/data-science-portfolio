
# ML FEATURE ENGINEERING RECOMMENDATIONS

**Date:** February 05, 2026  
**Prepared by:** Alex Domingues Batista, PhD - Chemical Data Scientist  
**For:** ML Engineering Team

---

## 🎯 OBJECTIVE

Provide data-driven guidance for feature engineering in next-generation catalyst activity prediction models, based on analysis of 330 validated experimental measurements.

---

## 📊 CURRENT FEATURE IMPORTANCE (Random Forest)

1. **Pt_percent**: 0.517
2. **Ru_percent**: 0.172
5. **temperature_C**: 0.109
6. **pH**: 0.069
3. **Ir_percent**: 0.068
4. **surface_area_m2_g**: 0.065


**Key insights:**
- **Composition features** (Pt_percent, Ru_percent) dominate prediction
- Surface area shows moderate importance (physical property)
- Experimental conditions (temp, pH) have lower but non-zero influence

---

## 🔬 RECOMMENDED FEATURE ENGINEERING

### Priority 1: Composition-Derived Features (High Expected Value)

Based on electrochemistry literature and our data patterns:

1. **d-band center proxies:**
   - `Pt_weighted_dband = Pt% * (-2.25 eV)`
   - `Ru_weighted_dband = Ru% * (-1.05 eV)`
   - `Composite_dband = sum of weighted values`
   - **Why:** d-band theory correlates strongly with OER activity

2. **Synergy terms:**
   - `Pt_Ru_interaction = (Pt% * Ru%) / 100`
   - `Ternary_mixing = (Pt% * Ru% * Ir%) / 10000`
   - **Why:** Bimetallic synergy effects observed in data

3. **Composition ratios:**
   - `Pt_to_Ru_ratio = Pt% / (Ru% + 0.1)`
   - `Noble_metal_fraction = (Pt% + Ir%) / 100`
   - **Why:** Relative composition may matter more than absolute

### Priority 2: Surface & Structural Features (Medium Expected Value)

4. **Specific activity:**
   - `Current_density_normalized = i_0 / surface_area`
   - **Why:** Removes size effects, focuses on intrinsic activity

5. **Electrochemical surface area (ECSA):**
   - Request from lab: CV-derived ECSA measurements
   - **Why:** Better proxy than geometric surface area

### Priority 3: Non-linear Transformations

6. **Polynomial features (degree 2):**
   - `Pt%²`, `Ru%²`, cross-terms
   - **Why:** Observed non-linear trends in composition space

7. **Log-transforms for current density:**
   - `log10(i_0)`, `log10(R_ct)`
   - **Why:** Exchange current spans orders of magnitude

---

## ⚠️ DATA QUALITY FLAGS FOR ML MODELS

### Samples to EXCLUDE from training:


- 120 samples with quality issues
- Criteria: `measurement_quality == 0` OR `replicate_std > 0.03`
- CSV export: `data/ml_exclusion_list.csv`

### Temperature normalization:

Current data spans 23.9-26.3°C.

**Recommendation:** Normalize overpotential to 25°C using Nernst correction:
```python
eta_normalized = eta_measured - (T - 298.15) * 0.0008  # ~0.8 mV/K
```

---

## 🧪 EXPERIMENTAL DATA NEEDS FOR BETTER MODELS

Based on feature importance and electrochemical theory:

### High Priority (Request for Campaign 4):
1. **Electrochemical Surface Area (ECSA)** - CV-derived, for all samples
2. **Crystallite size (XRD)** - Relates to active site density
3. **Surface composition (XPS)** - May differ from bulk composition

### Medium Priority (Future):
4. **Impedance spectroscopy** - Full Nyquist plots (not just R_ct)
5. **Long-term stability** - Chronopotentiometry for top 10 catalysts
6. **pH variation** - Test best catalysts at pH 12, 13, 14

### Nice to Have:
7. **In-situ characterization** - Raman spectroscopy during OER
8. **Computational descriptors** - DFT-derived OH* binding energies

---

## 📈 MODEL PERFORMANCE TARGETS

Based on current RF baseline (R² ≈ 0.65 on Campaign 3 data):

| Model Iteration | Target R² | Target MAE | Rationale |
|-----------------|-----------|-----------|-----------|
| v1.0 (baseline) | 0.65 | 25 mV | Current performance |
| v2.0 (+engineered features) | 0.75 | 18 mV | With d-band & synergy terms |
| v3.0 (+ECSA data) | 0.80 | 15 mV | With physical characterization |
| v4.0 (+DFT descriptors) | 0.85 | 12 mV | Full multi-fidelity model |

**Success criterion:** MAE < 20 mV enables confident screening

---

## 🔄 FEEDBACK LOOP

**What's working:**
- Composition features are highly predictive ✓
- Data quality improvements enable better models ✓

**What to improve:**
- Need more physical characterization data
- Consider active learning for next campaign sample selection

**Next steps:**
1. Implement Priority 1 features in v2.0 model
2. Coordinate with lab on ECSA measurements
3. Monthly model performance review

---

*Questions on feature engineering? alexdbatista@materials-discovery.com*
