def format_currency_inr(value):
    """
    Formats a numeric value as INR currency string.
    Example: 1234567.89 -> ₹12,34,567.89
    """
    try:
        val_float = float(value)
        # Indian Numbering System formatting:
        # e.g. 12,34,567.89
        is_negative = val_float < 0
        val_abs = abs(val_float)
        
        s = f"{val_abs:.2f}"
        parts = s.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]
        
        if len(integer_part) <= 3:
            res = integer_part
        else:
            last_three = integer_part[-3:]
            remaining = integer_part[:-3]
            
            # Group the remaining by 2s
            grouped = []
            while len(remaining) > 0:
                if len(remaining) >= 2:
                    grouped.insert(0, remaining[-2:])
                    remaining = remaining[:-2]
                else:
                    grouped.insert(0, remaining)
                    remaining = ""
            
            res = ",".join(grouped) + "," + last_three
            
        formatted = f"₹{'-' if is_negative else ''}{res}.{decimal_part}"
        return formatted
    except Exception:
        return f"₹{value}"

def format_currency_usd(value):
    """
    Formats a numeric value as USD currency string.
    """
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return f"${value}"

def print_section_header(title):
    """
    Prints a formatted section header for console output.
    """
    border = "=" * 80
    print(f"\n{border}")
    print(f" {title.upper()}")
    print(f"{border}")
