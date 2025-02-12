
# 4 Ways to Validate Email Addresses in Python

# 1. Basic – Validation using parseaddr (very simple)
from email.utils import parseaddr
def is_valid_email(email: str) -> bool:
    try:
        # parseaddr returns a tuple (name, extracted_email)
        parsed = parseaddr(email)[1]
        return "@" in parsed and "." in parsed
    except Exception:
        return False

# 2. Basic – Validation using string methods (very restrictive)
def is_valid_email(email: str) -> bool:
    try:
        if email.count("@") != 1 or "." not in email:
            return False
        at_index = email.index("@")
        last_dot_index = email.rindex(".")
        if at_index > last_dot_index:
            return False
        local_part = email[:at_index]
        domain_part = email[at_index+1:last_dot_index]
        tld_part = email[last_dot_index+1:]
        if not local_part or not domain_part or not tld_part:
            return False
        # Warning: This check allows only alphanumeric characters (very strict)
        if not local_part.isalnum() or not domain_part.isalnum() or not (tld_part.isalpha() and len(tld_part) >= 2):
            return False
        return True
    except Exception:
        return False
 
      
# 3. Advanced – Validation using regular expressions (Regex)
import re
def is_valid_email(email: str) -> bool:
    try:
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return bool(email_regex.match(email))
    except Exception:
        return False
 
    
# 4. Most Advanced (Production Quality) – Validation using email_validator package
from email_validator import validate_email, EmailNotValidError
def is_valid_email(email: str, return_details: bool = False, check_deliverability: bool = True):
    try:
        result = validate_email(email, check_deliverability=check_deliverability)
        if return_details:
            return {
                "valid": True,
                "normalized": result["email"],
                "local": result.get("local"),
                "domain": result.get("domain"),
                "domain_info": result.get("domain_info")
            }
        return True
    except EmailNotValidError as e:
        if return_details:
            return {"valid": False, "error": str(e)}
        return False
    except Exception as e:
        if return_details:
            return {"valid": False, "error": "Unknown error: " + str(e)}
        return False

# Test Code 
emails = [
    "test@example.com",             
    "invalid-email",
    "cod1ing.together@gmail.com",                
    "another.test@domain.co.uk",    
    "wrong@domain,com",             
    "user@domain..com"                 
]

for email in emails:
    valid = is_valid_email(email)
    print(f"{email}: {'valid' if valid else 'invalid'}")
