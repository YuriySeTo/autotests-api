from http import HTTPStatus

# 1. ИМПОРТЫ (допиши то, чего не хватает)
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.base import assert_status_code, assert_equal
from tools.assertions.schema import validate_json_schema


def test_create_course():
    # ШАГ 1. Создаем пользователя
    public_client = get_public_users_client()
    user_request = CreateUserRequestSchema()
    create_user_response = public_client.create_user(user_request)

    # ШАГ 2. Авторизуемся (создаем AuthenticationUserSchema)
    auth_user = AuthenticationUserSchema(
        email=user_request.email,
        password=user_request.password
    )

    # ШАГ 3. Создаем клиентов (файлы и курсы)
    files_client = get_files_client(auth_user)
    courses_client = get_courses_client(auth_user)

    # ШАГ 4. Создаем файл
    file_request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")
    create_file_response = files_client.create_file(file_request)

    # ШАГ 5. Создаем курс
    course_request = CreateCourseRequestSchema(
        preview_file_id=create_file_response.file.id,
        created_by_user_id=create_user_response.user.id
    )

    # 1. Проверяем статус-код
    assert_status_code(create_course_response.status_code, HTTPStatus.OK)

    # 2. Превращаем сырой ответ в Pydantic-модель
    course_data = CreateCourseResponseSchema.model_validate_json(create_course_response.text)

    # 3. Валидируем JSON-схему
    validate_json_schema(create_course_response.json(), course_data.model_json_schema())

    # 4. Проверяем, что название курса совпадает
    assert_equal(course_data.course.title, course_request.title, "title")