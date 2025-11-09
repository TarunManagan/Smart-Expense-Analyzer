# 💰 AI Finance Manager

An intelligent personal finance management system that analyzes your transaction data and provides personalized financial advice. **100% FREE** - no paid APIs required!

## 🚀 Features

### 📄 Data Input
- **PDF Bank Statements**: Upload and parse bank statement PDFs
- **CSV Files**: Direct upload of transaction data
- **Automatic Categorization**: Smart categorization of transactions

### 👤 User Profile
- **Personalized Questionnaire**: Income, age, occupation, financial goals
- **Savings Targets**: Set monthly savings goals
- **Priority Areas**: Identify spending priorities and cost-cutting areas

### 📊 Interactive Dashboard
- **Financial Health Score**: Overall financial wellness indicator
- **Expense Breakdown**: Visual charts by category
- **Monthly Trends**: Spending patterns over time
- **Key Metrics**: Income, expenses, savings analysis

### 💡 Personalized Suggestions
- **Smart Recommendations**: Based on your profile and spending patterns
- **Budget Recommendations**: 50/30/20 rule with custom adjustments
- **Quick Tips**: Actionable financial advice
- **Category-Specific Advice**: Targeted suggestions for each spending area

### 💬 AI Chat Assistant
- **Free AI Chatbot**: No paid APIs - uses intelligent templates
- **Context-Aware Responses**: Personalized based on your profile
- **Suggested Questions**: Pre-generated questions based on your data
- **Real-time Guidance**: Instant financial advice

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai-finance-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📋 How to Use

### Step 1: Upload Your Data
1. Go to **"📄 Upload Data"** page
2. Choose one of two options:
   - **PDF Upload**: Upload your bank statement PDF
   - **CSV Upload**: Upload transaction data in CSV format
3. The system will automatically parse and categorize your transactions

### Step 2: Create Your Profile
1. Go to **"👤 User Profile"** page
2. Fill out the questionnaire:
   - Monthly income
   - Age range
   - Occupation
   - Monthly savings target
   - Priority spending categories
   - Areas where you want to cut costs
3. Click "Create Profile" to analyze your transactions

### Step 3: View Your Dashboard
1. Go to **"🏠 Dashboard"** page
2. See your financial health score and key metrics
3. Explore interactive charts showing your spending patterns
4. Review your top spending categories

### Step 4: Get Personalized Suggestions
1. Go to **"💡 Suggestions"** page
2. Click "Generate New Suggestions"
3. Get personalized financial advice based on your profile
4. View budget recommendations and quick tips

### Step 5: Chat with AI Assistant
1. Go to **"💬 Chat Assistant"** page
2. Ask questions about your finances
3. Get instant, personalized responses
4. Use suggested questions for quick guidance

## 🏗️ Project Structure

```
ai-finance-manager/
├── app.py                    # Main Streamlit application
├── config.py                # Configuration and categories
├── pdf_parser.py            # PDF parsing functionality
├── transaction_categorizer.py # Transaction categorization
├── user_profile.py          # User profile management
├── suggestions_engine.py    # Personalized suggestions
├── chatbot.py              # Free AI chatbot
├── demo_data.py            # Demo data generator
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── uploads/               # Directory for uploaded files
├── data/                  # Directory for processed data
└── profiles/              # Directory for user profiles
```

## 🎯 Key Features Explained

### PDF Parsing
- Extracts transactions from bank statement PDFs
- Supports both text-based and table-based PDFs
- Handles various date and amount formats
- Saves results to CSV for further analysis

### Smart Categorization
- **Rule-based**: Uses keyword matching for accurate categorization
- **11 Categories**: Food, Transportation, Shopping, Bills, Entertainment, etc.
- **Automatic**: No manual work required
- **Editable**: Manual adjustments available

### User Profile System
- **Comprehensive Questionnaire**: Captures financial goals and preferences
- **Personalized Analysis**: Tailored suggestions based on your profile
- **Goal Tracking**: Monitors progress toward savings targets
- **Priority Management**: Focuses on areas you want to improve

### Free AI Chatbot
- **Template-based Intelligence**: Smart responses without paid APIs
- **Context-Aware**: Uses your profile and transaction data
- **Personalized**: Responses tailored to your financial situation
- **Always Available**: No rate limits or usage restrictions

## 📊 Data Flow

1. **Upload** → PDF/CSV → **Parse** → Raw Transactions
2. **Categorize** → Smart Rules → **Categorized Data**
3. **Profile** → Questionnaire → **User Profile**
4. **Analyze** → Profile + Data → **Financial Insights**
5. **Suggest** → Insights → **Personalized Advice**
6. **Chat** → Questions → **AI Responses**

## 🔒 Privacy & Security

- **Local Processing**: All data processed on your machine
- **No Cloud Storage**: Data stays on your device
- **No API Calls**: No data sent to external services
- **Secure**: Your financial data remains private

## 🚨 Requirements

### CSV Format
If uploading CSV files, ensure they have these columns:
- `date`: Transaction date (YYYY-MM-DD format)
- `description`: Transaction description
- `amount`: Transaction amount (positive number)
- `type`: Transaction type (Debit/Credit)

### PDF Format
- Works best with standard bank statement formats
- Text-based PDFs work better than image-based ones
- Supports most major bank statement layouts

## 🛠️ Troubleshooting

### Common Issues

1. **"No transactions found in PDF"**
   - Try a different PDF format
   - Ensure the PDF contains readable text
   - Check if the bank statement format is supported

2. **"Error categorizing transactions"**
   - The system uses multiple fallback methods
   - Check if transaction descriptions are clear
   - Manual categorization is always available

3. **"Poor categorization accuracy"**
   - Use the manual categorization feature to adjust
   - The system learns from your corrections
   - Categories can be edited in the upload page

## 📈 Demo Data

To test the application without your own data:

1. Run the demo data generator:
   ```bash
   python demo_data.py
   ```

2. This creates sample transaction data and user profile
3. Upload the generated CSV file to test all features

## 🎓 Perfect for Final Year Projects

This project demonstrates:
- **Data Processing**: PDF parsing, CSV handling
- **Machine Learning**: Smart categorization algorithms
- **Web Development**: Streamlit dashboard
- **Data Visualization**: Interactive charts with Plotly
- **User Experience**: Intuitive interface design
- **AI Integration**: Free chatbot implementation

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Streamlit** for the web framework
- **Plotly** for interactive visualizations
- **PDFplumber** for PDF parsing
- **Pandas** for data manipulation
- **Scikit-learn** for machine learning algorithms

---

**Note**: This is a final year project for educational purposes. Always consult with a qualified financial advisor for important financial decisions.