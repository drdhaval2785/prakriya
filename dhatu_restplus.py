#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a web service for verb form derivation.

See api.sanskritworld.in for documentation.
Author - Dr. Dhaval Patel
Date - 16 December 2017
email - drdhaval2785@gmail.com
"""
from flask import Flask, jsonify
from flask_restplus import Api, Resource, reqparse
from flask_cors import CORS
import os
import json
from indic_transliteration import sanscript


app = Flask(__name__)
CORS(app)
apiversion = 'v0.0.2'
api = Api(app, version=apiversion, title=u'Prakriyāpradarśinī API', description='Describes step by step verb form generation according to Paninian grammar. Please report any issues <a href="https://github.com/drdhaval2785/prakriya/issues">here</a>. For more details, please see the github projects for <a href="https://github.com/drdhaval2785/SanskritVerb">SanskritVerb</a> and <a href="https://github.com/drdhaval2785/prakriya">prakriya</a>.')
storagedirectory = '/var/www/html/sanskritworldflask/'


@api.route('/' + apiversion + '/verbforms/<string:input_transliteration>/<string:verbform>')
@api.doc(params={'verbform': 'Verb form to be examined.', 'input_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis'})
class FullData(Resource):
    """Return the JSON data regarding verb information and derivation steps for given verb form."""

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('output_transliteration', location='args', default='devanagari', help='devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis')

    @api.expect(get_parser, validate=True)
    def get(self, input_transliteration, verbform):
        """Return the verb information and derivation steps for given verb form.

        This function reads the pregenerated JSON files.
        If the JSON file exists, it is loaded back.
        If the file is absent, an error is thrown.
        The JSON files are created by the script at SanskritVerb repository.
        See https://github.com/drdhaval2785/SanskritVerb/blob/master/jsongenerator.sh for details.
        """
        output_transliteration = self.get_parser.parse_args()['output_transliteration']
        if input_transliteration not in ['devanagari', 'slp1', 'iast', 'hk', 'wx', 'itrans', 'kolkata', 'velthuis']:
            return {'error': 'input_transliteration can only take specified values. Check again.'}
        if output_transliteration not in ['devanagari', 'slp1', 'iast', 'hk', 'wx', 'itrans', 'kolkata', 'velthuis']:
            return {'error': 'output_transliteration can only take specified values. Check again.'}
        verbform = sanscript.transliterate(verbform, input_transliteration, 'slp1')
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
                    subresult = {}
                    derivationlist = []
                    for item in datum:
                        if item in ['gana', 'padadecider_id', 'padadecider_sutra', 'number', 'meaning', 'lakAra', 'input', 'it_status', 'it_sutra', 'purusha', 'vachana', 'upasarga', 'suffix']:
                            tmp = datum[item]
                            if item == 'input':
                                tmp = tmp.replace('!', '~')
                            subresult[reversemaparguments(item)] = sanscript.transliterate(tmp, 'slp1', output_transliteration)
                        elif item == 'derivation':
                            pass
                        else:
                            subresult[reversemaparguments(item)] = datum[item]
                    for member in datum['derivation']:
                        sutratext = sanscript.transliterate(sutrainfo[member['sutra_num']], 'slp1', output_transliteration)
                        sutranum = sanscript.transliterate(member['sutra_num'].replace('~', '-'), 'slp1', output_transliteration)
                        form = sanscript.transliterate(member['text'].replace('@', 'u~'), 'slp1', output_transliteration)
                        derivationlist.append({'sutra': sutratext, 'sutra_num': sutranum, 'form': form})
                    subresult['derivation'] = derivationlist
                    result.append(subresult)
                return jsonify(result)
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/prakriya/issues.'}


@api.route('/' + apiversion + '/verbforms/<string:input_transliteration>/<string:verbform>/prakriya')
@api.doc(params={'verbform': 'Verb form to be examined.', 'input_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis'})
class GetPrakriya(Resource):
    """Return human readable derivation of a given verb form."""

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('output_transliteration', location='args', default='devanagari', help='devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis')

    @api.expect(get_parser, validate=True)
    def get(self, verbform, input_transliteration):
        """Return human readable derivation of a given verb form.

        This function converts the derivation data into human readable form.
        Typical line is 'Paninian rule (rule number) -> state of the verb form'.
        e.g. 'sArvaDAtukArDaDAtukayoH (7.3.84) -> Bo+a+tas'.

        Dependencies

        This function has a dependency on sutrainfo.json.
        sutrainfo.json has sutra number, sutra text key value pairs.
        The data stored in JSON does not have sutra text. it only has sutra number.
        sutra text is supplied from sutrainfo.json.
        See https://github.com/drdhaval2785/prakriya/blob/master/data/sutrainfo.json.
        """
        output_transliteration = self.get_parser.parse_args()['output_transliteration']
        if input_transliteration not in ['devanagari', 'slp1', 'iast', 'hk', 'wx', 'itrans', 'kolkata', 'velthuis']:
            return {'error': 'input_transliteration can only take specified values. Check again.'}
        if output_transliteration not in ['devanagari', 'slp1', 'iast', 'hk', 'wx', 'itrans', 'kolkata', 'velthuis']:
            return {'error': 'output_transliteration can only take specified values. Check again.'}
        verbform = sanscript.transliterate(verbform, input_transliteration, 'slp1')
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
                        sutratext = sanscript.transliterate(sutrainfo[member['sutra_num']], 'slp1', output_transliteration)
                        sutranum = sanscript.transliterate(member['sutra_num'].replace('~', '-'), 'slp1', output_transliteration)
                        form = sanscript.transliterate(member['text'].replace('@', 'u~'), 'slp1', output_transliteration)
                        subresult.append({'sutra': sutratext, 'sutra_num': sutranum, 'form': form})
                    result.append(subresult)
                return jsonify(result)
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/prakriya/issues.'}


@api.route('/' + apiversion + '/verbforms/<string:input_transliteration>/<string:verbform>/<string:argument>')
@api.doc(params={'verbform': 'Verb form to be examined.', 'argument': 'See Implementation notes / docstring of GET method.', 'input_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis'})
class SpecificInfo(Resource):
    """Return the specific sought for information of a given verb form."""

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('output_transliteration', location='args', default='devanagari', help='devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis')

    @api.expect(get_parser, validate=True)
    def get(self, verbform, argument, input_transliteration):
        """Return the specific sought for information of a given verb form.

        Valid arguments and expected output are as follows.

        "verb" - Return verb in Devanagari with accent marks.

        "verbslp" - Return the verb in SLP1 transliteration without accent marks.

        "lakara" - Return the lakAra (tense / mood) in which this form is generated.

        "purusha" - Return the purusha in which this form is generated.

        "suffix" - Return the suffix by which this form is generated.

        "vachana" - Return the vachana in which this form is generated.

        "gana" - Return the gaNa (class) of the verb.

        "meaning" - Return meaning of the verb in SLP1 transliteration.

        "number" - Return number of the verb in dhAtupATha.

        "madhaviya" - Return link to mAdhaviyadhAtuvRtti. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        "kshiratarangini" - Return link to kSIrataraGgiNI. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        "dhatupradipa" - Return link to dhAtupradIpa. http://sanskrit.uohyd.ac.in/scl/dhaatupaatha is the home page.

        "jnu" - Return link to JNU site for this verb form. http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp is the home page.

        "uohyd" - Return link to UoHyd site for this verb form. http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi is the home page.

        "upasarga" - Return upasarga, if any. Currently we do not support verb forms with upasargas.

        "padadecider_id" - Return the rule number which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

        "padadecider_sutra" - Return the rule text which decides whether the verb is parasmaipadI, AtmanepadI or ubhayapadI.

        "it_id" - Returns whether the verb is seT, aniT or veT, provided the form has iDAgama.

        "it_status" - Returns whether the verb form has iDAgama or not. seT, veT, aniT are the output.

        "it_sutra" - Returns rule number if iDAgama is caused by some special rule.
        """
        output_transliteration = self.get_parser.parse_args()['output_transliteration']
        verbform = sanscript.transliterate(verbform, input_transliteration, 'slp1')
        fileofinterest = filepath(verbform)
        validargs = ['jnu', 'uohyd', 'dhatupradipa', 'it_id', 'it_status', 'it_sutra', 'kshiratarangini', 'lakara', 'madhaviya', 'padadecider_id', 'padadecider_sutra', 'upasarga', 'verb', 'gana', 'meaning', 'number', 'verbslp', 'purusha', 'vachana', 'upasarga', 'suffix']
        if argument not in validargs:
            return {'error': 'argument is invalid. It can take only "jnu", "uohyd", "dhatupradipa", "it_id", "it_status", "it_sutra", "kshiratarangini", "lakara", "madhaviya", "padadecider_id", "padadecider_sutra", "upasarga", "verb", "gana", "meaning", "number", "verbslp", "purusha", "vachana", "upasarga", "suffix" values.'}
        argument = maparguments(argument)
        with open(fileofinterest, 'r') as fin:
            verbdata = json.load(fin)
            tmp = []
            for datum in verbdata:
                item = datum[argument]
                if argument in ['gana', 'padadecider_id', 'padadecider_sutra', 'number', 'meaning', 'lakAra', 'input', 'it_status', 'it_sutra', 'purusha', 'vachana', 'upasarga', 'suffix']:
                    if argument == 'input':
                        item = item.replace('!', '~')
                    tmp.append(sanscript.transliterate(item, 'slp1', output_transliteration))
                else:
                    tmp.append(item)
            result = []
            for member in tmp:
                if member not in result:
                    result.append(member)
            return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    """Give URIs if app hits 404."""
    uris = giveuris()
    return jsonify({'uris': uris, 'error': 'Use any of the URIs given below.'})


def filepath(verbform):
    """Return absolute path of file on server."""
    global storagedirectory
    return storagedirectory + 'data/json/' + verbform + '.json'


def giveuris(verbform='<verbform>', webserver='https://api.sanskritworld.in', version=apiversion):
    """Give the URIs list for RESTful service."""
    uris = {'prakriya_human_readable': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/prakriya?output_transliteration=<output_transliteration>',
            'prakriya_machine_readable': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/prakriya/machine?output_transliteration=<output_transliteration>',
            'verb_devanagari': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/verb?output_transliteration=<output_transliteration>',
            'verb_meaning': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/meaning?output_transliteration=<output_transliteration>',
            'verb_number': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/number?output_transliteration=<output_transliteration>',
            'verb_gana': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/gana?output_transliteration=<output_transliteration>',
            'purusha': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/purusha?output_transliteration=<output_transliteration>',
            'vachana': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/vachana?output_transliteration=<output_transliteration>',
            'suffix': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/suffix?output_transliteration=<output_transliteration>',
            'madhaviyadhatuvritti_link': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/madhaviya?output_transliteration=<output_transliteration>',
            'kshiratarangini_link': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/kshiratarangini?output_transliteration=<output_transliteration>',
            'dhatupradipa_link': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/dhatupradipa?output_transliteration=<output_transliteration>',
            'UoHyd_link': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/uohyd?output_transliteration=<output_transliteration>',
            'JNU_link': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/jnu?output_transliteration=<output_transliteration>',
            'verb_slp': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/verbslp?output_transliteration=<output_transliteration>',
            'lakAra_or_tense': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/lakara?output_transliteration=<output_transliteration>',
            'upasarga': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/upasarga?output_transliteration=<output_transliteration>',
            'padadecider_id': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/padadecider_id?output_transliteration=<output_transliteration>',
            'padadecider_sutra': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/padadecider_sutra?output_transliteration=<output_transliteration>',
            'it_sutra': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/it_sutra?output_transliteration=<output_transliteration>',
            'it_id': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/it_id?output_transliteration=<output_transliteration>',
            'it_status': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '/it_status?output_transliteration=<output_transliteration>',
            'all_details': webserver + '/' + version + '/verbforms/<input_transliteration>/' + verbform + '?output_transliteration=<output_transliteration>',
            }
    return uris


def maparguments(argument):
    """Map api friendly arguments to actual JSON keys."""
    mapapi = {'madhaviya': 'mAdhavIya',
              'kshiratarangini': 'kzIratarangiNI',
              'dhatupradipa': 'dhAtupradIpa',
              'uohyd': 'UoHyd',
              'verbslp': 'input',
              'lakara': 'lakAra',
              }
    if argument in mapapi:
        return mapapi[argument]
    else:
        return argument


def reversemaparguments(jsonkey):
    """Reversemap json keys to arguments of API."""
    reversemapapi = {'mAdhavIya': 'madhaviya',
                     'kzIratarangiNI': 'kshiratarangini',
                     'dhAtupradIpa': 'dhatupradipa',
                     'UoHyd': 'uohyd',
                     'input': 'verbslp',
                     'lakAra': 'lakara',
                     }
    if jsonkey in reversemapapi:
        return reversemapapi[jsonkey]
    else:
        return jsonkey


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
