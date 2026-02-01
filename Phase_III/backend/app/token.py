import jwt

payload = {"name": "dev-user-1", "email": "dev@test.com"}
token = jwt.encode(payload, "BETTER_AUTH_SECRET", algorithm="HS256")
print(token)
