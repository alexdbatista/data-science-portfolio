#!/usr/bin/env python3
"""
Improved NASA Turbofan RUL Prediction with Enhanced Feature Engineering
Goal: Reduce RMSE from 55.54 to ~30-40 cycles
"""

import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings('ignore')

print("="*70)
print("NASA TURBOFAN RUL PREDICTION - IMPROVED FEATURE ENGINEERING")
print("="*70)

# Load data
index_names = ['unit_nr', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = [f's_{i}' for i in range(1, 22)]
col_names = index_names + setting_names + sensor_names

df = pd.read_csv('train_FD001.txt', sep='\\s+', header=None, names=col_names)

# Remove flatline sensors
useless_sensors = ['s_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19'] + setting_names
df = df.drop(columns=useless_sensors)

# Calculate RUL
max_cycles = df.groupby('unit_nr')['time_cycles'].max().reset_index()
max_cycles.columns = ['unit_nr', 'max_cycle']
df = df.merge(max_cycles, on='unit_nr', how='left')
df['RUL'] = df['max_cycle'] - df['time_cycles']

print(f"\\n✓ Data loaded: {df.shape[0]} samples, {len(df.unit_nr.unique())} engines")

# Strong sensors that showed degradation patterns
strong_sensors = ['s_2', 's_3', 's_4', 's_7', 's_11', 's_12', 's_15']

print(f"\\n🔧 ENHANCED FEATURE ENGINEERING:")
print("-" * 70)

# 1. Rolling statistics (mean, std, min, max)
print("1. Rolling window statistics (window=10)...")
for col in strong_sensors:
    df[f'{col}_roll_mean'] = df.groupby('unit_nr')[col].transform(
        lambda x: x.rolling(window=10, min_periods=1).mean()
    )
    df[f'{col}_roll_std'] = df.groupby('unit_nr')[col].transform(
        lambda x: x.rolling(window=10, min_periods=1).std().fillna(0)
    )
    df[f'{col}_roll_min'] = df.groupby('unit_nr')[col].transform(
        lambda x: x.rolling(window=10, min_periods=1).min()
    )
    df[f'{col}_roll_max'] = df.groupby('unit_nr')[col].transform(
        lambda x: x.rolling(window=10, min_periods=1).max()
    )

# 2. Lag features (previous cycle values)
print("2. Lag features (t-5, t-10)...")
for col in strong_sensors:
    df[f'{col}_lag5'] = df.groupby('unit_nr')[col].shift(5).fillna(method='bfill')
    df[f'{col}_lag10'] = df.groupby('unit_nr')[col].shift(10).fillna(method='bfill')

# 3. Rate of change (degradation speed)
print("3. Rate of change features...")
for col in strong_sensors:
    df[f'{col}_diff'] = df.groupby('unit_nr')[col].diff().fillna(0)

# 4. Cumulative statistics
print("4. Cumulative features...")
for col in strong_sensors:
    df[f'{col}_cumsum'] = df.groupby('unit_nr')[col].cumsum()
    df[f'{col}_cummax'] = df.groupby('unit_nr')[col].cummax()

# 5. Time-based features
print("5. Engine operating time features...")
df['time_normalized'] = df.groupby('unit_nr')['time_cycles'].transform(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
df['cycles_squared'] = df['time_cycles'] ** 2

print(f"\\n✓ Feature engineering complete!")
print(f"   Original features: {len(strong_sensors)}")
print(f"   Total features now: {df.shape[1] - 4}")  # -4 for unit_nr, time_cycles, max_cycle, RUL

# Train/test split (by engine, not random)
train_engines = sorted(df.unit_nr.unique())[:80]
test_engines = sorted(df.unit_nr.unique())[80:]

train_df = df[df.unit_nr.isin(train_engines)].copy()
test_df = df[df.unit_nr.isin(test_engines)].copy()

# Prepare features
feature_cols = [col for col in df.columns if col not in ['unit_nr', 'time_cycles', 'max_cycle', 'RUL']]
X_train = train_df[feature_cols]
y_train = train_df['RUL']
X_test = test_df[feature_cols]
y_test = test_df['RUL']

print(f"\\n📊 DATASET SPLIT:")
print(f"   Training: {len(train_engines)} engines, {len(X_train)} samples")
print(f"   Test: {len(test_engines)} engines, {len(X_test)} samples")
print(f"   Features: {len(feature_cols)}")

# Model 1: Random Forest (baseline for comparison)
print(f"\\n🌲 MODEL 1: Random Forest (Baseline)")
print("-" * 70)
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,  # Increased from 10
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"RMSE: {rmse_rf:.2f} cycles")
print(f"MAE: {mae_rf:.2f} cycles")
print(f"R²: {r2_rf:.3f}")

# Model 2: Gradient Boosting (typically better for this task)
print(f"\\n🚀 MODEL 2: Gradient Boosting")
print("-" * 70)
gb_model = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    random_state=42
)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))
mae_gb = mean_absolute_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

print(f"RMSE: {rmse_gb:.2f} cycles")
print(f"MAE: {mae_gb:.2f} cycles")
print(f"R²: {r2_gb:.3f}")

# Comparison
print(f"\\n{'='*70}")
print("📊 PERFORMANCE COMPARISON")
print(f"{'='*70}")
print(f"\\n{'Metric':<20} {'Original':<15} {'RF Enhanced':<15} {'GB Enhanced':<15} {'Best':<10}")
print("-" * 70)
print(f"{'RMSE (cycles)':<20} {55.54:<15.2f} {rmse_rf:<15.2f} {rmse_gb:<15.2f} {'GB' if rmse_gb < rmse_rf else 'RF':<10}")
print(f"{'MAE (cycles)':<20} {39.32:<15.2f} {mae_rf:<15.2f} {mae_gb:<15.2f} {'GB' if mae_gb < mae_rf else 'RF':<10}")
print(f"{'R² Score':<20} {0.486:<15.3f} {r2_rf:<15.3f} {r2_gb:<15.3f} {'GB' if r2_gb > r2_rf else 'RF':<10}")

improvement_rmse = ((55.54 - min(rmse_rf, rmse_gb)) / 55.54) * 100
print(f"\\n✨ IMPROVEMENT: {improvement_rmse:.1f}% reduction in RMSE")

if min(rmse_rf, rmse_gb) < 40:
    print("\\n✅ SUCCESS: Achieved target RMSE < 40 cycles!")
else:
    print(f"\\n⚠️  Close! RMSE {min(rmse_rf, rmse_gb):.2f} (target was <40)")

# Feature importance from best model
best_model = gb_model if rmse_gb < rmse_rf else rf_model
best_name = "Gradient Boosting" if rmse_gb < rmse_rf else "Random Forest"

importances = pd.DataFrame({
    'feature': feature_cols,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\\n🔍 TOP 10 FEATURES ({best_name}):")
print("-" * 70)
for i, row in importances.head(10).iterrows():
    print(f"{row['feature']:<30} {row['importance']:.4f}")

print(f"\\n{'='*70}")
print("✅ ANALYSIS COMPLETE")
print(f"{'='*70}")
print(f"\\nBest Model: {best_name}")
print(f"Final RMSE: {min(rmse_rf, rmse_gb):.2f} cycles")
print(f"As % of lifespan: {min(rmse_rf, rmse_gb)/200*100:.1f}%")
print(f"\\nReady to update README with new results!")
