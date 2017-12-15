#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import json
import os.path


app = Flask(__name__)


@app.route('/api/v0.0.1/<string:verbform>', methods=['GET'])
def get_full_data(verbform):
    """Return the whole data regarding given verb form.

    This function reads the pregenerated JSON files.
    The files are created by the script at SanskritVerb repository.
    See https://github.com/drdhaval2785/SanskritVerb/blob/master/jsongenerator.sh for details.
    """
    fileofinterest = 'data/json/' + verbform + '.json'
    if os.path.exists(fileofinterest):
        with open(fileofinterest, 'r') as fin:
            return jsonify(json.load(fin))
    else:
        return jsonify({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'})


@app.route('/api/v0.0.1/<string:verbform>/prakriya', methods=['GET'])
def get_prakriya(verbform):
    """Return the specific sought for information of a given verb form.

    """
    with open('data/json/' + verbform + '.json', 'r') as fin:
        verbdata = json.load(fin)
        data = verbdata['derivation']
        result = []
        for member in data:
            result.append((member['sutra_num'], ','.join(member['text'])))
        return jsonify(result)


@app.route('/api/v0.0.1/<string:verbform>/<string:argument>', methods=['GET'])
def get_meaning(verbform, argument):
    """Return the specific sought for information of a given verb form.

    """
    with open('data/json/' + verbform + '.json', 'r') as fin:
        verbdata = json.load(fin)
        return jsonify(verbdata[argument])


if __name__ == '__main__':
    app.run(debug=True)
