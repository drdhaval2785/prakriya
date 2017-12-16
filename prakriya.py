#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form.

Example
-------
CLI usage - python prakriya.py verbform [argument] [readability]

Class usage -

>>> from prakriya import prakriya
>>> p = prakriya()
>>> p['Bavati']
>>> p['Bavati', 'prakriya']
>>> p['Bavati', 'prakriya', 'machine']
>>> p['Bavati', 'verb']

For details of arguments, see documentation on prakriya class.
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
            result = []
            temp = json.load(fin)
            # As the stored data is in list, read member of a list
            for member in temp:
                subresult = {}
                # Each member is a dict. Its key can be taken as submember.
                for submember in member:
                    subresult[reversemaparguments(submember)] = member[submember]
                # Append the subresult to the result list.
                result.append(subresult)
            return result
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
    u"""Generate a prakriya class.

    Parameters
    ----------
    It takes a list as parameters e.g. ['verbform', 'argument1', 'argument2']
    verbform is a string in SLP1.
    argument2 can only take 'machine' value, and that too only when 'argument1'
    is 'prakriya'.
    argument1 and argumen2 are optional.
    When they are not provided, the whole data gets loaded back.
    The results are always in list format.

    Valid argument1 and expected output are as follows.
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

    Example
    -------
    >>> from prakriya import prakriya
    >>> p = prakriya()
    >>> p['gacCati']
    [{'it_sutra': '', 'number': '01.1137', 'kshiratarangini': 'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//kRi658.html', 'uohyd': 'http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi?vb=gam1_gamLz_BvAxiH_gawO&prayoga=karwari&encoding=WX&upasarga=-&paxI=parasmEpaxI', 'lakara': 'law', 'meaning': 'gatO', 'jnu': 'JNU-X', 'gana': 'BvAdi', 'it_status': '', 'verbslp': 'gamx!', 'upasarga': None, 'padadecider_sutra': '', 'dhatupradipa': 'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//XA671.html', 'padadecider_id': 'parasmEpadI', 'verb': 'ग॒मॢँ॑', 'it_id': '', 'madhaviya': 'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//mA633.html', 'derivation': [{'style': 'pa', 'note': 0, 'text': ['gamx!'], 'sutra_num': '1.3.1'}, {'style': 'pa', 'note': 0, 'text': ['gamx!'], 'sutra_num': '1.3.2'}, {'style': 'sa', 'note': 0, 'text': ['gam'], 'sutra_num': '1.3.9'}, {'style': 'pa', 'note': 0, 'text': ['gam'], 'sutra_num': '3.4.69'}, {'style': 'sa', 'note': 0, 'text': ['gam+la!w'], 'sutra_num': '3.2.123'}, {'style': 'pa', 'note': 0, 'text': ['gam+la!w'], 'sutra_num': '3.4.77'}, {'style': 'pa', 'note': 0, 'text': ['gam+la!w'], 'sutra_num': '1.3.3'}, {'style': 'sa', 'note': 0, 'text': ['gam+la!'], 'sutra_num': '1.3.9'}, {'style': 'pa', 'note': 0, 'text': ['gam+la!'], 'sutra_num': '1.3.2'}, {'style': 'sa', 'note': 0, 'text': ['gam+l'], 'sutra_num': '1.3.9'}, {'style': 'sa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '3.4.78'}, {'style': 'pa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '1.4.99'}, {'style': 'pa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '1.4.101'}, {'style': 'pa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '1.4.102'}, {'style': 'pa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '1.4.108'}, {'style': 'pa', 'note': 0, 'text': ['gam+tip'], 'sutra_num': '3.4.113'}, {'style': 'sa', 'note': 0, 'text': ['gam+Sap+tip'], 'sutra_num': '3.1.68'}, {'style': 'sa', 'note': 0, 'text': ['gaC+Sap+tip'], 'sutra_num': '7.3.77'}, {'style': 'pa', 'note': 0, 'text': ['gaC+Sap+tip'], 'sutra_num': '3.4.113'}, {'style': 'pa', 'note': 0, 'text': ['gaC+Sap+tip'], 'sutra_num': '1.3.8'}, {'style': 'sa', 'note': 0, 'text': ['gaC+ap+tip'], 'sutra_num': '1.3.9'}, {'style': 'pa', 'note': 0, 'text': ['gaC+ap+tip'], 'sutra_num': '1.3.3'}, {'style': 'sa', 'note': 0, 'text': ['gaC+a+ti'], 'sutra_num': '1.3.9'}, {'style': 'sa', 'note': 0, 'text': ['gatC+a+ti'], 'sutra_num': '6.1.73'}, {'style': 'sa', 'note': 0, 'text': ['gacC+a+ti'], 'sutra_num': '8.4.40'}, {'style': 'sa', 'note': 0, 'text': ['gacCati'], 'sutra_num': '~2'}]}]
    >>> p['gacCati', 'verbslp']
    [u'gamx!']
    >>> p['gacCati', 'prakriya']
    [['BUvAdayo DAtavaH (1.3.1) -> gamx!', "upadeSe'janunAsika it (1.3.2) -> gamx!", 'tasya lopaH (1.3.9) -> gam', 'laH karmaRi ca BAve cAkarmakeByaH. (3.4.69) -> gam', 'vartamAne law (3.2.123) -> gam+la!w', 'lasya (3.4.77) -> gam+la!w', 'halantyam (1.3.3) -> gam+la!w', 'tasya lopaH (1.3.9) -> gam+la!', "upadeSe'janunAsika it (1.3.2) -> gam+la!", 'tasya lopaH (1.3.9) -> gam+l', 'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN (3.4.78) -> gam+tip', 'laH parasmEpadam (1.4.99) -> gam+tip', 'tiNastrIRi trIRi praTamamaDyamottamAH (1.4.101) -> gam+tip', 'tAnyekavacanadvivacanabahuvacanAnyekaSaH (1.4.102) -> gam+tip', 'Seze praTamaH (1.4.108) -> gam+tip', 'tiNSitsArvaDAtukam (3.4.113) -> gam+tip', 'kartari Sap\u200c (3.1.68) -> gam+Sap+tip', 'izugamiyamAM CaH (7.3.77) -> gaC+Sap+tip', 'tiNSitsArvaDAtukam (3.4.113) -> gaC+Sap+tip', 'laSakvatadDite (1.3.8) -> gaC+Sap+tip', 'tasya lopaH (1.3.9) -> gaC+ap+tip', 'halantyam (1.3.3) -> gaC+ap+tip', 'tasya lopaH (1.3.9) -> gaC+a+ti', 'Ce ca (6.1.73) -> gatC+a+ti', 'stoH ScunA ScuH (8.4.40) -> gacC+a+ti', 'Final form (~2) -> gacCati']]
    >>> p['gacCati', 'prakriya', 'machine']
    [[('BUvAdayo DAtavaH', '1.3.1', 'gamx!'), ("upadeSe'janunAsika it", '1.3.2', 'gamx!'), ('tasya lopaH', '1.3.9', 'gam'), ('laH karmaRi ca BAve cAkarmakeByaH.', '3.4.69', 'gam'), ('vartamAne law', '3.2.123', 'gam+la!w'), ('lasya', '3.4.77', 'gam+la!w'), ('halantyam', '1.3.3', 'gam+la!w'), ('tasya lopaH', '1.3.9', 'gam+la!'), ("upadeSe'janunAsika it", '1.3.2', 'gam+la!'), ('tasya lopaH', '1.3.9', 'gam+l'), ('tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', '3.4.78', 'gam+tip'), ('laH parasmEpadam', '1.4.99', 'gam+tip'), ('tiNastrIRi trIRi praTamamaDyamottamAH', '1.4.101', 'gam+tip'), ('tAnyekavacanadvivacanabahuvacanAnyekaSaH', '1.4.102', 'gam+tip'), ('Seze praTamaH', '1.4.108', 'gam+tip'), ('tiNSitsArvaDAtukam', '3.4.113', 'gam+tip'), ('kartari Sap\u200c', '3.1.68', 'gam+Sap+tip'), ('izugamiyamAM CaH', '7.3.77', 'gaC+Sap+tip'), ('tiNSitsArvaDAtukam', '3.4.113', 'gaC+Sap+tip'), ('laSakvatadDite', '1.3.8', 'gaC+Sap+tip'), ('tasya lopaH', '1.3.9', 'gaC+ap+tip'), ('halantyam', '1.3.3', 'gaC+ap+tip'), ('tasya lopaH', '1.3.9', 'gaC+a+ti'), ('Ce ca', '6.1.73', 'gatC+a+ti'), ('stoH ScunA ScuH', '8.4.40', 'gacC+a+ti'), ('Final form', '~2', 'gacCati')]]

    """

    def __getitem__(self, items):
        """Return the requested data by user."""
        readability = ''
        argument = ''
        if isinstance(items, str):
            verbform = items
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


def reversemaparguments(argument):
    """Map actual JSON keys to api friendly arguments."""
    reversemapapi = {'mAdhavIya': 'madhaviya',
                     'kzIratarangiNI': 'kshiratarangini',
                     'dhAtupradIpa': 'dhatupradipa',
                     'UoHyd': 'uohyd',
                     'input': 'verbslp',
                     'lakAra': 'lakara',
                     }
    if argument in reversemapapi:
        return reversemapapi[argument]
    else:
        return argument


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
