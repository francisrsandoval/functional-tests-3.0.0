
import requests
import json
import os

class VTN_event_tester():
    """VTN integration tests"""

    event_id = 0
    ven_token = 'ven_token'
    bl_token = 'bl_token'

    def __init__(self, base_url):
        self.events_baseUrl = base_url+"/events"
        pass

    def search_all_events(self, token):
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_events
            response = requests.get(self.events_baseUrl, headers=headers)
            # print(f"search_all_events: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_events(): %s\n" % e)

        return response

    def test_search_all_events(self, token):
        # TBD: add test for query params
        print("\n################################################################")
        print(f"test_search_all_events(): token={token}")
        response = self.search_all_events(token)
        if response.status_code != 200:
            print(f"test_search_all_events(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        events  = response.json()
        if events is not None:
            print("test_search_all_events(): PASSED")
            return True
        else:
            print("test_search_all_events(): FAILED. events is None")
            return False

    def search_event_by_id(self, event_id, token):
        url = self.events_baseUrl + '/' + str(event_id)
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_events
            response = requests.get(url, headers = headers)
            # print(f"search_event: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_event(): %s\n" % e)

        return response

    def test_search_event_by_id(self, token):
        # TBD: add test for query params
        print("\n################################################################")
        print (f"test_search_event_by_id(): token={token}")
        response = self.search_event_by_id(self.event_id, token)
        if response.status_code != 200:
            print(f"test_search_event_by_id(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        event  = response.json()
        if event["ID"] == self.event_id:
            print("test_search_event_by_id(): PASSED")
            return True
        else:
            eventID = event["ID"]
            print(f"test_search_event_by_id(): FAILED. event ID {eventID} does not match searched event ID {self.event_id}")
            return False

    def create_event(self, token):
        event = '{ "name": "myEvent", "programID": 0, "intervalPeriod": {"start": "0"}, "intervals": [{"ID": 0, "payloads": [{"payloadType": "PRICE", "values": [0.17]}]}] }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        # print(f"create_event: event={event}")

        try:
            # create_event
            response = requests.post(self.events_baseUrl, data=event, headers=headers)
            # print(f"create_event: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_event(): %s\n" % e)

        return response

    def test_create_event(self, token):
        print("\n################################################################")
        print (f"test_create_event(): token={token}")
        response = self.create_event(token)
        # print (f"test_create_event(): status_code= {response.status_code}")
        event = response.json()
        # print (f"test_create_event(): event= {event}")

        if token == self.bl_token and response.status_code != 200:
            print(f"test_create_event(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and (response.status_code == 403 or response.status_code == 400):
            print("test_create_event(): PASSED")
            return True

        if event['name'] == "myEvent":
            print("test_create_event(): PASSED")
            self.event_id = event['ID']
            return True
        else:
            print("test_create_event(): FAILED. event name does not match created event name")
            return False


    def update_event(self, event_id, token):
        event = '{ "name": "myNewEvent", "programID": 0, "intervalPeriod": {"start": "0"}, "intervals": [{"ID": 0, "payloads": [{"payloadType": "PRICE", "values": [0.17]}]}] }'
        url = self.events_baseUrl + '/' + str(event_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # update
            response = requests.put(url, data=event, headers=headers)
            # print(f"update_event: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_event(): %s\n" % e)

        return response

    def test_update_event(self, token):
        print("\n################################################################")
        print (f"test_update_event(): token={token}")
        response = self.update_event(self.event_id, token)

        if token == self.bl_token and response.status_code != 200:
            print(f"test_update_event(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_update_event(): PASSED")
            return True

        event = response.json()
        if event['name'] == "myNewEvent":
            print("test_update_event(): PASSED")
            return True
        else:
            print("test_update_event(): FAILED. event name does not match updated event name")
            return False

    def delete_event(self, event_id, token):
        url = self.events_baseUrl + '/' + str(event_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # delete event
            response = requests.delete(url, headers=headers)
            # print(f"delete_event: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling delete_event(): %s\n" % e)

        return response

    def test_delete_event(self, token):
        print("\n################################################################")
        print (f"test_delete_event(): token={token}")
        response = self.delete_event(self.event_id, token)

        if token == self.bl_token and response.status_code != 200:
            print(f"test_delete_event(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_delete_event(): PASSED")
            return True

        event = response.json()
        if event['ID'] == self.event_id:
            print("test_delete_event(): PASSED")
            return True
        else:
            print("test_delete_event(): FAILED. event ID does not match deleted event ID")
            return False

    def run_tests(self):

        # Verify that events can be read
        assert (self.test_search_all_events(self.ven_token))
        assert (self.test_search_all_events(self.bl_token))
        # Verify that a event resource may be created
        assert(self.test_create_event(self.ven_token))
        assert(self.test_create_event(self.bl_token))
        # # Verify that the event resource created above is available
        assert(self.test_search_event_by_id(self.ven_token))
        assert(self.test_search_event_by_id(self.bl_token))
        # Verify that the event resource created above cen be updated
        assert(self.test_update_event(self.ven_token))
        assert(self.test_update_event(self.bl_token))
        # Verify that the event resource created above cen be deleted
        assert(self.test_delete_event(self.ven_token))
        assert(self.test_delete_event(self.bl_token))

