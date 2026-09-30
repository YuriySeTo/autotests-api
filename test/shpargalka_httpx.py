# Логин

payload = {"email": "...", "password": "..."}
response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=payload)
data = response.json()
token = data["token"]["accessToken"]
print(data)
print(response.status_code)

# POST (создание, без токена)

payload = {"ключ": "значение"}
response = httpx.post("http://localhost:8000/url", json=payload)
data = response.json()
print(data)
print(response.status_code)

# POST (создание, с токеном)

payload = {"ключ": "значение"}
headers = {"Authorization": f"Bearer {token}"}
response = httpx.post("http://localhost:8000/url", json=payload, headers=headers)
data = response.json()
print(data)
print(response.status_code)

# GET (без токена)

response = httpx.get("http://localhost:8000/url")
data = response.json()
print(data)
print(response.status_code)

# GET (с токеном)

headers = {"Authorization": f"Bearer {token}"}
response = httpx.get("http://localhost:8000/url", headers=headers)
data = response.json()
print(data)
print(response.status_code)

# PATCH (с токеном)

payload = {"ключ": "новое_значение"}
headers = {"Authorization": f"Bearer {token}"}
response = httpx.patch("http://localhost:8000/url", json=payload, headers=headers)
data = response.json()
print(data)
print(response.status_code)

# DELETE (с токеном)

headers = {"Authorization": f"Bearer {token}"}
response = httpx.delete("http://localhost:8000/url", headers=headers)
print(response.status_code)

# Случайный email

new_email = f"test.{time.time()}@example.com"

# Импорты

import httpx
import time

#Токен

token = data["token"]["accessToken"]

# Создание файла (только метаданные, без самого файла)

payload = {
    "filename": "myfile.txt",
    "directory": "tests"
}
response = httpx.post("http://localhost:8000/api/v1/files", json=payload, headers=headers)
data = response.json()
print(data)
print(response.status_code)

# GET (получить файл по id)

headers = {"Authorization": f"Bearer {token}"}
response = httpx.get(f"http://localhost:8000/api/v1/files/{file_id}", headers=headers)
data = response.json()
print(data)
print(response.status_code)

# GET (список всех файлов)

headers = {"Authorization": f"Bearer {token}"}
response = httpx.get("http://localhost:8000/api/v1/files", headers=headers)
data = response.json()
print(data)
print(response.status_code)

# DELETE (удалить файл)

headers = {"Authorization": f"Bearer {token}"}
response = httpx.delete(f"http://localhost:8000/api/v1/files/{file_id}", headers=headers)
print(response.status_code)