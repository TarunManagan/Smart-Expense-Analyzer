import json
from datetime import datetime
import random
from config import USE_FREE_AI

class SuggestionsGenerator:
    def __init__(self):
        self.suggestion_templates = self._load_suggestion_templates()
    
    def _load_suggestion_templates(self):
        """Load predefined suggestion templates"""
        return {
            "high_food_spending": [
                "🍽️ Your food expenses are high. Try meal planning and cooking at home to save 30-40% on food costs.",
                "🥘 Consider batch cooking on weekends to reduce weekday food expenses and save time.",
                "🛒 Make a grocery list and stick to it to avoid impulse purchases at the supermarket."
            ],
            "high_transport_spending": [
                "🚗 Your transportation costs are significant. Consider carpooling or using public transport to reduce fuel expenses.",
                "⛽ Track your fuel consumption and plan routes efficiently to minimize unnecessary trips.",
                "🚲 For short distances, consider walking or cycling to save money and stay healthy."
            ],
            "high_shopping_spending": [
                "🛍️ Your shopping expenses are high. Implement a 24-hour rule before making non-essential purchases.",
                "📱 Unsubscribe from marketing emails to reduce impulse buying from online stores.",
                "💳 Use cash or debit cards for shopping to avoid credit card interest and overspending."
            ],
            "high_entertainment_spending": [
                "🎬 Look for free or low-cost entertainment alternatives like public libraries, free events, or streaming services.",
                "📺 Review your subscription services and cancel unused ones to save money monthly.",
                "🎮 Consider sharing subscription costs with family or friends for streaming services."
            ],
            "low_savings": [
                "💰 Set up automatic transfers to a savings account on payday to build your emergency fund.",
                "🎯 Start with saving 10% of your income and gradually increase it to 20%.",
                "📊 Track your expenses daily to identify areas where you can cut back and save more."
            ],
            "no_investments": [
                "📈 Start investing in low-risk options like index funds or SIPs to grow your wealth over time.",
                "🏦 Open a high-yield savings account or fixed deposit to earn better returns on your savings.",
                "💼 Consider consulting a financial advisor to create an investment strategy based on your goals."
            ],
            "high_recurring_expenses": [
                "🔄 Review your recurring subscriptions and cancel unused services to reduce monthly expenses.",
                "📋 Create a list of all your recurring payments and evaluate which ones are necessary.",
                "💡 Negotiate with service providers for better rates or switch to more affordable alternatives."
            ],
            "general_tips": [
                "📱 Use budgeting apps to track your expenses and stay within your financial goals.",
                "🎯 Set specific financial goals like building an emergency fund or saving for a vacation.",
                "📚 Educate yourself about personal finance through books, podcasts, or online courses.",
                "🛡️ Build an emergency fund of 3-6 months of expenses before making major investments.",
                "💳 Pay off high-interest debt first before focusing on investments or savings."
            ]
        }
    
    def generate_suggestions(self, user_profile, recent_transactions=None):
        """Generate personalized financial suggestions based on user profile"""
        return self._generate_smart_suggestions(user_profile)
    
    def _generate_smart_suggestions(self, user_profile):
        """Generate smart suggestions based on user profile analysis"""
        suggestions = []
        
        monthly_income = user_profile.get('monthly_income_avg', 0)
        monthly_expenses = user_profile.get('monthly_expenses_avg', 0)
        top_categories = user_profile.get('top_spending_categories', {})
        financial_health_score = user_profile.get('financial_health_score', 50)
        recurring_expenses = user_profile.get('recurring_expenses', [])
        
        # Calculate savings rate
        savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
        
        # High spending category suggestions
        for category, amount in list(top_categories.items())[:3]:
            if category == "Food & Dining" and amount > monthly_income * 0.15:
                suggestions.extend(random.sample(self.suggestion_templates["high_food_spending"], 1))
            elif category == "Transportation" and amount > monthly_income * 0.10:
                suggestions.extend(random.sample(self.suggestion_templates["high_transport_spending"], 1))
            elif category == "Shopping" and amount > monthly_income * 0.10:
                suggestions.extend(random.sample(self.suggestion_templates["high_shopping_spending"], 1))
            elif category == "Entertainment" and amount > monthly_income * 0.05:
                suggestions.extend(random.sample(self.suggestion_templates["high_entertainment_spending"], 1))
        
        # Savings suggestions
        if savings_rate < 10:
            suggestions.extend(random.sample(self.suggestion_templates["low_savings"], 1))
        
        # Investment suggestions
        if "Investments" not in top_categories or top_categories.get("Investments", 0) == 0:
            suggestions.extend(random.sample(self.suggestion_templates["no_investments"], 1))
        
        # Recurring expenses suggestions
        if len(recurring_expenses) > 8:
            suggestions.extend(random.sample(self.suggestion_templates["high_recurring_expenses"], 1))
        
        # Add general tips to fill up to 7 suggestions
        general_tips = random.sample(self.suggestion_templates["general_tips"], 
                                   max(0, 7 - len(suggestions)))
        suggestions.extend(general_tips)
        
        return suggestions[:7]  # Limit to 7 suggestions
    
    def generate_budget_recommendations(self, user_profile):
        """Generate budget recommendations based on spending patterns"""
        monthly_income = user_profile.get('monthly_income_avg', 0)
        expense_breakdown = user_profile.get('expense_breakdown', {})
        
        if monthly_income == 0:
            return {}
        
        # Standard budget percentages (50/30/20 rule with modifications)
        budget_recommendations = {
            'Food & Dining': 0.15,  # 15%
            'Transportation': 0.10,  # 10%
            'Bills & Utilities': 0.10,  # 10%
            'Shopping': 0.10,  # 10%
            'Entertainment': 0.05,  # 5%
            'Healthcare': 0.05,  # 5%
            'Education': 0.05,  # 5%
            'Travel': 0.05,  # 5%
            'Investments': 0.20,  # 20%
            'Emergency Fund': 0.15,  # 15%
        }
        
        recommendations = {}
        for category, percentage in budget_recommendations.items():
            recommended_amount = monthly_income * percentage
            current_amount = expense_breakdown.get(category, 0)
            
            recommendations[category] = {
                'recommended': recommended_amount,
                'current': current_amount,
                'difference': recommended_amount - current_amount,
                'percentage': percentage * 100
            }
        
        return recommendations
    
    def generate_quick_tips(self, user_profile):
        """Generate quick financial tips based on profile"""
        tips = []
        
        financial_health_score = user_profile.get('financial_health_score', 50)
        recurring_expenses = user_profile.get('recurring_expenses', [])
        
        if financial_health_score < 40:
            tips.append("🚨 Focus on reducing debt and building emergency savings")
        elif financial_health_score > 70:
            tips.append("✅ Great job! Consider increasing your investment contributions")
        
        if len(recurring_expenses) > 8:
            tips.append("📋 Review your recurring subscriptions - you might be paying for unused services")
        
        if user_profile.get('monthly_expenses_avg', 0) > user_profile.get('monthly_income_avg', 0):
            tips.append("⚠️ You're spending more than you earn - immediate action needed")
        
        tips.append("💡 Use the 24-hour rule before making non-essential purchases")
        tips.append("📊 Review your bank statements monthly to catch any errors or fraud")
        
        return tips

def generate_financial_suggestions(user_profile, recent_transactions=None):
    """Main function to generate financial suggestions"""
    generator = SuggestionsGenerator()
    suggestions = generator.generate_suggestions(user_profile, recent_transactions)
    budget_recommendations = generator.generate_budget_recommendations(user_profile)
    quick_tips = generator.generate_quick_tips(user_profile)
    
    return {
        'suggestions': suggestions,
        'budget_recommendations': budget_recommendations,
        'quick_tips': quick_tips
    }
