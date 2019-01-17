import argparse
import socket
import threading
import struct
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'contrib')))

from server_source_locator import *
from flask import Flask, request
app = Flask(__name__)

SOURCES_JSON = 'sources.json'

source_locator = ServerSourceLocator(SOURCES_JSON)

def full_json():
    d = {
        "(Core Library, v2.1)": {
            "hash": 1507179887,
            "size": 126
        },
        "(Lib A, v1.7)": {
            "hash": 501194260,
            "size": 229
        },
        "(Lib B, v1.4)": {
            "hash": 1555234999,
            "size": 221
        }
    }

    return json.dumps(d)

@app.route("/", methods=['POST', 'GET'])
def handle_client_request():
    REQUEST_TYPE_GET_SOURCE = "get_source"
    if request.method == 'POST':
        # Todo: handle post requests
        return "Post method is yet to be developed..."

    elif request.method == 'GET':
        #handling GET requests
        try:
            request_type = request.args.get('request_type')
            assert request_type != None, "No request type"

            if request_type == REQUEST_TYPE_GET_SOURCE:
                project_name = request.args.get('project_name')
                assert project_name != None, "No project name"

                project_version = request.args.get('project_version')
                assert project_version != None, "No project version"

                VersionNumber(project_version) # Make sure version is valid

                source = source_locator.get_source(project_name, project_version)
                return source.as_dict().encode()
            else:
                return "Request type is not yet supported..."
        except BaseException as e:
            print('Failed to handle request')
            return "error : "+ str(e)
    
if __name__ == '__main__':
    #main()
    app.run()
