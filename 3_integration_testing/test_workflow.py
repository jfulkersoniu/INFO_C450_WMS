import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_picking_workflow(client):
    # Login first
    client.post('/auth/login', data=dict(username='test_user', password='correct_password'))

    # Begin picking
    response = client.post('/picking/', data=dict(action='begin_picking'))
    assert response.status_code == 200
    assert b'Confirm Picking' in response.data

    # Confirm picking
    response = client.post('/picking/confirm', data=dict(order_id='00000001', upc_123456789012=1))
    assert response.status_code == 302  # Redirects after successful confirmation
    assert b'Order 00000001 successfully picked.' in response.data
