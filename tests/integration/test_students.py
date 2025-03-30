from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.students.models import Student
from app.students.schemas import SStudent


@pytest.mark.asyncio
async def test_root(client: TestClient):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK

@pytest.mark.run(order=1)
@pytest.mark.asyncio
async def test_create_one_valid_student(client: TestClient, test_db: AsyncSession):
    student = {'email': 'test@gmail.com'}
    response = client.post('/students', json=student)
    result = await test_db.execute(select(Student))
    objects = result.fetchall()
    assert response.status_code == HTTPStatus.CREATED
    assert len(objects) == 1

@pytest.mark.run(order=1)
@pytest.mark.asyncio
async def test_create_one_invalid_student(client: TestClient, test_db: AsyncSession):
    student = {'email': 'testgmail.com'}
    response = client.post('/students', json=student)
    result = await test_db.execute(select(Student))
    objects = result.fetchall()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(objects) == 0

@pytest.mark.asyncio
async def test_get_student_with_valid_id(client: TestClient):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    user = client.get('/students/1')

    assert user.status_code == HTTPStatus.OK
    assert user.json() == SStudent(**student).model_dump()

@pytest.mark.asyncio
async def test_get_student_with_invalid_id(client: TestClient):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    user = client.get('/students/2')

    assert user.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_update_student_with_valid_data(client: TestClient):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    new_data = {'email': 'new_email@gmail.com', 'first_name': 'Maksim'}
    response = client.patch('/students/1', json=new_data)
    user = client.get('/students/1').json()

    for field in user:
        if user[field] and field != 'id':
            assert user[field] == new_data[field]

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_update_student_with_invalid_data(client: TestClient):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    new_data = {'email': 'invalidemailgmail.com', 'first_name': 'Maksim'}
    response = client.patch('/students/1', json=new_data)
    user = client.get('/students/1').json()

    for field in user:
        if user[field]:
            assert user[field] == student[field]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_delete_student_with_valid_id(client: TestClient, test_db: AsyncSession):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    response = client.delete('/students/1')
    cursor = await test_db.execute(select(Student))
    objects = cursor.fetchall()

    assert len(objects) == 0
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_student_with_invalid_id(client: TestClient, test_db: AsyncSession):
    student = {'id': 1, 'email': 'test@gmail.com'}
    client.post('/students', json=student)

    response = client.delete('/students/2')
    cursor = await test_db.execute(select(Student))
    objects = cursor.fetchall()

    assert len(objects) == 1
    assert response.status_code == HTTPStatus.NOT_FOUND
