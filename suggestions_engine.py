import random
from config import CATEGORIES

class PersonalizedSuggestionsEngine:
    def __init__(self):
        self.suggestion_templates = self._load_suggestion_templates()
    
    def _load_suggestion_templates(self):
        """Load predefined suggestion templates"""
        return {
            "high_food_spending": [
                "🍽️ Your food expenses are high. Try meal planning and cooking at home to save 30-40% on food costs.",
                "🥘 Consider batch cooking on weekends to reduce weekday food expenses and save time.",
                "🛒 Make a grocery list and stick to it to avoid impulse purchases at the supermarket.",
                "🍕 Limit eating out to once or twice a week and cook more meals at home."
            ],
            "high_transport_spending": [
                "🚗 Your transportation costs are significant. Consider carpooling or using public transport to reduce fuel expenses.",
                "⛽ Track your fuel consumption and plan routes efficiently to minimize unnecessary trips.",
                "🚲 For short distances, consider walking or cycling to save money and stay healthy.",
                "🚌 Use public transportation or ride-sharing services for regular commutes."
            ],
            "high_shopping_spending": [
                "🛍️ Your shopping expenses are high. Implement a 24-hour rule before making non-essential purchases.",
                "📱 Unsubscribe from marketing emails to reduce impulse buying from online stores.",
                "💳 Use cash or debit cards for shopping to avoid credit card interest and overspending.",
                "🎯 Create a shopping list and stick to it to avoid unnecessary purchases."
            ],
            "high_entertainment_spending": [
                "🎬 Look for free or low-cost entertainment alternatives like public libraries, free events, or streaming services.",
                "📺 Review your subscription services and cancel unused ones to save money monthly.",
                "🎮 Consider sharing subscription costs with family or friends for streaming services.",
                "🎪 Look for free community events and activities in your area."
            ],
            "low_savings": [
                "💰 Set up automatic transfers to a savings account on payday to build your emergency fund.",
                "🎯 Start with saving 10% of your income and gradually increase it to 20%.",
                "📊 Track your expenses daily to identify areas where you can cut back and save more.",
                "🏦 Open a high-yield savings account to earn better returns on your savings."
            ],
            "no_investments": [
                "📈 Start investing in low-risk options like index funds or SIPs to grow your wealth over time.",
                "🏦 Open a high-yield savings account or fixed deposit to earn better returns on your savings.",
                "💼 Consider consulting a financial advisor to create an investment strategy based on your goals.",
                "🎯 Start with small amounts in mutual funds or SIPs to build investment habits."
            ],
            "budget_optimization": [
                "📊 Create a detailed monthly budget and track your spending against it.",
                "🎯 Use the 50/30/20 rule: 50% for needs, 30% for wants, 20% for savings and debt repayment.",
                "📱 Use budgeting apps to track your expenses and stay within your financial goals.",
                "💡 Review your budget monthly and adjust based on your spending patterns."
            ],
            "debt_management": [
                "💳 Focus on paying high-interest debt first (like credit cards) before low-interest debt.",
                "🔄 Consider debt consolidation if you have multiple high-interest loans.",
                "📋 Create a debt repayment plan and stick to it. Every extra payment helps reduce the total interest.",
                "🎯 Pay more than the minimum payment on credit cards to reduce interest charges."
            ],
            "general_tips": [
                "📱 Use budgeting apps to track your expenses and stay within your financial goals.",
                "🎯 Set specific financial goals like building an emergency fund or saving for a vacation.",
                "📚 Educate yourself about personal finance through books, podcasts, or online courses.",
                "🛡️ Build an emergency fund of 3-6 months of expenses before making major investments.",
                "💳 Pay off high-interest debt first before focusing on investments or savings."
            ]
        }
    
    def generate_personalized_suggestions(self, user_profile, transaction_analysis):
        """Generate personalized suggestions based on user profile and transaction analysis"""
        suggestions = []
        
        # Extract data
        user_info = user_profile.get('user_info', {})
        financial_goals = user_profile.get('financial_goals', {})
        monthly_income = transaction_analysis.get('monthly_income_avg', 0)
        monthly_expenses = transaction_analysis.get('monthly_expenses_avg', 0)
        top_categories = transaction_analysis.get('top_spending_categories', {})
        financial_health_score = transaction_analysis.get('financial_health_score', 50)
        savings_target = financial_goals.get('monthly_savings_target', 0)
        cut_cost_areas = financial_goals.get('cut_cost_areas', [])
        
        # Calculate current savings
        current_savings = monthly_income - monthly_expenses
        savings_rate = (current_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        # 1. Savings-related suggestions
        if savings_target > 0:
            if current_savings < savings_target:
                gap = savings_target - current_savings
                suggestions.append(f"🎯 You're saving ₹{current_savings:,.2f} but your target is ₹{savings_target:,.2f}. You need to save ₹{gap:,.2f} more per month.")
                suggestions.extend(random.sample(self.suggestion_templates["low_savings"], 2))
            else:
                suggestions.append(f"✅ Great job! You're meeting your savings target of ₹{savings_target:,.2f} per month.")
        
        # 2. Category-specific suggestions based on user's cut_cost_areas
        for category in cut_cost_areas:
            if category in top_categories:
                amount = top_categories[category]
                if category == "Food & Dining" and amount > monthly_income * 0.15:
                    suggestions.extend(random.sample(self.suggestion_templates["high_food_spending"], 1))
                elif category == "Transportation" and amount > monthly_income * 0.10:
                    suggestions.extend(random.sample(self.suggestion_templates["high_transport_spending"], 1))
                elif category == "Shopping" and amount > monthly_income * 0.10:
                    suggestions.extend(random.sample(self.suggestion_templates["high_shopping_spending"], 1))
                elif category == "Entertainment" and amount > monthly_income * 0.05:
                    suggestions.extend(random.sample(self.suggestion_templates["high_entertainment_spending"], 1))
        
        # 3. Investment suggestions
        if "Investments" not in top_categories or top_categories.get("Investments", 0) == 0:
            suggestions.extend(random.sample(self.suggestion_templates["no_investments"], 1))
        
        # 4. Budget optimization
        if financial_health_score < 60:
            suggestions.extend(random.sample(self.suggestion_templates["budget_optimization"], 1))
        
        # 5. General tips to fill up to 7 suggestions
        general_tips = random.sample(self.suggestion_templates["general_tips"], 
                                   max(0, 7 - len(suggestions)))
        suggestions.extend(general_tips)
        
        return suggestions[:7]  # Limit to 7 suggestions
    
    def generate_budget_recommendations(self, user_profile, transaction_analysis):
        """Generate budget recommendations based on user profile and spending patterns"""
        monthly_income = transaction_analysis.get('monthly_income_avg', 0)
        expense_breakdown = transaction_analysis.get('expense_breakdown', {})
        savings_target = user_profile.get('financial_goals', {}).get('monthly_savings_target', 0)
        
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
        
        # Adjust based on user's savings target
        if savings_target > 0:
            target_savings_percentage = savings_target / monthly_income
            if target_savings_percentage > 0.35:  # If target is more than 35%
                # Reduce other categories
                for category in budget_recommendations:
                    if category not in ['Investments', 'Emergency Fund']:
                        budget_recommendations[category] *= 0.8
        
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
    
    def generate_quick_tips(self, user_profile, transaction_analysis):
        """Generate quick tips based on user profile and analysis"""
        tips = []
        
        financial_health_score = transaction_analysis.get('financial_health_score', 50)
        monthly_income = transaction_analysis.get('monthly_income_avg', 0)
        monthly_expenses = transaction_analysis.get('monthly_expenses_avg', 0)
        savings_target = user_profile.get('financial_goals', {}).get('monthly_savings_target', 0)
        
        # Health score based tips
        if financial_health_score < 40:
            tips.append("🚨 Focus on reducing debt and building emergency savings")
        elif financial_health_score > 70:
            tips.append("✅ Great job! Consider increasing your investment contributions")
        
        # Savings target tips
        if savings_target > 0:
            current_savings = monthly_income - monthly_expenses
            if current_savings < savings_target:
                tips.append(f"🎯 You need to save ₹{savings_target - current_savings:,.2f} more to reach your monthly target")
            else:
                tips.append("🎉 You're exceeding your savings target! Consider investing the extra amount")
        
        # General tips
        tips.append("💡 Use the 24-hour rule before making non-essential purchases")
        tips.append("📊 Review your bank statements monthly to catch any errors or fraud")
        tips.append("🔄 Set up automatic bill payments to avoid late fees")
        
        return tips

def generate_personalized_suggestions(user_profile, transaction_analysis):
    """Main function to generate personalized suggestions"""
    engine = PersonalizedSuggestionsEngine()
    suggestions = engine.generate_personalized_suggestions(user_profile, transaction_analysis)
    budget_recommendations = engine.generate_budget_recommendations(user_profile, transaction_analysis)
    quick_tips = engine.generate_quick_tips(user_profile, transaction_analysis)
    
    return {
        'suggestions': suggestions,
        'budget_recommendations': budget_recommendations,
        'quick_tips': quick_tips
    }
