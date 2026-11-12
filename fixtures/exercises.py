import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
    """
    Модель для агрегации данных фикстуры function_exercise.
    """
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для получения API-клиента заданий.
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture
) -> ExerciseFixture:
    """
    Фикстура для создания тестового задания.
    """
    request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
    response = exercises_client.create_exercise(request)

    return ExerciseFixture(request=request, response=response)