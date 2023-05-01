
import requests
import json
import os

class VTN_ven_tester():
    """VTN integration tests"""

    ven_id = 0
    resource_id = 0
    ven_token = 'ven_token'
    bl_token = 'bl_token'

    def __init__(self, base_url):
        self.vens_baseUrl = base_url+"/vens"
        pass

    def search_all_vens(self, token):
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_vens
            response = requests.get(self.vens_baseUrl, headers=headers)
            # print(f"search_all_vens: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_vens(): %s\n" % e)

        return response

    def test_search_all_vens(self, token):
        print("\n################################################################")
        print(f"test_search_all_vens(): token={token}")
        response = self.search_all_vens(token)
        if response.status_code != 200:
            print(f"test_search_all_vens(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        vens  = response.json()
        if vens is not None:
            print("test_search_all_vens(): PASSED")
            return True
        else:
            print("test_search_all_vens(): FAILED. vens is None")
            return False

    def search_ven(self, ven_id, token):
        url = self.vens_baseUrl + '/' + str(ven_id)
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_vens
            response = requests.get(url, headers = headers)
            # print(f"search_ven: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_ven(): %s\n" % e)

        return response

    def test_search_ven(self, token):
        print("\n################################################################")
        print (f"test_search_ven(): token={token}")
        response = self.search_ven(self.ven_id, token)
        if response.status_code != 200:
            print(f"test_search_ven(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        vens  = response.json()
        if vens["ID"] == self.ven_id:
            print("test_search_ven(): PASSED")
            return True
        else:
            venID = vens["ID"]
            print(f"test_search_ven(): FAILED. venID {venID} does not motch ven_id {self.ven_id}")
            return False

    def create_ven(self, token):
        ven = '{"venID": "myVEN" }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_ven
            response = requests.post(self.vens_baseUrl, data=ven, headers=headers)
            # print(f"create_ven: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_ven(): %s\n" % e)

        return response

    def test_create_ven(self, token):
        print("\n################################################################")
        print (f"test_create_ven(): token={token}")
        response = self.create_ven(token)
        if response.status_code != 200:
            print(f"test_create_ven(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False


        ven  = response.json()
        # print (f"test_create_ven(): ven={ven}")
        if ven["venID"] == "myVEN":
            print("test_create_ven(): PASSED")
            self.ven_id = ven['ID']
            return True
        else:
            print("test_create_ven(): FAILED. venID does not match created ven")
            return False

    def delete_ven(self, ven_id, token):
        url = self.vens_baseUrl + '/' + str(ven_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_ven
            response = requests.delete(url, headers=headers)
            # print(f"delete_ven: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling delete_ven(): %s\n" % e)

        return response

    def test_delete_ven(self, token):
        print("\n################################################################")
        print (f"test_delete_ven(): token={token}")
        response = self.delete_ven(self.ven_id, token)

        if token == self.bl_token and response.status_code != 200:
            print(f"test_delete_ven(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_delete_ven(): PASSED")
            return True

        ven  = response.json()
        if ven["ID"] == self.ven_id:
            print("test_delete_ven(): PASSED")
            return True
        else:
            venID = ven["ID"]
            print(f"test_delete_ven(): FAILED, ven ID {venID} does not match ven_id {venID}")
            return False

    def update_ven(self, ven_id, token):
        ven = '{"venID": "myNewVEN" }'
        url = self.vens_baseUrl + '/' + str(ven_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_ven
            response = requests.put(url, data=ven, headers=headers)
            # print(f"update_ven: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_ven(): %s\n" % e)

        return response

    def test_update_ven(self, token):
        print("\n################################################################")
        print(f"test_update_ven(): token={token}")
        response = self.update_ven(self.ven_id, token)
        # print(f"test_update_ven(): response={response}")

        if response.status_code != 200:
            print(f"test_update_ven(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        ven = response.json()
        # print(f"test_update_ven: ven={ven}")
        if ven["venID"] == "myNewVEN":
            print("test_update_ven(): PASSED")
            return True
        else:
            print("test_update_ven(): FAILED, venID does not match updated ven")
            return False

    # def test_callback(self, token):
    #     # requires callback server to be running at http://localhost:8082
    #     print("\n################################################################")
    #     print(f"test_callback(): token={token}")
    #
    #     response = self.create_ven(token)
    #
    #     event = '{ "name": "myEvent", "programID": 0, "activePeriod": {"start": "0"}, "intervals": [{"ID": 0, "payloads": [{"payloadType": "PRICE", "values": [0.17]}]}] }'
    #     headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
    #
    #     try:
    #         # create_event
    #         response = requests.post('http://localhost:8080/pajarito/OpenAPI-3.0/1.0.0/events', data=event, headers=headers)
    #         # print(f"create_event: response={response.json()}")
    #     except requests.exceptions.RequestException as e:
    #         print("Exception when calling test_callback(): %s\n" % e)
    #
    #     # callback server will dump results into local file
    #     with open(self.callback_output, "r+") as f:
    #         data = json.load(f)
    #         if data['name'] == "myEvent":
    #             print("test_callback(): PASSED")
    #             return True
    #         else:
    #             print("test_callback(): FAILED. callback output does not match  ")
    #             return False


    def search_all_ven_resources(self, ven_id, token):
        url = self.vens_baseUrl + '/' + str(ven_id) + '/resources'
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_ven resources
            response = requests.get(self.vens_baseUrl, headers=headers)
            # print(f"search_all_ven_resources: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_ven_resources(): %s\n" % e)

        return response

    def test_search_all_ven_resources(self, token):
        print("\n################################################################")
        print(f"test_search_all_ven_resources(): token={token}")
        response = self.search_all_ven_resources(ven_id = 0, token=token)
        if response.status_code != 200:
            print(f"test_search_all_ven_resources(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        vens  = response.json()
        if vens is not None:
            print("test_search_all_ven_resources(): PASSED")
            return True
        else:
            print("test_search_all_ven_resources(): FAILED. ven = None")
            return False

    def search_ven_resource(self, ven_id, resource_id, token):
        url = self.vens_baseUrl + '/' + str(ven_id)+ '/resources/' + str(resource_id)
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_vens
            response = requests.get(url, headers = headers)
            # print(f"search_ven_resource: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_ven_resource(): %s\n" % e)

        return response

    def test_search_ven_resource(self, token):
        print("\n################################################################")
        print (f"test_search_ven_resource(): token={token}")
        response = self.search_ven_resource(self.ven_id, resource_id=0, token=token)
        if response.status_code != 200:
            print(f"test_search_ven_resource(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        resource  = response.json()
        if resource["ID"] == 0:
            print("test_search_ven_resource(): PASSED")
            return True
        else:
            print("test_search_ven_resource(): FAILED. reosurce[ID] does not match requested resource")
            return False

    def create_ven_resource(self, token, ven_id):
        resource = '{"resourceID": "myResource" }'
        url = self.vens_baseUrl + '/' + str(ven_id) + '/resources'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_ven
            response = requests.post(url, data=resource, headers=headers)
            # print(f"create_ven: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_ven_resource(): %s\n" % e)

        return response


    def test_create_ven_resource(self, token):
        print("\n################################################################")
        print (f"test_create_ven_resource(): token={token}")
        response = self.create_ven_resource(token, ven_id=0)
        if response.status_code != 200:
            print(f"test_create_ven_resource(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False


        resource  = response.json()
        # print (f"test_create_ven_resource(): resource={resource}")
        if resource["resourceID"] == "myResource":
            print("test_create_ven_resource(): PASSED")
            self.resource_id = resource['ID']
            return True
        else:
            print("test_create_ven_resource(): FAILED. resourceID does not match created resource")
            return False

    def delete_ven_resource(self, token, ven_id, resource_id):
        url = self.vens_baseUrl + '/' + str(ven_id) + '/resources/' +str(resource_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # delete_ven_resource
            response = requests.delete(url, headers=headers)
            # print(f"create_ven: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_ven(): %s\n" % e)

        return response


    def test_delete_ven_resource(self, token):
        print("\n################################################################")
        print (f"test_delete_ven_resource(): token={token}")
        response = self.delete_ven_resource(token, ven_id=0, resource_id=0)
        if response.status_code != 200:
            print(f"test_delete_ven_resource(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        print("test_delete_ven_resource(): PASSED")
        return True


    def update_ven_resource(self, token, ven_id, resource_id):
        resource = '{"resourceID": "myNewResource" }'
        url = self.vens_baseUrl + '/' + str(ven_id) + '/resources/' +str(resource_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # update_ven_resource
            response = requests.put(url, data=resource, headers=headers)
            # print(f"update_ven_resource: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_ven_resource(): %s\n" % e)

        return response


    def test_update_ven_resource(self, token):
        print("\n################################################################")
        print (f"test_update_ven_resource(): token={token}")
        response = self.update_ven_resource(token, ven_id=0, resource_id=0)
        if response.status_code != 200:
            print(f"test_update_ven_resource(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        resource  = response.json()
        # print (f"test_update_ven_resource(): resource={resource}")
        if resource["resourceID"] == "myNewResource":
            print("test_update_ven_resource(): PASSED")
            return True
        else:
            print("test_update_ven_resource(): FAILED. resourceID does not match updated resource")
            return False

    def run_tests(self):
        # Verify that no vens are available
        assert(self.test_search_all_vens(self.ven_token))
        # Verify that a ven may be created
        assert(self.test_create_ven(self.ven_token))
        # Verify that the ven created above is available
        assert(self.test_search_ven(self.ven_token))
        # Verify that the ven created above cen be updated
        assert (self.test_update_ven(self.ven_token))
        # Verify that the ven created above cen be deleted
        assert (self.test_delete_ven(self.ven_token))

        # Verify that ven  resource may be created
        assert (self.test_create_ven_resource(self.ven_token))
        # # Verify that ven  resource may be searched
        assert (self.test_search_ven_resource(self.ven_token))
        # Verify that ven  resource may be updated
        assert (self.test_update_ven_resource(self.ven_token))
        # Verify that ven  resource may be deleted
        assert (self.test_delete_ven_resource(self.ven_token))

