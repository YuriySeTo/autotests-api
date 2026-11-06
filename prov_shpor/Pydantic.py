"""

==========================================
ШПОРА: TypedDict -> Pydantic
==========================================

1. ИМПОРТЫ

Было:
    from typing import TypedDict

Стало:
    from pydantic import BaseModel, Field, EmailStr, HttpUrl


2. ОБЩЕЕ ПРАВИЛО ДЛЯ МОДЕЛЕЙ

    TypedDict   ->  BaseModel
    XxxDict     ->  XxxSchema
    camelCase   ->  snake_case
    (нет)       ->  Field(alias="camelCase")


3. МОДЕЛИ ЗАПРОСОВ

Было:
    class CreateUsersRequestDict(TypedDict):
        email: str
        password: str
        lastName: str
        firstName: str
        middleName: str

Стало:
    class CreateUserRequestSchema(BaseModel):
        email: EmailStr
        password: str
        last_name: str = Field(alias="lastName")
        first_name: str = Field(alias="firstName")
        middle_name: str = Field(alias="middleName")

Для обновления (добавляем | None = None):
    class UpdateUserRequestSchema(BaseModel):
        email: EmailStr | None = None
        last_name: str | None = Field(alias="lastName", default=None)
        first_name: str | None = Field(alias="firstName", default=None)
        middle_name: str | None = Field(alias="middleName", default=None)


4. МОДЕЛИ СУЩНОСТЕЙ

Было:
    class User(TypedDict):
        id: str
        email: str
        lastName: str
        firstName: str
        middleName: str

Стало:
    class UserSchema(BaseModel):
        id: str
        email: EmailStr
        last_name: str = Field(alias="lastName")
        first_name: str = Field(alias="firstName")
        middle_name: str = Field(alias="middleName")


5. МОДЕЛИ ОТВЕТОВ

Было:
    class GetUserResponseDict(TypedDict):
        user: User

    class GetUsersResponseDict(TypedDict):
        users: list[User]

Стало:
    class GetUserResponseSchema(BaseModel):
        user: UserSchema

    class GetUsersResponseSchema(BaseModel):
        users: list[UserSchema]

Правило:
    один объект -> user: UserSchema
    список      -> users: list[UserSchema]


6. *_API МЕТОДЫ

Было:
    def create_user_api(self, request: CreateUsersRequestDict) -> Response:
        return self.post("/api/v1/users", json=request)

Стало:
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        return self.post(
            "/api/v1/users",
            json=request.model_dump(by_alias=True)
        )

Для PATCH (с exclude_none=True):
    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        return self.patch(
            f"/api/v1/users/{user_id}",
            json=request.model_dump(by_alias=True, exclude_none=True)
        )


7. МЕТОДЫ БЕЗ _API

Было:
    def create_user(self, request: CreateUsersRequestDict) -> CreateUserResponseDict:
        response = self.create_user_api(request)
        return response.json()

Стало:
    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema(**response.json())


8. ИСПОЛЬЗОВАНИЕ В СКРИПТЕ

Было:
    create_user_request = CreateUsersRequestDict(
        email=get_random_email(),
        password="string",
    )
    user_id = create_user_response['user']['id']

Стало:
    create_user_request = CreateUserRequestSchema(
        email=get_random_email(),
        password="string",
    )
    user_id = create_user_response.user.id


9. ЧЕК-ЛИСТ ПЕРЕХОДА

Для каждой модели:
    [ ] TypedDict -> BaseModel
    [ ] XxxDict -> XxxSchema
    [ ] camelCase -> snake_case
    [ ] Field(alias="camelCase") где был camelCase
    [ ] str -> EmailStr для email
    [ ] str -> HttpUrl для url
    [ ] опциональные -> | None = None

Для каждого *_api:
    [ ] json=request -> json=request.model_dump(by_alias=True)
    [ ] для PATCH -> добавить exclude_none=True

Для каждого метода без _api:
    [ ] return response.json() -> return XxxSchema(**response.json())


10. ШПАРГАЛКА PYTHON

    BaseModel                                       родитель моделей
    Field(alias="...")                              связь с API именем
    Field(default=...)                              значение по умолчанию
    EmailStr                                        валидация email
    HttpUrl                                         валидация URL
    model_dump()                                    модель -> словарь (Python имена)
    model_dump(by_alias=True)                       модель -> словарь (API имена)
    model_dump(by_alias=True, exclude_none=True)    словарь без None
    Schema(**dict)                                  создать модель из словаря
    Schema.model_validate_json(json_str)            создать модель из JSON
    ValidationError                                 исключение при ошибке

==========================================

"""