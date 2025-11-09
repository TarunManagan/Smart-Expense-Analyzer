"""
Demo data generator for testing the AI Finance Manager
This creates sample transaction data for demonstration purposes
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_demo_transactions(num_transactions=50):
    """Generate demo transaction data"""
    
    # Sample transaction descriptions
    food_descriptions = [
        "SWIGGY FOOD DELIVERY", "ZOMATO ORDER", "DOMINOS PIZZA", "MCDONALDS", 
        "STARBUCKS COFFEE", "GROCERY STORE", "SUPERMARKET", "RESTAURANT BILL"
    ]
    
    transport_descriptions = [
        "UBER RIDE", "OLA CAB", "PETROL PUMP", "DIESEL FILLING", 
        "BUS TICKET", "TRAIN TICKET", "PARKING FEE", "TOLL GATE"
    ]
    
    shopping_descriptions = [
        "AMAZON PURCHASE", "FLIPKART ORDER", "MYNTRA SHOPPING", "CLOTHES STORE",
        "ELECTRONICS SHOP", "BOOKSTORE", "ONLINE SHOPPING", "MALL PURCHASE"
    ]
    
    bills_descriptions = [
        "ELECTRICITY BILL", "WATER BILL", "INTERNET BILL", "PHONE BILL",
        "GAS BILL", "RENT PAYMENT", "INSURANCE PREMIUM", "CREDIT CARD BILL"
    ]
    
    entertainment_descriptions = [
        "NETFLIX SUBSCRIPTION", "SPOTIFY PREMIUM", "MOVIE TICKET", "GAME PURCHASE",
        "CONCERT TICKET", "THEATER SHOW", "GAMING STORE", "STREAMING SERVICE"
    ]
    
    income_descriptions = [
        "SALARY CREDIT", "BONUS PAYMENT", "FREELANCE INCOME", "INVESTMENT RETURN",
        "REFUND CREDIT", "CASHBACK REWARD", "INTEREST EARNED", "DIVIDEND PAYMENT"
    ]
    
    # Create transactions
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(num_transactions):
        # Random date within last 3 months
        random_days = random.randint(0, 90)
        date = start_date + timedelta(days=random_days)
        
        # Random category and description
        category = random.choice(['Food & Dining', 'Transportation', 'Shopping', 
                                'Bills & Utilities', 'Entertainment', 'Income'])
        
        if category == 'Food & Dining':
            description = random.choice(food_descriptions)
            amount = random.uniform(50, 800)
            transaction_type = 'Debit'
        elif category == 'Transportation':
            description = random.choice(transport_descriptions)
            amount = random.uniform(20, 500)
            transaction_type = 'Debit'
        elif category == 'Shopping':
            description = random.choice(shopping_descriptions)
            amount = random.uniform(100, 2000)
            transaction_type = 'Debit'
        elif category == 'Bills & Utilities':
            description = random.choice(bills_descriptions)
            amount = random.uniform(200, 1500)
            transaction_type = 'Debit'
        elif category == 'Entertainment':
            description = random.choice(entertainment_descriptions)
            amount = random.uniform(50, 1000)
            transaction_type = 'Debit'
        elif category == 'Income':
            description = random.choice(income_descriptions)
            amount = random.uniform(5000, 50000)
            transaction_type = 'Credit'
        
        transactions.append({
            'date': date.date(),
            'description': description,
            'amount': round(amount, 2),
            'type': transaction_type,
            'category': category
        })
    
    return pd.DataFrame(transactions)

def create_demo_files():
    """Create demo files for testing"""
    
    # Generate demo transactions
    print("Generating demo transaction data...")
    demo_df = generate_demo_transactions(100)
    
    # Save to CSV
    demo_df.to_csv('data/demo_transactions.csv', index=False)
    print("✅ Demo transactions saved to data/demo_transactions.csv")
    
    # Create a sample profile
    from user_profile import UserProfileManager
    manager = UserProfileManager()
    
    # Sample user data
    sample_user_data = {
        'monthly_income': 50000,
        'age': '26-35',
        'occupation': 'Software Engineer',
        'monthly_savings_target': 15000,
        'priority_categories': ['Food & Dining', 'Transportation', 'Shopping'],
        'cut_cost_areas': ['Food & Dining', 'Entertainment']
    }
    
    profile = manager.create_user_profile(sample_user_data)
    profile = manager.analyze_transactions(demo_df, profile)
    
    # Save profile
    import json
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
    with open('profiles/demo_profile.json', 'w') as f:
        json.dump(profile_serializable, f, indent=2, default=str)
    print("✅ Demo profile saved to profiles/demo_profile.json")
    
    print("\n🎉 Demo data created successfully!")
    print("You can now test the application with this sample data.")
    print("\nTo use demo data:")
    print("1. Go to 'Upload Data' page")
    print("2. Upload the demo_transactions.csv file")
    print("3. Create a user profile")
    print("4. Explore the dashboard and suggestions!")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('profiles', exist_ok=True)
    
    create_demo_files()