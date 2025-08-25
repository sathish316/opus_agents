"""
Utility functions for portfolio analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from scipy.optimize import fsolve
# import yfinance as yf  # Not needed for mock implementation
from models import Transaction, Fund, FundCategory, TransactionType


def calculate_xirr(transactions: List[Transaction], current_nav: float = None) -> float:
    """
    Calculate XIRR (Extended Internal Rate of Return) for a series of transactions.
    
    Args:
        transactions: List of transactions for a fund
        current_nav: Current NAV of the fund
        
    Returns:
        XIRR as a percentage
    """
    if not transactions:
        return 0.0
        
    # Sort transactions by date
    sorted_transactions = sorted(transactions, key=lambda x: x.date)
    
    # Create cash flows
    cash_flows = []
    dates = []
    
    for txn in sorted_transactions:
        if txn.transaction_type == TransactionType.BUY:
            cash_flows.append(-abs(txn.transaction_count))  # Negative for investment
        elif txn.transaction_type == TransactionType.SELL:
            cash_flows.append(abs(txn.transaction_count))   # Positive for redemption
        dates.append(txn.date)
    
    # Add current value as final cash flow
    if current_nav and cash_flows:
        # Calculate current units (simplified - assumes unit price of 1 for simplicity)
        total_units = sum(txn.transaction_count if txn.transaction_type == TransactionType.BUY 
                         else -txn.transaction_count for txn in sorted_transactions)
        current_value = total_units * current_nav
        cash_flows.append(current_value)
        dates.append(datetime.now())
    
    if len(cash_flows) < 2:
        return 0.0
    
    # Calculate XIRR using scipy
    try:
        def xirr_func(rate):
            return sum([cf / ((1 + rate) ** ((date - dates[0]).days / 365.0)) 
                       for cf, date in zip(cash_flows, dates)])
        
        rate = fsolve(xirr_func, 0.1)[0]
        return rate * 100  # Convert to percentage
    except:
        return 0.0


def categorize_fund(fund_name: str, fund_code: str) -> FundCategory:
    """
    Categorize fund based on name and code.
    """
    name_lower = fund_name.lower()
    
    if any(keyword in name_lower for keyword in ['gold', 'precious', 'metal']):
        return FundCategory.GOLD
    elif 'silver' in name_lower:
        return FundCategory.SILVER
    elif any(keyword in name_lower for keyword in ['debt', 'bond', 'liquid', 'money market', 'gilt']):
        return FundCategory.DEBT
    elif any(keyword in name_lower for keyword in ['hybrid', 'balanced', 'aggressive hybrid']):
        return FundCategory.HYBRID
    else:
        return FundCategory.EQUITY


def get_fund_nav(fund_code: str) -> float:
    """
    Get current NAV for a fund. For demo purposes, returns mock data.
    In production, this would call actual fund APIs.
    """
    # Mock NAV data - in production, integrate with actual fund APIs
    mock_navs = {
        'UTI_NIFTY': 150.25,
        'SBI_SENSEX': 45.80,
        'HDFC_DEBT': 25.90,
        'ICICI_HYBRID': 35.60,
        'NIPPON_GOLD': 12.45,
        'KOTAK_SILVER': 8.90
    }
    
    return mock_navs.get(fund_code, 100.0)


def load_portfolio_from_csv(file_path: str) -> Tuple[List[Transaction], Dict[str, Fund]]:
    """
    Load portfolio data from CSV file.
    
    Expected CSV format: date, fund_code, fund_name, transaction_type, transaction_count
    """
    df = pd.read_csv(file_path)
    
    transactions = []
    funds = {}
    
    for _, row in df.iterrows():
        # Parse transaction
        transaction = Transaction(
            date=pd.to_datetime(row['date']),
            fund_code=row['fund_code'],
            fund_name=row['fund_name'],
            transaction_type=TransactionType(row['transaction_type'].upper()),
            transaction_count=float(row['transaction_count'])
        )
        transactions.append(transaction)
        
        # Create fund if not exists
        if row['fund_code'] not in funds:
            fund_category = categorize_fund(row['fund_name'], row['fund_code'])
            funds[row['fund_code']] = Fund(
                code=row['fund_code'],
                name=row['fund_name'],
                category=fund_category,
                current_price=get_fund_nav(row['fund_code'])
            )
    
    return transactions, funds


def get_benchmark_xirr(category: FundCategory) -> float:
    """
    Get benchmark XIRR for different fund categories.
    These are hardcoded optimal returns for Indian market.
    """
    benchmarks = {
        FundCategory.EQUITY: 12.0,    # Expected equity returns
        FundCategory.DEBT: 7.5,       # Expected debt returns  
        FundCategory.HYBRID: 10.0,    # Expected hybrid returns
        FundCategory.GOLD: 8.0,       # Expected gold returns
        FundCategory.SILVER: 9.0      # Expected silver returns
    }
    return benchmarks.get(category, 8.0)


def get_marquee_funds(category: FundCategory) -> List[str]:
    """
    Get recommended marquee funds for each category in India.
    """
    marquee_funds = {
        FundCategory.EQUITY: [
            "UTI Nifty Index Fund",
            "SBI Sensex Index Fund", 
            "HDFC Index Fund - Nifty 50 Plan"
        ],
        FundCategory.DEBT: [
            "SBI Magnum Gilt Fund",
            "HDFC Short Term Debt Fund",
            "ICICI Prudential Liquid Fund"
        ],
        FundCategory.HYBRID: [
            "HDFC Balanced Advantage Fund",
            "ICICI Prudential Balanced Advantage Fund",
            "SBI Balanced Advantage Fund"
        ],
        FundCategory.GOLD: [
            "Nippon India Gold Savings Fund",
            "HDFC Gold Fund",
            "SBI Gold Fund"
        ],
        FundCategory.SILVER: [
            "Kotak Silver ETF Fund",
            "ICICI Prudential Silver ETF Fund"
        ]
    }
    return marquee_funds.get(category, [])