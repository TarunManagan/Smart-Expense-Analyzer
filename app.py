import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Import our custom modules
from pdf_parser import parse_bank_statement
from transaction_categorizer import categorize_transactions
from user_profile import create_user_profile, analyze_user_transactions
from suggestions_engine import generate_personalized_suggestions
from chatbot import chat_with_bot, get_suggested_questions
from config import CATEGORIES

# Helper functions for flexible CSV handling
def auto_detect_columns(columns):
    """Auto-detect and map CSV columns to standard format"""
    column_mapping = {}
    columns_lower = [col.lower().strip() for col in columns]
    
    # Date column detection
    date_keywords = ['date', 'transaction_date', 'posted_date', 'value_date', 'tran_date', 'trans_date']
    for keyword in date_keywords:
        for i, col in enumerate(columns_lower):
            if keyword in col:
                column_mapping[columns[i]] = 'date'
                break
        if 'date' in column_mapping.values():
            break
    
    # Description column detection
    desc_keywords = ['description', 'memo', 'details', 'narration', 'particulars', 'transaction_details', 'remarks', 'note']
    for keyword in desc_keywords:
        for i, col in enumerate(columns_lower):
            if keyword in col:
                column_mapping[columns[i]] = 'description'
                break
        if 'description' in column_mapping.values():
            break
    
    # Amount column detection
    amount_keywords = ['amount', 'value', 'sum', 'total', 'transaction_amount', 'debit', 'credit', 'balance']
    for keyword in amount_keywords:
        for i, col in enumerate(columns_lower):
            if keyword in col:
                column_mapping[columns[i]] = 'amount'
                break
        if 'amount' in column_mapping.values():
            break
    
    # Type column detection (optional - can be inferred from amount)
    type_keywords = ['type', 'debit_credit', 'dr_cr', 'transaction_type', 'cr_dr', 'd_c']
    for keyword in type_keywords:
        for i, col in enumerate(columns_lower):
            if keyword in col:
                column_mapping[columns[i]] = 'type'
                break
    
    # Check if we have at least date, description, and amount
    required_mappings = ['date', 'description', 'amount']
    if all(mapping in column_mapping.values() for mapping in required_mappings):
        return column_mapping
    
    return None

def clean_transaction_data(df):
    """Clean and standardize transaction data"""
    try:
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # Clean date column
        if 'date' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
            # Remove rows with invalid dates
            df_clean = df_clean.dropna(subset=['date'])
        
        # Clean description column
        if 'description' in df_clean.columns:
            df_clean['description'] = df_clean['description'].astype(str).str.strip()
            # Remove rows with empty descriptions
            df_clean = df_clean[df_clean['description'] != '']
        
        # Clean amount column
        if 'amount' in df_clean.columns:
            # Convert to numeric, handling various formats
            df_clean['amount'] = pd.to_numeric(df_clean['amount'], errors='coerce')
            # Remove rows with invalid amounts
            df_clean = df_clean.dropna(subset=['amount'])
            # Remove zero amounts
            df_clean = df_clean[df_clean['amount'] != 0]
        
        # Handle type column
        if 'type' not in df_clean.columns:
            # If no type column, try to infer from amount or other columns
            df_clean['type'] = 'Debit'  # Default to debit
        else:
            # Clean type column
            df_clean['type'] = df_clean['type'].astype(str).str.strip().str.title()
            # Standardize type values
            type_mapping = {
                'Dr': 'Debit', 'Debit': 'Debit', 'D': 'Debit', 'Deb': 'Debit',
                'Cr': 'Credit', 'Credit': 'Credit', 'C': 'Credit', 'Cred': 'Credit'
            }
            df_clean['type'] = df_clean['type'].map(type_mapping).fillna('Debit')
        
        # Remove rows with missing essential data
        df_clean = df_clean.dropna(subset=['date', 'description', 'amount'])
        
        # Sort by date
        df_clean = df_clean.sort_values('date')
        
        # Reset index
        df_clean = df_clean.reset_index(drop=True)
        
        return df_clean
        
    except Exception as e:
        print(f"Error cleaning data: {e}")
        return pd.DataFrame()

# Page configuration
st.set_page_config(
    page_title="AI Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .suggestion-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #f3e5f5;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    # Header
    st.markdown('<h1 class="main-header">💰 AI Finance Manager</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.selectbox("Choose a page:", [
            "🏠 Dashboard",
            "📄 Upload Data",
            "👤 User Profile",
            "💡 Suggestions",
            "💬 Chat Assistant"
        ])
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        if st.session_state.user_profile and 'transaction_analysis' in st.session_state.user_profile:
            analysis = st.session_state.user_profile['transaction_analysis']
            st.metric("Financial Health", f"{analysis.get('financial_health_score', 0)}/100")
            st.metric("Monthly Income", f"₹{analysis.get('monthly_income_avg', 0):,.2f}")
            st.metric("Monthly Expenses", f"₹{analysis.get('monthly_expenses_avg', 0):,.2f}")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📄 Upload Data":
        show_upload_page()
    elif page == "👤 User Profile":
        show_profile_page()
    elif page == "💡 Suggestions":
        show_suggestions_page()
    elif page == "💬 Chat Assistant":
        show_chat_page()

def show_dashboard():
    """Main dashboard with overview"""
    st.header("📊 Financial Dashboard")
    
    if st.session_state.user_profile is None or 'transaction_analysis' not in st.session_state.user_profile:
        st.info("👆 Please upload your transaction data and create your user profile to see your financial dashboard.")
        return
    
    analysis = st.session_state.user_profile['transaction_analysis']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Financial Health Score",
            f"{analysis.get('financial_health_score', 0)}/100",
            delta=f"{analysis.get('financial_health_score', 0) - 50}"
        )
    
    with col2:
        monthly_income = analysis.get('monthly_income_avg', 0)
        monthly_expenses = analysis.get('monthly_expenses_avg', 0)
        savings = monthly_income - monthly_expenses
        st.metric(
            "Monthly Savings",
            f"₹{savings:,.2f}",
            delta=f"{(savings/monthly_income*100):.1f}%" if monthly_income > 0 else "0%"
        )
    
    with col3:
        st.metric(
            "Total Transactions",
            analysis.get('total_transactions', 0)
        )
    
    with col4:
        spending_trend = analysis.get('spending_trend', 'stable')
        trend_emoji = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}.get(spending_trend, "➡️")
        st.metric(
            "Spending Trend",
            f"{trend_emoji} {spending_trend.title()}"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Expense breakdown pie chart
        expense_breakdown = analysis.get('expense_breakdown', {})
        if expense_breakdown:
            fig_pie = px.pie(
                values=list(expense_breakdown.values()),
                names=list(expense_breakdown.keys()),
                title="Expense Breakdown by Category"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Monthly spending trend
        monthly_spending = analysis.get('monthly_spending', {})
        if monthly_spending:
            months = list(monthly_spending.keys())
            amounts = list(monthly_spending.values())
            
            fig_line = px.line(
                x=months,
                y=amounts,
                title="Monthly Spending Trend",
                labels={'x': 'Month', 'y': 'Amount (₹)'}
            )
            st.plotly_chart(fig_line, use_container_width=True)
    
    # Top spending categories
    st.subheader("🏆 Top Spending Categories")
    top_categories = analysis.get('top_spending_categories', {})
    if top_categories:
        df_categories = pd.DataFrame(list(top_categories.items()), columns=['Category', 'Amount'])
        fig_bar = px.bar(
            df_categories,
            x='Category',
            y='Amount',
            title="Top Spending Categories"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def show_upload_page():
    """Page for uploading transaction data"""
    st.header("📄 Upload Transaction Data")
    
    # File upload section
    st.subheader("📁 Upload Files")
    
    # Option 1: PDF Upload
    st.markdown("### Option 1: Upload Bank Statement (PDF)")
    uploaded_pdf = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your bank statement in PDF format",
        key="pdf_upload"
    )
    
    if uploaded_pdf is not None:
        # Save uploaded file
        with open(f"uploads/{uploaded_pdf.name}", "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        
        st.success(f"✅ File {uploaded_pdf.name} uploaded successfully!")
        
        # Parse button
        if st.button("🔍 Parse PDF and Extract Transactions", type="primary"):
            with st.spinner("Parsing bank statement..."):
                try:
                    transactions, csv_path = parse_bank_statement(f"uploads/{uploaded_pdf.name}")
                    
                    if transactions:
                        st.session_state.transactions = pd.DataFrame(transactions)
                        st.success(f"✅ Successfully parsed {len(transactions)} transactions!")
                        
                        # Show sample transactions
                        st.subheader("📋 Sample Transactions")
                        st.dataframe(st.session_state.transactions.head(10))
                        
                        # Download CSV
                        csv_data = st.session_state.transactions.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Transactions CSV",
                            data=csv_data,
                            file_name="transactions.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("❌ No transactions found in the PDF. Please check the file format.")
                        
                except Exception as e:
                    st.error(f"❌ Error parsing PDF: {str(e)}")
    
    st.markdown("---")
    
    # Option 2: CSV Upload
    st.markdown("### Option 2: Upload Transaction Data (CSV)")
    uploaded_csv = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your transaction data in CSV format",
        key="csv_upload"
    )
    
    if uploaded_csv is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_csv)
            
            # Auto-detect and map columns
            column_mapping = auto_detect_columns(df.columns)
            
            if column_mapping:
                # Rename columns to standard format
                df_standardized = df.rename(columns=column_mapping)
                
                # Validate and clean the data
                df_cleaned = clean_transaction_data(df_standardized)
                
                if not df_cleaned.empty:
                    st.session_state.transactions = df_cleaned
                    st.success(f"✅ Successfully loaded {len(df_cleaned)} transactions!")
                    
                    # Show column mapping
                    st.subheader("📋 Column Mapping Applied")
                    mapping_df = pd.DataFrame([
                        {"Original Column": orig, "Mapped To": mapped} 
                        for orig, mapped in column_mapping.items()
                    ])
                    st.dataframe(mapping_df, use_container_width=True)
                    
                    # Show sample transactions
                    st.subheader("📋 Sample Transactions")
                    st.dataframe(df_cleaned.head(10))
                else:
                    st.error("❌ No valid transactions found after cleaning the data.")
            else:
                st.error("❌ Could not detect required transaction columns in your CSV.")
                st.info("""
                **Expected column types:**
                - **Date**: Any date column (e.g., 'date', 'transaction_date', 'posted_date')
                - **Description**: Transaction description (e.g., 'description', 'memo', 'details', 'narration')
                - **Amount**: Transaction amount (e.g., 'amount', 'value', 'sum', 'total')
                - **Type**: Transaction type (e.g., 'type', 'debit_credit', 'dr_cr', 'transaction_type')
                
                **Your CSV columns:** """ + ", ".join(df.columns.tolist()))
                
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
    
    # Categorization section
    if st.session_state.transactions is not None:
        st.markdown("---")
        st.subheader("🏷️ Categorize Transactions")
        
        # Check if transactions have category column
        has_category = 'category' in st.session_state.transactions.columns
        
        if not has_category:
            st.info("📝 Your transactions need to be categorized for better analysis.")
            if st.button("🤖 Auto-Categorize Transactions", type="primary"):
                with st.spinner("Categorizing transactions..."):
                    try:
                        categorized_df, csv_path = categorize_transactions(st.session_state.transactions)
                        st.session_state.transactions = categorized_df
                        st.success("✅ Transactions categorized successfully!")
                        
                        # Show categorized transactions
                        st.subheader("📋 Categorized Transactions")
                        st.dataframe(categorized_df.head(10))
                        
                        # Category distribution
                        st.subheader("📊 Category Distribution")
                        category_counts = categorized_df['category'].value_counts()
                        fig = px.bar(
                            x=category_counts.index,
                            y=category_counts.values,
                            title="Transactions by Category"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error categorizing transactions: {str(e)}")
        else:
            st.info("✅ Transactions are already categorized!")
            
            # Show category distribution
            st.subheader("📊 Current Category Distribution")
            category_counts = st.session_state.transactions['category'].value_counts()
            fig = px.bar(
                x=category_counts.index,
                y=category_counts.values,
                title="Transactions by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Manual categorization option
            st.subheader("✏️ Manual Category Adjustment")
            st.write("You can manually adjust categories if needed:")
            
            # Create editable dataframe
            display_columns = ['date', 'description', 'amount', 'category']
            if 'type' in st.session_state.transactions.columns:
                display_columns = ['date', 'description', 'amount', 'type', 'category']
            
            edited_df = st.data_editor(
                st.session_state.transactions[display_columns].head(20),
                column_config={
                    "category": st.column_config.SelectboxColumn(
                        "Category",
                        options=CATEGORIES,
                        required=True,
                    )
                },
                num_rows="dynamic"
            )
            
            if st.button("💾 Save Manual Changes"):
                st.session_state.transactions.update(edited_df)
                st.success("✅ Changes saved!")

def show_profile_page():
    """Page for user profile creation"""
    st.header("👤 User Profile")
    
    if st.session_state.transactions is None:
        st.info("👆 Please upload your transaction data first.")
        return
    
    # Check if transactions are categorized
    if 'category' not in st.session_state.transactions.columns:
        st.warning("⚠️ Your transactions need to be categorized first for better analysis.")
        st.info("Please go to the 'Upload Data' page and categorize your transactions before creating your profile.")
        return
    
    # Check if profile already exists
    if st.session_state.user_profile is not None:
        st.subheader("📊 Current Profile")
        
        user_info = st.session_state.user_profile.get('user_info', {})
        financial_goals = st.session_state.user_profile.get('financial_goals', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Information:**")
            st.write(f"• Monthly Income: ₹{user_info.get('monthly_income', 0):,.2f}")
            st.write(f"• Age: {user_info.get('age', 'Not specified')}")
            st.write(f"• Occupation: {user_info.get('occupation', 'Not specified')}")
        
        with col2:
            st.write("**Financial Goals:**")
            st.write(f"• Monthly Savings Target: ₹{financial_goals.get('monthly_savings_target', 0):,.2f}")
            st.write(f"• Priority Categories: {', '.join(financial_goals.get('priority_categories', []))}")
            st.write(f"• Cut Cost Areas: {', '.join(financial_goals.get('cut_cost_areas', []))}")
        
        if st.button("🔄 Update Profile"):
            st.session_state.user_profile = None
            st.rerun()
    
    else:
        st.subheader("📝 Create Your Profile")
        st.write("Help us understand your financial situation to provide personalized suggestions.")
        
        with st.form("user_profile_form"):
            st.markdown("### Personal Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_income = st.number_input(
                    "Monthly Income (₹)",
                    min_value=0,
                    value=50000,
                    step=1000,
                    help="Your approximate monthly income"
                )
                
                age = st.selectbox(
                    "Age Range",
                    ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"],
                    help="Select your age range"
                )
            
            with col2:
                occupation = st.text_input(
                    "Occupation",
                    placeholder="e.g., Software Engineer, Teacher, Business Owner",
                    help="Your profession or job title"
                )
            
            st.markdown("### Financial Goals")
            
            monthly_savings_target = st.number_input(
                "Monthly Savings Target (₹)",
                min_value=0,
                value=10000,
                step=1000,
                help="How much do you want to save each month?"
            )
            
            priority_categories = st.multiselect(
                "Priority Spending Categories",
                CATEGORIES,
                default=["Food & Dining", "Transportation", "Shopping"],
                help="Select categories where you spend the most"
            )
            
            cut_cost_areas = st.multiselect(
                "Areas Where You Want to Cut Costs",
                CATEGORIES,
                default=["Food & Dining", "Entertainment"],
                help="Select categories where you want to reduce spending"
            )
            
            submitted = st.form_submit_button("💾 Create Profile", type="primary")
            
            if submitted:
                # Create user profile
                user_data = {
                    'monthly_income': monthly_income,
                    'age': age,
                    'occupation': occupation,
                    'monthly_savings_target': monthly_savings_target,
                    'priority_categories': priority_categories,
                    'cut_cost_areas': cut_cost_areas
                }
                
                profile, profile_path = create_user_profile(user_data)
                st.session_state.user_profile = profile
                
                # Analyze transactions with profile
                with st.spinner("Analyzing your transactions..."):
                    enhanced_profile, _ = analyze_user_transactions(st.session_state.transactions, profile)
                    st.session_state.user_profile = enhanced_profile
                
                st.success("✅ Profile created and transactions analyzed!")
                st.rerun()

def show_suggestions_page():
    """Page for personalized suggestions"""
    st.header("💡 Personalized Financial Suggestions")
    
    if st.session_state.user_profile is None or 'transaction_analysis' not in st.session_state.user_profile:
        st.info("👆 Please create your user profile first.")
        return
    
    # Check if transactions are categorized
    if st.session_state.transactions is not None and 'category' not in st.session_state.transactions.columns:
        st.warning("⚠️ Your transactions need to be categorized first for better suggestions.")
        st.info("Please go to the 'Upload Data' page and categorize your transactions.")
        return
    
    if st.button("🎯 Generate New Suggestions", type="primary"):
        with st.spinner("Generating personalized suggestions..."):
            try:
                suggestions_data = generate_personalized_suggestions(
                    st.session_state.user_profile,
                    st.session_state.user_profile['transaction_analysis']
                )
                st.session_state.suggestions = suggestions_data
                st.success("✅ Suggestions generated!")
                
                display_suggestions(suggestions_data)
                
            except Exception as e:
                st.error(f"❌ Error generating suggestions: {str(e)}")
    
    # Display existing suggestions
    if st.session_state.suggestions:
        st.subheader("💡 Your Personalized Suggestions")
        display_suggestions(st.session_state.suggestions)

def display_suggestions(suggestions_data):
    """Display suggestions in a formatted way"""
    suggestions = suggestions_data.get('suggestions', [])
    quick_tips = suggestions_data.get('quick_tips', [])
    
    # Main suggestions
    st.subheader("🎯 Action Items")
    for i, suggestion in enumerate(suggestions, 1):
        st.markdown(f"""
        <div class="suggestion-box">
            <strong>{i}.</strong> {suggestion}
        </div>
        """, unsafe_allow_html=True)
    
    # Quick tips
    if quick_tips:
        st.subheader("💡 Quick Tips")
        for tip in quick_tips:
            st.write(f"• {tip}")
    
    # Budget recommendations
    budget_recommendations = suggestions_data.get('budget_recommendations', {})
    if budget_recommendations:
        st.subheader("📊 Budget Recommendations")
        
        # Create budget comparison chart
        categories = list(budget_recommendations.keys())
        recommended = [budget_recommendations[cat]['recommended'] for cat in categories]
        current = [budget_recommendations[cat]['current'] for cat in categories]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Recommended', x=categories, y=recommended, marker_color='lightblue'))
        fig.add_trace(go.Bar(name='Current', x=categories, y=current, marker_color='lightcoral'))
        
        fig.update_layout(
            title="Budget Recommendations vs Current Spending",
            xaxis_title="Categories",
            yaxis_title="Amount (₹)",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_chat_page():
    """Page for chat assistant"""
    st.header("💬 AI Finance Assistant")
    
    # Check if we have user profile for better responses
    if st.session_state.user_profile is None:
        st.info("💡 Create your user profile for more personalized responses!")
    
    # Chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Suggested questions
    if st.session_state.user_profile and 'transaction_analysis' in st.session_state.user_profile:
        st.subheader("💭 Suggested Questions")
        suggested_questions = get_suggested_questions(
            st.session_state.user_profile,
            st.session_state.user_profile['transaction_analysis']
        )
        
        cols = st.columns(2)
        for i, question in enumerate(suggested_questions):
            with cols[i % 2]:
                if st.button(question, key=f"suggested_{i}"):
                    # Add to chat
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.rerun()
    
    # Chat input
    user_input = st.text_input("Ask me anything about your finances:", key="chat_input")
    
    if st.button("Send", type="primary") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get assistant response
        with st.spinner("Thinking..."):
            response = chat_with_bot(
                user_input,
                st.session_state.user_profile,
                st.session_state.user_profile['transaction_analysis'] if st.session_state.user_profile else None
            )
        
        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Clear input and rerun
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    main()