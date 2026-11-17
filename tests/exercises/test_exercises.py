from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_get_exercise_response,
    assert_update_exercise_response,
    assert_exercise_not_found_response
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
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное получение данных созданного задания.
        """
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное обновление данных задания.
        """
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(
            self,
            exercises_client: ExercisesClient,
            function_exercise: ExerciseFixture
    ):
        """
        Тест проверяет успешное удаление задания и то, что оно больше не находится по ID.
        """
        exercise_id = function_exercise.response.exercise.id

        # 1. Удаляем задание
        delete_response = exercises_client.delete_exercise_api(exercise_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # 2. Пытаемся получить удаленное задание
        get_response = exercises_client.get_exercise_api(exercise_id)

        # 3. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)

        # 4. Парсим ответ в модель внутренней ошибки
        response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # 5. Проверяем текст ошибки и валидируем JSON-схему
        assert_exercise_not_found_response(response_data)
        validate_json_schema(get_response.json(), response_data.model_json_schema())