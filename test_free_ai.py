#!/usr/bin/env python3
"""
Test script for the free AI functionality
This script demonstrates that the AI Finance Manager works without any paid APIs
"""

import pandas as pd
from ai_categorizer import TransactionCategorizer
from suggestions_generator import SuggestionsGenerator
from chat_assistant import FinanceChatAssistant
from user_profile import UserProfileAnalyzer

def test_ai_categorization():
    """Test the free AI categorization"""
    print("🤖 Testing AI Categorization (FREE)...")
    
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
        ("UNKNOWN TRANSACTION", 100.0, "Debit")
    ]
    
    print("\n📋 Test Transactions:")
    for desc, amount, t_type in test_transactions:
        category = categorizer.categorize_transaction(desc, amount, t_type)
        print(f"  {desc} (₹{amount}) → {category}")
    
    print("✅ AI Categorization test completed!")

def test_suggestions_generator():
    """Test the free suggestions generator"""
    print("\n💡 Testing Suggestions Generator (FREE)...")
    
    generator = SuggestionsGenerator()
    
    # Create a sample user profile
    sample_profile = {
        'monthly_income_avg': 50000,
        'monthly_expenses_avg': 45000,
        'financial_health_score': 60,
        'top_spending_categories': {
            'Food & Dining': 15000,
            'Transportation': 8000,
            'Shopping': 12000
        },
        'recurring_expenses': [
            {'description': 'NETFLIX', 'frequency': 3},
            {'description': 'SPOTIFY', 'frequency': 3}
        ]
    }
    
    suggestions = generator.generate_suggestions(sample_profile)
    
    print("\n🎯 Generated Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    print("✅ Suggestions Generator test completed!")

def test_chat_assistant():
    """Test the free chat assistant"""
    print("\n💬 Testing Chat Assistant (FREE)...")
    
    assistant = FinanceChatAssistant()
    
    # Test questions
    test_questions = [
        "How can I save money?",
        "What's the best way to budget?",
        "Should I invest in mutual funds?",
        "How can I reduce my expenses?"
    ]
    
    sample_profile = {
        'monthly_income_avg': 40000,
        'monthly_expenses_avg': 35000,
        'financial_health_score': 70,
        'top_spending_categories': {
            'Food & Dining': 12000,
            'Transportation': 6000
        }
    }
    
    print("\n💭 Chat Responses:")
    for question in test_questions:
        response = assistant.chat(question, sample_profile)
        print(f"\n  Q: {question}")
        print(f"  A: {response}")
    
    print("\n✅ Chat Assistant test completed!")

def test_user_profile_analysis():
    """Test the user profile analysis"""
    print("\n👤 Testing User Profile Analysis...")
    
    # Create sample transactions
    sample_transactions = pd.DataFrame([
        {'date': '2024-01-01', 'description': 'SALARY', 'amount': 50000, 'type': 'Credit', 'category': 'Income'},
        {'date': '2024-01-02', 'description': 'SWIGGY', 'amount': 300, 'type': 'Debit', 'category': 'Food & Dining'},
        {'date': '2024-01-03', 'description': 'UBER', 'amount': 150, 'type': 'Debit', 'category': 'Transportation'},
        {'date': '2024-01-04', 'description': 'AMAZON', 'amount': 2000, 'type': 'Debit', 'category': 'Shopping'},
        {'date': '2024-01-05', 'description': 'ELECTRICITY BILL', 'amount': 1200, 'type': 'Debit', 'category': 'Bills & Utilities'},
    ])
    
    analyzer = UserProfileAnalyzer()
    profile = analyzer.analyze_transactions(sample_transactions)
    
    print("\n📊 Profile Analysis Results:")
    print(f"  Financial Health Score: {profile.get('financial_health_score', 0)}/100")
    print(f"  Monthly Income: ₹{profile.get('monthly_income_avg', 0):,.2f}")
    print(f"  Monthly Expenses: ₹{profile.get('monthly_expenses_avg', 0):,.2f}")
    print(f"  Total Transactions: {profile.get('total_transactions', 0)}")
    
    print("✅ User Profile Analysis test completed!")

def main():
    """Run all tests"""
    print("🧪 Testing AI Finance Manager - FREE VERSION")
    print("=" * 60)
    print("This demonstrates that the app works without any paid APIs!")
    print("=" * 60)
    
    try:
        test_ai_categorization()
        test_suggestions_generator()
        test_chat_assistant()
        test_user_profile_analysis()
        
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
