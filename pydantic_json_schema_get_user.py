from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake

# Создаем пользователя
public_client = get_public_users_client()
request = CreateUserRequestSchema(
    email=fake.email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
response = public_client.create_user(request)
print(f"Юзер создан с ID: {response.user.id}")

# Авторизуемся под этим пользователем и создаем приватный клиент
auth_user = AuthenticationUserSchema(
    email=request.email,
    password=request.password
)
private_client = get_private_users_client(auth_user)

# Получаем данные пользователя
raw_response = private_client.get_user_api(response.user.id)

# Генерируем ожидаемую JSON-схему из Pydantic-модели
schema = GetUserResponseSchema.model_json_schema()

# Валидируем ответ от сервера по этой схеме
validate_json_schema(instance=raw_response.json(), schema=schema)

print("Success")