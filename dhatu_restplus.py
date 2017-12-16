#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a web service for verb form derivation.

See api.sanskritworld.in for documentation.
Author - Dr. Dhaval Patel
Date - 16 December 2017
email - drdhaval2785@gmail.com
"""
from flask import Flask, jsonify
from flask_restplus import Api, Resource
from flask_cors import CORS
import os
import json


app = Flask(__name__)
CORS(app)
apiversion = 'v0.0.1'
api = Api(app, version=apiversion, title=u'Prakriyāpradarśinī API', description='Describes step by step verb form generation according to Paninian grammar.')
storagedirectory = '/var/www/html/sanskritworldflask/'
# storagedirectory = '/var/www/html/prakriya/'


@api.route('/' + apiversion + '/<string:verbform>')
class FullData(Resource):
    """Return the whole data regarding given verb form.

    This function reads the pregenerated JSON files.
    The files are created by the script at SanskritVerb repository.
    See https://github.com/drdhaval2785/SanskritVerb/blob/master/jsongenerator.sh for details.
    """

    def get(self, verbform):
        """Return the whole data regarding given verb form."""
        uris = giveuris(verbform)
        fileofinterest = filepath(verbform)
        if os.path.exists(fileofinterest):
            with open(fileofinterest, 'r') as fin:
                return json.load(fin)
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


@api.route('/' + apiversion + '/<string:verbform>/prakriya')
class GetPrakriya(Resource):
    """Return human readable derivation of a given verb form."""

    def get(self, verbform):
        """Return human readable derivation of a given verb form."""
        fileofinterest = filepath(verbform)
        uris = giveuris(verbform)
        if not os.path.exists(storagedirectory + 'data/sutrainfo.json'):
            return {'error': 'file data/sutrainfo.json missing. You can obtain it from https://github.com/drdhaval2785/SanskritVerb/blob/master/Data/sutrainfo.json'}
        elif os.path.exists(fileofinterest):
            with open(fileofinterest, 'r') as fin:
                verbdata = json.load(fin)
                result = []
                with open(storagedirectory + 'data/sutrainfo.json', 'r') as sutrafile:
                    sutrainfo = json.load(sutrafile)
                data = verbdata
                for datum in data:
                    subresult = []
                    for member in datum['derivation']:
                        subresult.append(sutrainfo[member['sutra_num']] + ' (' + member['sutra_num'] + ') -> ' + ','.join(member['text']))
                    result.append(subresult)
                return result
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


@api.route('/' + apiversion + '/<string:verbform>/prakriya/machine')
class GetPrakriyaMachinified(Resource):
    """Return machine readable derivation of a given verb form."""

    def get(self, verbform):
        """Return machine readable derivation of a given verb form."""
        uris = giveuris(verbform)
        fileofinterest = filepath(verbform)
        if not os.path.exists(storagedirectory + 'data/sutrainfo.json'):
            return {'error': 'file data/sutrainfo.json missing. You can obtain it from https://github.com/drdhaval2785/SanskritVerb/blob/master/Data/sutrainfo.json'}
        elif os.path.exists(fileofinterest):
            with open(fileofinterest, 'r') as fin:
                verbdata = json.load(fin)
                result = []
                with open(storagedirectory + 'data/sutrainfo.json', 'r') as sutrafile:
                    sutrainfo = json.load(sutrafile)
                data = verbdata
                for datum in data:
                    subresult = []
                    for member in datum['derivation']:
                        subresult.append((sutrainfo[member['sutra_num']], member['sutra_num'], ','.join(member['text'])))
                    result.append(subresult)
                return result
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


@api.route('/' + apiversion + '/<string:verbform>/<string:argument>')
class SpecificInfo(Resource):
    """Return the specific sought for information of a given verb form."""

    def get(self, verbform, argument):
        """Return the specific sought for information of a given verb form.

        Valid arguments are "jnu", "uohyd", "dhatupradipa", "it_id", "it_status", "it_sutra", "kshiratarangini", "lakara", "madhaviya", "padadecider_id", "padadecider_sutra", "upasarga", "verb", "gana", "meaning", "number", "verbslp".
        """
        fileofinterest = filepath(verbform)
        validargs = ['jnu', 'uohyd', 'dhatupradipa', 'it_id', 'it_status', 'it_sutra', 'kshiratarangini', 'lakara', 'madhaviya', 'padadecider_id', 'padadecider_sutra', 'upasarga', 'verb', 'gana', 'meaning', 'number', 'verbslp']
        if argument not in validargs:
            return {'error': 'argument is invalid. It can take only "jnu", "uohyd", "dhatupradipa", "it_id", "it_status", "it_sutra", "kshiratarangini", "lakara", "madhaviya", "padadecider_id", "padadecider_sutra", "upasarga", "verb", "gana", "meaning", "number", "verbslp" values.'}
        with open(fileofinterest, 'r') as fin:
            verbdata = json.load(fin)
            tmp = []
            for datum in verbdata:
                arg = maparguments(argument)
                tmp.append(datum[arg])
            result = []
            for member in tmp:
                if member not in result:
                    result.append(member)
            return result


@app.errorhandler(404)
def not_found(error):
    """Give URIs if app hits 404."""
    uris = giveuris()
    return jsonify({'uris': uris, 'error': 'Use any of the URIs given below.'})


def filepath(verbform):
    """Return absolute path of file on server."""
    global storagedirectory
    return storagedirectory + 'data/json/' + verbform + '.json'


def giveuris(verbform='<verbform>', webserver='api.sanskritworld.in', version=apiversion):
    """Give the URIs list for RESTful service."""
    uris = {'prakriya_human_readable': webserver + '/' + version + '/' + verbform + '/prakriya',
            'prakriya_machine_readable': webserver + '/' + version + '/' + verbform + '/prakriya/machine',
            'verb_devanagari': webserver + '/' + version + '/' + verbform + '/verb',
            'verb_meaning': webserver + '/' + version + '/' + verbform + '/meaning',
            'verb_number': webserver + '/' + version + '/' + verbform + '/number',
            'verb_gana': webserver + '/' + version + '/' + verbform + '/gana',
            'madhaviyadhatuvritti_link': webserver + '/' + version + '/' + verbform + '/madhaviya',
            'kshiratarangini_link': webserver + '/' + version + '/' + verbform + '/kshiratarangini',
            'dhatupradipa_link': webserver + '/' + version + '/' + verbform + '/dhatupradipa',
            'UoHyd_link': webserver + '/' + version + '/' + verbform + '/uohyd',
            'JNU_link': webserver + '/' + version + '/' + verbform + '/jnu',
            'verb_slp': webserver + '/' + version + '/' + verbform + '/verbslp',
            'lakAra_or_tense': webserver + '/' + version + '/' + verbform + '/lakara',
            'upasarga': webserver + '/' + version + '/' + verbform + '/upasarga',
            'padadecider_id': webserver + '/' + version + '/' + verbform + '/padadecider_id',
            'padadecider_sutra': webserver + '/' + version + '/' + verbform + '/padadecider_sutra',
            'it_sutra': webserver + '/' + version + '/' + verbform + '/it_sutra',
            'it_id': webserver + '/' + version + '/' + verbform + '/it_id',
            'it_status': webserver + '/' + version + '/' + verbform + '/it_status',
            'all_details': webserver + '/' + version + '/' + verbform,
            }
    return uris


def maparguments(argument):
    """Map api friendly arguments to actual JSON keys."""
    mapapi = {'verb': 'verb',
              'meaning': 'meaning',
              'number': 'number',
              'gana': 'gana',
              'madhaviya': 'mAdhavIya',
              'kshiratarangini': 'kzIratarangiNI',
              'dhatupradipa': 'dhAtupradIpa',
              'uohyd': 'UoHyd',
              'jnu': 'jnu',
              'verbslp': 'input',
              'lakara': 'lakAra',
              'upasarga': 'upasarga',
              'padadecider_id': 'padadecider_id',
              'padadecider_sutra': 'padadecider_sutra',
              'it_id': 'it_id',
              'it_sutra': 'it_sutra',
              'it_status': 'it_status'
              }
    return mapapi[argument]


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
