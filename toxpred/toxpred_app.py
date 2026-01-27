import pickle
import os
import requests
import streamlit as st
import numpy as np
import matplotlib
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
import rdkit.Chem.Descriptors as Descriptors

# Set backend to avoid GUI crashes
matplotlib.use('Agg')

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="ToxPred AI: Enterprise Edition", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional look
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stMetric {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. MODEL LOADING ---
@st.cache_resource
def load_models():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    paths = {
        'sol': os.path.join(current_dir, 'solubility_model.pkl'),
        'tox': os.path.join(current_dir, 'toxicity_model.pkl'),
        'bbb': os.path.join(current_dir, 'bbb_model.pkl')
    }
    models = {}
    for name, path in paths.items():
        try:
            with open(path, 'rb') as f:
                models[name] = pickle.load(f)
        except:
            models[name] = None
    return models

models = load_models()

# --- 3. HELPER FUNCTIONS ---
def calculate_druggability_score(res):
    """Calculate overall druggability score (0-100)"""
    score = 0
    max_score = 100
    
    # Lipinski Rules (40 points - 10 each)
    if res.get('MolWeight', 600) < 500: score += 10
    if res.get('LogP', 6) < 5: score += 10
    if res.get('HBDonors', 10) < 5: score += 10
    if res.get('HBAcceptors', 15) < 10: score += 10
    
    # Veber Rules (20 points - 10 each)
    if res.get('TPSA', 200) <= 140: score += 10
    if res.get('RotBonds', 15) <= 10: score += 10
    
    # Solubility (15 points)
    logs = res.get('LogS', -10)
    if logs > -2: score += 15
    elif logs > -4: score += 10
    elif logs > -6: score += 5
    
    # Toxicity (15 points)
    tox_prob = res.get('Tox_Prob', 0)
    if tox_prob > 0.7: score += 15
    elif tox_prob > 0.5: score += 10
    elif tox_prob > 0.3: score += 5
    
    # BBB (10 points - bonus/penalty based on TPSA)
    tpsa = res.get('TPSA', 200)
    if tpsa < 90: score += 10  # Good for CNS drugs
    elif tpsa < 140: score += 5  # Moderate
    
    return min(score, max_score)

# --- 4. ANALYSIS LOGIC ---
def analyze_compound(compound_name, is_smiles=False):
    result = {"Compound": compound_name}
    smiles = None
    
    try:
        # If input is SMILES, use it directly
        if is_smiles:
            smiles = compound_name
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                result["SMILES"] = smiles
                result["CID"] = None
            else:
                result["Status"] = "Invalid SMILES structure"
                return result
        else:
            # Query PubChem for compound name
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/IsomericSMILES,CanonicalSMILES,ConnectivitySMILES,SMILES/JSON"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                props = data['PropertyTable']['Properties'][0]
                
                # Find Best SMILES
                smiles = next((props[k] for k in ['IsomericSMILES', 'CanonicalSMILES', 'SMILES'] if k in props), None)
                result["SMILES"] = smiles
                result["CID"] = props.get('CID', None)
            else:
                result["Status"] = "Compound not found in PubChem"
                return result
        
        if smiles and (mol := Chem.MolFromSmiles(smiles)):
                # --- A. CALCULATED PROPERTIES (RDKit) ---
                result["MolWeight"] = Descriptors.MolWt(mol)
                result["LogP"] = Descriptors.MolLogP(mol)
                result["HBDonors"] = Descriptors.NumHDonors(mol)
                result["HBAcceptors"] = Descriptors.NumHAcceptors(mol)
                result["RotBonds"] = Descriptors.NumRotatableBonds(mol)
                result["TPSA"] = Descriptors.TPSA(mol)
                result["MolFormula"] = Descriptors.rdMolDescriptors.CalcMolFormula(mol)
                result["Status"] = "OK"

                # --- B. AI PREDICTIONS (Random Forest) ---
                # 1. Generate Morgan Fingerprint (2048 bits)
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                fp_array = np.array(fp).reshape(1, -1)

                # 2. Run Models
                # Solubility
                if models['sol']:
                    pred = models['sol'].predict(fp_array)[0]
                    result["LogS"] = pred
                    result["Sol_Class"] = "High" if pred > -2 else "Medium" if pred > -4 else "Low"
                
                # Toxicity
                if models['tox']:
                    prob = models['tox'].predict_proba(fp_array)[0][1]
                    result["Tox_Prob"] = prob
                    result["Tox_Class"] = "Safe" if prob > 0.6 else "Toxic"

                # BBB (Brain)
                if models['bbb']:
                    prob_bbb = models['bbb'].predict_proba(fp_array)[0][1]
                    result["BBB_Prob"] = prob_bbb
                    result["BBB_Class"] = "Permeable" if prob_bbb > 0.5 else "Impermeable"
        else:
            result["Status"] = "Invalid SMILES structure"
            
    except Exception as e:
        result["Status"] = f"Error: {str(e)}"
    
    return result

# --- 5. SIDEBAR INFO ---
with st.sidebar:
    st.header("📘 Methodology & Models")
    
    st.markdown("### 🧠 The AI Engine")
    st.info("""
    **Algorithm:** Random Forest Ensemble (Scikit-Learn).
    **Features:** Morgan Fingerprints (ECFP4), radius 2, 2048 bits.
    """)
    
    st.markdown("### 📊 Model Performance")
    st.write("**1. Solubility (Regression)**")
    st.caption("Training Data: ESOL (Delaney)")
    st.progress(0.87, text="R² Score: 0.87")
    
    st.write("**2. Toxicity (Classification)**")
    st.caption("Training Data: ClinTox (FDA)")
    st.progress(0.76, text="Accuracy: 76%")
    
    st.write("**3. Blood-Brain Barrier**")
    st.caption("Training Data: BBBP")
    st.progress(0.85, text="ROC-AUC: 0.85")
    
    st.markdown("---")
    st.caption("Built with Python, RDKit & Streamlit.")

# --- 6. MAIN UI ---
st.title("🧬 ToxPred AI: In-Silico Screening")
st.markdown("""
**Accelerate Drug Discovery.** Predict physicochemical properties, toxicity risks, and brain penetration using advanced Machine Learning.
""")

# Example compounds
st.markdown("**Quick Examples:**")
col_ex1, col_ex2, col_ex3, col_ex4, col_ex5 = st.columns(5)
with col_ex1:
    if st.button("💊 Aspirin", use_container_width=True):
        st.session_state['compound_input'] = 'Aspirin'
        st.session_state['input_mode'] = 'name'
with col_ex2:
    if st.button("☕ Caffeine", use_container_width=True):
        st.session_state['compound_input'] = 'Caffeine'
        st.session_state['input_mode'] = 'name'
with col_ex3:
    if st.button("💉 Morphine", use_container_width=True):
        st.session_state['compound_input'] = 'Morphine'
        st.session_state['input_mode'] = 'name'
with col_ex4:
    if st.button("🩸 Warfarin", use_container_width=True):
        st.session_state['compound_input'] = 'Warfarin'
        st.session_state['input_mode'] = 'name'
with col_ex5:
    if st.button("🧪 Dopamine", use_container_width=True):
        st.session_state['compound_input'] = 'Dopamine'
        st.session_state['input_mode'] = 'name'

st.markdown("---")

# Input mode toggle
input_mode = st.radio("Input Type:", ["Compound Name", "SMILES String"], horizontal=True, key='input_mode_radio')
is_smiles = input_mode == "SMILES String"

# Get default value from session state
default_value = st.session_state.get('compound_input', 'Aspirin' if not is_smiles else 'CC(=O)Oc1ccccc1C(=O)O')

col_search, col_btn = st.columns([3, 1])
with col_search:
    if is_smiles:
        compound_name = st.text_input("Enter SMILES (e.g., CC(=O)Oc1ccccc1C(=O)O for Aspirin)", 
                                     value=default_value if st.session_state.get('input_mode') == 'smiles' else 'CC(=O)Oc1ccccc1C(=O)O')
    else:
        compound_name = st.text_input("Enter Chemical Name (e.g., Aspirin, Dopamine, Dieldrin)", 
                                     value=default_value if st.session_state.get('input_mode') == 'name' else 'Aspirin')
with col_btn:
    st.write("")
    st.write("")
    run_btn = st.button("🚀 Analyze Molecule", type="primary", use_container_width=True)

if run_btn:
    spinner_text = f"Computing Molecular Fingerprints for {compound_name}..." if is_smiles else f"Querying PubChem & Computing Fingerprints for {compound_name}..."
    with st.spinner(spinner_text):
        res = analyze_compound(compound_name, is_smiles=is_smiles)
        
        if res["Status"] == "OK":
            # --- OVERALL SCORE ---
            druggability = calculate_druggability_score(res)
            
            # Color coding for score
            if druggability >= 80:
                score_color = "🟢"
                score_label = "Excellent Drug Candidate"
            elif druggability >= 60:
                score_color = "🟡"
                score_label = "Good Drug Candidate"
            elif druggability >= 40:
                score_color = "🟠"
                score_label = "Moderate Potential"
            else:
                score_color = "🔴"
                score_label = "Poor Drug Candidate"
            
            st.markdown(f"### {score_color} Overall Druggability Score: **{druggability}/100** - {score_label}")
            st.progress(druggability / 100)
            
            # Molecular Info Row
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown(f"**Molecular Formula:** {res.get('MolFormula', 'N/A')}")
            with info_col2:
                st.markdown(f"**SMILES:** `{res['SMILES'][:50]}{'...' if len(res['SMILES']) > 50 else ''}`")
            
            st.markdown("---")
            
            # --- RESULTS LAYOUT ---
            
            # TOP SECTION: Structure & Key Links
            c_left, c_right = st.columns([1, 2])
            
            with c_left:
                st.subheader("Structure")
                mol = Chem.MolFromSmiles(res["SMILES"])
                st.image(Draw.MolToImage(mol, size=(350, 350)), caption="2D Chemical Structure")
                if res.get("CID"):
                    st.link_button("View on PubChem ↗", f"https://pubchem.ncbi.nlm.nih.gov/compound/{res['CID']}", use_container_width=True)

            with c_right:
                st.subheader("🤖 AI-Driven ADMET Profile")
                
                # METRICS ROW 1: The Predictions
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    st.metric("Solubility (LogS)", f"{res.get('LogS',0):.2f}", res.get('Sol_Class',''))
                    st.caption("Log Molar Solubility. > -2 is good.")

                with m2:
                    tox_c = res.get('Tox_Class', '')
                    tox_p = res.get('Tox_Prob', 0)
                    st.metric("Clinical Toxicity", tox_c, f"{tox_p:.0%} Safe")
                    st.caption("Probability of FDA Approval vs Failure.")

                with m3:
                    bbb_c = res.get('BBB_Class', '')
                    bbb_p = res.get('BBB_Prob', 0)
                    st.metric("Brain Barrier (BBB)", bbb_c, f"{bbb_p:.0%} Prob.")
                    st.caption("Can it cross into the brain?")

                st.markdown("---")

                # METRICS ROW 2: Drug Likeness (Lipinski)
                st.subheader("💊 Drug-Likeness (Lipinski Rules)")
                
                # Check Rules
                fails = 0
                r_mw = res['MolWeight'] < 500
                r_logp = res['LogP'] < 5
                r_hbd = res['HBDonors'] < 5
                r_hba = res['HBAcceptors'] < 10
                if not r_mw: fails += 1
                if not r_logp: fails += 1
                if not r_hbd: fails += 1
                if not r_hba: fails += 1

                l1, l2, l3, l4 = st.columns(4)
                l1.metric("MW", f"{res['MolWeight']:.0f}", "Pass (<500)" if r_mw else "Fail")
                l2.metric("LogP", f"{res['LogP']:.2f}", "Pass (<5)" if r_logp else "Fail")
                l3.metric("H-Donors", res['HBDonors'], "Pass (<5)" if r_hbd else "Fail")
                l4.metric("H-Accept", res['HBAcceptors'], "Pass (<10)" if r_hba else "Fail")

                if fails == 0: st.success("✨ **Excellent Candidate:** Follows all Lipinski rules for oral drugs.")
                elif fails == 1: st.warning("⚠️ **Warning:** Violates 1 Lipinski rule.")
                else: st.error(f"❌ **Poor Candidate:** Violates {fails} Lipinski rules (likely poor absorption).")
                
                st.markdown("---")
                
                # Veber Rules
                st.subheader("📋 Veber Rules (Oral Bioavailability)")
                veber_tpsa = res['TPSA'] <= 140
                veber_rot = res['RotBonds'] <= 10
                veber_pass = veber_tpsa and veber_rot
                
                v1, v2 = st.columns(2)
                v1.metric("TPSA ≤ 140 Ų", "✓ Pass" if veber_tpsa else "✗ Fail", f"{res['TPSA']:.1f} Ų")
                v2.metric("Rotatable Bonds ≤ 10", "✓ Pass" if veber_rot else "✗ Fail", f"{res['RotBonds']} bonds")
                
                if veber_pass:
                    st.success("✅ **Veber Compliant:** High probability of oral bioavailability")
                else:
                    st.warning("⚠️ **Veber Non-Compliant:** May have reduced oral bioavailability")
                
                st.markdown("---")
                st.subheader("🔬 Additional Physicochemical Properties")
                
                # Additional metrics
                a1, a2 = st.columns(2)
                
                with a1:
                    tpsa_val = res['TPSA']
                    tpsa_status = "Excellent" if tpsa_val < 90 else "Good" if tpsa_val < 140 else "Poor"
                    st.metric("TPSA (Polar Surface Area)", f"{tpsa_val:.1f} Ų", tpsa_status)
                    if tpsa_val < 90:
                        st.caption("✓ Likely BBB permeable & good oral absorption")
                    elif tpsa_val < 140:
                        st.caption("✓ Good oral absorption, limited BBB penetration")
                    else:
                        st.caption("⚠ May have poor membrane permeability")
                
                with a2:
                    rot_bonds = res['RotBonds']
                    rot_status = "Rigid" if rot_bonds < 5 else "Flexible" if rot_bonds < 10 else "Very Flexible"
                    st.metric("Rotatable Bonds", rot_bonds, rot_status)
                    if rot_bonds < 10:
                        st.caption("✓ Good oral bioavailability expected")
                    else:
                        st.caption("⚠ High flexibility may reduce bioavailability")

            # --- DEEP DIVE SECTION ---
            st.markdown("---")
            with st.expander("🔍 Deep Dive: Parameter Explanations & Importance", expanded=False):
                tpsa_val = res['TPSA']
                st.markdown(f"""
                ### 🔍 Physiological Gatekeepers: Why These Numbers Matter

                #### 1. LogP (Lipophilicity / The "Grease" Factor)
                * **What is it?** A measure of how a molecule distributes between oil and water.
                * **Clinical Insight:** * **Low LogP (< 0):** Highly hydrophilic. These molecules stay in the blood and are rapidly cleared by the kidneys.
                    * **High LogP (> 5):** Highly lipophilic. These can bioaccumulate in fat tissues.
                    * **The "Sweet Spot":** 1 to 5 allows for **passive diffusion** while maintaining solubility.



                #### 2. TPSA (Topological Polar Surface Area)
                * **Current Value:** **{tpsa_val:.1f} Å²**
                * **What is it?** The sum of the surface area of all polar atoms (Oxygen, Nitrogen, etc.).
                * **Clinical Insight:** * **Cell Permeability:** Values **< 140 Å²** are generally required for gut absorption.
                    * **Neuro-Access:** Values **< 90 Å²** are the standard for crossing the **Blood-Brain Barrier (BBB)**.



                #### 3. LogS (Aqueous Solubility)
                * **What is it?** The baseline ability of the drug to dissolve in water.
                * **Clinical Insight:** If a drug cannot dissolve (LogS < -6), it cannot be absorbed, regardless of its potency.

                #### 4. Blood-Brain Barrier (BBB) Penetration
                * **The Strategy:**
                    * **Targeted Design:** Necessary for CNS drugs (e.g., antidepressants).
                    * **Side Effect Mitigation:** For heart or stomach medication, crossing the BBB is often a "fail" as it leads to central side effects like drowsiness.
                """)

        else:
            st.error(f"Analysis Failed: {res['Status']}")