"""
Configuration manager for IPL Auction System.
Supports Supabase Cloud PostgreSQL and SQLite3 local relational database.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Database Configuration
DB_MODE = os.getenv("DB_MODE", "sqlite").lower().strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

# SQLite Database File Path
SQLITE_DB_PATH = BASE_DIR / "ipl_auction.db"


def format_currency(amount: float) -> str:
    """Format numeric Indian Rupee amounts into Crores / Lakhs / Rupees readable format."""
    if amount is None:
        amount = 0.0
    amount = float(amount)
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount / 100_000:.2f} L"
    elif amount > 0:
        return f"₹{amount:,.0f}"
    else:
        return "₹0"


def is_supabase_configured() -> bool:
    """Check if Supabase credentials are provided."""
    return bool(SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL.startswith("http"))
