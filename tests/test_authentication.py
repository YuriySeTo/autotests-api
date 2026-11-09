from http import HTTPStatus
import pytest
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema



@pytest.mark.authentication  # Добавили маркировку authentication
@pytest.mark.regression  # Добавили маркировку regression
def test_login():
    # 1. Создаем пользователя
    public_client = get_public_users_client()
    user_request = CreateUserRequestSchema()
    public_client.create_user(user_request)

    # 2. Логинимся
    auth_client = get_authentication_client()
    # Создаем запрос на логин, передаем email и пароль из user_request
    login_request = LoginRequestSchema(
        email=user_request.email,
        password=user_request.password
    )

    # Вызываем метод с припиской _api (чтобы получить сырой ответ)
    login_response = auth_client.login_api(login_request)

    # 3. Превращаем в модель Pydantic
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # 4. Проверяем статус
    assert_status_code(login_response.status_code, HTTPStatus.OK)

    # 5. Проверяем тело ответа
    assert_login_response(login_response_data)

    # 6. Валидируем схему
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())