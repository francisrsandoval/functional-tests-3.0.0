
import requests
import json
import os

class VTN_report_tester():
    """VTN integration tests"""

    report_id=0
    ven_token = 'ven_token'
    bl_token = 'bl_token'

    def __init__(self, base_url):
        self.reports_baseUrl = base_url+"/reports"
        pass

    def search_all_reports(self, token):
        headers = {'Authorization': 'Bearer ' + token}
        try:
            # search_all_reports
            response = requests.get(self.reports_baseUrl, headers=headers)
            # print(f"search_all_reports: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_all_reports(): %s\n" % e)

        return response

    def test_search_all_reports(self, token):
        print("\n################################################################")
        print(f"test_search_all_reports(): token={token}")
        response = self.search_all_reports(token)
        if response.status_code != 200:
            print(f"test_search_all_reports(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        reports  = response.json()
        if reports is not None:
            print("test_search_all_reports(): PASSED")
            return True
        else:
            print("test_search_all_reports(): FAILED. reports is None")
            return False

    def search_report(self, report_id, token):
        url = self.reports_baseUrl + '/' + str(report_id)
        headers = {'Authorization': 'Bearer ' + token}

        try:
            # search_all_reports
            response = requests.get(url, headers = headers)
            # print(f"search_report: response.json={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling search_report(): %s\n" % e)

        return response

    def test_search_report(self, token):
        print("\n################################################################")
        print (f"test_search_report(): token={token}")
        response = self.search_report(self.report_id, token)
        if response.status_code != 200:
            print(f"test_search_report(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False

        report  = response.json()
        if report['ID'] == self.report_id:
            print("test_search_report(): PASSED")
            return True
        else:
            reportID = report['ID']
            print(f"test_search_report(): FAILED. report ID {reportID} does not match search program_id {self.report_id}")
            return False

    def create_report(self, token):
        report = '{ "programID": 0, "eventID": 0, "clientID": 0  }'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_report
            response = requests.post(self.reports_baseUrl, data=report, headers=headers)
            # print(f"create_report: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling create_report(): %s\n" % e)

        return response

    def test_create_report(self, token):
        print("\n################################################################")
        print (f"test_create_report(): token={token}")
        response = self.create_report(token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_create_report(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_create_report(): PASSED")
            return True

        report  = response.json()
        # print (f"test_create_report(): report={report}")
        if report['clientID'] == 0:
            print("test_create_report(): PASSED")
            self.report_id = report['ID']
            return True
        else:
            print("test_create_report(): FAILED. clientID does not match created report clientID")
            return False

    def update_report(self, report_id, token):
        report = '{ "programID": 0, "eventID": 0, "clientID": 99  }'
        url = self.reports_baseUrl + '/' + str(report_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}

        try:
            # create_report
            response = requests.put(url, data=report, headers=headers)
            # print(f"update_report: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling update_report(): %s\n" % e)

        return response

    def test_update_report(self, token):
        print("\n################################################################")
        print (f"test_update_report(): token={token}")
        response = self.update_report(self.report_id, token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_update_report(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_update_report(): PASSED")
            return True

        report = response.json()
        if report['clientID'] == 99:
            print("test_update_report(): PASSED")
            return True
        else:
            print("test_update_report(): FAILED. client ID does not match update report")
            return False

    def delete_report(self, report_id, token):
        url = self.reports_baseUrl + '/' + str(report_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' + token}
        try:
            # create_report
            response = requests.delete(url, headers=headers)
            # print(f"delete_report: response={response.json()}")
        except requests.exceptions.RequestException as e:
            print("Exception when calling delete_report(): %s\n" % e)

        return response

    def test_delete_report(self, token):
        print("\n################################################################")
        print (f"test_delete_report(): token={token}")
        response = self.delete_report(self.report_id, token)
        if token == self.bl_token and response.status_code != 200:
            print(f"test_delete_report(): FAILED response.status_code != 200 response.status_code={response.status_code}")
            return False
        elif token == self.ven_token and response.status_code == 403:
            print("test_delete_report(): PASSED")
            return True

        report = response.json()
        # print (f"test_delete_report(): report= {report}")
        if report['ID'] == self.report_id:
            print("test_delete_report(): PASSED")
            return True
        else:
            print("test_delete_report(): FAILED. report ID does not match deleted report")
            return False

    def run_tests(self):
        # Assume server has been restarted.
        # Verify that no reports resources are available
        assert(self.test_search_all_reports(self.ven_token))
        assert(self.test_search_all_reports(self.bl_token))
        # Verify that a report resource may be created
        assert(self.test_create_report(self.ven_token))
        # Verify that the report resource created above is available
        assert(self.test_search_report(self.ven_token))
        # Verify that the report resource created above cen be updated
        assert(self.test_update_report(self.ven_token))
        # Verify that the report resource created above cen be deleted
        assert(self.test_delete_report(self.ven_token))

        # Verify that the report resource created above cen be deleted
        assert(self.test_create_report(self.bl_token))
        assert(self.test_search_report(self.bl_token))
        assert(self.test_update_report(self.bl_token))
        assert(self.test_delete_report(self.bl_token))
