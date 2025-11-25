# Utils/budgetfunctions.py
import os, csv, string

budget_file = os.path.normpath(os.path.expanduser("~/.Pearl/budget.csv"))

def initialize_budget():
    """Create budget file if it doesn't exist"""
    create_budget_file()

def create_budget_file():
    """Initialize budget CSV with default categories and amounts"""
    os.makedirs(os.path.dirname(budget_file), exist_ok=True)
    if not os.path.exists(budget_file):
        with open(budget_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount"])
            default_budget = []
            writer.writerows(default_budget)

def read_budget():
    """Read budget data from CSV"""
    budget = {}
    if os.path.exists(budget_file):
        with open(budget_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                amount_str = row[1].strip(' "\t\n\r')
                budget[row[0]] = float(amount_str)
    return budget

def update_budget(category, amount_change=None, new_amount=None):
    """Update budget category with new amount or adjustment"""
    budget = read_budget()
    category = category.title()
    
    if new_amount is not None:
        if not isinstance(new_amount, (int, float)):
            return f"Error: new_amount must be a number, got {type(new_amount)}"
        if new_amount < 0:
            return f"Warning! Can’t set {category} to a negative amount!"
        budget[category] = float(new_amount)
    elif amount_change is not None:
        if not isinstance(amount_change, (int, float)):
            return f"Error: amount_change must be a number, got {type(amount_change)}"
        if category in budget:
            updated_amount = budget[category] + amount_change
            if updated_amount < 0:
                return f"Warning! Can’t adjust {category}—it’d go negative!"
            budget[category] = float(updated_amount)
        else:
            if amount_change < 0:
                return f"Warning! Can’t subtract from {category}—it doesn’t exist yet!"
            budget[category] = float(amount_change)
    else:
        return "Error: No amount specified!"
    
    # Save updated budget
    with open(budget_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Amount"])
        for cat, amt in budget.items():
            writer.writerow([cat, str(amt)])
    return f"Updated {category} to {budget[category]}"

def clean_amount(amount_str):
    """Extract valid number from amount string"""
    digits_and_decimal = [c for c in amount_str if c.isdigit() or c == '.']
    cleaned = ''
    has_decimal = False
    for c in digits_and_decimal:
        if c == '.' and not has_decimal:
            cleaned += c
            has_decimal = True
        elif c.isdigit():
            cleaned += c
    if not cleaned:
        raise ValueError("No valid number found")
    return cleaned if '.' in cleaned else cleaned + '.0'

def parse_command(command):
    """Parse budget-related commands (add, subtract, set, show)"""
    command = command.lower().strip()
    parts = command.split()
    
    if "add" in parts and "to" in parts:
        try:
            add_index = parts.index("add")
            to_index = parts.index("to")
            amount_str_raw = parts[add_index + 1]
            amount_str = clean_amount(amount_str_raw)
            amount = float(amount_str)
            category_parts = parts[to_index + 1:]
            category = ' '.join(category_parts).rstrip(string.punctuation).title()
            return update_budget(category, amount_change=amount)
        except ValueError as e:
            return f"Invalid amount: {str(e)}. Please use a number like '$50' or '50'."
        except IndexError:
            return "Invalid add command format. Try 'Add $50 to groceries'."
    
    elif ("subtract" in parts or "remove" in parts) and "from" in parts:
        verb = "subtract" if "subtract" in parts else "remove"
        try:
            verb_index = parts.index(verb)
            from_index = parts.index("from")
            amount_str_raw = parts[verb_index + 1]
            amount_str = clean_amount(amount_str_raw)
            amount = float(amount_str)
            category_parts = parts[from_index + 1:]
            category = ' '.join(category_parts).rstrip(string.punctuation).title()
            return update_budget(category, amount_change=-amount)
        except ValueError as e:
            return f"Invalid amount: {str(e)}. Please use a number like '$20' or '20'."
        except IndexError:
            return "Invalid subtract command format. Try 'Subtract $20 from restaurants'."
    
    elif ("change" in parts or "set" in parts) and "to" in parts:
        verb = "change" if "change" in parts else "set"
        try:
            verb_index = parts.index(verb)
            to_index = parts.index("to")
            category_parts = parts[verb_index + 1:to_index]
            category = ' '.join(category_parts).title()
            amount_str_raw = parts[to_index + 1]
            amount_str = clean_amount(amount_str_raw)
            amount = float(amount_str)
            return update_budget(category, new_amount=amount)
        except ValueError as e:
            return f"Invalid amount: {str(e)}. Please use a number like '$300' or '300'."
        except IndexError:
            return "Invalid change command format. Try 'Change groceries to $300'."
    
    elif "show" in parts or "read" in parts:
        return str(read_budget())
    
    return ""