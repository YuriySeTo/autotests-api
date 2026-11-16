from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(
            self,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):
        """
        Тест проверяет успешное создание нового задания.
        """
        # 1. Формируем запрос, используя фикстуру function_course для course_id
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)

        # 2. Отправляем POST-запрос
        response = exercises_client.create_exercise_api(request)

        # 3. Проверяем статус-код (200 OK)
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 4. Парсим ответ в Pydantic-модель
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # 5. Проверяем тело ответа
        assert_create_exercise_response(request, response_data)

        # 6. Валидируем JSON-схему
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное получение данных созданного задания.
        """
        # 1. Отправляем GET-запрос по ID задания
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)

        # 2. Проверяем статус-код
        assert_status_code(response.status_code, HTTPStatus.OK)

        # 3. Парсим ответ
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # 4. Сравниваем данные с тем, что было при создании
        assert_get_exercise_response(response_data, function_exercise.response)

        # 5. Валидируем JSON-схему
        validate_json_schema(response.json(), response_data.model_json_schema())