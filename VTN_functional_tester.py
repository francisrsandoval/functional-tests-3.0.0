#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import threading

import VTN_program_tester
import VTN_event_tester
import VTN_report_tester
import VTN_subscription_tester
import VTN_ven_tester
import VTN_ven_tester
from get_token import get_token

BASE_URL = "http://localhost:8080/francisrsandoval/OpenADR-3.0/1.0.0"
BASE_URL = "http://localhost:8080/pajarito/OpenADR-3.0/1.0.0"
# BASE_URL = "http://localhost:8080/oadr3/OpenADR-3.0/1.0.0"

hostName = "localhost"
serverPort = 8082

webServer=None

CALLBACK_PATH = "./callback_output"
CALLBACK_OUTPUT = CALLBACK_PATH+"/callback.json"

VEN_CLIENT_ID = 'ven_client'
VEN_CLIENT_SECRET = 999

class MyServer(BaseHTTPRequestHandler):
    """webhook calback server"""
    def do_GET(self):
        self.send_response(200)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        body = str(post_body)
        # print (f"MyServer.do_POST(): content_len={content_len} body = {body}")
        # fuss around with odd formatting
        body = body.lstrip("b'")
        body = body.lstrip('"')
        body = body.rstrip("'")
        body = body.rstrip('"')
        body = body.replace("\\","")
        # print (f"MyServer.do_POST(): body = {body}")
        parsed = json.loads(body)
        json_object = json.dumps(parsed, indent=4)
        print(f"MyServer.do_POST(): json = {json_object}")

        if not os.path.exists(CALLBACK_PATH):
            os.mkdir(CALLBACK_PATH)
        with open(CALLBACK_OUTPUT, "w") as outfile:
            outfile.write(json_object)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

def start_server():
    global webServer
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("webhook server starting http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()

def stop_server():
    global webServer
    webServer.server_close()


def VTN_test():

    tester = VTN_program_tester.VTN_program_tester(BASE_URL)
    tester.run_tests()
    tester = VTN_event_tester.VTN_event_tester(BASE_URL)
    tester.run_tests()
    tester = VTN_report_tester.VTN_report_tester(BASE_URL)
    tester.run_tests()
    tester = VTN_subscription_tester.VTN_subscription_tester(BASE_URL, CALLBACK_OUTPUT)
    tester.run_tests()
    tester = VTN_ven_tester.VTN_ven_tester(BASE_URL)
    tester.run_tests()

if __name__ == '__main__':

    # get_token(BASE_URL, VEN_CLIENT_ID, VEN_CLIENT_SECRET)

    thread = threading.Thread(target = start_server)
    thread.daemon = True
    thread.start()
    print("webhook server started")

    VTN_test()

    stop_server()
    print("webhook server stopped.")