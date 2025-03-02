# backend/ml_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def predict_anomalies(transactions_df):
    """
    Basic anomaly detection using Isolation Forest
    Returns dictionary of {transaction_id: anomaly_score}
    """
    # Extract numerical features
    features = ['amount']
    
    # Add derived features
    if len(transactions_df) > 0:
        # Group by vendor
        vendor_stats = transactions_df.groupby('vendor_id')['amount'].agg(['mean', 'std'])
        
        # Map back to transactions
        transactions_df = transactions_df.merge(
            vendor_stats, 
            left_on='vendor_id', 
            right_index=True, 
            how='left'
        )
        
        # Calculate z-score relative to vendor history
        transactions_df['amount_zscore'] = np.abs((transactions_df['amount'] - transactions_df['mean']) / transactions_df['std'].replace(0, 1))
        
        features.append('amount_zscore')
    
    # Select features for model
    X = transactions_df[features].fillna(0)
    
    # Standardize features
    X_scaled = StandardScaler().fit_transform(X)
    
    # Fit model
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)
    
    # Get anomaly scores (-1 for anomalies, 1 for normal)
    # Convert to 0-1 scale where 1 is most anomalous
    scores = -model.score_samples(X_scaled)
    normalized_scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
    
    # Create dictionary of transaction_id: score
    result = dict(zip(transactions_df['id'], normalized_scores))
    
    return result