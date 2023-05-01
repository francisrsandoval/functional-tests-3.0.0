
import requests
import json
import os

CALLBACK_URL="http://localhost:8082"


class VTN_subscription_tester():
    """VTN integration tests"""

    subscription_id = 0
    ven_token = 'ven_token'
    bl_token = 'bl_token'

    def __init__(self, base_url, callback_output):
        self.base_url = base_url
        self.subscriptions_baseUrl = base_url+"/subscriptions"
        self.callback_output = callback_output
        pass

    def search_all_subscriptions(self, token):
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_subscriptions
            response = requests.get(self.subscriptions_baseUrl, headers=headers)
            # print(f"search_all_subscriptions(): response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_subscriptions(): %s\n" % e)

        return response

    def test_search_all_subscriptions(self, token):
        print("\n################################################################")
        print(f"test_search_all_subscriptions(): token={token}")
        response = self.search_all_subscriptions(token)
        if response.status_code != 200:
            print(f"test_search_all_subscriptions(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        subscriptions  = response.json()
        if subscriptions is not None:
            print("test_search_all_subscriptions(): PASSED")
            return True
        else:
            print("test_search_all_subscriptions(): FAILED. subscriptions = None")
            return False

    def search_subscription(self, subscription_id, token):
        url = self.subscriptions_baseUrl + '/' + str(subscription_id)
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_subscriptions
            response = requests.get(url, headers = headers)
            # print(f"search_subscription(): response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_subscription(): %s\n" % e)

        return response

    def test_search_subscription(self, token):
        print("\n################################################################")
        print (f"test_search_subscription(): token={token}")
        response = self.search_subscription(self.subscription_id, token)
        if response.status_code != 200:
            print(f"test_search_subscription(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        subscription  = response.json()
        if subscription["ID"] == self.subscription_id:
            print("test_search_subscription(): PASSED")
            return True
        else:
            id = subscription["ID"]
            print(f"test_search_subscription(): FAILED. ID does not match, response ID={id} subscription_id={self.subscription_id}")
            return False

    def create_subscription(self, token):
        subscription = '{"clientID": 0, "programID": 978, "resourceOperations": [{"resources": ["EVENT"], "operations": ["POST"], "callbackUrl": "http://localhost:8082"}] }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_subscription
            response = requests.post(self.subscriptions_baseUrl, data=subscription, headers=headers)
            # print(f"create_subscription(): response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_subscription(): %s\n" % e)

        return response

    def test_create_subscription(self, token):
        print("\n################################################################")
        print (f"test_create_subscription(): token={token}")
        response = self.create_subscription(token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_create_subscription(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_create_subscription(): PASSED")
            return True

        subscription  = response.json()
        # print (f"test_create_subscription(): subscription={subscription}")
        if subscription["programID"] == 978:
            print("test_create_subscription(): PASSED")
            self.subscription_id = subscription['ID']
            return True
        else:
            programID = subscription["programID"]
            print("test_create_subscription(): FAILED. programID does not match. programID={programID}")
            return False

    def delete_subscription(self, subscription_id, token):
        url = self.subscriptions_baseUrl + '/' + str(subscription_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_subscription
            response = requests.delete(url, headers=headers)
            # print(f"delete_subscription(): response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling delete_subscription(): %s\n" % e)

        return response

    def test_delete_subscription(self, token):
        print("\n################################################################")
        print (f"test_delete_subscription(): token={token}")
        response = self.delete_subscription(self.subscription_id, token)

        if token == self.bl_token and response.status_code != 200:
            print(f"test_delete_subscription(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_delete_subscription(): PASSED")
            return True

        subscription  = response.json()
        if subscription["ID"] == self.subscription_id:
            print("test_delete_subscription(): PASSED")
            return True
        else:
            id = subscription["ID"]
            print(f"test_delete_subscription(): FAILED. ID does not match, response ID={id} subscription_id={self.subscription_id}")
            return False

    def update_subscription(self, subscription_id, token):
        subscription = '{"clientID": 342, "programID": 978, "resourceOperations": [{"resources": ["EVENT"], "operations": ["POST"], "callbackUrl": "'+CALLBACK_URL+'"}] }'
        # print (f"update_subscription(): subscription={subscription}")
        url = self.subscriptions_baseUrl + '/' + str(subscription_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_subscription
            response = requests.put(url, data=subscription, headers=headers)
            # print(f"update_subscription(): response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_subscription(): %s\n" % e)

        return response

    def test_update_subscription(self, token):
        print("\n################################################################")
        print(f"test_update_subscription(): token={token}")
        response = self.update_subscription(self.subscription_id, token)
        # print(f"test_update_subscription(): response={response}")

        if response.status_code != 200:
            print(f"test_update_subscription(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        subscription = response.json()
        # print(f"test_update_subscription(): subscription={subscription}")
        if subscription["clientID"] == 342:
            print("test_update_subscription(): PASSED")
            return True
        else:
            clientID=subscription["clientID"]
            print(f"test_update_subscription(): FAILED. clientID does not match clientID={clientID}")
            return False

    def test_callback(self, token):
        # requires callback server to be running at http://localhost:8082
        print("\n################################################################")
        print(f"test_callback(): token={token}")

        response = self.create_subscription(token)

        event = '{ "name": "myEvent", "programID": 0, "activePeriod": {"start": "0"}, "intervals": [{"ID": 0, "payloads": [{"payloadType": "PRICE", "values": [0.17]}]}] }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_event
            response = requests.post(self.base_url+"/events", data=event, headers=headers)
            # print(f"create_event(): response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_event(): %s\n" % e)

        # callback server will dump results into local file
        with open(self.callback_output, "r+") as f:
            event = json.load(f)
            if event['name'] == "myEvent":
                print("test_callback(): PASSED")
                return True
            else:
                name=event['name']
                print(f"test_callback(): FAILED. event name does not match {name}")
                return False

    def run_tests(self):
        # Verify that no subscriptions resources are available
        assert(self.test_search_all_subscriptions(self.ven_token))
        # Verify that a subscription resource may be created
        assert(self.test_create_subscription(self.ven_token))
        # Verify that the subscription resource created above is available
        assert(self.test_search_subscription(self.ven_token))
        # Verify that the subscription resource created above cen be updated
        assert (self.test_update_subscription(self.ven_token))
        # Verify that the subscription resource created above cen be deleted
        assert (self.test_delete_subscription(self.ven_token))
        # Verify that the subscription callback is invoked on event creation
        assert(self.test_callback(self.ven_token))

        # Verify that a subscription resource may be created
        assert(self.test_create_subscription(self.bl_token))
        # Verify that the subscription resource created above is available
        assert(self.test_search_subscription(self.bl_token))
        # Verify that the subscription resource created above cen be updated
        assert (self.test_update_subscription(self.bl_token))
        # Verify that the subscription resource created above cen be deleted
        assert(self.test_delete_subscription(self.bl_token))
