"""
GuardianCGM: Module 05 - Production Drift Monitoring & Alerting System

Author: Alex Domingues Batista, PhD

Purpose:
--------
Production-ready drift monitoring system for continuous glucose monitoring (CGM) 
prediction models. Detects statistical drift, performance degradation, and bias 
drift to trigger retraining alerts before clinical safety is compromised.

Regulatory Context:
-------------------
- FDA 21 CFR Part 820: Quality System Regulation requires performance monitoring
- EU MDR (2017/745): Post-Market Clinical Follow-up (PMCF) mandates continuous surveillance
- ISO 13485: Medical device quality management requires trending and corrective action
- ISO/IEC TR 24027:2021: Bias monitoring in AI systems

Key Features:
-------------
1. Statistical Drift Detection (Kolmogorov-Smirnov, Population Stability Index)
2. Performance Degradation Monitoring (RMSE, MAE, Clarke Error Grid)
3. Bias Drift Tracking (demographic subgroup performance)
4. Data Quality Checks (missing values, outliers, sensor artifacts)
5. Multi-Level Alerting (warning, critical, retraining required)
6. Audit Logging for regulatory compliance
7. Automated reporting for PMCF submissions

Usage:
------
    from drift_monitoring import DriftMonitor
    
    monitor = DriftMonitor(
        model_path='models/glucose_rf_v1.pkl',
        reference_data_path='data/processed_biomarkers.csv'
    )
    
    # Monitor new batch of data
    alerts = monitor.check_drift(new_data)
    
    # Generate regulatory report
    monitor.generate_pmcf_report(output_path='reports/pmcf_monthly.pdf')

"""

import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from scipy import stats
import json
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# Configuration Classes
# ============================================================================

@dataclass
class MonitoringThresholds:
    """Configurable thresholds for drift detection and alerting."""
    
    # Performance thresholds
    rmse_warning: float = 7.0  # mg/dL
    rmse_critical: float = 9.0  # mg/dL
    mae_warning: float = 5.5  # mg/dL
    mae_critical: float = 7.0  # mg/dL
    clarke_ab_min: float = 95.0  # % in zones A+B (FDA threshold)
    
    # Statistical drift thresholds
    ks_test_alpha: float = 0.01  # Kolmogorov-Smirnov significance level
    psi_warning: float = 0.10  # Population Stability Index
    psi_critical: float = 0.25
    
    # Bias drift thresholds
    subgroup_rmse_disparity_max: float = 2.0  # mg/dL difference
    
    # Data quality thresholds
    missing_rate_max: float = 0.05  # 5% missing values
    outlier_rate_max: float = 0.02  # 2% outliers
    
    # Retraining trigger conditions (any one triggers alert)
    retraining_required_if: List[str] = None
    
    def __post_init__(self):
        if self.retraining_required_if is None:
            self.retraining_required_if = [
                'rmse_critical_exceeded',
                'clarke_ab_below_threshold',
                'multiple_critical_alerts'
            ]


@dataclass
class DriftAlert:
    """Structure for drift detection alerts."""
    timestamp: str
    severity: str  # 'INFO', 'WARNING', 'CRITICAL', 'RETRAINING_REQUIRED'
    category: str  # 'PERFORMANCE', 'STATISTICAL_DRIFT', 'BIAS_DRIFT', 'DATA_QUALITY'
    metric: str
    value: float
    threshold: float
    message: str
    metadata: Dict = None


# ============================================================================
# Main Drift Monitoring Class
# ============================================================================

class DriftMonitor:
    """
    Production drift monitoring system for CGM prediction models.
    
    Monitors model performance, statistical drift, bias evolution, and data quality
    to detect when retraining is required. Logs all findings for regulatory compliance.
    """
    
    def __init__(
        self,
        model_path: str,
        reference_data_path: str,
        thresholds: MonitoringThresholds = None,
        log_dir: str = 'logs',
        report_dir: str = 'reports'
    ):
        """
        Initialize drift monitoring system.
        
        Parameters
        ----------
        model_path : str
            Path to trained model (.pkl file)
        reference_data_path : str
            Path to reference dataset (training data with features)
        thresholds : MonitoringThresholds, optional
            Custom monitoring thresholds
        log_dir : str
            Directory for audit logs
        report_dir : str
            Directory for PMCF reports
        """
        self.model_path = Path(model_path)
        self.reference_data_path = Path(reference_data_path)
        self.thresholds = thresholds or MonitoringThresholds()
        self.log_dir = Path(log_dir)
        self.report_dir = Path(report_dir)
        
        # Create directories
        self.log_dir.mkdir(exist_ok=True)
        self.report_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Load model and reference data
        self.model = self._load_model()
        self.reference_data = self._load_reference_data()
        
        # Feature columns (must match training)
        self.feature_cols = [
            'glucose_raw', 'glucose_smooth', 'velocity', 'acceleration',
            'volatility_1h', 'lag_15m', 'lag_30m', 'lag_60m'
        ]
        
        # Alert history
        self.alert_history: List[DriftAlert] = []
        
        self.logger.info("DriftMonitor initialized successfully")
        self.logger.info(f"Model: {self.model_path}")
        self.logger.info(f"Reference data: {self.reference_data_path}")
    
    def _setup_logging(self):
        """Configure audit logging for regulatory compliance."""
        log_file = self.log_dir / f"drift_monitor_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_model(self):
        """Load trained model."""
        try:
            model = joblib.load(self.model_path)
            self.logger.info(f"Model loaded: {type(model).__name__}")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def _load_reference_data(self) -> pd.DataFrame:
        """Load reference dataset for drift comparison."""
        try:
            df = pd.read_csv(self.reference_data_path)
            self.logger.info(f"Reference data loaded: {len(df)} samples")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load reference data: {e}")
            raise
    
    # ========================================================================
    # Main Drift Checking Interface
    # ========================================================================
    
    def check_drift(
        self,
        new_data: pd.DataFrame,
        demographic_cols: Optional[List[str]] = None
    ) -> Dict:
        """
        Comprehensive drift check on new production data.
        
        Parameters
        ----------
        new_data : pd.DataFrame
            New data batch with features and true glucose values
        demographic_cols : List[str], optional
            Columns for subgroup analysis (e.g., ['age_group', 'bmi_category'])
        
        Returns
        -------
        Dict
            Drift report with alerts, metrics, and retraining recommendation
        """
        self.logger.info("="*80)
        self.logger.info("DRIFT MONITORING CHECK INITIATED")
        self.logger.info(f"New data batch: {len(new_data)} samples")
        self.logger.info("="*80)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'n_samples': len(new_data),
            'alerts': [],
            'metrics': {},
            'retraining_required': False,
            'summary': ''
        }
        
        try:
            # 1. Data Quality Checks
            self.logger.info("\n[1/5] Running data quality checks...")
            quality_alerts = self._check_data_quality(new_data)
            report['alerts'].extend(quality_alerts)
            
            # 2. Statistical Drift Detection
            self.logger.info("\n[2/5] Running statistical drift detection...")
            drift_alerts = self._check_statistical_drift(new_data)
            report['alerts'].extend(drift_alerts)
            
            # 3. Performance Monitoring
            self.logger.info("\n[3/5] Running performance monitoring...")
            perf_metrics, perf_alerts = self._check_performance(new_data)
            report['metrics']['performance'] = perf_metrics
            report['alerts'].extend(perf_alerts)
            
            # 4. Bias Drift Monitoring
            if demographic_cols and all(col in new_data.columns for col in demographic_cols):
                self.logger.info("\n[4/5] Running bias drift monitoring...")
                bias_alerts = self._check_bias_drift(new_data, demographic_cols)
                report['alerts'].extend(bias_alerts)
            else:
                self.logger.info("\n[4/5] Skipping bias drift (no demographic data)")
            
            # 5. Retraining Decision
            self.logger.info("\n[5/5] Evaluating retraining necessity...")
            report['retraining_required'] = self._evaluate_retraining_need(report['alerts'])
            
            # Store alerts in history
            self.alert_history.extend(report['alerts'])
            
            # Generate summary
            report['summary'] = self._generate_summary(report)
            
            # Log final report
            self._log_report(report)
            
            return report
        
        except Exception as e:
            self.logger.error(f"Drift check failed: {e}")
            raise
    
    # ========================================================================
    # Data Quality Checks
    # ========================================================================
    
    def _check_data_quality(self, data: pd.DataFrame) -> List[DriftAlert]:
        """Check for data quality issues."""
        alerts = []
        
        # Missing values
        missing_rate = data[self.feature_cols].isnull().sum().sum() / (len(data) * len(self.feature_cols))
        if missing_rate > self.thresholds.missing_rate_max:
            alert = DriftAlert(
                timestamp=datetime.now().isoformat(),
                severity='WARNING',
                category='DATA_QUALITY',
                metric='missing_rate',
                value=missing_rate,
                threshold=self.thresholds.missing_rate_max,
                message=f"Missing data rate {missing_rate:.1%} exceeds threshold {self.thresholds.missing_rate_max:.1%}",
                metadata={'affected_features': data[self.feature_cols].isnull().sum().to_dict()}
            )
            alerts.append(alert)
            self.logger.warning(alert.message)
        else:
            self.logger.info(f"✓ Missing data rate: {missing_rate:.1%} (OK)")
        
        # Outlier detection (Z-score > 4)
        z_scores = np.abs(stats.zscore(data[self.feature_cols].select_dtypes(include=[np.number]).dropna()))
        outlier_rate = (z_scores > 4).sum().sum() / z_scores.size
        if outlier_rate > self.thresholds.outlier_rate_max:
            alert = DriftAlert(
                timestamp=datetime.now().isoformat(),
                severity='WARNING',
                category='DATA_QUALITY',
                metric='outlier_rate',
                value=outlier_rate,
                threshold=self.thresholds.outlier_rate_max,
                message=f"Outlier rate {outlier_rate:.1%} exceeds threshold {self.thresholds.outlier_rate_max:.1%}",
                metadata={'outlier_count': int((z_scores > 4).sum().sum())}
            )
            alerts.append(alert)
            self.logger.warning(alert.message)
        else:
            self.logger.info(f"✓ Outlier rate: {outlier_rate:.1%} (OK)")
        
        # Sensor range check (glucose should be 40-400 mg/dL)
        if 'glucose_raw' in data.columns:
            out_of_range = ((data['glucose_raw'] < 40) | (data['glucose_raw'] > 400)).sum()
            if out_of_range > 0:
                alert = DriftAlert(
                    timestamp=datetime.now().isoformat(),
                    severity='CRITICAL',
                    category='DATA_QUALITY',
                    metric='sensor_range_violations',
                    value=float(out_of_range),
                    threshold=0.0,
                    message=f"{out_of_range} samples outside physiological glucose range (40-400 mg/dL)",
                    metadata={'out_of_range_count': int(out_of_range)}
                )
                alerts.append(alert)
                self.logger.error(alert.message)
            else:
                self.logger.info("✓ All glucose values within physiological range (OK)")
        
        return alerts
    
    # ========================================================================
    # Statistical Drift Detection
    # ========================================================================
    
    def _check_statistical_drift(self, data: pd.DataFrame) -> List[DriftAlert]:
        """Detect statistical drift in feature distributions."""
        alerts = []
        
        for feature in self.feature_cols:
            if feature not in data.columns or feature not in self.reference_data.columns:
                continue
            
            ref_values = self.reference_data[feature].dropna()
            new_values = data[feature].dropna()
            
            if len(new_values) < 30:  # Minimum sample size
                continue
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_pval = stats.ks_2samp(ref_values, new_values)
            
            if ks_pval < self.thresholds.ks_test_alpha:
                severity = 'CRITICAL' if ks_pval < 0.001 else 'WARNING'
                alert = DriftAlert(
                    timestamp=datetime.now().isoformat(),
                    severity=severity,
                    category='STATISTICAL_DRIFT',
                    metric=f'ks_test_{feature}',
                    value=float(ks_stat),
                    threshold=self.thresholds.ks_test_alpha,
                    message=f"Significant distribution drift detected in '{feature}' (KS p-value: {ks_pval:.4f})",
                    metadata={
                        'ks_statistic': float(ks_stat),
                        'p_value': float(ks_pval),
                        'ref_mean': float(ref_values.mean()),
                        'new_mean': float(new_values.mean()),
                        'ref_std': float(ref_values.std()),
                        'new_std': float(new_values.std())
                    }
                )
                alerts.append(alert)
                self.logger.warning(alert.message)
            else:
                self.logger.info(f"✓ Feature '{feature}': No significant drift (p={ks_pval:.3f})")
            
            # Population Stability Index (PSI)
            psi = self._calculate_psi(ref_values, new_values)
            if psi > self.thresholds.psi_critical:
                alert = DriftAlert(
                    timestamp=datetime.now().isoformat(),
                    severity='CRITICAL',
                    category='STATISTICAL_DRIFT',
                    metric=f'psi_{feature}',
                    value=float(psi),
                    threshold=self.thresholds.psi_critical,
                    message=f"Critical PSI for '{feature}': {psi:.3f} (threshold: {self.thresholds.psi_critical})",
                    metadata={'psi_value': float(psi)}
                )
                alerts.append(alert)
                self.logger.error(alert.message)
            elif psi > self.thresholds.psi_warning:
                alert = DriftAlert(
                    timestamp=datetime.now().isoformat(),
                    severity='WARNING',
                    category='STATISTICAL_DRIFT',
                    metric=f'psi_{feature}',
                    value=float(psi),
                    threshold=self.thresholds.psi_warning,
                    message=f"Warning PSI for '{feature}': {psi:.3f} (threshold: {self.thresholds.psi_warning})",
                    metadata={'psi_value': float(psi)}
                )
                alerts.append(alert)
                self.logger.warning(alert.message)
        
        return alerts
    
    def _calculate_psi(self, reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
        """
        Calculate Population Stability Index (PSI).
        
        PSI < 0.1: No significant change
        PSI 0.1-0.25: Moderate change
        PSI > 0.25: Significant change (retraining recommended)
        """
        # Create bins based on reference data
        breakpoints = np.linspace(reference.min(), reference.max(), bins + 1)
        breakpoints[0] = -np.inf
        breakpoints[-1] = np.inf
        
        # Calculate distributions
        ref_counts = pd.cut(reference, bins=breakpoints).value_counts(sort=False)
        cur_counts = pd.cut(current, bins=breakpoints).value_counts(sort=False)
        
        ref_percents = ref_counts / len(reference)
        cur_percents = cur_counts / len(current)
        
        # Avoid division by zero
        ref_percents = ref_percents.replace(0, 0.0001)
        cur_percents = cur_percents.replace(0, 0.0001)
        
        # Calculate PSI
        psi = np.sum((cur_percents - ref_percents) * np.log(cur_percents / ref_percents))
        
        return psi
    
    # ========================================================================
    # Performance Monitoring
    # ========================================================================
    
    def _check_performance(self, data: pd.DataFrame) -> Tuple[Dict, List[DriftAlert]]:
        """Monitor model performance metrics."""
        alerts = []
        metrics = {}
        
        # Ensure target column exists
        if 'target_30min' not in data.columns:
            self.logger.error("Missing 'target_30min' column for performance evaluation")
            return metrics, alerts
        
        # Generate predictions
        X = data[self.feature_cols]
        y_true = data['target_30min']
        y_pred = self.model.predict(X)
        
        # Calculate metrics
        rmse = np.sqrt(np.mean((y_pred - y_true) ** 2))
        mae = np.mean(np.abs(y_pred - y_true))
        
        metrics['rmse'] = float(rmse)
        metrics['mae'] = float(mae)
        metrics['n_predictions'] = len(y_pred)
        
        self.logger.info(f"Performance metrics: RMSE={rmse:.2f} mg/dL, MAE={mae:.2f} mg/dL")
        
        # RMSE checks
        if rmse > self.thresholds.rmse_critical:
            alert = DriftAlert(
                timestamp=datetime.now().isoformat(),
                severity='CRITICAL',
                category='PERFORMANCE',
                metric='rmse',
                value=float(rmse),
                threshold=self.thresholds.rmse_critical,
                message=f"CRITICAL: RMSE {rmse:.2f} mg/dL exceeds threshold {self.thresholds.rmse_critical} mg/dL",
                metadata={'mae': float(mae)}
            )
            alerts.append(alert)
            self.logger.error(alert.message)
        elif rmse > self.thresholds.rmse_warning:
            alert = DriftAlert(
                timestamp=datetime.now().isoformat(),
                severity='WARNING',
                category='PERFORMANCE',
                metric='rmse',
                value=float(rmse),
                threshold=self.thresholds.rmse_warning,
                message=f"WARNING: RMSE {rmse:.2f} mg/dL exceeds threshold {self.thresholds.rmse_warning} mg/dL",
                metadata={'mae': float(mae)}
            )
            alerts.append(alert)
            self.logger.warning(alert.message)
        else:
            self.logger.info(f"✓ RMSE within acceptable range (threshold: {self.thresholds.rmse_warning} mg/dL)")
        
        # Clarke Error Grid analysis
        clarke_metrics = self._calculate_clarke_metrics(y_true, y_pred)
        metrics['clarke'] = clarke_metrics
        
        zone_ab_pct = clarke_metrics['zone_a_pct'] + clarke_metrics['zone_b_pct']
        
        if zone_ab_pct < self.thresholds.clarke_ab_min:
            alert = DriftAlert(
                timestamp=datetime.now().isoformat(),
                severity='CRITICAL',
                category='PERFORMANCE',
                metric='clarke_ab_percentage',
                value=float(zone_ab_pct),
                threshold=self.thresholds.clarke_ab_min,
                message=f"CRITICAL: Clarke Zone A+B = {zone_ab_pct:.1f}% (below FDA threshold {self.thresholds.clarke_ab_min}%)",
                metadata=clarke_metrics
            )
            alerts.append(alert)
            self.logger.error(alert.message)
        else:
            self.logger.info(f"✓ Clarke Zone A+B: {zone_ab_pct:.1f}% (FDA compliant)")
        
        return metrics, alerts
    
    def _calculate_clarke_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Calculate Clarke Error Grid zone distribution."""
        zones = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
        
        for true_val, pred_val in zip(y_true, y_pred):
            zone = self._clarke_zone(true_val, pred_val)
            zones[zone] += 1
        
        n_total = len(y_true)
        return {
            'zone_a_pct': zones['A'] / n_total * 100,
            'zone_b_pct': zones['B'] / n_total * 100,
            'zone_c_pct': zones['C'] / n_total * 100,
            'zone_d_pct': zones['D'] / n_total * 100,
            'zone_e_pct': zones['E'] / n_total * 100,
            'zone_counts': zones
        }
    
    def _clarke_zone(self, true_glucose: float, pred_glucose: float) -> str:
        """Classify single prediction into Clarke Error Grid zone."""
        # Zone A
        if true_glucose <= 70 and pred_glucose <= 70:
            return 'A'
        if abs(pred_glucose - true_glucose) <= 0.2 * true_glucose:
            return 'A'
        
        # Zone E (dangerous)
        if (true_glucose <= 70 and pred_glucose >= 180) or (true_glucose >= 180 and pred_glucose <= 70):
            return 'E'
        
        # Zone D (failure to detect)
        if (true_glucose < 70 and pred_glucose > 180) or (true_glucose > 240 and pred_glucose < 70):
            return 'D'
        
        # Zone C (unnecessary treatment)
        if (70 <= true_glucose <= 290) and pred_glucose <= 70:
            return 'C'
        if (70 <= true_glucose <= 180) and pred_glucose >= 240:
            return 'C'
        
        # Default: Zone B (benign errors)
        return 'B'
    
    # ========================================================================
    # Bias Drift Monitoring
    # ========================================================================
    
    def _check_bias_drift(self, data: pd.DataFrame, demographic_cols: List[str]) -> List[DriftAlert]:
        """Monitor for bias drift in demographic subgroups."""
        alerts = []
        
        if 'target_30min' not in data.columns:
            return alerts
        
        # Generate predictions
        X = data[self.feature_cols]
        y_true = data['target_30min']
        y_pred = self.model.predict(X)
        
        data = data.copy()
        data['prediction_error'] = y_pred - y_true
        data['absolute_error'] = np.abs(data['prediction_error'])
        
        # Check each demographic variable
        for demo_col in demographic_cols:
            if demo_col not in data.columns:
                continue
            
            # Calculate RMSE by subgroup
            subgroup_rmse = data.groupby(demo_col).apply(
                lambda x: np.sqrt(np.mean(x['prediction_error'] ** 2))
            )
            
            max_rmse = subgroup_rmse.max()
            min_rmse = subgroup_rmse.min()
            disparity = max_rmse - min_rmse
            
            if disparity > self.thresholds.subgroup_rmse_disparity_max:
                alert = DriftAlert(
                    timestamp=datetime.now().isoformat(),
                    severity='WARNING',
                    category='BIAS_DRIFT',
                    metric=f'subgroup_disparity_{demo_col}',
                    value=float(disparity),
                    threshold=self.thresholds.subgroup_rmse_disparity_max,
                    message=f"Bias drift detected in '{demo_col}': RMSE disparity = {disparity:.2f} mg/dL",
                    metadata={
                        'subgroup_rmse': subgroup_rmse.to_dict(),
                        'worst_group': subgroup_rmse.idxmax(),
                        'best_group': subgroup_rmse.idxmin()
                    }
                )
                alerts.append(alert)
                self.logger.warning(alert.message)
            else:
                self.logger.info(f"✓ Subgroup '{demo_col}': Disparity {disparity:.2f} mg/dL (acceptable)")
        
        return alerts
    
    # ========================================================================
    # Retraining Decision Logic
    # ========================================================================
    
    def _evaluate_retraining_need(self, alerts: List[DriftAlert]) -> bool:
        """Determine if model retraining is required based on alerts."""
        critical_count = sum(1 for alert in alerts if alert.severity == 'CRITICAL')
        warning_count = sum(1 for alert in alerts if alert.severity == 'WARNING')
        
        # Immediate retraining triggers
        for alert in alerts:
            if alert.metric == 'rmse' and alert.severity == 'CRITICAL':
                self.logger.error("🚨 RETRAINING REQUIRED: Critical RMSE threshold exceeded")
                return True
            
            if alert.metric == 'clarke_ab_percentage' and alert.value < self.thresholds.clarke_ab_min:
                self.logger.error("🚨 RETRAINING REQUIRED: FDA safety threshold violated")
                return True
        
        # Multiple critical alerts
        if critical_count >= 3:
            self.logger.error(f"🚨 RETRAINING REQUIRED: {critical_count} critical alerts detected")
            return True
        
        # High warning count
        if warning_count >= 5:
            self.logger.warning(f"⚠️  RETRAINING RECOMMENDED: {warning_count} warnings detected")
            return True
        
        self.logger.info("✓ No retraining required at this time")
        return False
    
    # ========================================================================
    # Reporting & Logging
    # ========================================================================
    
    def _generate_summary(self, report: Dict) -> str:
        """Generate human-readable summary."""
        n_alerts = len(report['alerts'])
        n_critical = sum(1 for alert in report['alerts'] if alert.severity == 'CRITICAL')
        n_warning = sum(1 for alert in report['alerts'] if alert.severity == 'WARNING')
        
        if report['retraining_required']:
            status = "🚨 RETRAINING REQUIRED"
        elif n_critical > 0:
            status = "⚠️  CRITICAL ISSUES DETECTED"
        elif n_warning > 0:
            status = "⚠️  WARNINGS DETECTED"
        else:
            status = "✓ ALL CHECKS PASSED"
        
        summary = f"""
{status}
{'='*80}
Total Alerts: {n_alerts} (Critical: {n_critical}, Warning: {n_warning})
Samples Monitored: {report['n_samples']}
Timestamp: {report['timestamp']}
Retraining Required: {report['retraining_required']}
"""
        
        if 'performance' in report['metrics']:
            perf = report['metrics']['performance']
            summary += f"\nPerformance Metrics:\n"
            summary += f"  - RMSE: {perf.get('rmse', 'N/A'):.2f} mg/dL\n"
            summary += f"  - MAE: {perf.get('mae', 'N/A'):.2f} mg/dL\n"
            if 'clarke' in perf:
                clarke = perf['clarke']
                summary += f"  - Clarke Zone A+B: {clarke['zone_a_pct'] + clarke['zone_b_pct']:.1f}%\n"
        
        return summary
    
    def _log_report(self, report: Dict):
        """Log full report to file."""
        self.logger.info("\n" + report['summary'])
        
        # Save detailed JSON report
        report_file = self.report_dir / f"drift_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert alerts to serializable format
        serializable_report = report.copy()
        serializable_report['alerts'] = [asdict(alert) for alert in report['alerts']]
        
        with open(report_file, 'w') as f:
            json.dump(serializable_report, f, indent=2)
        
        self.logger.info(f"Full report saved: {report_file}")
    
    # ========================================================================
    # PMCF Report Generation
    # ========================================================================
    
    def generate_pmcf_report(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate Post-Market Clinical Follow-up (PMCF) report for regulatory submission.
        
        Parameters
        ----------
        start_date : str, optional
            Start date for report period (ISO format)
        end_date : str, optional
            End date for report period (ISO format)
        output_path : str, optional
            Custom output path for report
        
        Returns
        -------
        str
            Path to generated report
        """
        if output_path is None:
            output_path = self.report_dir / f"PMCF_Report_{datetime.now().strftime('%Y%m')}.txt"
        
        # Filter alerts by date range if specified
        filtered_alerts = self.alert_history
        if start_date:
            filtered_alerts = [a for a in filtered_alerts if a.timestamp >= start_date]
        if end_date:
            filtered_alerts = [a for a in filtered_alerts if a.timestamp <= end_date]
        
        # Generate report content
        report_content = f"""
{'='*80}
POST-MARKET CLINICAL FOLLOW-UP (PMCF) REPORT
GuardianCGM Glucose Prediction Model
{'='*80}

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Reporting Period: {start_date or 'Inception'} to {end_date or 'Present'}

1. EXECUTIVE SUMMARY
-------------------
Total Monitoring Events: {len(filtered_alerts)}
Critical Alerts: {sum(1 for a in filtered_alerts if a.severity == 'CRITICAL')}
Warning Alerts: {sum(1 for a in filtered_alerts if a.severity == 'WARNING')}
Retraining Events: {sum(1 for a in filtered_alerts if 'RETRAINING' in a.severity)}

2. ALERT BREAKDOWN BY CATEGORY
-------------------------------
"""
        
        # Alert categories
        categories = {}
        for alert in filtered_alerts:
            if alert.category not in categories:
                categories[alert.category] = []
            categories[alert.category].append(alert)
        
        for category, alerts in categories.items():
            report_content += f"\n{category}:\n"
            report_content += f"  Total: {len(alerts)}\n"
            report_content += f"  Critical: {sum(1 for a in alerts if a.severity == 'CRITICAL')}\n"
            report_content += f"  Warnings: {sum(1 for a in alerts if a.severity == 'WARNING')}\n"
        
        report_content += f"""

3. REGULATORY COMPLIANCE STATUS
--------------------------------
FDA 21 CFR Part 820 (Quality System): [COMPLIANT/NON-COMPLIANT]
EU MDR (2017/745) PMCF: [COMPLIANT/NON-COMPLIANT]
ISO 13485: [COMPLIANT/NON-COMPLIANT]

4. CORRECTIVE ACTIONS TAKEN
----------------------------
[To be filled by clinical/regulatory team]

5. RISK ASSESSMENT
------------------
Current Risk Level: [LOW/MEDIUM/HIGH]
[Details to be completed based on alerts]

6. RECOMMENDATIONS
------------------
"""
        
        if any(a.severity == 'CRITICAL' for a in filtered_alerts):
            report_content += "- IMMEDIATE ACTION REQUIRED: Critical alerts detected\n"
            report_content += "- Recommend model retraining and revalidation\n"
            report_content += "- Consider temporary halt of predictions until resolution\n"
        else:
            report_content += "- Continue routine monitoring\n"
            report_content += "- No immediate action required\n"
        
        report_content += f"""

{'='*80}
Report prepared by: GuardianCGM Drift Monitoring System
Signature: _________________________ Date: _____________
Approved by: ________________________ Date: _____________
{'='*80}
"""
        
        # Save report
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"PMCF report generated: {output_path}")
        return str(output_path)


# ============================================================================
# Command-Line Interface (Optional)
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GuardianCGM Drift Monitoring System")
    parser.add_argument('--model', type=str, required=True, help='Path to trained model')
    parser.add_argument('--reference', type=str, required=True, help='Path to reference dataset')
    parser.add_argument('--new-data', type=str, required=True, help='Path to new data for monitoring')
    parser.add_argument('--pmcf-report', action='store_true', help='Generate PMCF report')
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = DriftMonitor(
        model_path=args.model,
        reference_data_path=args.reference
    )
    
    # Load and check new data
    new_data = pd.read_csv(args.new_data)
    report = monitor.check_drift(new_data)
    
    # Print summary
    print(report['summary'])
    
    # Generate PMCF report if requested
    if args.pmcf_report:
        pmcf_path = monitor.generate_pmcf_report()
        print(f"\nPMCF Report: {pmcf_path}")
