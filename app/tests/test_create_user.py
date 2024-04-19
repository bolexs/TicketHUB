from app import model
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.utils.auth import create_access_token

class TestCreateUser:

    def test_create_user(self, client, mocker):
        mocker.patch('app.utils.services.new_user_register', return_value=
        {"message": "User created successfully"})
        response = client.post('/api/v1/user/register', json={
            "name" : "stringrr",
            "email": "user@testing.com",
            "role" : "attendee",
            "password": "string1"
        })
        assert response.status_code == 201
        assert response.json() == {"message": "User created successfully"}

    def test_get_user_by_id(self, client, mocker):
        mocker.patch('app.utils.services.get_user_by_id', return_value={
            "id" : 1,
            "name" : "stringrr",
            "email": "user@testing.com",
            "role" : "attendee",
        })
        user_token = create_access_token(data={"sub": "user@testing.com"})
        response = client.get('/api/v1/user/1', headers={'Authorization': f'Bearer {user_token}'})

        assert response.status_code == 200
        assert response.json() == {
            "id" : 1,
            "name" : "stringrr",
            "email": "user@testing.com",
            "role" : "attendee",
        }

    def test_delete_user_by_id(self, client, mocker):
        mocker.patch('app.utils.services.delete_user_by_id', return_value=None)
        user_token = create_access_token(data={"sub": "user@testing.com"})
        response = client.delete('/api/v1/user/1', headers={'Authorization': f'Bearer {user_token}'})

        assert response.status_code == 204