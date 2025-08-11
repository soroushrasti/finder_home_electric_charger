import jwt
from datetime import datetime, timedelta

# Token configuration
SECRET_KEY = "your-secret-key"  # Use the same secret as your FastAPI app
ALGORITHM = "HS256"

# Create payload with 1 year expiration
payload = {
    "sub": "test-user",
    "exp": datetime.utcnow() + timedelta(days=365)  # Valid for 1 year
}

# Generate the token
fresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Fresh 1-year token: {fresh_token}")