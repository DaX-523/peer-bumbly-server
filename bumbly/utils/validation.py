def signup_validation(data):
  if not data.get("email"):
    return "Email is required"
  if not data.get("password"):
    return "Password is required"
  if data.get("password") != data.get("confirm_password"):
    return "Passwords do not match"
  if len(data.get("password")) < 8:
    return "Password must be at least 8 characters long"
  if not data.get("first_name"):
    return "First name is required"
  if not data.get("last_name"):
    return "Last name is required"

def login_validation(data):
  if not data.get("email"):
    return "Email is required"
  if not data.get("password"):
    return "Password is required"

def forgot_password_validation(data):
  pass

def reset_password_validation(data):
  pass