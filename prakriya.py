#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form.

Example
-------
python prakriya.py verbform [argument] [readability]
"""
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
            return json.load(fin)
    else:
        return {'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


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
        return result


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
            return result
    else:
        return {'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


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
            return result
    else:
        return {'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}


class prakriya():
    """Generate a prakriya class.

    Example
    -------
    >>> from prakriya import prakriya
    >>> d = prakriya()
    >>> d['gacCati']
    [[u'BUvAdayo DAtavaH (1.3.1) -> gamx!', u"upadeSe'janunAsika it (1.3.2) -> gamx!", u'tasya lopaH (1.3.9) -> gam', u'laH karmaRi ca BAve cAkarmakeByaH. (3.4.69) -> gam', u'vartamAne law (3.2.123) -> gam+la!w', u'lasya (3.4.77) -> gam+la!w', u'halantyam (1.3.3) -> gam+la!w', u'tasya lopaH (1.3.9) -> gam+la!', u"upadeSe'janunAsika it (1.3.2) -> gam+la!", u'tasya lopaH (1.3.9) -> gam+l', u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN (3.4.78) -> gam+tip', u'laH parasmEpadam (1.4.99) -> gam+tip', u'tiNastrIRi trIRi praTamamaDyamottamAH (1.4.101) -> gam+tip', u'tAnyekavacanadvivacanabahuvacanAnyekaSaH (1.4.102) -> gam+tip', u'Seze praTamaH (1.4.108) -> gam+tip', u'tiNSitsArvaDAtukam (3.4.113) -> gam+tip', u'kartari Sap\u200c (3.1.68) -> gam+Sap+tip', u'izugamiyamAM CaH (7.3.77) -> gaC+Sap+tip', u'tiNSitsArvaDAtukam (3.4.113) -> gaC+Sap+tip', u'laSakvatadDite (1.3.8) -> gaC+Sap+tip', u'tasya lopaH (1.3.9) -> gaC+ap+tip', u'halantyam (1.3.3) -> gaC+ap+tip', u'tasya lopaH (1.3.9) -> gaC+a+ti', u'Ce ca (6.1.73) -> gatC+a+ti', u'stoH ScunA ScuH (8.4.40) -> gacC+a+ti', u'Final form (~2) -> gacCati']]
    >>> d['gacCati', 'verbslp']
    [u'gamx!']
    >>> d['gacCati', 'prakriya']
    [[u'BUvAdayo DAtavaH (1.3.1) -> gamx!', u"upadeSe'janunAsika it (1.3.2) -> gamx!", u'tasya lopaH (1.3.9) -> gam', u'laH karmaRi ca BAve cAkarmakeByaH. (3.4.69) -> gam', u'vartamAne law (3.2.123) -> gam+la!w', u'lasya (3.4.77) -> gam+la!w', u'halantyam (1.3.3) -> gam+la!w', u'tasya lopaH (1.3.9) -> gam+la!', u"upadeSe'janunAsika it (1.3.2) -> gam+la!", u'tasya lopaH (1.3.9) -> gam+l', u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN (3.4.78) -> gam+tip', u'laH parasmEpadam (1.4.99) -> gam+tip', u'tiNastrIRi trIRi praTamamaDyamottamAH (1.4.101) -> gam+tip', u'tAnyekavacanadvivacanabahuvacanAnyekaSaH (1.4.102) -> gam+tip', u'Seze praTamaH (1.4.108) -> gam+tip', u'tiNSitsArvaDAtukam (3.4.113) -> gam+tip', u'kartari Sap\u200c (3.1.68) -> gam+Sap+tip', u'izugamiyamAM CaH (7.3.77) -> gaC+Sap+tip', u'tiNSitsArvaDAtukam (3.4.113) -> gaC+Sap+tip', u'laSakvatadDite (1.3.8) -> gaC+Sap+tip', u'tasya lopaH (1.3.9) -> gaC+ap+tip', u'halantyam (1.3.3) -> gaC+ap+tip', u'tasya lopaH (1.3.9) -> gaC+a+ti', u'Ce ca (6.1.73) -> gatC+a+ti', u'stoH ScunA ScuH (8.4.40) -> gacC+a+ti', u'Final form (~2) -> gacCati']]
    >>> d['gacCati', 'prakriya', 'machine']
    [[(u'BUvAdayo DAtavaH', u'1.3.1', u'gamx!'), (u"upadeSe'janunAsika it", u'1.3.2', u'gamx!'), (u'tasya lopaH', u'1.3.9', u'gam'), (u'laH karmaRi ca BAve cAkarmakeByaH.', u'3.4.69', u'gam'), (u'vartamAne law', u'3.2.123', u'gam+la!w'), (u'lasya', u'3.4.77', u'gam+la!w'), (u'halantyam', u'1.3.3', u'gam+la!w'), (u'tasya lopaH', u'1.3.9', u'gam+la!'), (u"upadeSe'janunAsika it", u'1.3.2', u'gam+la!'), (u'tasya lopaH', u'1.3.9', u'gam+l'), (u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', u'3.4.78', u'gam+tip'), (u'laH parasmEpadam', u'1.4.99', u'gam+tip'), (u'tiNastrIRi trIRi praTamamaDyamottamAH', u'1.4.101', u'gam+tip'), (u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', u'1.4.102', u'gam+tip'), (u'Seze praTamaH', u'1.4.108', u'gam+tip'), (u'tiNSitsArvaDAtukam', u'3.4.113', u'gam+tip'), (u'kartari Sap\u200c', u'3.1.68', u'gam+Sap+tip'), (u'izugamiyamAM CaH', u'7.3.77', u'gaC+Sap+tip'), (u'tiNSitsArvaDAtukam', u'3.4.113', u'gaC+Sap+tip'), (u'laSakvatadDite', u'1.3.8', u'gaC+Sap+tip'), (u'tasya lopaH', u'1.3.9', u'gaC+ap+tip'), (u'halantyam', u'1.3.3', u'gaC+ap+tip'), (u'tasya lopaH', u'1.3.9', u'gaC+a+ti'), (u'Ce ca', u'6.1.73', u'gatC+a+ti'), (u'stoH ScunA ScuH', u'8.4.40', u'gacC+a+ti'), (u'Final form', u'~2', u'gacCati')]]
    """

    def __getitem__(self, items):
        """Return the requested data by user."""
        readability = ''
        if isinstance(items, str):
            verbform = items
            argument = 'prakriya'
        else:
            verbform = items[0]
            if len(items) > 1:
                argument = items[1]
            else:
                argument = 'prakriya'
            if len(items) > 2 and items[2] == 'machine':
                readability = 'machine'
        if argument == 'prakriya' and readability == '':
            result = get_prakriya(verbform)
        elif argument == 'prakriya' and readability == 'machine':
            result = get_prakriya_jsonified(verbform)
        elif argument == '':
            result = get_full_data(verbform)
        elif not argument == '':
            result = get_specific_info(verbform, argument)
        return result


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
    # print(timestamp())
    syslen = len(sys.argv)
    if syslen < 2 or syslen > 4:
        print(json.dumps({'error': 'Kindly use the following syntax. `python prakriya.py verbform [argument] [readability]`.'}))
        exit(0)
    elif syslen == 4 and not sys.argv[3] == 'machine':
        print(json.dumps({'error': 'The third argument can only be `machine`.'}))
        exit(0)

    if syslen >= 2:
        verbform = sys.argv[1]
    if syslen >= 3:
        argument = sys.argv[2]
    if syslen == 4:
        readability = sys.argv[3]

    if not os.path.exists('data/json/' + verbform + '.json'):
        print(json.dumps({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}))
        exit(0)
    if syslen == 4 and readability == 'machine':
        print(json.dumps({'message': 'for human readable output, use `python prakriya.py verbform prakriya`', 'result': get_prakriya_jsonified(verbform)}, indent=4))
    elif syslen == 3 and argument == 'prakriya':
        print(json.dumps({'message': 'for machine friendly output, use `python prakriya.py verbform prakriya machine`.', 'result': get_prakriya(verbform)}, indent=4))
    elif syslen == 3:
        print(json.dumps(get_specific_info(verbform, argument), indent=4))
    elif syslen == 2:
        print(json.dumps(get_full_data(verbform), indent=4))
    # print(timestamp())
    data = prakriya(verbform)
    print data.verbform
