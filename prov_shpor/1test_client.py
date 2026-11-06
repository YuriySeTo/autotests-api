from pydantic import BaseModel, Field, uuid


class BookSchema(BaseModel):
    id: str
    name: str
    price: int
    in_stock: bool = Field(alias="inStock")
    created_at: str = Field(alias="createdAt")
    image_url: HttpUrl = Field(alias="imageUrl")
    description: str | None = None

product_json ='''
{
    "id": "prod-123",
    "name": "Ноутбук",
    "price": 75000,
    "inStock": true,
    "createdAt": "2024-01-15",
    "imageUrl": "https://example.com/img.png",
    "description": null
}
'''

product_from_json = ProductSchema.model_validate_json(product_json)
print('Product JSON model:', product_from_json)
print(product_from_json.model_dump())
print(product_from_json.model_dump(by_alias=True))








class UpdateExercisesRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания.
    Все поля опциональны — передаём только то, что меняем.
    """
    title: str | None = None
    maxScore: int | None = None
    minScore: int | None = None
    orderIndex: int | None = None
    description: str | None = None
    estimatedTime: str | None = None


class GetExercisesResponseSchema(BaseModel):
    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class CreateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class UpdateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения списка заданий.

        :param query: Модель с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get("/api/v1/exercises", params=query.model_dump())

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExercisesRequestSchema) -> Response:
        """
        Метод создания задания.

        :param request: Модель с title, courseId, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/exercises", json=request.model_dump())

    def update_exercise_api(
        self, exercise_id: str, request: UpdateExercisesRequestSchema
    ) -> Response:
        """
        Метод обновления задания.

        :param exercise_id: Идентификатор задания.
        :param request: Модель с опциональными title, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(
            f"/api/v1/exercises/{exercise_id}",
            json=request.model_dump(exclude_none=True),
        )

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        """
        Метод получения списка заданий.

        :param query: Модель с courseId.
        :return: Список заданий.
        """
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate(response.json())

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        """
        Метод получения задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Данные задания.
        """
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate(response.json())

    def create_exercise(
        self, request: CreateExercisesRequestSchema
    ) -> CreateExerciseResponseSchema:
        """
        Метод создания задания.

        :param request: Модель с title, courseId, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Данные созданного задания.
        """
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate(response.json())

    def update_exercise(
        self, exercise_id: str, request: UpdateExercisesRequestSchema
    ) -> UpdateExerciseResponseSchema:
        """
        Метод обновления задания.

        :param exercise_id: Идентификатор задания.
        :param request: Модель с опциональными title, maxScore, minScore, orderIndex,
        description, estimatedTime.
        :return: Данные обновлённого задания.
        """
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate(response.json())


def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))