import json
import random
from datetime import datetime
from config import USE_FREE_AI

class FinanceChatAssistant:
    def __init__(self):
        self.response_templates = self._load_response_templates()
    
    def _load_response_templates(self):
        """Load predefined response templates for different types of questions"""
        return {
            "budget": [
                "💡 Here's a simple budgeting approach: Use the 50/30/20 rule - 50% for needs, 30% for wants, and 20% for savings and debt repayment.",
                "📊 Start by tracking all your expenses for a month to understand where your money goes, then create a realistic budget.",
                "🎯 Set specific financial goals and allocate your income accordingly. Remember, a budget is a plan for your money."
            ],
            "saving": [
                "💰 Start small - even saving ₹100 per day adds up to ₹36,500 per year! Set up automatic transfers to make it easier.",
                "🏦 Build an emergency fund first (3-6 months of expenses), then focus on other savings goals.",
                "📈 Consider high-yield savings accounts or fixed deposits for better returns on your savings."
            ],
            "investing": [
                "📈 Start with low-risk options like index funds or SIPs. Remember, time in the market beats timing the market.",
                "💼 Diversify your investments across different asset classes to reduce risk.",
                "🎯 Consider your risk tolerance and investment horizon before making investment decisions."
            ],
            "debt": [
                "💳 Focus on paying high-interest debt first (like credit cards) before low-interest debt.",
                "🔄 Consider debt consolidation if you have multiple high-interest loans.",
                "📋 Create a debt repayment plan and stick to it. Every extra payment helps reduce the total interest."
            ],
            "expenses": [
                "📱 Track your expenses daily using apps or a simple spreadsheet to identify spending patterns.",
                "🛒 Use the 24-hour rule for non-essential purchases - wait a day before buying.",
                "💡 Look for ways to reduce recurring expenses like subscriptions you don't use."
            ],
            "general": [
                "💡 Financial success comes from consistent small actions over time, not big changes overnight.",
                "📚 Educate yourself about personal finance through books, podcasts, or online courses.",
                "🎯 Set SMART financial goals: Specific, Measurable, Achievable, Relevant, and Time-bound."
            ]
        }
    
    def chat(self, user_message, user_profile=None, recent_transactions=None, chat_history=None):
        """Handle chat interaction with financial context"""
        return self._generate_smart_response(user_message, user_profile)
    
    def _generate_smart_response(self, user_message, user_profile):
        """Generate smart responses based on user message and profile"""
        message_lower = user_message.lower()
        
        # Determine the topic of the question
        topic = self._identify_topic(message_lower)
        
        # Get appropriate response
        if topic in self.response_templates:
            response = random.choice(self.response_templates[topic])
        else:
            response = random.choice(self.response_templates["general"])
        
        # Add personalized context if available
        if user_profile:
            personalized_context = self._add_personalized_context(user_profile, topic)
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
        elif any(word in message_lower for word in ['expense', 'spending', 'cost', 'reduce']):
            return "expenses"
        else:
            return "general"
    
    def _add_personalized_context(self, user_profile, topic):
        """Add personalized context based on user profile"""
        monthly_income = user_profile.get('monthly_income_avg', 0)
        monthly_expenses = user_profile.get('monthly_expenses_avg', 0)
        financial_health_score = user_profile.get('financial_health_score', 50)
        top_categories = user_profile.get('top_spending_categories', {})
        
        context_parts = []
        
        if topic == "budget":
            if monthly_income > 0:
                savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100)
                if savings_rate < 10:
                    context_parts.append("Based on your current spending, consider reducing expenses in your top categories to improve your savings rate.")
                elif savings_rate > 20:
                    context_parts.append("Great job on your savings rate! You're doing well with your budget.")
        
        elif topic == "saving":
            if financial_health_score < 40:
                context_parts.append("Given your current financial situation, focus on building a small emergency fund first.")
            elif financial_health_score > 70:
                context_parts.append("Your financial health is good! Consider increasing your savings rate or starting investments.")
        
        elif topic == "investing":
            if "Investments" not in top_categories or top_categories.get("Investments", 0) == 0:
                context_parts.append("I notice you don't have any investment transactions yet. This could be a great next step for you!")
        
        elif topic == "expenses":
            if top_categories:
                top_category = list(top_categories.keys())[0]
                top_amount = list(top_categories.values())[0]
                context_parts.append(f"Your highest expense category is {top_category} (₹{top_amount:,.2f}). Consider reviewing this area for potential savings.")
        
        return " ".join(context_parts) if context_parts else None
    
    def get_suggested_questions(self, user_profile=None):
        """Get suggested questions based on user profile"""
        if not user_profile:
            return [
                "How can I start budgeting?",
                "What's the best way to save money?",
                "Should I invest in mutual funds?",
                "How much should I save for emergencies?",
                "How can I reduce my expenses?"
            ]
        
        suggestions = []
        financial_health_score = user_profile.get('financial_health_score', 50)
        monthly_income = user_profile.get('monthly_income_avg', 0)
        monthly_expenses = user_profile.get('monthly_expenses_avg', 0)
        top_categories = user_profile.get('top_spending_categories', {})
        
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
        
        if 'Entertainment' in top_categories:
            suggestions.append("How can I find cheaper entertainment options?")
        
        # Generic suggestions
        suggestions.extend([
            "How should I allocate my monthly income?",
            "What's a good emergency fund amount?",
            "How can I track my expenses better?"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions

def chat_with_assistant(user_message, user_profile=None, recent_transactions=None, chat_history=None):
    """Main function to chat with the financial assistant"""
    assistant = FinanceChatAssistant()
    response = assistant.chat(user_message, user_profile, recent_transactions, chat_history)
    return response

def get_suggested_questions(user_profile=None):
    """Get suggested questions for the user"""
    assistant = FinanceChatAssistant()
    return assistant.get_suggested_questions(user_profile)
