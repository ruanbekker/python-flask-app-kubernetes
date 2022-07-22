from server import app

def test_index_route():
    response = app.test_client().get('/hostname')

    assert response.status_code == 200
    assert response.data.decode('utf-8').startswith("hello from")
