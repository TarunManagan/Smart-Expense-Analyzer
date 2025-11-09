import pandas as pd
import re
from config import CATEGORIES, CATEGORY_KEYWORDS

class TransactionCategorizer:
    def __init__(self):
        pass
    
    def categorize_transaction(self, description, amount, transaction_type):
        """Categorize a single transaction using rule-based approach"""
        description_lower = description.lower()
        
        # Check each category's keywords
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        # Amount-based fallback
        if transaction_type == "Credit":
            return "Income"
        elif amount > 10000:
            return "Shopping"  # Large amounts likely to be shopping
        elif amount > 1000:
            return "Bills & Utilities"  # Medium amounts likely to be bills
        else:
            return "Other"
    
    def categorize_transactions_batch(self, transactions_df):
        """Categorize multiple transactions"""
        if transactions_df.empty:
            return transactions_df
        
        # Add category column
        transactions_df['category'] = ""
        
        for index, row in transactions_df.iterrows():
            category = self.categorize_transaction(
                row['description'], 
                row['amount'], 
                row['type']
            )
            transactions_df.at[index, 'category'] = category
        
        return transactions_df
    
    def save_categorized_transactions(self, transactions_df, filename="categorized_transactions.csv"):
        """Save categorized transactions to CSV"""
        filepath = f"data/{filename}"
        transactions_df.to_csv(filepath, index=False)
        return filepath

def categorize_transactions(transactions_df):
    """Main function to categorize transactions"""
    categorizer = TransactionCategorizer()
    categorized_df = categorizer.categorize_transactions_batch(transactions_df)
    csv_path = categorizer.save_categorized_transactions(categorized_df)
    return categorized_df, csv_path
