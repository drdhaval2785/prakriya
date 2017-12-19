#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a python library which returns details about a verb form.

Example
-------
CLI usage - python prakriya.py verbform [argument]

Class usage -

>>> from prakriya import prakriya
>>> p = prakriya()
>>> p['Bavati']
>>> p['Bavati', 'prakriya']
>>> p['Bavati', 'verb']

For details of arguments, see documentation on prakriya class.
"""
import os.path
import json
import sys


storagedirectory = '/var/www/html/sanskritworldflask/'


class prakriya():
    u"""Generate a prakriya class.

    Parameters
    ----------
    It takes a list as parameters e.g. ['verbform', 'argument1']
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
        argument = ''
        if isinstance(items, str):
            verbform = items
        else:
            verbform = items[0]
            if len(items) > 1:
                argument = items[1]
        data = get_full_data(verbform)
        if argument == '':
            result = data
        else:
            result = keepSpecific(data, argument)
        return result


def get_full_data(verbform):
    """Get whole data from the json file for given verb form."""
    global storagedirectory
    fileofinterest = storagedirectory + 'data/json/' + verbform + '.json'
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
                if item not in ['derivation', 'verb']:
                    tmp = datum[item]
                elif item == 'verb':
                    tmp = datum[item]
                    tmp = tmp.replace('!', '~')
                subresult[item] = tmp
            for member in datum['derivation']:
                sutratext = sutrainfo[member['sutra_num']]
                sutranum = member['sutra_num'].replace('~', '-')
                form = member['form'].replace('@', 'u~')
                derivationlist.append({'sutra': sutratext, 'sutra_num': sutranum, 'form': form})
            subresult['prakriya'] = derivationlist
            result.append(subresult)
        return result


def keepSpecific(data, argument):
    """Create a list of only the relavent argument."""
    return [member[argument] for member in data]


if __name__ == '__main__':
    # print(timestamp())
    syslen = len(sys.argv)
    if syslen < 2 or syslen > 3:
        print(json.dumps({'error': 'Kindly use the following syntax. `python prakriya.py verbform [argument]`.'}))
        exit(0)

    if syslen >= 2:
        verbform = sys.argv[1]
    if syslen == 3:
        argument = sys.argv[2]

    if not os.path.exists('data/json/' + verbform + '.json'):
        print(json.dumps({'error': 'The verb form is not in our database. If you feel it deserves to be included, kindly notify us on https://github.com/drdhaval2785/sktderivation/issues.'}))
        exit(0)
    else:
        data = get_full_data(verbform)
        if syslen == 2:
            result = data
        else:
            result = keepSpecific(data, argument)
        print(json.dumps(result, indent=4))
