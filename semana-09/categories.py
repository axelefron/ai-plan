"""Expense categories and their keywords (US merchants).

Data only: the matching logic lives in expenses.py.
Keywords are lowercase and without accents. Order matters:
if a description matches two categories, the first one wins.
That is why "dining" comes before "transportation": "Uber Eats" is food, not a ride.
"""

DEFAULT_CATEGORY = "other"

CATEGORIES = {
    "groceries": ["walmart", "publix", "target", "costco", "kroger", "aldi", "trader joe", "whole foods"],
    "dining": ["starbucks", "mcdonald", "chipotle", "doordash", "uber eats", "cafe", "pizza"],
    "transportation": ["uber", "lyft", "shell", "chevron", "exxon", "gas", "parking", "toll"],
    "utilities": ["electric", "water", "internet", "comcast", "xfinity", "verizon", "at&t"],
    "subscriptions": ["netflix", "spotify", "hulu", "disney", "youtube"],
    "health": ["cvs", "walgreens", "pharmacy", "doctor", "dentist", "copay"],
}
