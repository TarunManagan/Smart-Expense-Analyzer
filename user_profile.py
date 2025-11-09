import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import os

class UserProfileManager:
    def __init__(self):
        pass
    
    def create_user_profile(self, user_data):
        """Create user profile from questionnaire data"""
        profile = {
            'created_date': datetime.now().isoformat(),
            'user_info': user_data,
            'financial_goals': {
                'monthly_savings_target': user_data.get('monthly_savings_target', 0),
                'priority_categories': user_data.get('priority_categories', []),
                'cut_cost_areas': user_data.get('cut_cost_areas', [])
            }
        }
        return profile
    
    def analyze_transactions(self, transactions_df, user_profile):
        """Analyze transactions and enhance user profile"""
        if transactions_df.empty:
            return user_profile
        
        # Convert date column to datetime
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        
        # Basic analysis
        analysis = {
            'total_transactions': len(transactions_df),
            'date_range': {
                'start': transactions_df['date'].min().isoformat(),
                'end': transactions_df['date'].max().isoformat()
            }
        }
        
        # Income analysis
        income_data = self._analyze_income(transactions_df)
        analysis.update(income_data)
        
        # Expense analysis
        expense_data = self._analyze_expenses(transactions_df)
        analysis.update(expense_data)
        
        # Spending patterns
        spending_patterns = self._analyze_spending_patterns(transactions_df)
        analysis.update(spending_patterns)
        
        # Financial health score
        analysis['financial_health_score'] = self._calculate_financial_health_score(analysis, user_profile)
        
        # Add analysis to profile
        user_profile['transaction_analysis'] = analysis
        
        return user_profile
    
    def _analyze_income(self, df):
        """Analyze income patterns"""
        income_df = df[df['category'] == 'Income']
        
        if income_df.empty:
            return {
                'total_income': 0,
                'monthly_income_avg': 0,
                'income_sources': []
            }
        
        total_income = income_df['amount'].sum()
        monthly_income = income_df.groupby(income_df['date'].dt.to_period('M'))['amount'].sum()
        avg_monthly_income = monthly_income.mean()
        
        # Identify income sources
        income_sources = income_df['description'].value_counts().head(5).to_dict()
        
        return {
            'total_income': float(total_income),
            'monthly_income_avg': float(avg_monthly_income),
            'income_sources': income_sources
        }
    
    def _analyze_expenses(self, df):
        """Analyze expense patterns"""
        expense_df = df[df['category'] != 'Income']
        
        if expense_df.empty:
            return {
                'total_expenses': 0,
                'monthly_expenses_avg': 0,
                'expense_breakdown': {},
                'top_spending_categories': []
            }
        
        total_expenses = expense_df['amount'].sum()
        monthly_expenses = expense_df.groupby(expense_df['date'].dt.to_period('M'))['amount'].sum()
        avg_monthly_expenses = monthly_expenses.mean()
        
        # Category breakdown
        category_breakdown = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        expense_breakdown = category_breakdown.to_dict()
        
        # Top spending categories
        top_categories = category_breakdown.head(5).to_dict()
        
        return {
            'total_expenses': float(total_expenses),
            'monthly_expenses_avg': float(avg_monthly_expenses),
            'expense_breakdown': expense_breakdown,
            'top_spending_categories': top_categories
        }
    
    def _analyze_spending_patterns(self, df):
        """Analyze spending patterns over time"""
        expense_df = df[df['category'] != 'Income']
        
        if expense_df.empty:
            return {
                'spending_trend': 'stable',
                'highest_spending_month': None,
                'lowest_spending_month': None
            }
        
        # Monthly spending
        monthly_spending = expense_df.groupby(expense_df['date'].dt.to_period('M'))['amount'].sum()
        
        if len(monthly_spending) > 1:
            # Calculate trend
            spending_values = monthly_spending.values
            trend_slope = np.polyfit(range(len(spending_values)), spending_values, 1)[0]
            
            if trend_slope > 0:
                spending_trend = 'increasing'
            elif trend_slope < 0:
                spending_trend = 'decreasing'
            else:
                spending_trend = 'stable'
        else:
            spending_trend = 'insufficient_data'
        
        # Highest and lowest spending months
        highest_month = monthly_spending.idxmax().strftime('%Y-%m') if not monthly_spending.empty else None
        lowest_month = monthly_spending.idxmin().strftime('%Y-%m') if not monthly_spending.empty else None
        
        return {
            'spending_trend': spending_trend,
            'highest_spending_month': highest_month,
            'lowest_spending_month': lowest_month,
            'monthly_spending': monthly_spending.to_dict()
        }
    
    def _calculate_financial_health_score(self, analysis, user_profile):
        """Calculate a simple financial health score (0-100)"""
        score = 50  # Base score
        
        monthly_income = analysis.get('monthly_income_avg', 0)
        monthly_expenses = analysis.get('monthly_expenses_avg', 0)
        savings_target = user_profile.get('financial_goals', {}).get('monthly_savings_target', 0)
        
        # Income vs Expenses ratio
        if monthly_income > 0:
            savings_ratio = (monthly_income - monthly_expenses) / monthly_income
            
            if savings_ratio > 0.2:  # 20% savings
                score += 20
            elif savings_ratio > 0.1:  # 10% savings
                score += 10
            elif savings_ratio > 0:  # Positive savings
                score += 5
            else:  # Negative savings
                score -= 20
            
            # Compare with user's savings target
            if savings_target > 0:
                actual_savings = monthly_income - monthly_expenses
                if actual_savings >= savings_target:
                    score += 15
                elif actual_savings >= savings_target * 0.8:
                    score += 10
                elif actual_savings >= savings_target * 0.5:
                    score += 5
        
        # Spending trend
        spending_trend = analysis.get('spending_trend', 'stable')
        if spending_trend == 'decreasing':
            score += 10
        elif spending_trend == 'increasing':
            score -= 10
        
        return max(0, min(100, score))  # Clamp between 0 and 100
    
    def save_profile(self, profile, user_id="default"):
        """Save user profile to JSON file"""
        filename = f"{user_id}_profile.json"
        filepath = os.path.join("profiles", filename)
        
        # Convert Period objects to strings for JSON serialization
        def convert_periods(obj):
            if hasattr(obj, 'strftime'):
                return obj.strftime('%Y-%m')
            elif isinstance(obj, dict):
                return {str(k): convert_periods(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_periods(item) for item in obj]
            return obj
        
        profile_serializable = convert_periods(profile)
        
        with open(filepath, 'w') as f:
            json.dump(profile_serializable, f, indent=2, default=str)
        
        return filepath
    
    def load_profile(self, user_id="default"):
        """Load user profile from JSON file"""
        filename = f"{user_id}_profile.json"
        filepath = os.path.join("profiles", filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None

def create_user_profile(user_data):
    """Main function to create user profile"""
    manager = UserProfileManager()
    profile = manager.create_user_profile(user_data)
    profile_path = manager.save_profile(profile)
    return profile, profile_path

def analyze_user_transactions(transactions_df, user_profile):
    """Main function to analyze transactions with user profile"""
    manager = UserProfileManager()
    enhanced_profile = manager.analyze_transactions(transactions_df, user_profile)
    profile_path = manager.save_profile(enhanced_profile)
    return enhanced_profile, profile_path