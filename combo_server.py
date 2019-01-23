import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'contrib')))

from server_source_maintainer import *
from flask import Flask, request
import argparse

app = Flask(__name__)
DEFAULT_SOURCES_JSON = 'sources.json'


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

        source = source_maintainer.get_source(project_name, project_version)
        return json.dumps(source).encode()
    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


@app.route('/add_project', methods=['POST'])
def add_project_request():
    try:
        project_name = request.values.get('project_name')
        assert project_name is not None, 'Missing project name'

        source_type = request.values.get('source_type')  # Optional

        source_maintainer.add_project(project_name, source_type)
        return 'Added project "{}" successfully'.format(project_name)

    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


@app.route('/add_version', methods=['POST'])
def add_version_request():
    try:
        # TODO: Consider that in the future this will not be received,
        # and instead this will be extracted using the version details.
        # Otherwise, we probably still want to validate it, so it will probably be cloned anyway
        project_name = request.values.get('project_name')
        assert project_name is not None, 'Missing project name'
        assert source_maintainer.project_exists(project_name), 'Project {} does not exist'.format(project_name)

        project_version = request.values.get('project_version')
        assert project_version is not None, 'Missing project version'
        VersionNumber.validate(project_version)

        version_details_str = request.values.get('version_details')
        assert version_details_str is not None, 'Missing version details'
        version_details = json.loads(version_details_str)

        source_maintainer.add_version(project_name, project_version, version_details)
        return 'Added details of version "{}" of project "{}" successfully'.format(project_version, project_name)

    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combo server arguments')
    parser.add_argument('port', help='Server port number', type=int)
    parser.add_argument('--sources-json', '-j', help='A JSON file that maps the dependencies sources',
                        nargs='?', default=DEFAULT_SOURCES_JSON)
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    source_maintainer = ServerSourceMaintainer(args.sources_json)

    app.run(port=args.port, debug=args.debug)
