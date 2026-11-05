from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email

client = get_public_users_client()
request = CreateUserRequestSchema(email=get_random_email(), password="str", last_name="a", first_name="b", middle_name="c")

# 1. Запрос (используем _api!)
response = client.create_user_api(request)

# 2. Схема
schema = CreateUserResponseSchema.model_json_schema()

# 3. Валидация
validate_json_schema(instance=response.json(), schema=schema)

"""
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import GetCoursesQuerySchema, CreateCourseResponseSchema
from tools.assertions.schema import validate_json_schema

client = get_courses_client(auth_user)
query = GetCoursesQuerySchema(user_id="123")

# 1. Запрос
response = client.get_courses_api(query)

# 2. Схема (модель ответа для списка курсов)
schema = CreateCourseResponseSchema.model_json_schema() # (в идеале тут должен быть GetCoursesResponseSchema)

# 3. Валидация
validate_json_schema(instance=response.json(), schema=schema)
"""

"""
# 1. Импорты
from tools.assertions.schema import validate_json_schema
from clients.courses.courses_schema import CreateCourseResponseSchema

# ...

# 2. Запрос через _api
response = courses_client.create_course_api(create_course_request)

# 3. Схема
schema = CreateCourseResponseSchema.model_json_schema()

# 4. Валидация
validate_json_schema(instance=response.json(), schema=schema)

# 5. Вывод
print("Create course data validated successfully!")
"""