import pandas as pd
import numpy as np
import pickle
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

current_dir = os.path.dirname(os.path.abspath(__file__))
sol_path = os.path.join(current_dir, 'solubility_model.pkl')
tox_path = os.path.join(current_dir, 'toxicity_model.pkl')
bbb_path = os.path.join(current_dir, 'bbb_model.pkl')

print(f"🚀 Starting Multi-Objective Model Generation...")

# --- HELPER: Fingerprints ---
def get_fingerprint(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            return np.array(fp)
    except:
        return None
    return None

# --- 1. SOLUBILITY (Regressor) ---
print("\n💧 Training Solubility Model...")
url_esol = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"
df_esol = pd.read_csv(url_esol)

X, y = [], []
for i, row in df_esol.iterrows():
    fp = get_fingerprint(row['smiles'])
    if fp is not None:
        X.append(fp)
        y.append(row['measured log solubility in mols per litre'])

model_sol = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model_sol.fit(X, y)
with open(sol_path, 'wb') as f: pickle.dump(model_sol, f)
print("✅ Solubility Saved")

# --- 2. TOXICITY (Classifier) ---
print("\n☠️ Training Toxicity Model...")
url_tox = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/clintox.csv.gz"
df_tox = pd.read_csv(url_tox).dropna(subset=['CT_TOX'])

X, y = [], []
for i, row in df_tox.iterrows():
    fp = get_fingerprint(row['smiles'])
    if fp is not None:
        X.append(fp)
        y.append(row['CT_TOX'])

model_tox = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
model_tox.fit(X, y)
with open(tox_path, 'wb') as f: pickle.dump(model_tox, f)
print("✅ Toxicity Saved")

# --- 3. BLOOD-BRAIN BARRIER (Classifier) ---
print("\n🧠 Training BBB Model (Neuroscience)...")
# p_np: 1 = Permeable (Enters Brain), 0 = Non-Permeable
url_bbb = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"
df_bbb = pd.read_csv(url_bbb).dropna(subset=['p_np'])

X, y = [], []
for i, row in df_bbb.iterrows():
    fp = get_fingerprint(row['smiles'])
    if fp is not None:
        X.append(fp)
        y.append(row['p_np'])

model_bbb = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
model_bbb.fit(X, y)
with open(bbb_path, 'wb') as f: pickle.dump(model_bbb, f)
print("✅ BBB Saved")

print("\n✨ All 3 Models Ready.")