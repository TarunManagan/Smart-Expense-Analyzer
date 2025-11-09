import os

# Transaction Categories
CATEGORIES = [
    "Food & Dining",
    "Transportation", 
    "Shopping",
    "Bills & Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Travel",
    "Investments",
    "Income",
    "Other"
]

# Category keywords for rule-based categorization
CATEGORY_KEYWORDS = {
    "Food & Dining": [
        "food", "restaurant", "swiggy", "zomato", "dominos", "mcdonalds", 
        "starbucks", "grocery", "supermarket", "cafe", "dining", "meal",
        "pizza", "burger", "coffee", "tea", "snack", "lunch", "dinner"
    ],
    "Transportation": [
        "uber", "ola", "taxi", "cab", "petrol", "diesel", "fuel", "gas",
        "bus", "train", "metro", "parking", "toll", "transport", "ride"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "shopping", "mall", "store", "shop",
        "clothes", "fashion", "electronics", "book", "purchase", "order"
    ],
    "Bills & Utilities": [
        "electricity", "water", "internet", "phone", "bill", "utility",
        "gas", "rent", "insurance", "credit card", "premium", "subscription"
    ],
    "Entertainment": [
        "netflix", "spotify", "movie", "cinema", "game", "gaming", "entertainment",
        "concert", "theater", "streaming", "music", "video", "show"
    ],
    "Healthcare": [
        "hospital", "doctor", "medicine", "pharmacy", "health", "medical",
        "clinic", "dental", "eye", "prescription", "treatment"
    ],
    "Education": [
        "school", "college", "university", "course", "book", "education",
        "tuition", "fee", "student", "learning", "training"
    ],
    "Travel": [
        "hotel", "flight", "travel", "vacation", "trip", "booking",
        "airline", "resort", "tourism", "journey"
    ],
    "Investments": [
        "investment", "mutual fund", "stock", "savings", "sip", "equity",
        "portfolio", "fund", "trading", "brokerage"
    ],
    "Income": [
        "salary", "bonus", "income", "credit", "deposit", "refund",
        "cashback", "interest", "dividend", "freelance", "payment"
    ]
}

# File paths
UPLOAD_DIR = "uploads"
DATA_DIR = "data"
PROFILES_DIR = "profiles"

# Create directories if they don't exist
for directory in [UPLOAD_DIR, DATA_DIR, PROFILES_DIR]:
    os.makedirs(directory, exist_ok=True)