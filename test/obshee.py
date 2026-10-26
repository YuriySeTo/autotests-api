# ЧАСТЬ 1: Каркас клиента
# Файл: clients/xxx/xxx_client.py

from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client
from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient

from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


# ==========================================
# 1. TypedDict — запросы
# ==========================================
class CreateXxxRequestDict(TypedDict):
    """Описание структуры запроса на создание xxx."""
    поле1: str
    поле2: int


class UpdateXxxRequestDict(TypedDict):
    """Описание структуры запроса на обновление xxx."""
    поле1: str | None
    поле2: int | None


# ==========================================
# 2. TypedDict — сущность
# ==========================================
class Xxx(TypedDict):
    """Описание структуры xxx."""
    id: str
    поле1: str
    поле2: int


# ==========================================
# 3. TypedDict — ответы
# ==========================================
class GetXxxResponseDict(TypedDict):
    """Описание структуры ответа на получение xxx."""
    xxx: Xxx


class CreateXxxResponseDict(TypedDict):
    """Описание структуры ответа на создание xxx."""
    xxx: Xxx


# ==========================================
# 4. Класс клиента
# ==========================================
class XxxClient(APIClient):
    """Клиент для работы с /api/v1/xxx"""

    # --- *_api методы (сырой Response) ---
    def get_xxx_api(self, xxx_id: str) -> Response:
        """Метод получения xxx по id."""
        return self.get(f"/api/v1/xxx/{xxx_id}")

    def create_xxx_api(self, request: CreateXxxRequestDict) -> Response:
        """Метод создания xxx."""
        return self.post("/api/v1/xxx", json=request)

    def update_xxx_api(self, xxx_id: str, request: UpdateXxxRequestDict) -> Response:
        """Метод обновления xxx."""
        return self.patch(f"/api/v1/xxx/{xxx_id}", json=request)

    def delete_xxx_api(self, xxx_id: str) -> Response:
        """Метод удаления xxx."""
        return self.delete(f"/api/v1/xxx/{xxx_id}")

    # --- методы без _api (JSON) ---
    def get_xxx(self, xxx_id: str) -> GetXxxResponseDict:
        """Метод получения xxx (JSON)."""
        response = self.get_xxx_api(xxx_id)
        return response.json()

    def create_xxx(self, request: CreateXxxRequestDict) -> CreateXxxResponseDict:
        """Метод создания xxx (JSON)."""
        response = self.create_xxx_api(request)
        return response.json()


# ==========================================
# 5. Builder
# ==========================================
def get_xxx_client(user: AuthenticationUserDict) -> XxxClient:
    """Функция создаёт XxxClient с настроенным httpx.Client."""
    return XxxClient(client=get_private_http_client(user))


# ЧАСТЬ 2: Каркас скрипта
# Файл: api_client_xxx.py (в корне)

from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExercisesRequestDict
from tools.fakers import get_random_email


# ==========================================
# 1. Создать пользователя
# ==========================================
public_users_client = get_public_users_client()

create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string"
)
create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response)

user_id = create_user_response['user']['id']


# ==========================================
# 2. Логин + клиенты
# ==========================================
authentication_user = AuthenticationUserDict(
    email=create_user_request['email'],
    password=create_user_request['password']
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)


# ==========================================
# 3. Создать файл
# ==========================================
create_file_request = CreateFileRequestDict(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

file_id = create_file_response['file']['id']


# ==========================================
# 4. Создать курс
# ==========================================
create_course_request = CreateCourseRequestDict(
    title="Python",
    maxScore=100,
    minScore=10,
    description="Python API course",
    estimatedTime="2 weeks",
    previewFileId=file_id,
    createdByUserId=user_id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

course_id = create_course_response['course']['id']


# ==========================================
# 5. Создать задание
# ==========================================
create_exercise_request = CreateExercisesRequestDict(
    title="Exercise 1",
    courseId=course_id,
    maxScore=5,
    minScore=1,
    orderIndex=0,
    description="Exercise 1",
    estimatedTime="5 minutes"
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)

exercise_id = create_exercise_response['exercise']['id']


# ==========================================
# 6. Получить задание
# ==========================================
get_exercise_response = exercises_client.get_exercise(exercise_id)
print('Get exercise data:', get_exercise_response)

# ЧАСТЬ 3: Правило 4 вопросов

"""
 ЧАСТЬ 3: Правило 4 вопросов
Перед каждым методом:

Вопрос	Ответ
Какой метод?	get / post / patch / delete
Какой URL?	/api/v1/xxx (без base_url!)
Есть тело?	json=request
Есть query?	params=query

📌 ЧАСТЬ 4: Где что смотреть
Что нужно	Где смотреть
URL эндпоинта	Swagger
Метод (GET/POST/...)	Swagger
Поля запроса	Swagger → Request body
Поля ответа	Swagger → Response
Query-параметры	Swagger → Parameters

📌 ЧАСТЬ 5: Откуда брать id
id	Откуда
user_id	create_user_response['user']['id']
file_id	create_file_response['file']['id']
course_id	create_course_response['course']['id']
exercise_id	create_exercise_response['exercise']['id']

📌 ЧАСТЬ 6: Что где хранится
Что	                             Где
base_url	                 В httpx.Client
headers (токен)	             В httpx.Client
get/post/patch/delete	     В APIClient
Конкретные эндпоинты	     В XxxClient
Логика сценария	             В скрипте
"""



