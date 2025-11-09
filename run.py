#!/usr/bin/env python3
"""
AI Finance Manager - Main Entry Point
Run this file to start the Streamlit application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import pdfplumber
        import sklearn
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'data', 'profiles']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def main():
    """Main function to run the application"""
    print("🚀 Starting AI Finance Manager (100% FREE VERSION)...")
    print("=" * 60)
    print("💰 Personal Finance Management with AI")
    print("📊 Transaction Analysis & Personalized Suggestions")
    print("🤖 Free AI Chatbot - No API Keys Required!")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("=" * 60)
    print("🌐 Starting Streamlit application...")
    print("The app will open in your default web browser")
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    # Run Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()