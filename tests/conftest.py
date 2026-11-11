import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema
# Новые импорты для приватного клиента
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    # Новое свойство для авторизации
    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        return AuthenticationUserSchema(
            email=self.request.email,
            password=self.request.password
        )


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)


# Новая фикстура для приватного клиента
@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    return get_private_users_client(function_user.authentication_user)