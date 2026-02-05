"""
Generate synthetic electrocatalyst screening data for portfolio demonstration.

This script creates realistic experimental data from multiple campaigns,
including various artifacts and quality issues that a data scientist would
need to identify and handle.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_campaign_data(campaign_id, n_samples=100, base_date='2025-01-01'):
    """
    Generate synthetic electrocatalyst screening data.
    
    Parameters:
    -----------
    campaign_id : int
        Campaign identifier
    n_samples : int
        Number of samples to generate
    base_date : str
        Starting date for the campaign
    """
    
    # Base parameters for different campaigns (learning evolution)
    campaign_params = {
        1: {'temp_drift': 0.5, 'ref_stability': 0.95, 'success_rate': 0.60},
        2: {'temp_drift': 0.3, 'ref_stability': 0.97, 'success_rate': 0.70},
        3: {'temp_drift': 0.1, 'ref_stability': 0.99, 'success_rate': 0.80}
    }
    
    params = campaign_params.get(campaign_id, campaign_params[1])
    
    # Generate sample IDs
    sample_ids = [f"CAT-{campaign_id:02d}-{i:03d}" for i in range(1, n_samples + 1)]
    
    # Generate timestamps
    start_date = datetime.strptime(base_date, '%Y-%m-%d')
    timestamps = [start_date + timedelta(hours=i*2) for i in range(n_samples)]
    
    # Generate material compositions (simplified)
    # Representing Pt-Ru-Ir ternary catalysts (percentages)
    pt_content = np.random.uniform(40, 80, n_samples)
    ru_content = np.random.uniform(10, 40, n_samples)
    ir_content = 100 - pt_content - ru_content
    
    # Generate electrochemical properties with realistic physics
    # Overpotential (η) - lower is better for catalysts
    base_overpotential = 0.35 - 0.002 * pt_content + 0.001 * ru_content
    noise = np.random.normal(0, 0.02, n_samples)
    overpotential = base_overpotential + noise
    
    # Add temperature drift artifact (improves over campaigns)
    temp_variation = np.linspace(0, params['temp_drift'], n_samples)
    overpotential += temp_variation * np.random.uniform(-0.01, 0.01, n_samples)
    
    # Tafel slope (mV/dec) - should be ~40-120 for good catalysts
    tafel_slope = 60 + 30 * np.random.randn(n_samples) + 10 * (overpotential - 0.3)
    tafel_slope = np.clip(tafel_slope, 30, 150)
    
    # Exchange current density (A/cm²) - higher is better
    log_j0 = -5 + 2 * (0.4 - overpotential) + np.random.normal(0, 0.5, n_samples)
    exchange_current = 10 ** log_j0
    
    # Charge transfer resistance (Ohm·cm²) - lower is better
    rct = 10 ** (-log_j0 - 3) * np.random.uniform(0.8, 1.2, n_samples)
    
    # Add reference electrode stability issues (improves over campaigns)
    ref_drift = np.random.binomial(1, 1 - params['ref_stability'], n_samples)
    overpotential[ref_drift == 1] += np.random.uniform(0.05, 0.15, np.sum(ref_drift))
    
    # Temperature (should be controlled at 25°C)
    temperature = 25 + np.random.normal(0, params['temp_drift'], n_samples)
    
    # pH (should be controlled at 1.0 for acidic conditions)
    ph = 1.0 + np.random.normal(0, 0.1, n_samples)
    
    # Surface area (m²/g) - affects activity
    surface_area = np.random.uniform(40, 120, n_samples)
    
    # Replicate measurements (3 per sample)
    replicate_std = np.random.uniform(0.005, 0.03, n_samples)
    
    # Quality flags
    # 1 = good, 0 = failed
    measurement_quality = np.random.binomial(1, params['success_rate'], n_samples)
    
    # Introduce missing data (equipment failures)
    missing_mask = np.random.binomial(1, 0.05, n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'sample_id': sample_ids,
        'campaign': campaign_id,
        'timestamp': timestamps,
        'Pt_percent': np.round(pt_content, 1),
        'Ru_percent': np.round(ru_content, 1),
        'Ir_percent': np.round(ir_content, 1),
        'overpotential_V': np.round(overpotential, 4),
        'tafel_slope_mV_dec': np.round(tafel_slope, 1),
        'exchange_current_A_cm2': exchange_current,
        'charge_transfer_resistance_Ohm_cm2': np.round(rct, 2),
        'surface_area_m2_g': np.round(surface_area, 1),
        'temperature_C': np.round(temperature, 2),
        'pH': np.round(ph, 2),
        'replicate_std': np.round(replicate_std, 4),
        'measurement_quality': measurement_quality,
        'operator': np.random.choice(['Alice', 'Bob', 'Charlie'], n_samples),
        'instrument_id': f'POTENTIOSTAT-{campaign_id:02d}'
    })
    
    # Apply missing data
    for col in ['overpotential_V', 'tafel_slope_mV_dec', 'exchange_current_A_cm2']:
        df.loc[missing_mask == 1, col] = np.nan
    
    # Set failed measurements to NaN
    df.loc[df['measurement_quality'] == 0, 
           ['overpotential_V', 'tafel_slope_mV_dec', 'exchange_current_A_cm2']] = np.nan
    
    return df

# Generate three campaigns with improving quality
print("Generating Campaign 1 data...")
campaign1 = generate_campaign_data(1, n_samples=120, base_date='2025-01-01')
campaign1.to_csv('data/campaign_1_results.csv', index=False)
print(f"  Saved {len(campaign1)} samples to campaign_1_results.csv")

print("\nGenerating Campaign 2 data...")
campaign2 = generate_campaign_data(2, n_samples=150, base_date='2025-02-01')
campaign2.to_csv('data/campaign_2_results.csv', index=False)
print(f"  Saved {len(campaign2)} samples to campaign_2_results.csv")

print("\nGenerating Campaign 3 data...")
campaign3 = generate_campaign_data(3, n_samples=180, base_date='2025-03-01')
campaign3.to_csv('data/campaign_3_results.csv', index=False)
print(f"  Saved {len(campaign3)} samples to campaign_3_results.csv")

print("\n✅ Data generation complete!")
print("\nData characteristics:")
print("- Campaign 1: Early stage, more artifacts, 60% success rate")
print("- Campaign 2: Improved protocols, 70% success rate")
print("- Campaign 3: Refined methods, 80% success rate")
print("\nArtifacts included:")
print("- Temperature drift (decreases over campaigns)")
print("- Reference electrode instability (improves over campaigns)")
print("- Missing data (~5% random failures)")
print("- Measurement quality flags")
print("- Replicate variability")
