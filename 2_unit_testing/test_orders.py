import pytest
import cluster

def test_confirm_pick():
    order_id = "00000001"
    confirmations = [{"upc": "123456789012", "quantity_confirmed": 1}]
    result = cluster.confirm_pick(order_id, confirmations)
    assert result['success'] == True

def test_pack_order_success():
    order_id = "00000001"
    carton_id = "CARTON_123"
    result = cluster.pack_order(order_id, carton_id)
    assert result['success'] == True

def test_pack_order_failure():
    order_id = "non_existent_order"
    carton_id = "CARTON_123"
    result = cluster.pack_order(order_id, carton_id)
    assert result['error'] == "Order with ID non_existent_order does not exist."
