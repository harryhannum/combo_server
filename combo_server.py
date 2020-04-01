import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'contrib')))

from global_source_maintainer import *
from combo_core.importer import *
from flask import Flask, request, jsonify

import argparse

app = Flask(__name__)
DEFAULT_INDEXER_JSON = 'sources_index.json'

@app.route('/get_upload_params', methods=['GET'])
def get_upload_parameters():
    try:
        project_name = request.args.get('src_type')
        assert project_name is not None, 'Missing source type'

        upload_parameters = {
            'git': ["commit_hash", "remote_url"],
            'test': ["test1", "test2"]
        }

        if (upload_parameters.has_key(project_name)):
            result_parameters = upload_parameters[project_name]
        else:
            result_parameters = [""]
        
        response = jsonify(json.dumps(result_parameters))
        return response
    
    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


@app.route('/get_available_versions', methods=['GET'])
def get_available_versions_request():
    # TODO: Get actual dictionary
    d = {
        '(Combo Core, v0.1.0)': {
            "hash": 1507179887,
            "size": 146
        },
        '(Combo Core, v0.1.1)': {
            "hash": 1507179887,
            "size": 126
        },
        '(Combo Core, v0.2.0)': {
            "hash": 1507179887,
            "size": 134
        },
        '(Combo Core, v0.3.0)': {
            "hash": 1507179887,
            "size": 112
        },
        '(Combo Core, v0.4.0)': {
            "hash": 1507179887,
            "size": 867
        },
        '(Combo Core, v0.5.0)': {
            "hash": 1507179887,
            "size": 234
        },
        '(Combo Core, v0.6.0)': {
            "hash": 1507179887,
            "size": 624
        },
        '(Combo Core, v0.7.0)': {
            "hash": 1507179887,
            "size": 765
        },
        '(Combo Core, v0.8.0)': {
            "hash": 1507179887,
            "size": 254
        },
        '(Combo Core, v0.9.0)': {
            "hash": 1507179887,
            "size": 645
        },
        '(Combo Core, v0.10.0)': {
            "hash": 1507179887,
            "size": 564
        },
        '(Combo Core, v0.11.0)': {
            "hash": 1507179887,
            "size": 435
        },
        '(Combo Core, v0.12.0)': {
            "hash": 1507179887,
            "size": 132
        },
        '(My Executable, v1.0.0)': {
            "hash": 1507179887,
            "size": 534
        },
        '(Lib A, v1.1.0)': {
            "hash": 501194260,
            "size": 654
        },
        '(Lib A, v1.5.0)': {
            "hash": 501194260,
            "size": 765
        },
        '(Lib A, v1.6.0)': {
            "hash": 501194260,
            "size": 756
        },
        '(Lib A, v1.7.0)': {
            "hash": 501194260,
            "size": 124
        },
        '(Lib A, v2.0.0)': {
            "hash": 501194260,
            "size": 433
        },
        '(Lib B, v1.2.0)': {
            "hash": 501194260,
            "size": 233
        },
        '(Lib B, v1.3.0)': {
            "hash": 501194260,
            "size": 432
        },
        '(Lib B, v1.4.0)': {
            "hash": 501194260,
            "size": 432
        }
    }

    response = jsonify(json.dumps(d))
    return response

@app.route('/get_source', methods=['GET'])
def get_source_request():
    try:
        project_name = request.args.get('project_name')
        assert project_name is not None, 'Missing project name'

        project_version = request.args.get('project_version')
        assert project_version is not None, 'Missing project version'
        VersionNumber.validate(project_version)

        source = source_maintainer.get_source(project_name, project_version)
        response = jsonify(json.dumps(source))
        return response
    
    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/add_project', methods=['POST'])
def add_project_request():
    try:
        print ('Add project activated')
        project_name = request.json['project_name']

        assert project_name is not None, 'Missing project name'

        source_type = request.values.get('source_type')  # Optional
        source_maintainer.add_project(project_name, source_type)

        response = jsonify('Added project "{}" successfully'.format(project_name))
        return response

    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


@app.route('/add_version', methods=['POST'])
def add_version_request():
    try:
        print ('Add version activated')
        version_details = request.json
        print ("version details")
        print (request.json)
        assert version_details is not None, 'Missing version details'

        details = source_maintainer.add_version(version_details)
        if details:
            return 'Added details of version "{}" of project "{}" successfully'.format(details.version, details.name)

        return 'Added version details "{}" successfully'.format(version_details)

    except BaseException as e:
        print('Failed to handle request')
        return 'Error (type {}): {}'.format(type(e), e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combo server arguments')
    parser.add_argument('port', help='Server port number', type=int)
    parser.add_argument('--sources-json', '-j', help='A JSON file that maps the dependencies sources',
                        nargs='?', default=DEFAULT_INDEXER_JSON)
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    source_maintainer = GlobalSourceMaintainer(args.sources_json)

    app.run(port=args.port, debug=args.debug)
