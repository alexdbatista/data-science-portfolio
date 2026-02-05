# ML Feature Engineering Recommendations

**Campaign Analysis:** CAT-01 through CAT-03  
**For:** ML Engineering Team  
**From:** Alex Batista, PhD - Chemical Data Scientist  
**Date:** April 1, 2025

---

## 🎯 Purpose

Based on analysis of Campaigns 1-3, this document recommends **which experimental signals should inform ML feature design** for predictive catalyst models. Focus is on features with strong electrochemical justification and demonstrated predictive power.

---

## 📊 Feature Importance: What the Data Tells Us

### Tier 1: High-Impact Features (Include in all models)

#### 1. **Composition Features**
**Use:** Pt%, Ru%, Ir% (atomic percentages)

**Why it matters:**
- Pt content shows **strong negative correlation** with overpotential (r = -0.68)
- Ru content shows moderate positive correlation with kinetic activity
- Ir improves stability (not captured in short-term screening but critical for durability)

**Feature engineering recommendations:**
```python
# Basic features
- Pt_percent, Ru_percent, Ir_percent

# Derived features with physical meaning
- Pt_to_Ru_ratio  # Captures balance between cost and activity
- total_Pt_group_metals = Pt + Ru + Ir  # Should be ~100%, QC check
- Ru_enrichment = Ru_percent / (Pt_percent + Ru_percent)  # 0 to 1 scale
```

**Electrochemical justification:**
- Pt is the benchmark catalyst but expensive
- Ru increases intrinsic activity (lower Tafel slopes observed)
- Ir adds durability in acidic conditions

---

#### 2. **Surface Area (m²/g)**
**Use:** Measured BET surface area

**Why it matters:**
- Activity scales approximately linearly with surface area
- Models need to distinguish between intrinsic activity and geometric effects

**Feature engineering recommendations:**
```python
# Keep as direct feature (log-scale may help)
- surface_area_m2_g
- log_surface_area  # For models assuming multiplicative effects

# Derived: specific activity (area-normalized)
- specific_overpotential = overpotential / log(surface_area)
```

**Electrochemical justification:**
- More surface area → more active sites → higher current
- Need to normalize to find "best catalyst per site" not just "most surface area"

---

#### 3. **Exchange Current Density (j₀)**
**Use:** Measured electrochemically

**Why it matters:**
- Fundamental kinetic parameter (Butler-Volmer equation)
- Directly relates to catalyst intrinsic activity
- Strong correlation with overpotential (r = 0.72)

**Feature engineering recommendations:**
```python
# Use log scale (spans orders of magnitude)
- log_j0 = log10(exchange_current_A_cm2)

# Derived: kinetic barrier estimate
- activation_overpotential = (RT/F) * log(target_current / j0)  # Theoretical calculation
```

**Electrochemical justification:**
- j₀ represents rate at equilibrium potential
- Higher j₀ → faster kinetics → lower overpotential needed

---

### Tier 2: Useful Features (Include if model complexity allows)

#### 4. **Tafel Slope (mV/dec)**
**Use:** Fitted from Tafel plot

**Why it matters:**
- Indicates reaction mechanism (Volmer-Heyrovsky vs Volmer-Tafel)
- Lower slopes = better catalysts generally
- Moderate correlation with overpotential (r = 0.45)

**Feature engineering recommendations:**
```python
- tafel_slope_mV_dec  # Direct use
- tafel_category = 'low' if slope < 60 else 'med' if slope < 90 else 'high'  # Categorical
```

**Electrochemical justification:**
- Theoretical Tafel slope for single-electron transfer: 118 mV/dec (25°C)
- Lower slopes indicate more efficient electron transfer
- Very low slopes (< 40) may indicate mass transport artifacts

---

#### 5. **Charge Transfer Resistance (Rct)**
**Use:** From impedance spectroscopy (EIS)

**Why it matters:**
- Inversely related to kinetic activity
- Complements j₀ measurement (different technique, cross-validation)
- Helps identify samples with poor electrical contact

**Feature engineering recommendations:**
```python
- log_Rct = log10(charge_transfer_resistance_Ohm_cm2)
- kinetic_quality_flag = (Rct < 100)  # Flag samples with good electrical contact
```

**Electrochemical justification:**
- Rct ∝ 1/j₀ (theoretical relationship)
- High Rct → sluggish kinetics or contact issues

---

### Tier 3: Contextual Features (For quality filtering, not prediction)

#### 6. **Temperature & pH**
**Use:** Experimental conditions

**Why it matters:**
- Should be tightly controlled (Campaign 3: ±0.1°C, pH 1.0 ± 0.2)
- Large deviations indicate problematic measurements
- Include as **QC filters** rather than predictive features

**Feature engineering recommendations:**
```python
# QC flags
- temp_deviation = abs(temperature_C - 25.0)
- ph_deviation = abs(pH - 1.0)
- measurement_valid = (temp_deviation < 0.5) & (ph_deviation < 0.3)

# Don't use as predictive features (controlled variables, not material properties)
```

---

#### 7. **Replicate Variability**
**Use:** Standard deviation across replicates

**Why it matters:**
- High variability → low confidence in measurement
- Use as **uncertainty estimate**, not predictor

**Feature engineering recommendations:**
```python
- measurement_confidence = 1 / (1 + replicate_std)  # 0 to 1 scale
- high_confidence_sample = (replicate_std < 0.015)  # Boolean flag

# Weight training samples by confidence
- sample_weight = measurement_confidence  # In model training
```

---

## 🧪 Features NOT to Use (Avoid These)

### ❌ Timestamp
**Why:** No physical meaning for catalyst activity  
**Exception:** Can use for campaign/batch effects as categorical feature

### ❌ Sample ID
**Why:** Arbitrary labels, no predictive power  
**Exception:** Can extract campaign number (CAT-01-XXX → Campaign 1)

### ❌ Operator Name
**Why:** Campaign 3 data shows no operator effect (good!)  
**If operator effects existed:** Would indicate SOP problem, not material property

### ❌ Instrument ID
**Why:** Should be controlled/calibrated (systematic bias is a data quality issue, not a feature)

---

## 🎯 Recommended Feature Set for First Model

### Minimal Viable Feature Set (Start Here)
```python
features = [
    'Pt_percent',
    'Ru_percent', 
    'Ir_percent',
    'surface_area_m2_g',
    'log_j0'
]

target = 'overpotential_V'
```

**Why minimal:** Only 5 features, all have clear physical interpretation, proven correlations

**Expected performance:** R² > 0.70 based on correlation analysis

---

### Extended Feature Set (After Baseline)
```python
features = [
    # Composition
    'Pt_percent', 'Ru_percent', 'Ir_percent',
    'Pt_to_Ru_ratio',
    
    # Kinetics
    'log_j0',
    'tafel_slope_mV_dec',
    'log_Rct',
    
    # Geometry
    'surface_area_m2_g',
    'log_surface_area',
    
    # Quality indicators
    'measurement_confidence'
]

sample_weight = data['measurement_confidence']  # Weight high-quality measurements more
```

---

## 🔬 Feature Interactions to Test

Based on electrochemical theory, these interactions may be important:

```python
# Synergistic effects
- 'Pt_percent * surface_area'  # High Pt + high area = expensive but effective
- 'Ru_enrichment * log_j0'  # Ru enhances kinetics

# Composition sweet spots (non-linear)
- 'Pt_percent^2'  # Quadratic term to capture optimal range
- 'Ru_percent^2'
```

---

## 📊 Feature Validation Recommendations

### Cross-validation strategy:
1. **Campaign-based CV:** Train on Campaign 1+2, test on Campaign 3
   - Tests generalization to improved protocols
   
2. **Composition-based CV:** Hold out certain composition ranges
   - Tests interpolation vs extrapolation
   
3. **Random CV:** Standard k-fold
   - Tests overall model stability

### Feature importance analysis:
```python
# After training
- SHAP values (global and local interpretation)
- Permutation importance (which features hurt most when removed)
- Partial dependence plots (how does overpotential change with Pt%?)
```

---

## 🎯 Next Steps for ML Team

**Immediate (This Week):**
1. ✅ Implement minimal viable feature set (5 features)
2. ✅ Train baseline Random Forest / Gradient Boosting model
3. ✅ Calculate SHAP values for interpretation

**Short-term (Next 2 Weeks):**
1. Add extended features and test improvement
2. Try feature interactions
3. Implement campaign-based cross-validation

**Medium-term (Next Month):**
1. Integrate with Campaign 4 data (online learning)
2. Build confidence intervals for predictions
3. Deploy model endpoint for real-time screening

---

## 💬 Discussion Points

**Questions for ML team:**
1. What model architecture do you recommend? (Tree-based vs neural network vs linear?)
2. How should we handle missing data? (Imputation vs exclusion?)
3. What's your preferred uncertainty quantification method?

**Let's collaborate:** I can provide electrochemical interpretation of model predictions and help identify problematic features.

---

## 📧 Contact

Alex Batista, PhD  
Chemical Data Scientist  
📧 alexdbatista@gmail.com

**Data source:** Campaign 1-3 analysis  
**Code:** `/electrocatalyst-data-analysis/02_campaign_comparison_learning.ipynb`
