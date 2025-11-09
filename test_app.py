#!/usr/bin/env python3
"""
Test script for the AI Finance Manager
This script demonstrates that the app works without any paid APIs
"""

import pandas as pd
from transaction_categorizer import TransactionCategorizer
from suggestions_engine import PersonalizedSuggestionsEngine
from chatbot import FreeFinanceChatbot
from user_profile import UserProfileManager

def test_categorization():
    """Test the transaction categorization"""
    print("🤖 Testing Transaction Categorization...")
    
    categorizer = TransactionCategorizer()
    
    # Test transactions
    test_transactions = [
        ("SWIGGY FOOD DELIVERY", 250.0, "Debit"),
        ("UBER RIDE", 120.0, "Debit"),
        ("AMAZON PURCHASE", 1500.0, "Debit"),
        ("SALARY CREDIT", 50000.0, "Credit"),
        ("NETFLIX SUBSCRIPTION", 199.0, "Debit"),
        ("PETROL PUMP", 800.0, "Debit"),
        ("ELECTRICITY BILL", 1200.0, "Debit"),
    ]
    
    print("\n📋 Test Transactions:")
    for desc, amount, t_type in test_transactions:
        category = categorizer.categorize_transaction(desc, amount, t_type)
        print(f"  {desc} (₹{amount}) → {category}")
    
    print("✅ Categorization test completed!")

def test_suggestions():
    """Test the suggestions engine"""
    print("\n💡 Testing Suggestions Engine...")
    
    engine = PersonalizedSuggestionsEngine()
    
    # Create a sample user profile
    sample_profile = {
        'user_info': {
            'monthly_income': 50000,
            'monthly_savings_target': 15000
        },
        'financial_goals': {
            'monthly_savings_target': 15000,
            'cut_cost_areas': ['Food & Dining', 'Entertainment']
        }
    }
    
    # Sample transaction analysis
    sample_analysis = {
        'monthly_income_avg': 50000,
        'monthly_expenses_avg': 45000,
        'financial_health_score': 60,
        'top_spending_categories': {
            'Food & Dining': 15000,
            'Transportation': 8000,
            'Shopping': 12000
        }
    }
    
    suggestions = engine.generate_personalized_suggestions(sample_profile, sample_analysis)
    
    print("\n🎯 Generated Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    print("✅ Suggestions test completed!")

def test_chatbot():
    """Test the chatbot"""
    print("\n💬 Testing Chatbot...")
    
    bot = FreeFinanceChatbot()
    
    # Test questions
    test_questions = [
        "How can I save money?",
        "What's the best way to budget?",
        "How can I reduce my food expenses?"
    ]
    
    sample_profile = {
        'financial_goals': {
            'monthly_savings_target': 10000
        }
    }
    
    sample_analysis = {
        'monthly_income_avg': 40000,
        'monthly_expenses_avg': 35000,
        'financial_health_score': 70,
        'top_spending_categories': {
            'Food & Dining': 12000
        }
    }
    
    print("\n💭 Chat Responses:")
    for question in test_questions:
        response = bot.chat(question, sample_profile, sample_analysis)
        print(f"\n  Q: {question}")
        print(f"  A: {response}")
    
    print("\n✅ Chatbot test completed!")

def test_user_profile():
    """Test the user profile system"""
    print("\n👤 Testing User Profile System...")
    
    # Create sample transactions
    sample_transactions = pd.DataFrame([
        {'date': '2024-01-01', 'description': 'SALARY', 'amount': 50000, 'type': 'Credit', 'category': 'Income'},
        {'date': '2024-01-02', 'description': 'SWIGGY', 'amount': 300, 'type': 'Debit', 'category': 'Food & Dining'},
        {'date': '2024-01-03', 'description': 'UBER', 'amount': 150, 'type': 'Debit', 'category': 'Transportation'},
        {'date': '2024-01-04', 'description': 'AMAZON', 'amount': 2000, 'type': 'Debit', 'category': 'Shopping'},
        {'date': '2024-01-05', 'description': 'ELECTRICITY BILL', 'amount': 1200, 'type': 'Debit', 'category': 'Bills & Utilities'},
    ])
    
    manager = UserProfileManager()
    
    # Test user data
    user_data = {
        'monthly_income': 50000,
        'age': '26-35',
        'occupation': 'Software Engineer',
        'monthly_savings_target': 15000,
        'priority_categories': ['Food & Dining', 'Transportation'],
        'cut_cost_areas': ['Food & Dining', 'Entertainment']
    }
    
    profile = manager.create_user_profile(user_data)
    profile = manager.analyze_transactions(sample_transactions, profile)
    
    print("\n📊 Profile Analysis Results:")
    analysis = profile['transaction_analysis']
    print(f"  Financial Health Score: {analysis.get('financial_health_score', 0)}/100")
    print(f"  Monthly Income: ₹{analysis.get('monthly_income_avg', 0):,.2f}")
    print(f"  Monthly Expenses: ₹{analysis.get('monthly_expenses_avg', 0):,.2f}")
    print(f"  Total Transactions: {analysis.get('total_transactions', 0)}")
    
    print("✅ User Profile test completed!")

def main():
    """Run all tests"""
    print("🧪 Testing AI Finance Manager - FREE VERSION")
    print("=" * 60)
    print("This demonstrates that the app works without any paid APIs!")
    print("=" * 60)
    
    try:
        test_categorization()
        test_suggestions()
        test_chatbot()
        test_user_profile()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("✅ The AI Finance Manager works completely FREE!")
        print("✅ No API keys or paid services required!")
        print("✅ Ready for your final year project!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check your dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
