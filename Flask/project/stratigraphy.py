from flask import Blueprint, request, jsonify
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import json
import os
stratigraphy = Blueprint('stratigraphy', __name__)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
wellpath_url = os.path.join(SITE_ROOT, "static/project/files", "wellpath.json")
stratigraphy_url = os.path.join(SITE_ROOT, "static/project/files", "stratigraphy.json")
output_url = os.path.join(SITE_ROOT, "static/project/files", "output.json")

@stratigraphy.route('/process_save_data')
def process_save_data():
    wellpath_file = []
    stratigraphy_file = []
    new_dict = {}
    new_list = []

    with open(wellpath_url, 'r') as wellpath_file:
        # load wellpath json file
        wellpath_file = json.load(wellpath_file)
        # print(json.dumps(wellpath_file, indent = 4, sort_keys=True))

    with open(stratigraphy_url, 'r') as stratigraphy_file:
        # load stratigraphy json file
        stratigraphy_file = json.load(stratigraphy_file)
        # print(json.dumps(stratigraphy_file, indent = 4, sort_keys=True))

        # because dictionary is within a list there is a double loop
        for index in range(len(stratigraphy_file)):
            # for key in stratigraphy_file[index]:
            # if record contains 'base' under the key 'pickName'
            if 'base' in stratigraphy_file[index]['pickName']:
                # then replace the 'base' occurence with 'undifferentiated'
                stratigraphy_file[index]['pickName'] = 'undifferentiated'

            # convert feet to meters
            # stratigraphy_file[index]['pickDepth'] = format(float(stratigraphy_file[index]['pickDepth'])/3.281,".2f")
            stratigraphy_file[index]['pickDepth'] = format(int(float(stratigraphy_file[index]['pickDepth']) / 3.281))

            # iterate over second json
            for index2 in range(len(wellpath_file)):
                # if values of both jsons match (md from wellpath and pickDepth from stratigraphy)
                if int(wellpath_file[index2]['md']) == int(stratigraphy_file[index]['pickDepth']):
                    # create new pair to be added
                    md_tvd_pair = {
                        "pickName": str(stratigraphy_file[index]['pickName']),
                        "md": int(wellpath_file[index2]['md']),
                        "tvd": float(wellpath_file[index2]['tvd']),
                    }

                    new_list.append(md_tvd_pair)

    final_pair = {}
    final_list = []

    for idx, v in enumerate(new_list):
        if idx < (len(new_list) - 1):
            pickName = str(new_list[idx]['pickName'])
            md_current = int(new_list[idx]['md'])
            tvd_current = float(new_list[idx]['tvd'])
            md_next = int(new_list[idx + 1]['md'])
            tvd_next = float(new_list[idx + 1]['tvd'])

            final_pair = {
                "pickName": pickName,
                "depth": {
                    "top": {
                        "md": md_current,
                        "tvd": tvd_current,
                    },
                    "bottom": {
                        "md": md_next,
                        "tvd": tvd_next,
                    }
                }
            }

        final_list.append(final_pair)

    final_list.pop()

    # print(json.dumps(final_list, indent = 4, sort_keys=False))

    with open(output_url, 'w') as f:
        json.dump(final_list, f, indent=4, sort_keys=False)

    return jsonify({
        'message': 'Output file created',
    }), 200  # ok


@stratigraphy.route('/output')
def output():
    with open(output_url, 'r') as output_file:
        # load wellpath json file
        output_file = json.load(output_file)

    return jsonify(output_file), 200
