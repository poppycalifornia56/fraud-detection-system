import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Transaction
        
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

def get_recent_transactions(db, limit=100):
    """
    Retrieves the most recent transactions from the database using SQLAlchemy ORM.
    
    Parameters:
        db: SQLAlchemy session object
        limit: Maximum number of transactions to retrieve (default: 100)
        
    Returns:
        pandas.DataFrame: DataFrame containing the recent transactions
    """
    
    try:
        # Assuming there's a Transaction model defined somewhere in your project
        # If you're using a different model name, replace 'Transaction' accordingly
        
        # Query to get the most recent transactions using ORM
        # Order by transaction_date in descending order and limit results
        transactions = (
            db.query(Transaction)
            .order_by(desc(Transaction.transaction_date))
            .limit(limit)
            .all()
        )
        
        # Convert ORM objects to dictionaries for DataFrame creation
        transaction_dicts = []
        for transaction in transactions:
            # Convert each Transaction object to a dictionary
            # This assumes that Transaction has the attributes listed below
            # Modify to match your actual Transaction model attributes
            transaction_dict = {
                'transaction_id': transaction.transaction_id,
                'customer_id': transaction.customer_id,
                'transaction_date': transaction.transaction_date,
                'amount': transaction.amount,
                'transaction_type': transaction.transaction_type,
                'status': transaction.status,
                'description': transaction.description
            }
            transaction_dicts.append(transaction_dict)
        
        # Create a DataFrame from the list of dictionaries
        transactions_df = pd.DataFrame(transaction_dicts)
        
        # Convert transaction_date to datetime if it exists in the columns
        if 'transaction_date' in transactions_df.columns:
            transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
        
        return transactions_df
    
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return pd.DataFrame()