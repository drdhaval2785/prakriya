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
    r"""Generate a prakriya class.

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
    >>> p['Bavati']
    [{u'kshiratarangini': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//kRi1.html', u'suffix': u'tip', u'jnu': u'http://sanskrit.jnu.ac.in/tinanta/tinanta.jsp?t=1', u'padadecider_id': u'parasmEpadI', u'number': u'01.0001', u'gana': u'BvAdi', 'prakriya': [{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}, {'sutra': u'laH karmaRi ca BAve cAkarmakeByaH.', 'sutra_num': u'3.4.69', 'form': u'BU'}, {'sutra': u'vartamAne law', 'sutra_num': u'3.2.123', 'form': u'BU+la~w'}, {'sutra': u'lasya', 'sutra_num': u'3.4.77', 'form': u'BU+la~w'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+la~w'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+la~'}, {'sutra': u"upadeSe'janunAsika it", 'sutra_num': u'1.3.2', 'form': u'BU+la~'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+l'}, {'sutra': u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', 'sutra_num': u'3.4.78', 'form': u'BU+tip'}, {'sutra': u'laH parasmEpadam', 'sutra_num': u'1.4.99', 'form': u'BU+tip'}, {'sutra': u'tiNastrIRi trIRi praTamamaDyamottamAH', 'sutra_num': u'1.4.101', 'form': u'BU+tip'}, {'sutra': u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', 'sutra_num': u'1.4.102', 'form': u'BU+tip'}, {'sutra': u'Seze praTamaH', 'sutra_num': u'1.4.108', 'form': u'BU+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+tip'}, {'sutra': u'kartari Sap\u200c', 'sutra_num': u'3.1.68', 'form': u'BU+Sap+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+Sap+tip'}, {'sutra': u'laSakvatadDite', 'sutra_num': u'1.3.8', 'form': u'BU+Sap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+ap+tip'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+ap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+a+ti'}, {'sutra': u'sArvaDAtukArDaDAtukayoH', 'sutra_num': u'7.3.84', 'form': u'Bo+a+ti'}, {'sutra': u"eco'yavAyAvaH", 'sutra_num': u'6.1.78', 'form': u'Bav+a+ti'}, {'sutra': u'antimaM rUpam', 'sutra_num': u'-2', 'form': u'Bavati'}], u'madhaviya': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//mA1.html', u'lakara': u'law', u'dhatupradipa': u'http://sanskrit.uohyd.ac.in/scl/dhaatupaatha/files-15-03-2017//XA1.html', u'meaning': u'sattAyAm', u'verb': u'BU', u'it_id': u'', u'derivation': u'praTama', u'purusha': u'praTama', u'padadecider_sutra': u'', u'uohyd': u'http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi?vb=BU1_BU_BvAxiH_sawwAyAm&prayoga=karwari&encoding=WX&upasarga=-&paxI=parasmEpaxI', u'it_status': u'', u'vachana': u'eka', u'verbaccent': u'\u092d\u0942\u0951', u'it_sutra': u'', u'upasarga': u''}]
    >>> p['Bavati', 'verb']
    [u'BU']
    >>> p['Bavati', 'prakriya']
    [[{'sutra': u'BUvAdayo DAtavaH', 'sutra_num': u'1.3.1', 'form': u'BU'}, {'sutra': u'laH karmaRi ca BAve cAkarmakeByaH.', 'sutra_num': u'3.4.69', 'form': u'BU'}, {'sutra': u'vartamAne law', 'sutra_num': u'3.2.123', 'form': u'BU+la~w'}, {'sutra': u'lasya', 'sutra_num': u'3.4.77', 'form': u'BU+la~w'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+la~w'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+la~'}, {'sutra': u"upadeSe'janunAsika it", 'sutra_num': u'1.3.2', 'form': u'BU+la~'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+l'}, {'sutra': u'tiptasJisipTasTamibvasmas tAtAMJaTAsATAMDvamiqvahimahiN', 'sutra_num': u'3.4.78', 'form': u'BU+tip'}, {'sutra': u'laH parasmEpadam', 'sutra_num': u'1.4.99', 'form': u'BU+tip'}, {'sutra': u'tiNastrIRi trIRi praTamamaDyamottamAH', 'sutra_num': u'1.4.101', 'form': u'BU+tip'}, {'sutra': u'tAnyekavacanadvivacanabahuvacanAnyekaSaH', 'sutra_num': u'1.4.102', 'form': u'BU+tip'}, {'sutra': u'Seze praTamaH', 'sutra_num': u'1.4.108', 'form': u'BU+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+tip'}, {'sutra': u'kartari Sap\u200c', 'sutra_num': u'3.1.68', 'form': u'BU+Sap+tip'}, {'sutra': u'tiNSitsArvaDAtukam', 'sutra_num': u'3.4.113', 'form': u'BU+Sap+tip'}, {'sutra': u'laSakvatadDite', 'sutra_num': u'1.3.8', 'form': u'BU+Sap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+ap+tip'}, {'sutra': u'halantyam', 'sutra_num': u'1.3.3', 'form': u'BU+ap+tip'}, {'sutra': u'tasya lopaH', 'sutra_num': u'1.3.9', 'form': u'BU+a+ti'}, {'sutra': u'sArvaDAtukArDaDAtukayoH', 'sutra_num': u'7.3.84', 'form': u'Bo+a+ti'}, {'sutra': u"eco'yavAyAvaH", 'sutra_num': u'6.1.78', 'form': u'Bav+a+ti'}, {'sutra': u'antimaM rUpam', 'sutra_num': u'-2', 'form': u'Bavati'}]]

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
