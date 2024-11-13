import json
import requests
import logging
import time
import uuid
import pytest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

order_1 = {
    "restaurantId": 1,
    "orderId": str(uuid.uuid4()),
    "orderItems": [
        {
            "id": 1,
            "name": "Spaghetti",
            "price": 9.99,
            "quantity": 1
        },
        {
            "id": 2,
            "name": "Pizza - SMALL",
            "price": 4.99,
            "quantity": 2
        },
    ],
    "totalAmount": 19.97,
    "status": "PLACED"
}

@pytest.fixture
def orders_endpoint(global_config):
  '''Returns the endpoint for the Orders service'''
  orders_endpoint = global_config["OrdersServiceEndpoint"] + '/orders'
  logger.debug("Orders Endpoint = " + orders_endpoint)
  return orders_endpoint

@pytest.fixture
def user_token(global_config):
  '''Returns the user_token for authentication to the Orders service'''
  user_token = global_config["user1UserIdToken"]
  logger.debug("     User Token = " + user_token)
  return user_token


def test_access_orders_without_authentication(orders_endpoint):
  print("\n\n========== test_access_orders_without_authentication\n")

  print(f"orders_endpoint = {orders_endpoint}")

  print("\n======================================\n")
  response = requests.post(orders_endpoint)
  assert response.status_code == 401
  print("*****************************\n\n")


def test_add_new_order(global_config, orders_endpoint, user_token):
  print("\n\n========== test_add_new_order\n")

  print("global_config = \n" + json.dumps(global_config, indent=4))
  print("\n")
  print("orders_endpoint = \n" + json.dumps(orders_endpoint, indent=4))
  print("\n")
  print(f"user_token = {user_token}")

  print("*****************************\n\n")
  
  response = requests.post(orders_endpoint, data=json.dumps(order_1),
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )
  logger.debug("Add new order response: %s", response.text)
  assert response.status_code == 200
  order_info = response.json()
  order_id = order_info['orderId']
  order_time = order_info['orderTime']
  logger.debug("New orderId: %s", order_id)
  global_config['orderId'] = order_id
  global_config['orderTime'] = order_time
  assert order_info['status'] == "PLACED"
  print("*****************************")


def test_get_order(global_config, orders_endpoint, user_token):
  print("\n\n=========== test_get_order")

  print("preforming request.....\n Waiting for a response....\n")
  response = requests.get(orders_endpoint + "/" + global_config['orderId'],
      headers={'Authorization': user_token, 'Content-Type': 'application/json'}
      )
  
  print("response = \n")
  print("response.text = \n" + response.text)
  

  logger.debug(response.text)
  order_info = json.loads(response.text)
  assert order_info['orderId'] == global_config['orderId']
  assert order_info['status'] == "PLACED"
  assert order_info['totalAmount'] == 19.97
  assert order_info['restaurantId'] == 1
  assert len(order_info['orderItems']) == 2
  print("*****************************\n\n")