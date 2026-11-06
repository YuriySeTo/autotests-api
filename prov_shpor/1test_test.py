from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, GetCourseResponseSchema

# Создаем пользователя
public_client = get_public_users_client()
request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
response = public_client.create_user(request)  # <--- Исправлено
print(f"Юзер создан с ID: {response.user.id}")

auth_user = AuthenticationUserSchema(
    email=request.email,
    password=request.password
)
files_client = get_files_client(auth_user)
courses_client = get_courses_client(auth_user)

# Создаем файл
file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
file_response = files_client.create_file(file_request)

# Создаем курс
course_request = CreateCourseRequestSchema(
    title="Python",
    max_score=100,
    min_score=10,
    description="Python API course",
    estimated_time="2 weeks",
    preview_file_id=file_response.file.id,
    created_by_user_id=response.user.id  # <--- Исправлено
)
course_response = courses_client.create_course(course_request)

# Получаем сырой ответ (метод с _api)
raw_response = courses_client.get_course_api(course_response.course.id)

# Генерируем схему из модели GetCourseResponseSchema
schema = GetCourseResponseSchema.model_json_schema()

# Валидируем
validate_json_schema(instance=raw_response.json(), schema=schema)
print("Курс успешно провалидирован!")