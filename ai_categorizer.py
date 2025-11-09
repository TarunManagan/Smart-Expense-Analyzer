import pandas as pd
import json
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import CATEGORIES, CATEGORY_KEYWORDS

class TransactionCategorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.category_vectors = None
        self._build_category_vectors()
    
    def _build_category_vectors(self):
        """Build TF-IDF vectors for each category based on keywords"""
        category_texts = []
        for category, keywords in CATEGORY_KEYWORDS.items():
            # Create a text representation of the category
            category_text = " ".join(keywords)
            category_texts.append(category_text)
        
        # Fit the vectorizer and transform category texts
        self.category_vectors = self.vectorizer.fit_transform(category_texts)
    
    def categorize_transaction(self, description, amount, transaction_type):
        """Categorize a single transaction using free AI methods"""
        # First try rule-based categorization
        rule_based_category = self._rule_based_categorization(description, amount, transaction_type)
        if rule_based_category != "Other":
            return rule_based_category
        
        # If rule-based fails, try ML-based categorization
        ml_category = self._ml_based_categorization(description)
        if ml_category != "Other":
            return ml_category
        
        # Final fallback
        return self._amount_based_categorization(amount, transaction_type)
    
    def _rule_based_categorization(self, description, amount, transaction_type):
        """Rule-based categorization using keyword matching"""
        description_lower = description.lower()
        
        # Check each category's keywords
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        return "Other"
    
    def _ml_based_categorization(self, description):
        """ML-based categorization using TF-IDF and cosine similarity"""
        try:
            # Transform the description
            description_vector = self.vectorizer.transform([description])
            
            # Calculate cosine similarity with category vectors
            similarities = cosine_similarity(description_vector, self.category_vectors)[0]
            
            # Get the category with highest similarity
            best_category_idx = np.argmax(similarities)
            best_similarity = similarities[best_category_idx]
            
            # Only return category if similarity is above threshold
            if best_similarity > 0.1:  # Low threshold since we're using keywords
                return list(CATEGORY_KEYWORDS.keys())[best_category_idx]
            
            return "Other"
        except Exception as e:
            print(f"Error in ML categorization: {e}")
            return "Other"
    
    def _amount_based_categorization(self, amount, transaction_type):
        """Amount-based categorization as final fallback"""
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
