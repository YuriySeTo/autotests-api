# Шаблон 1: APIClient

import httpx


class APIClient:
    def __init__(self, client):
        self.client = client

    def get(self, url, params=None):
        return self.client.get(url, params=params)

    def post(self, url, json=None, data=None, files=None):
        return self.client.post(url, json=json, data=data, files=files)

    def put(self, url, json=None):
        return self.client.put(url, json=json)

    def patch(self, url, json=None):
        return self.client.patch(url, json=json)

    def delete(self, url):
        return self.client.delete(url)


# Шаблон 2: Дочерний клиент

from clients.api_client import APIClient


class XxxClient(APIClient):
    # ============================================
    # GET — получить список (без параметров)
    # ============================================
    def get_xxx_list(self):
        return self.get("/api/v1/xxx")

    # ============================================
    # GET — получить список с query-параметрами
    # query = {"userId": "123"}  (словарь)
    # ============================================
    def get_xxx_list(self, query):
        return self.get("/api/v1/xxx", params=query)

    # ============================================
    # GET — получить один объект по id
    # xxx_id = "..."  (строка)
    # ============================================
    def get_xxx(self, xxx_id):
        return self.get(f"/api/v1/xxx/{xxx_id}")

    # ============================================
    # POST — создать объект
    # request = {"поле1": "значение1", ...}  (словарь)
    # ============================================
    def create_xxx(self, request):
        return self.post("/api/v1/xxx", json=request)

    # ============================================
    # PATCH — обновить объект
    # xxx_id = "..."  (строка)
    # request = {"поле1": "новое", ...}  (словарь)
    # ============================================
    def update_xxx(self, xxx_id, request):
        return self.patch(f"/api/v1/xxx/{xxx_id}", json=request)

    # ============================================
    # DELETE — удалить объект
    # xxx_id = "..."  (строка)
    # ============================================
    def delete_xxx(self, xxx_id):
        return self.delete(f"/api/v1/xxx/{xxx_id}")


# Шаблон 3: Использование

import httpx
from clients.xxx.xxx_client import XxxClient


# 1. Создаём httpx.Client

httpx_client = httpx.Client(
    base_url="http://localhost:8000",
    headers={"Authorization": f"Bearer {token}"}
)

# 2. Оборачиваем в свой клиент
client = XxxClient(httpx_client)

# 3. Вызываем методы
response = client.get_xxx()
print(response.json())

response = client.create_xxx(payload)
print(response.json())

