
import requests
import json
import os

class VTN_program_tester():
    """VTN integration tests"""

    program_id=0
    ven_token = 'ven_token'
    bl_token = 'bl_token'

    def __init__(self, base_url):
        self.programs_baseUrl = base_url + "/programs"
        pass

    def search_all_programs(self, token):
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_programs
            response = requests.get(self.programs_baseUrl, headers=headers)
                # headers=self.ven_headers)
            # print(f"search_all_programs: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_programs(): %s\n" % e)

        return response

    def test_search_all_programs(self, token):
        print("\n################################################################")
        print(f"test_search_all_programs(): token={token}")
        response = self.search_all_programs(token)
        if response.status_code != 200:
            print(f"test_search_all_programs(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        programs  = response.json()
        if programs is not None:
            print("test_search_all_programs(): PASSED")
            return True
        else:
            print("test_search_all_programs(): FAILED. programs in None")
            return False

    def search_program_by_id(self, program_id, token):
        url = self.programs_baseUrl + '/' + str(program_id)
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_programs
            response = requests.get(url, headers = headers)
            # print(f"search_program: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_program(): %s\n" % e)

        return response

    def test_search_program_by_id(self, token):
        print("\n################################################################")
        print (f"test_search_program_by_id(): token={token}")
        response = self.search_program_by_id(self.program_id, token)
        if response.status_code != 200:
            print(f"test_search_program(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        programs  = response.json()
        if programs["ID"] == self.program_id:
            print("test_search_program(): PASSED")
            return True
        else:
            programID = programs["ID"]
            print(f"test_search_program(): FAILED, program ID {programID} does not match serach program_id [self.program_id")
            return False

    def create_program(self, token):
        program = '{ "programName": "myProgram" }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_program
            response = requests.post(self.programs_baseUrl, data=program, headers=headers)
            # print(f"create_program: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_program(): %s\n" % e)

        return response

    def test_create_program(self, token):
        print("\n################################################################")
        print (f"test_create_program(): token={token}")
        response = self.create_program(token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_create_program(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_create_program(): PASSED")
            return True

        program  = response.json()
        if program['programName'] == "myProgram":
            print("test_create_program(): PASSED")
            self.program_id = program['ID']
            return True
        else:
            print("test_create_program(): FAILED. program name does not match created program")
            return False

    def update_program(self, program_id, token):
        url = self.programs_baseUrl + '/' + str(program_id)
        program = '{ "programName": "myNewProgram" }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_program
            response = requests.put(url, data=program, headers=headers)
            # print(f"update_program: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_program(): %s\n" % e)

        return response

    def test_update_program(self, token):
        print("\n################################################################")
        print (f"test_update_program(): token={token}")
        response = self.update_program(self.program_id, token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_update_program(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_update_program(): PASSED")
            return True

        program = response.json()
        if program['programName'] == "myNewProgram":
            print("test_update_program(): PASSED")
            return True
        else:
            print("test_update_program(): FAILED. program name does not match updated program")
            return False

    def delete_program(self, program_id, token):
        url = self.programs_baseUrl + '/' + str(program_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_program
            response = requests.delete(url, headers=headers)
            # print(f"delete_program: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling delete_program(): %s\n" % e)

        return response

    def test_delete_program(self, token):
        print("\n################################################################")
        print (f"test_delete_program(): token={token}")
        response = self.delete_program(self.program_id, token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_delete_program(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_delete_program(): PASSED")
            return True

        program = response.json()
        if program['ID'] == self.program_id:
            print("test_delete_program(): PASSED")
            return True
        else:
            programID = program['ID']
            print(f"test_delete_program(): FAILED. program ID {programID} does not match {self.program_id}")
            return False

    def run_tests(self):
        # Assume server has been restarted.
        # Verify that no programs resources are available
        assert(self.test_search_all_programs(self.ven_token))
        assert(self.test_search_all_programs(self.bl_token))
        # Verify that a program resource may be created
        assert(self.test_create_program(self.ven_token))
        assert(self.test_create_program(self.bl_token))
        # Verify that the program resource created above is available
        assert(self.test_search_program_by_id(self.ven_token))
        assert(self.test_search_program_by_id(self.bl_token))
        # Verify that the program resource created above cen be updated
        assert(self.test_update_program(self.ven_token))
        assert(self.test_update_program(self.bl_token))
        # Verify that the program resource created above cen be deleted
        assert(self.test_delete_program(self.ven_token))
        assert(self.test_delete_program(self.bl_token))
