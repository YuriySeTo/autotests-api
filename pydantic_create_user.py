from pydantic import BaseModel, Field, EmailStr
from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


# ==========================================
# 1. Модели запросов
# ==========================================
class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """
    email: EmailStr | None = None
    last_name: str | None = Field(alias="lastName", default=None)
    first_name: str | None = Field(alias="firstName", default=None)
    middle_name: str | None = Field(alias="middleName", default=None)


# ==========================================
# 2. Модель сущности
# ==========================================
class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


# ==========================================
# 3. Модели ответов
# ==========================================
class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение пользователя.
    """
    user: UserSchema


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание пользователя.
    """
    user: UserSchema


class UpdateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление пользователя.
    """
    user: UserSchema


# ==========================================
# 4. Класс клиента
# ==========================================
class UsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    # --- *_api методы ---
    def get_user_me_api(self) -> Response:
        """
        Метод получения текущего пользователя.
        """
        return self.get("/api/v1/users/me")

    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получения пользователя по идентификатору.
        """
        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Метод создания пользователя.
        """
        return self.post(
            "/api/v1/users",
            json=request.model_dump(by_alias=True)
        )

    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        """
        Метод обновления пользователя.
        """
        return self.patch(
            f"/api/v1/users/{user_id}",
            json=request.model_dump(by_alias=True, exclude_none=True)
        )

    def delete_user_api(self, user_id: str) -> Response:
        """
        Метод удаления пользователя.
        """
        return self.delete(f"/api/v1/users/{user_id}")

    # --- методы без _api ---
    def get_user_me(self) -> GetUserResponseSchema:
        """
        Метод получения текущего пользователя (JSON).
        """
        response = self.get_user_me_api()
        return GetUserResponseSchema(**response.json())

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """
        Метод получения пользователя по идентификатору (JSON).
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema(**response.json())

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """
        Метод создания пользователя (JSON).
        """
        response = self.create_user_api(request)
        return CreateUserResponseSchema(**response.json())

    def update_user(self, user_id: str, request: UpdateUserRequestSchema) -> UpdateUserResponseSchema:
        """
        Метод обновления пользователя (JSON).
        """
        response = self.update_user_api(user_id, request)
        return UpdateUserResponseSchema(**response.json())


# ==========================================
# 5. Builder
# ==========================================
def get_users_client(user: AuthenticationUserDict) -> UsersClient:
    """
    Функция создаёт экземпляр UsersClient с уже настроенным HTTP-клиентом.
    """
    return UsersClient(client=get_private_http_client(user))