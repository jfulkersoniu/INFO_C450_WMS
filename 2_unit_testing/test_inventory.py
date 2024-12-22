import pytest
import cluster

def test_add_inventory_item():
    upc = "123456789012"
    quantity = 10
    location = "Aisle 1"
    reserved = False
    result = cluster.add_inventory_item(upc, quantity, location, reserved)
    assert result is not None

def test_find_item():
    upc = "123456789012"
    item = cluster.find_item(upc)
    assert item is not None
    assert item['upc'] == upc
