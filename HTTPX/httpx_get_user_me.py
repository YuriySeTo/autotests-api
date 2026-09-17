import httpx

# Данные для входа
login_payload = {
    "email": "1@1.com",
    "password": "123456"
}

# Логин — получаем токен
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_data = login_response.json()

# Достаём accessToken
access_token = login_data["token"]["accessToken"]

# Запрос на /users/me с токеном
headers = {
    "Authorization": f"Bearer {access_token}"
}
user_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
user_data = user_response.json()

# Вывод
print(user_data)
print(user_response.status_code)