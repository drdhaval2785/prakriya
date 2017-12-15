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
    fileofinterest = 'data/json/' + verbform + '.json'
    if os.path.exists(fileofinterest):
        with open(fileofinterest, 'r') as fin:
            return json.dumps(json.load(fin))
    else:
        return json.dumps({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'})


def get_specific_info(verbform, argument):
    """Return the specific sought for information of a given verb form."""
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
        return json.dumps(result)


def get_prakriya(verbform):
    """Return the specific sought for information of a given verb form."""
    fileofinterest = 'data/json/' + verbform + '.json'
    if not os.path.exists('data/sutrainfo.json'):
        return json.dumps({'error': 'file data/sutrainfo.json missing. You can obtain it from https://github.com/drdhaval2785/SanskritVerb/blob/master/Data/sutrainfo.json'})
    elif os.path.exists(fileofinterest):
        with open(fileofinterest, 'r') as fin:
            verbdata = json.load(fin)
            result = []
            with open('data/sutrainfo.json', 'r') as sutrafile:
                sutrainfo = json.load(sutrafile)
            data = verbdata
            for datum in data:
                subresult = []
                for member in datum['derivation']:
                    subresult.append(sutrainfo[member['sutra_num']] + ' (' + member['sutra_num'] + ') -> ' + ','.join(member['text']))
                result.append(subresult)
            return json.dumps({'message': 'for machine friendly output, use /api/v0.0.1/verbform/prakriya/jsonified', 'result': result}, indent=4)
    else:
        return json.dumps({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'})


def get_prakriya_jsonified(verbform):
    """Return the specific sought for information of a given verb form."""
    fileofinterest = 'data/json/' + verbform + '.json'
    if not os.path.exists('data/sutrainfo.json'):
        return json.dumps({'error': 'file data/sutrainfo.json missing. You can obtain it from https://github.com/drdhaval2785/SanskritVerb/blob/master/Data/sutrainfo.json'})
    elif os.path.exists(fileofinterest):
        with open(fileofinterest, 'r') as fin:
            verbdata = json.load(fin)
            result = []
            with open('data/sutrainfo.json', 'r') as sutrafile:
                sutrainfo = json.load(sutrafile)
            data = verbdata
            for datum in data:
                subresult = []
                for member in datum['derivation']:
                    subresult.append((sutrainfo[member['sutra_num']], member['sutra_num'], ','.join(member['text'])))
                result.append(subresult)
            return json.dumps({'message': 'for human readable output, use `python prakriya.py verbform prakriya`', 'result': result}, indent=4)
    else:
        return json.dumps({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'})


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
    print(timestamp())
    syslen = len(sys.argv)
    if syslen < 2 or syslen > 4:
        print json.dumps({'error': 'Kindly use the following syntax. `python prakriya.py verbform [argument] [readability]`.'})
        exit(0)
    elif syslen == 4 and not sys.argv[3] == 'machine':
        print json.dumps({'error': 'The third argument can only be `machine`.'})
        exit(0)

    if syslen >= 2:
        verbform = sys.argv[1]
    if syslen >= 3:
        argument = sys.argv[2]
    if syslen == 4:
        readability = sys.argv[3]

    if syslen == 4 and readability == 'machine':
        print(get_prakriya_jsonified(verbform))
    elif syslen == 3 and argument == 'prakriya':
        print(get_prakriya(verbform))
    elif syslen == 3:
        print(get_specific_info(verbform, argument))
    elif syslen == 2:
        print(get_full_data(verbform))
    print(timestamp())
