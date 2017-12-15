#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import json
import sys
import datetime


def timestamp():
    """Return timestamp."""
    return datetime.datetime.now()


def get_full_data(verbform):
    """Return the whole data regarding given verb form.

    This function reads the pregenerated JSON files.
    The files are created by the script at SanskritVerb repository.
    See https://github.com/drdhaval2785/SanskritVerb/blob/master/jsongenerator.sh for details.
    """
    uris = giveuris(verbform)
    fileofinterest = 'data/json/' + verbform + '.json'
    if os.path.exists(fileofinterest):
        with open(fileofinterest, 'r') as fin:
            return json.dumps({'uris': uris, 'result': json.load(fin)})
    else:
        return json.dumps({'uris': uris, 'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'})


def get_specific_info(verbform, argument):
    """Return the specific sought for information of a given verb form."""
    uris = giveuris(verbform)
    with open('data/json/' + verbform + '.json', 'r') as fin:
        verbdata = json.load(fin)
        tmp = []
        for datum in verbdata:
            arg = maparguments(argument)
            tmp.append(datum[arg])
        result = []
        for member in tmp:
            if member not in result:
                result.append(member)
        return json.dumps({'uris': uris, 'result': result})


def giveuris(verbform='<verbform>', webserver='127.0.0.1:5000', version='v0.0.1'):
    """Give the URIs list for RESTful service."""
    uris = {'prakriya_human_readable': webserver + '/api/' + version + '/' + verbform + '/prakriya',
            'prakriya_machine_readable': webserver + '/api/' + version + '/' + verbform + '/prakriya/machine',
            'verb_devanagari': webserver + '/api/' + version + '/' + verbform + '/verb',
            'verb_meaning': webserver + '/api/' + version + '/' + verbform + '/meaning',
            'verb_number': webserver + '/api/' + version + '/' + verbform + '/number',
            'verb_gana': webserver + '/api/' + version + '/' + verbform + '/gana',
            'madhaviyadhatuvritti_link': webserver + '/api/' + version + '/' + verbform + '/madhaviya',
            'kshiratarangini_link': webserver + '/api/' + version + '/' + verbform + '/kshiratarangini',
            'dhatupradipa_link': webserver + '/api/' + version + '/' + verbform + '/dhatupradipa',
            'UoHyd_link': webserver + '/api/' + version + '/' + verbform + '/uohyd',
            'JNU_link': webserver + '/api/' + version + '/' + verbform + '/jnu',
            'verb_slp': webserver + '/api/' + version + '/' + verbform + '/verbslp',
            'lakAra_or_tense': webserver + '/api/' + version + '/' + verbform + '/lakara',
            'upasarga': webserver + '/api/' + version + '/' + verbform + '/upasarga',
            'padadecider_id': webserver + '/api/' + version + '/' + verbform + '/padadecider_id',
            'padadecider_sutra': webserver + '/api/' + version + '/' + verbform + '/padadecider_sutra',
            'it_sutra': webserver + '/api/' + version + '/' + verbform + '/it_sutra',
            'it_id': webserver + '/api/' + version + '/' + verbform + '/it_id',
            'it_status': webserver + '/api/' + version + '/' + verbform + '/it_status',
            'all_details': webserver + '/api/' + version + '/' + verbform,
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
    # uris = giveuris()
    print(timestamp())
    syslen = len(sys.argv)
    if syslen >= 2:
        verbform = sys.argv[1]
    if syslen >= 3:
        argument = sys.argv[2]
    if syslen >= 4:
        readability = sys.argv[3]
    if syslen < 2:
        print json.dumps({'error': 'Kindly use the following syntax. `python prakriya.py verbform [argument] [readability]`.'})
        exit(0)
    # print(get_full_data(verbform))
    print(get_specific_info(verbform, argument))
    print(timestamp())
