import pdfplumber
import pandas as pd
import re
from datetime import datetime
import os

class BankStatementParser:
    def __init__(self):
        self.transactions = []
    
    def parse_pdf(self, pdf_path):
        """Parse bank statement PDF and extract transactions"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
                
                # Try to extract tables first
                tables = self._extract_tables(pdf)
                if tables:
                    return self._process_tables(tables)
                else:
                    return self._process_text(all_text)
                    
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None
    
    def _extract_tables(self, pdf):
        """Extract tables from PDF pages"""
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
        return tables
    
    def _process_tables(self, tables):
        """Process extracted tables to find transactions"""
        transactions = []
        
        for table in tables:
            if not table:
                continue
                
            # Look for header row
            header_row = None
            for i, row in enumerate(table):
                if row and any(keyword in str(row).lower() for keyword in ['date', 'description', 'amount', 'debit', 'credit']):
                    header_row = i
                    break
            
            if header_row is not None:
                # Process data rows
                for row in table[header_row + 1:]:
                    if row and len(row) >= 3:
                        transaction = self._parse_table_row(row)
                        if transaction:
                            transactions.append(transaction)
        
        return transactions
    
    def _process_text(self, text):
        """Process raw text to extract transactions"""
        transactions = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for transaction patterns
            transaction = self._parse_text_line(line)
            if transaction:
                transactions.append(transaction)
        
        return transactions
    
    def _parse_table_row(self, row):
        """Parse a table row into transaction format"""
        try:
            # Clean the row data
            clean_row = [str(cell).strip() if cell else "" for cell in row]
            
            # Find date, description, and amount
            date = None
            description = ""
            amount = None
            transaction_type = "Debit"
            
            for cell in clean_row:
                # Check for date
                if self._is_date(cell):
                    date = self._parse_date(cell)
                # Check for amount
                elif self._is_amount(cell):
                    amount = self._parse_amount(cell)
                    if amount < 0:
                        transaction_type = "Credit"
                        amount = abs(amount)
                # Use as description if not date/amount
                elif cell and not self._is_date(cell) and not self._is_amount(cell):
                    description += cell + " "
            
            if date and amount is not None and description.strip():
                return {
                    'date': date,
                    'description': description.strip(),
                    'amount': amount,
                    'type': transaction_type
                }
        except Exception as e:
            print(f"Error parsing row: {e}")
        
        return None
    
    def _parse_text_line(self, line):
        """Parse a text line for transaction data"""
        # Simple regex patterns for common bank statement formats
        patterns = [
            # Date Description Amount pattern
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(.+?)\s+([+-]?\d+\.?\d*)',
            # Amount Date Description pattern  
            r'([+-]?\d+\.?\d*)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Determine which group is what based on content
                        date = None
                        description = ""
                        amount = None
                        
                        for group in groups:
                            if self._is_date(group):
                                date = self._parse_date(group)
                            elif self._is_amount(group):
                                amount = self._parse_amount(group)
                            else:
                                description = group.strip()
                        
                        if date and amount is not None and description:
                            transaction_type = "Credit" if amount < 0 else "Debit"
                            return {
                                'date': date,
                                'description': description,
                                'amount': abs(amount),
                                'type': transaction_type
                            }
                except Exception as e:
                    continue
        
        return None
    
    def _is_date(self, text):
        """Check if text looks like a date"""
        if not text:
            return False
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{1,2}\s+\w{3}\s+\d{2,4}',
        ]
        return any(re.search(pattern, text) for pattern in date_patterns)
    
    def _is_amount(self, text):
        """Check if text looks like an amount"""
        if not text:
            return False
        amount_pattern = r'[+-]?\d+\.?\d*'
        return bool(re.match(amount_pattern, text.replace(',', '').replace('₹', '').replace('$', '')))
    
    def _parse_date(self, date_str):
        """Parse date string into datetime object"""
        try:
            # Try different date formats
            formats = [
                '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d',
                '%d-%m-%Y', '%m-%d-%Y',
                '%d %b %Y', '%d %B %Y'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            
            # If no format works, return today's date
            return datetime.now().date()
        except:
            return datetime.now().date()
    
    def _parse_amount(self, amount_str):
        """Parse amount string into float"""
        try:
            # Remove currency symbols and commas
            clean_amount = re.sub(r'[₹$,\s]', '', amount_str)
            return float(clean_amount)
        except:
            return 0.0
    
    def save_to_csv(self, transactions, filename="transactions.csv"):
        """Save transactions to CSV file"""
        if not transactions:
            return None
        
        df = pd.DataFrame(transactions)
        filepath = os.path.join("data", filename)
        df.to_csv(filepath, index=False)
        return filepath

def parse_bank_statement(pdf_file):
    """Main function to parse bank statement"""
    parser = BankStatementParser()
    transactions = parser.parse_pdf(pdf_file)
    
    if transactions:
        csv_path = parser.save_to_csv(transactions)
        return transactions, csv_path
    else:
        return None, None