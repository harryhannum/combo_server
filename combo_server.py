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
        '(Core Library, v2.1)': {
            "hash": 1507179887,
            "size": 126
        },
        '(Lib A, v1.7)': {
            "hash": 501194260,
            "size": 229
        },
        '(Lib B, v1.4)': {
            "hash": 1555234999,
            "size": 221
        }
    }

    return json.dumps(d).encode()


@app.route('/get_source', methods=['GET'])
def get_source_request():
    try:
        project_name = request.args.get('project_name')
        assert project_name is not None, 'Missing project name'

        project_version = request.args.get('project_version')
        assert project_version is not None, 'Missing project version'
        VersionNumber.validate(project_version)

        source = source_locator.get_source(project_name, project_version)
        return json.dumps(source).encode()
    except BaseException as e:
        print('Failed to handle request')
        return 'Error: ' + str(e)


@app.route('/add_project', methods=['POST'])
def add_project_request():
    try:
        project_name = request.args.get('project_name')
        assert project_name is not None, 'Missing project name'

        # TODO: Actually add the project
        return 'Adding project named "{}"'.format(project_name)
    except BaseException as e:
        print('Failed to handle request')
        return 'Error: ' + str(e)


@app.route('/add_version', methods=['POST'])
def add_version_request():
    try:
        project_name = request.args.get('project_name')
        assert project_name is not None, 'Missing project name'
        assert source_locator.project_exists(project_name), 'Project {} does not exist'.format(project_name)

        project_version = request.args.get('project_version')
        assert project_version is not None, 'Missing project version'
        VersionNumber.validate(project_version)

        # TODO: Actually add the version, and also request source parameters (dictionary)
        return 'Adding version "{}" for project "{}"'.format(project_version, project_name)
    except BaseException as e:
        print('Failed to handle request')
        return 'Error: ' + str(e)


if __name__ == '__main__':
    app.run()
