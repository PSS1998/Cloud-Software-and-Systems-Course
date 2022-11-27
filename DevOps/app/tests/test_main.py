from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_course():
    ## TODO: Check if GET /courses/{course_id} returns status code 200 and that the json response is
    ## correct (as per db) when the course exists
    response = client.get('/courses/CS-E4190') # Fix the route to API as required
    assert response.json() == {"id": "CS-E4190", "name": "Cloud software and systems",
                 "instructor": "Mario Di francesco", "keyword": ["cloud", "container"]}
    assert response.status_code == 200


def test_read_nonexistent_course():
    ## TODO: Check if GET /courses/{course_id} returns status code 404 and that the json response is
    ## {"detail": "Course does not exist"} when the course does not exist
    response = client.get('/courses/CS-E4191') # Fix the route to API as required
    assert response.json() == {"detail": "Course does not exist"}
    assert response.status_code == 404


def test_create_course():
    ## TODO: Check if POST /courses/ returns status code 200 and that the json response
    ## contains the correct data if the course does not exist in the db.
    response = client.post('/courses/',json={"id": "CS-E4192", "name": "Cloud software and systems",
                 "instructor": "Mario Di francesco", "keyword": ["cloud", "container"]}) # Fix the route to API and data as required
    assert response.json() == {"id": "CS-E4192", "name": "Cloud software and systems",
                 "instructor": "Mario Di francesco", "keyword": ["cloud", "container"]}
    assert response.status_code == 200

def test_create_existing_course():
    ## TODO: Check if POST /courses/ returns status code 400 and that the json response
    ## is {"detail": "Course already exists"} if the course already exists in the db.
    response = client.post('/courses/',json={"id": "CS-E4190", "name": "Cloud software and systems",
                 "instructor": "Mario Di francesco", "keyword": ["cloud", "container"]})  # Fix the route to API and data as required
    assert response.json() == {"detail": "Course already exists"}
    assert response.status_code == 400
