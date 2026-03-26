import re

# OLD function (keep it)
def rule_check(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*]", password):
        score += 1

    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Medium"
    else:
        return "Strong"


# ✅ ADD THIS FUNCTION (IMPORTANT)
def validate_password(password):
    if len(password) < 8 or len(password) > 12:
        return "Password must be 8–12 characters"

    if not re.search(r"[A-Z]", password):
        return "Must include uppercase letter"

    if not re.search(r"[a-z]", password):
        return "Must include lowercase letter"

    if not re.search(r"[0-9]", password):
        return "Must include number"

    if not re.search(r"[!@#$%^&*]", password):
        return "Must include special character"

    return "Valid"