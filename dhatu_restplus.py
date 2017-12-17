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
from indic_transliteration import sanscript


app = Flask(__name__)
CORS(app)
apiversion = 'v0.0.2'
api = Api(app, version=apiversion, title=u'Prakriyāpradarśinī API', description='Describes step by step verb form generation according to Paninian grammar.')
storagedirectory = '/var/www/html/sanskritworldflask/'
# storagedirectory = '/var/www/html/prakriya/'


@api.route('/' + apiversion + '/input/<string:input_transliteration>/output/<string:output_transliteration>/<string:verbform>')
@api.doc(params={'verbform': 'Verb form to be examined.'})
class FullData(Resource):
    """Return the JSON data regarding verb information and derivation steps for given verb form."""

    def get(self, verbform, input_transliteration, output_transliteration):
        """Return the JSON data regarding verb information and derivation steps for given verb form.

        This function reads the pregenerated JSON files.
        If the JSON file exists, it is loaded back.
        If the file is absent, an error is thrown.
        The JSON files are created by the script at SanskritVerb repository.
        See https://github.com/drdhaval2785/SanskritVerb/blob/master/jsongenerator.sh for details.
        """
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
                        if item in ['gana', 'padadecider_id', 'padadecider_sutra', 'number', 'meaning', 'lakAra', 'input', 'it_status', 'it_sutra']:
                            # Handle wrong slp1 for chandrabindu.
                            tmp = datum[item].replace('!', '~')
                            subresult[item] = sanscript.transliterate(tmp, 'slp1', output_transliteration)
                        elif item == 'derivation':
                            pass
                        else:
                            subresult[item] = datum[item]
                    for member in datum['derivation']:
                        derivationlist.append((sanscript.transliterate(sutrainfo[member['sutra_num']].replace('!', '~'), input_transliteration, output_transliteration), sanscript.transliterate(member['sutra_num'].replace('~', '-'), input_transliteration, output_transliteration), sanscript.transliterate(','.join(member['text']).replace('!', '~'), input_transliteration, output_transliteration)))
                        # subresult.append(sanscript.transliterate(sutrainfo[member['sutra_num']] + ' (' + member['sutra_num'] + ') -> ' + ','.join(member['text']), 'slp1', output_transliteration))
                    subresult['derivation'] = derivationlist
                    result.append(subresult)
                return result
                return json.load(fin)
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/prakriya/issues.'}


@api.route('/' + apiversion + '/input/<string:input_transliteration>/output/<string:output_transliteration>/<string:verbform>/prakriya')
@api.doc(params={'verbform': 'Verb form under examination.', 'input_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis', 'output_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis'})
class GetPrakriya(Resource):
    """Return human readable derivation of a given verb form."""

    def get(self, verbform, input_transliteration, output_transliteration):
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
                        # subresult.append(sutrainfo[member['sutra_num']] + ' (' + member['sutra_num'] + ') -> ' + ','.join(member['text']))
                        subresult.append(sanscript.transliterate(sutrainfo[member['sutra_num']].replace('!', '~') + ' (' + member['sutra_num'].replace('~', '-') + ') -> ' + ','.join(member['text']).replace('!', '~'), 'slp1', output_transliteration))
                    result.append(subresult)
                return result
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


@api.route('/' + apiversion + '/input/<string:input_transliteration>/output/<string:output_transliteration>/<string:verbform>/prakriya/machine')
@api.doc(params={'verbform': 'Verb form under examination.', 'input_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis', 'output_transliteration': 'devanagari/slp1/iast/hk/wx/itrans/kolkata/velthuis'})
class GetPrakriyaMachinified(Resource):
    """Return machine readable derivation of a given verb form."""

    def get(self, verbform, input_transliteration, output_transliteration):
        """Return machine readable derivation of a given verb form.

        It is similar to the prakriya API, with only one difference.
        prakriya API is designed to be more human readable, whereas this API is more machine readable.
        In this API every step is returned as a tuple (sutra text, sutra number, state of verbform).
        e.g. ("sArvaDAtukArDaDAtukayoH", "7.3.84", "Bo+a+tas").
        c.f. 'sArvaDAtukArDaDAtukayoH (7.3.84) -> Bo+a+tas' of prakriya API.
        """
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
                    subresult = []
                    for member in datum['derivation']:
                        subresult.append((sanscript.transliterate(sutrainfo[member['sutra_num']].replace('!', '~'), input_transliteration, output_transliteration), sanscript.transliterate(member['sutra_num'].replace('~', '-'), input_transliteration, output_transliteration), sanscript.transliterate(','.join(member['text']).replace('!', '~'), input_transliteration, output_transliteration)))
                    result.append(subresult)
                return result
        else:
            return {'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


@api.route('/' + apiversion + '/<string:verbform>/<string:argument>')
@api.doc(params={'verbform': 'Verb form to be examined.', 'argument': 'See Implementation notes / docstring of GET method.'})
class SpecificInfo(Resource):
    """Return the specific sought for information of a given verb form."""

    def get(self, verbform, argument):
        """Return the specific sought for information of a given verb form.

        Valid arguments and expected output are as follows.

        "verb" - Return verb in Devanagari with accent marks.

        "verbslp" - Return the verb in SLP1 transliteration without accent marks.

        "lakara" - Return the lakAra (tense / mood) in which this form is generated.

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


def giveuris(verbform='<verbform>', webserver='https://api.sanskritworld.in', version=apiversion):
    """Give the URIs list for RESTful service."""
    uris = {'prakriya_human_readable': webserver + '/' + version + '/input/<input_transliteration>/outout/<output_transliteration>/' + verbform + '/prakriya',
            'prakriya_machine_readable': webserver + '/' + version + '/input/<input_transliteration>/outout/<output_transliteration>/' + verbform + '/prakriya/machine',
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
