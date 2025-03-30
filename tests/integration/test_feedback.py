from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.feedback.models import Feedback


@pytest.mark.asyncio
async def test_create_feedback_with_valid_data(client: TestClient, test_db: AsyncSession):
    client.post('/students', json={'id': 1, 'email': 'test@gmail.com'})
    feedback_data = {'user_id': 1, 'title': 'test title', 'text': 'text'}
    feedback = client.post('/feedbacks', json=feedback_data)
    feedback_json = feedback.json()

    cursor = await test_db.execute(select(Feedback))
    objects = cursor.fetchall()

    assert feedback.status_code == HTTPStatus.CREATED
    assert len(objects) == 1
    for key, value in feedback_data.items():
        assert feedback_json.get(key) == value

@pytest.mark.asyncio
async def test_create_feedback_with_invalid_data(client: TestClient, test_db: AsyncSession):
    client.post('/students', json={'id': 1, 'email': 'test@gmail.com'})
    feedback = client.post('/feedbacks', json={'user_id': 1, 'title': 'test title'})

    cursor = await test_db.execute(select(Feedback))
    objects = cursor.fetchall()

    assert feedback.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert len(objects) == 0

@pytest.mark.asyncio
async def test_get_feedback_with_valid_id(client: TestClient):
    client.post('/students', json={'id': 1, 'email': 'test@gmail.com'})
    feedback_data = {'user_id': 1, 'title': 'test title', 'text': 'text'}
    feedback = client.post('/feedbacks', json=feedback_data)
    feedback_json = feedback.json()

    response = client.get('/feedbacks/1')

    assert response.status_code == HTTPStatus.OK
    for key, value in feedback_data.items():
        assert feedback_json.get(key) == value

@pytest.mark.asyncio
async def test_get_many_feedbacks(client: TestClient):
    client.post('/students', json={'id': 1, 'email': 'test@gmail.com'})

    feedback1_data = {'user_id': 1, 'title': 'test title1', 'text': 'text1'}
    feedback2_data = {'user_id': 1, 'title': 'test title2', 'text': 'text2'}

    feedback1 = client.post('/feedbacks', json=feedback1_data)
    feedback2 = client.post('/feedbacks', json=feedback2_data)

    feedback1_json = feedback1.json()
    feedback2_json = feedback2.json()

    feedbacks_response = client.get('/feedbacks')
    feedbacks = feedbacks_response.json()

    assert len(feedbacks) == 2  # noqa: PLR2004

    for key, value in feedback1_data.items():
        assert feedback1_json.get(key) == value
    for key, value in feedback2_data.items():
        assert feedback2_json.get(key) == value
