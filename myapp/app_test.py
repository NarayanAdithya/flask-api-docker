from app import app
import pytest
import json
from pathlib import Path

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config["TESTING"] = True
    yield app.test_client()  # tests run here

def test_server(client):
    rv=client.get('/test1')
    assert b"Success" in rv.data

def test_addition(client):
    response=client.get('/addition/4/6',content_type='application/json')
    response=json.loads(response.data)
    assert response['result']==10

def test_post(client):
    response=client.post('/todo/api/v1.0/tasks',json={
        'title':"Trial Test",
        'description':"This has to pass",
        'done':False
    })
    assert response.status_code==201

def test_post_retreival(client):
    response=client.post('/todo/api/v1.0/tasks',json={
        'title':"Trial Test",
        'description':"This has to pass",
        'done':False
    })
    last_inserted=json.loads(response.data)['task']
    response=client.get('/todo/api/v1.0/tasks')
    data=json.loads(response.data)
    data=data['tasks'][-1]
    assert last_inserted==data


