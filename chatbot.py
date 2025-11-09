import random
from config import CATEGORIES

class FreeFinanceChatbot:
    def __init__(self):
        self.response_templates = self._load_response_templates()
        self.conversation_context = {}
    
    def _load_response_templates(self):
        """Load predefined response templates for different types of questions"""
        return {
            "budget": [
                "💡 Here's a simple budgeting approach: Use the 50/30/20 rule - 50% for needs, 30% for wants, and 20% for savings and debt repayment.",
                "📊 Start by tracking all your expenses for a month to understand where your money goes, then create a realistic budget.",
                "🎯 Set specific financial goals and allocate your income accordingly. Remember, a budget is a plan for your money.",
                "📱 Use budgeting apps to track your expenses and stay within your financial goals."
            ],
            "saving": [
                "💰 Start small - even saving ₹100 per day adds up to ₹36,500 per year! Set up automatic transfers to make it easier.",
                "🏦 Build an emergency fund first (3-6 months of expenses), then focus on other savings goals.",
                "📈 Consider high-yield savings accounts or fixed deposits for better returns on your savings.",
                "🎯 Set up automatic transfers to a savings account on payday to build your emergency fund."
            ],
            "investing": [
                "📈 Start with low-risk options like index funds or SIPs. Remember, time in the market beats timing the market.",
                "💼 Diversify your investments across different asset classes to reduce risk.",
                "🎯 Consider your risk tolerance and investment horizon before making investment decisions.",
                "🏦 Start with small amounts in mutual funds or SIPs to build investment habits."
            ],
            "debt": [
                "💳 Focus on paying high-interest debt first (like credit cards) before low-interest debt.",
                "🔄 Consider debt consolidation if you have multiple high-interest loans.",
                "📋 Create a debt repayment plan and stick to it. Every extra payment helps reduce the total interest.",
                "🎯 Pay more than the minimum payment on credit cards to reduce interest charges."
            ],
            "expenses": [
                "📱 Track your expenses daily using apps or a simple spreadsheet to identify spending patterns.",
                "🛒 Use the 24-hour rule for non-essential purchases - wait a day before buying.",
                "💡 Look for ways to reduce recurring expenses like subscriptions you don't use.",
                "🎯 Create a shopping list and stick to it to avoid unnecessary purchases."
            ],
            "food_saving": [
                "🍽️ Plan your meals for the week and make a grocery list to avoid impulse purchases.",
                "🥘 Cook in bulk and freeze portions for busy days to save time and money.",
                "🛒 Buy generic brands for basic items - they're often just as good as name brands.",
                "🍕 Limit eating out to special occasions and cook more meals at home."
            ],
            "transport_saving": [
                "🚗 Carpool with colleagues or friends to split fuel costs.",
                "🚌 Use public transportation when possible - it's much cheaper than driving.",
                "🚲 Consider walking or cycling for short distances to save money and stay healthy.",
                "⛽ Plan your routes efficiently to minimize fuel consumption."
            ],
            "shopping_saving": [
                "🛍️ Wait for sales and use coupons when shopping for non-essential items.",
                "📱 Unsubscribe from marketing emails to reduce impulse buying.",
                "💳 Use cash or debit cards for shopping to avoid credit card interest.",
                "🎯 Buy quality items that last longer instead of cheap items that need frequent replacement."
            ],
            "general": [
                "💡 Financial success comes from consistent small actions over time, not big changes overnight.",
                "📚 Educate yourself about personal finance through books, podcasts, or online courses.",
                "🎯 Set SMART financial goals: Specific, Measurable, Achievable, Relevant, and Time-bound.",
                "🛡️ Build an emergency fund of 3-6 months of expenses before making major investments."
            ]
        }
    
    def chat(self, user_message, user_profile=None, transaction_analysis=None):
        """Handle chat interaction with financial context"""
        message_lower = user_message.lower()
        
        # Determine the topic of the question
        topic = self._identify_topic(message_lower)
        
        # Get appropriate response
        if topic in self.response_templates:
            response = random.choice(self.response_templates[topic])
        else:
            response = random.choice(self.response_templates["general"])
        
        # Add personalized context if available
        if user_profile and transaction_analysis:
            personalized_context = self._add_personalized_context(user_profile, transaction_analysis, topic)
            if personalized_context:
                response += f"\n\n{personalized_context}"
        
        return response
    
    def _identify_topic(self, message_lower):
        """Identify the topic of the user's question"""
        if any(word in message_lower for word in ['budget', 'budgeting', 'allocate', 'spend']):
            return "budget"
        elif any(word in message_lower for word in ['save', 'saving', 'savings', 'emergency fund']):
            return "saving"
        elif any(word in message_lower for word in ['invest', 'investment', 'mutual fund', 'sip', 'stock']):
            return "investing"
        elif any(word in message_lower for word in ['debt', 'loan', 'credit card', 'pay off']):
            return "debt"
        elif any(word in message_lower for word in ['food', 'eating', 'restaurant', 'grocery']):
            return "food_saving"
        elif any(word in message_lower for word in ['transport', 'fuel', 'petrol', 'uber', 'taxi']):
            return "transport_saving"
        elif any(word in message_lower for word in ['shopping', 'amazon', 'flipkart', 'buy', 'purchase']):
            return "shopping_saving"
        elif any(word in message_lower for word in ['expense', 'spending', 'cost', 'reduce']):
            return "expenses"
        else:
            return "general"
    
    def _add_personalized_context(self, user_profile, transaction_analysis, topic):
        """Add personalized context based on user profile and transaction analysis"""
        context_parts = []
        
        monthly_income = transaction_analysis.get('monthly_income_avg', 0)
        monthly_expenses = transaction_analysis.get('monthly_expenses_avg', 0)
        financial_health_score = transaction_analysis.get('financial_health_score', 50)
        top_categories = transaction_analysis.get('top_spending_categories', {})
        savings_target = user_profile.get('financial_goals', {}).get('monthly_savings_target', 0)
        
        if topic == "budget":
            if monthly_income > 0:
                savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100)
                if savings_rate < 10:
                    context_parts.append("Based on your current spending, consider reducing expenses in your top categories to improve your savings rate.")
                elif savings_rate > 20:
                    context_parts.append("Great job on your savings rate! You're doing well with your budget.")
        
        elif topic == "saving":
            if savings_target > 0:
                current_savings = monthly_income - monthly_expenses
                if current_savings < savings_target:
                    gap = savings_target - current_savings
                    context_parts.append(f"You're currently saving ₹{current_savings:,.2f} but your target is ₹{savings_target:,.2f}. You need to save ₹{gap:,.2f} more per month.")
                else:
                    context_parts.append(f"Excellent! You're meeting your savings target of ₹{savings_target:,.2f} per month.")
        
        elif topic == "investing":
            if "Investments" not in top_categories or top_categories.get("Investments", 0) == 0:
                context_parts.append("I notice you don't have any investment transactions yet. This could be a great next step for you!")
        
        elif topic in ["food_saving", "transport_saving", "shopping_saving"]:
            if top_categories:
                # Find the relevant category
                relevant_category = None
                if topic == "food_saving":
                    relevant_category = "Food & Dining"
                elif topic == "transport_saving":
                    relevant_category = "Transportation"
                elif topic == "shopping_saving":
                    relevant_category = "Shopping"
                
                if relevant_category in top_categories:
                    amount = top_categories[relevant_category]
                    context_parts.append(f"Your {relevant_category} expenses are ₹{amount:,.2f}. Here are some specific tips to reduce this category.")
        
        return " ".join(context_parts) if context_parts else None
    
    def get_suggested_questions(self, user_profile=None, transaction_analysis=None):
        """Get suggested questions based on user profile and transaction analysis"""
        if not user_profile or not transaction_analysis:
            return [
                "How can I start budgeting?",
                "What's the best way to save money?",
                "Should I invest in mutual funds?",
                "How much should I save for emergencies?",
                "How can I reduce my expenses?"
            ]
        
        suggestions = []
        financial_health_score = transaction_analysis.get('financial_health_score', 50)
        monthly_income = transaction_analysis.get('monthly_income_avg', 0)
        monthly_expenses = transaction_analysis.get('monthly_expenses_avg', 0)
        top_categories = transaction_analysis.get('top_spending_categories', {})
        savings_target = user_profile.get('financial_goals', {}).get('monthly_savings_target', 0)
        
        # Health score based suggestions
        if financial_health_score < 40:
            suggestions.extend([
                "How can I improve my financial health?",
                "What should I prioritize: saving or paying debt?",
                "How can I reduce my monthly expenses?"
            ])
        elif financial_health_score > 70:
            suggestions.extend([
                "How can I optimize my investments?",
                "What are good long-term investment options?",
                "How can I maximize my savings rate?"
            ])
        
        # Income vs expenses based suggestions
        if monthly_expenses > monthly_income:
            suggestions.append("I'm spending more than I earn. What should I do?")
        
        # Category-based suggestions
        if 'Food & Dining' in top_categories:
            suggestions.append("How can I reduce my food expenses?")
        
        if 'Transportation' in top_categories:
            suggestions.append("What are cost-effective transportation options?")
        
        if 'Shopping' in top_categories:
            suggestions.append("How can I save money on shopping?")
        
        # Savings target suggestions
        if savings_target > 0:
            current_savings = monthly_income - monthly_expenses
            if current_savings < savings_target:
                suggestions.append("How can I reach my monthly savings target?")
        
        # Generic suggestions
        suggestions.extend([
            "How should I allocate my monthly income?",
            "What's a good emergency fund amount?",
            "How can I track my expenses better?"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions

def chat_with_bot(user_message, user_profile=None, transaction_analysis=None):
    """Main function to chat with the financial bot"""
    bot = FreeFinanceChatbot()
    response = bot.chat(user_message, user_profile, transaction_analysis)
    return response

def get_suggested_questions(user_profile=None, transaction_analysis=None):
    """Get suggested questions for the user"""
    bot = FreeFinanceChatbot()
    return bot.get_suggested_questions(user_profile, transaction_analysis)
