import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'contrib')))

from server_source_locator import *
from flask import Flask, request
app = Flask(__name__)

SOURCES_JSON = 'sources.json'

source_locator = ServerSourceLocator(SOURCES_JSON)


@app.route('/get_available_versions', methods=['GET'])
def get_available_versions_request():
    # TODO: Get actual dictionary
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

    return json.dumps(d).encode()


@app.route("/get_source", methods=['GET'])
def get_source_request():
    try:
        project_name = request.args.get('project_name')
        assert project_name is not None, "No project name"

        project_version = request.args.get('project_version')
        assert project_version is not None, "No project version"

        VersionNumber(project_version)  # Make sure version is valid

        source = source_locator.get_source(project_name, project_version)
        return json.dumps(source).encode()
    except BaseException as e:
        print('Failed to handle request')
        return "Error: " + str(e)


@app.route("/", methods=['POST'])
def handle_post_request():
    # TODO: handle post requests
    return "Post method is yet to be developed..."


if __name__ == '__main__':
    app.run()
