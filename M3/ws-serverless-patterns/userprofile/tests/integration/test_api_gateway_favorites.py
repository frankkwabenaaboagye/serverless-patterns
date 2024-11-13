
import json
import requests
import logging
import time
import uuid

LOGGER = logging.getLogger(__name__)

user1_new_favorite = {"restaurantId": str(uuid.uuid4())}
user2_new_favorite = {"restaurantId": str(uuid.uuid4())}

def test_access_to_the_favorites_without_authentication(global_config):
    print("\n==========test_access_to_the_favorites_without_authentication")
    response = requests.get(global_config["ProfileApiEndpoint"] + '/favorite')
    assert response.status_code == 401  

def test_add_user_favorite(global_config):
    print("\n=============test_add_user_favorite")
    # LOGGER.info("ID token: %s", global_config["user1UserIdToken"])
    # LOGGER.info("Endpoint: %s", global_config["ProfileApiEndpoint"])
    print(f"ID token: {global_config['user1UserIdToken']}")
    print(f"ID token: {global_config['ProfileApiEndpoint']}")
    response = requests.post(
        global_config["ProfileApiEndpoint"] + '/favorite',
        data=json.dumps(user1_new_favorite),
        headers={'Authorization': global_config["user1UserIdToken"], 
            'Content-Type': 'application/json'}
    ) 
    LOGGER.info(response)
    assert response.status_code == 200  

    # ensure the async request in the queue has time to be processed
    time.sleep(1)

    response = requests.get(
        global_config["ProfileApiEndpoint"] + '/favorite',
        headers={'Authorization': global_config["user1UserIdToken"], 
            'Content-Type': 'application/json'}
    )
    assert response.status_code == 200

    response_data = json.loads(response.text)
    # LOGGER.info(response.text)
    assert len(response_data['favorites']) == 1
    assert response_data['favorites'][0]['restaurant_id'] == user1_new_favorite['restaurantId']

def test_delete_user_favorite(global_config):
    print("\n===========test_delete_user_favorite")
    response = requests.post(
        global_config["ProfileApiEndpoint"] + '/favorite',
        data=json.dumps(user1_new_favorite),
        headers={'Authorization': global_config["user1UserIdToken"], 
            'Content-Type': 'application/json'}
    ) 
    assert response.status_code == 200  

    # ensure the async request in the queue has time to be processed
    time.sleep(1)

    response = requests.delete(
        global_config["ProfileApiEndpoint"] + '/favorite/' + user1_new_favorite['restaurantId'],
        headers={'Authorization': global_config["user1UserIdToken"], 
            'Content-Type': 'application/json'}        
    )
    assert response.status_code == 200

    # ensure the async request in the queue has time to be processed
    time.sleep(1)    

    response = requests.get(
        global_config["ProfileApiEndpoint"] + '/favorite',
        headers={'Authorization': global_config["user1UserIdToken"], 
            'Content-Type': 'application/json'}
    )
    assert response.status_code == 200

    response_data = json.loads(response.text)
    assert len(response_data['favorites']) == 0
