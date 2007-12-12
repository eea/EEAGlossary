# -*- coding: latin1 -*-
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Original Code is EEAGlossary version 1.0.0
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Finsiel Romania
# Antonio De Marinis, EEA
# Cornel Nitu, Finsiel Romania


#Python imports
import string
import whrandom
import codecs
import csv
import re

#Zope imports
from Products.PythonScripts.standard import url_quote

#product imports
from EEAGlossary_constants import *

#constants
class utils:

    def __init__(self):
        self.win_cp1252 = {
                128: 8364, # euro sign
                130: 8218, # single low-9 quotation mark
                131:  402, # latin small letter f with hook
                132: 8222, # double low-9 quotation mark
                133: 8230, # horizontal ellipsis
                134: 8224, # dagger
                135: 8225, # double dagger
                136:  710, # modifier letter circumflex accent
                137: 8240, # per mille sign
                138:  352, # latin capital letter s with caron
                139: 8249, # single left-pointing angle quotation mark
                140:  338, # latin capital ligature oe
                142:  381, # latin capital letter z with caron
                145: 8216, # left single quotation mark
                146: 8217, # right single quotation mark
                147: 8220, # left double quotation mark
                148: 8221, # right double quotation mark
                149: 8226, # bullet
                150: 8211, # en dash
                151: 8212, # em dash
                152:  732, # small tilde
                153: 8482, # trade mark sign
                154:  353, # latin small letter s with caron
                155: 8250, # single right-pointing angle quotation mark
                156:  339, # latin small ligature oe
                158:  382, # latin small letter z with caron
                159:  376} # latin capital letter y with diaeresis

    def ut_test_even(self, p_number):
        """ return true if even """
        return not(p_number%2)

    def ut_test_definition(self, p_def):
        """."""
        if p_def == 'Definition':
            return 1
        return 0

    def ut_makeId(self, p_name):
        """ generate the ID """
        res = ''
        transtab=string.maketrans('/ +@','____')
        p_name = unicode(p_name, 'latin-1')
        p_name = p_name.encode('ascii', 'replace')
        res = string.translate(p_name,transtab,"?'&!;,\"()<=>*#[]{}^~:|\/???$?%?")
        p = re.compile('_+')
        res = p.sub('_', res)
        p = re.compile('_*-_*')
        res = p.sub('-', res)
        return res

    def csv_reader(self, file_path, quoting=None):
        """ CSV reader """
        if quoting is None: quoting = csv.excel
        return csv.reader(open(file_path, "rb"), quoting)

    def element_list_sorted(self):
        """ return all 'EEA Glossary Element' from a Centre root """
        lista=self.objectItems([EEA_GLOSSARY_SYNONYM_METATYPE, EEA_GLOSSARY_ELEMENT_METATYPE])
        lista.sort()
        return lista

    def utConvertToInt(self, p_string):
        """ """
        if len(p_string) == 0:  return 0
        elif len(p_string) == 1:  return int(p_string)
        else:  return 1

    def utSplitToList(self, something, separator='/'):
        """ get a string like value1<separator>value2..., and returns a list [value1, values...] """
        if something == '':  return []
        else:  return string.split(something, separator)

    def utGetSynonyms(self):
        """ return elements found in synonyms """
        results=[]
        if len(self.synonyms) != 0:
            results.append(self.unrestrictedTraverse(self.synonyms[0], None))
        return results

#        results = []
#        cat_obj = self.cu_get_cataloged_objects(meta_type=EEA_GLOSSARY_ELEMENT_METATYPE)
#        for obj in cat_obj:
#            if obj.name in self.synonyms:
#                results.append(obj)
#        return results

    def utGetElement(self,p_name):
        """ return an element from catalog """
        cat_obj = self.cu_get_cataloged_objects(meta_type=EEA_GLOSSARY_ELEMENT_METATYPE)
        for obj in cat_obj:
            if obj.name == p_name:
                return obj

    def utIsSynonym(self):
        """ check if the object is a synonym """
        return self.meta_type==EEA_GLOSSARY_SYNONYM_METATYPE

    def utIsElement(self):
        """ check if the object is a element """
        return self.meta_type==EEA_GLOSSARY_ELEMENT_METATYPE

#    def utCompare(self, x, y):
#        """ compare two strings """
#        return cmp(string.lower(x[0].name), string.lower(y[0].name))

    def utAddObjectAction(self, REQUEST=None):
        """ check if adding an object """
        res = 0
        if REQUEST:
            res = REQUEST.has_key('add')
        return res

    def utUpdateObjectAction(self, REQUEST=None):
        """ check if updating an object """
        res = 0
        if REQUEST:
            res = REQUEST.has_key('update')
        return res

    def utDeleteObjectAction(self, REQUEST=None):
        """ check if deleting an object """
        res = 0
        if REQUEST:
            res = REQUEST.has_key('delete')
        return res

    def utConvertToList(self, something):
        """ convert to list """
        ret = something
        if type(something) is type(''):
            ret = [something]
        return ret

    def utSortList(self, list):
        """ sort a list """
        list.sort()
        return list

    def utConvertLinesToList(self, value):
        """ takes a value from a textarea control and returns a list of values """
        if type(value) == type([]):
            return value
        if value == '':
            return []
        else:
            values = []
            for v in string.split(value , '\r\n'):
                if v != '':
                    values.append(v)
        return values

    def utConvertListToLines(self, values):
        """ takes a list of values and returns a value for a textarea control """
        if len(values) == 0:
            return ''
        else:
            return string.join(values, '\r\n')
            
    def utUrlEncode(self, p_string):
        """ encode a string using url_encode """
        return url_quote(p_string)

    def utISOFormat(self):
        """ return the currect time in ISO format """
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def utIsEmptyString(self, term='',REQUEST=None):
        """ return true if a string contains only white characters """
        return not len(term.strip())

    def utGetROOT(self):
        """ get the ROOT object """
        return self.unrestrictedTraverse(('',))

    def utGetObject(self, url):
        """ get an object given the url """
        return self.unrestrictedTraverse(url, None)

    def utOpenFile(self, path, mode='r'):
        """ read from a file """
        file = open(path, mode)
        content = file.read()
        file.close()
        return content

    def utSortListOfDictionariesByKey(self, p_list, p_key, p_order=0):
        """ sort a list of dictionary by key """
        if p_order==0:   #ascending
            p_list.sort(lambda x, y, param=p_key: cmp(x[param], y[param]))
        else:            #desceding
            p_list.sort(lambda x, y, param=p_key: cmp(y[param], x[param]))

    def utUtf8Encode(self, p_value):
        """ encode a iven value to utf-8 """
        return unicode(p_value, 'utf-8')

    def latin1_to_utf8(self, s):
        return unicode(s, 'latin1').encode('utf-8')

    def utf8_to_latin1(self, s):
        return self.encodeLatin1(self.decodeUTF8(s)[0])[0]

    encodeLatin1, decodeLatin1 = codecs.lookup('latin1')[:2]
    encodeUTF8, decodeUTF8 = codecs.lookup('UTF8')[:2]
    encodeISO88592, decodeISO88592 = codecs.lookup('iso-8859-2')[:2]

    def debug(self, error):
        """ """
        import sys
        return str(error) + ' at line ' + str(sys.exc_info()[2].tb_lineno)

    def convertValToHex(self, val):
        return unichr(int(val.group()[2:-1]))

    def convertHTMLCodesToHex(self, term):
        import re
        return re.sub('&#[0-9]+;', self.convertValToHex, term)

    def convertWinCodesToHTMLCodes(self, term):
        for i in range(len(term)-1,-1,-1):
            if ord(term[i]) in self.win_cp1252.keys():
                term=term[0:i] + "&#" + str(self.win_cp1252[ord(term[i])]) + ";" + term[i+1:]
        return term      

    def utXmlEncode(self, p_str):
        """Encode some special chars"""
        if isinstance(p_str, unicode): tmp = p_str.encode('utf-8')
        else: tmp = str(p_str)
        tmp = tmp.replace('&', '&amp;')
        tmp = tmp.replace('<', '&lt;')
        tmp = tmp.replace('"', '&quot;')
        tmp = tmp.replace('\'', '&apos;')
        tmp = tmp.replace('>', '&gt;')
        return tmp

    def utCleanUpStr(self, p_str):
        """Cleanup a string of the NON-ASCII chars"""
        tmp = self.utXmlEncode(p_str)
        tmp = tmp.replace('—', '-')
        tmp = tmp.replace('–', '-')
        tmp = tmp.replace('‘', '&quot;')
        tmp = tmp.replace('’', '&quot;')
        tmp = tmp.replace(' ', " ")
        tmp = tmp.replace('´', '&quot;')
        tmp = tmp.replace("Â'", '&quot;')
        tmp = tmp.replace('“', '&quot;')
        tmp = tmp.replace('”', '&quot;')
        tmp = tmp.replace('§', "-")
        tmp = tmp.replace('¤', " ")
        tmp = tmp.replace('«', "&quot;")
        tmp = tmp.replace('»', "&quot;")
        tmp = tmp.replace('…', "...")
        tmp = tmp.replace('•', "* ")

        tmp=tmp.replace('é','e')
        tmp=tmp.replace('ê','e')
        tmp=tmp.replace('È','E')
        return tmp

    ######################
    #   Synonym Linking  #
    ######################

    def utElementSynAdd(self, p_old_id, p_syn_au):
        """for convert or when change synonyms property"""
        if len(p_syn_au) != 0:
            syn = self.unrestrictedTraverse(p_syn_au, None)
            elem = self.unrestrictedTraverse(syn.synonyms[0])
            elem.synonym.append(syn.absolute_url(1))
        else:
            elem = self.unrestrictedTraverse(self.synonyms[0], None)
            elem.synonym.append(string.upper(self.id[0])+'/'+self.id)
        elem._p_changed = 1
        if len(p_old_id) != 0:
            elem_old = self.unrestrictedTraverse(p_old_id[0], None)
            elem_old.synonym.remove(self.absolute_url(1))
            elem_old._p_changed = 1

#    def utElementSynAdd(self, p_old_id, p_syn_au):
#        """for convert or when change synonyms property"""
#        if len(p_syn_au) != 0:
#            syn = self.unrestrictedTraverse(p_syn_au, None)
#            elem = self.unrestrictedTraverse(syn.synonyms[0])
#            elem.synonym.append(syn.absolute_url(1))
#        else:
#            elem = self.unrestrictedTraverse(self.synonyms[0], None)
#            elem.synonym.append(self.absolute_url(1))
#        elem._p_changed = 1
#        if len(p_old_id) != 0:
#            elem_old = self.unrestrictedTraverse(p_old_id[0], None)
#            elem_old.synonym.remove(self.absolute_url(1))
#            elem_old._p_changed = 1

    def utElementSynDel(self):
        """for deleting a synonym"""
        if self.synonyms != []:
            elem = self.unrestrictedTraverse(self.synonyms[0], None)
            try:
                elem.synonym.remove(string.upper(self.id[0])+'/'+self.id)
                elem.cu_recatalog_object()
            except:
                pass

#    def utSynonymElRename(self):
#        """."""
#        for l_syn_id in self.synonym:
#            syn = self._getOb(l_syn_id)
#            syn.synonym = [self.name]

    def utSynonymElDel(self):
        """for deleting an element"""
        for l_syn_id in self.synonym:
            syn = self.unrestrictedTraverse(l_syn_id, None)
            syn.synonyms = []
            syn.cu_recatalog_object()


class catalog_utils:

    def __init__(self):
        """ """
        pass

    def __build_catalog_path(self, item):
        """ creates an id for the item to be added in catalog """
        return '/'.join(item.getPhysicalPath())

    def __searchCatalog(self, criteria):
        """ search catalog """
        catalog = self.getGlossaryCatalog()
        return catalog(criteria)

    def __get_objects(self, brains):
        """ given the brains return the objects """
        catalog = self.getGlossaryCatalog()
        try:
            return map(catalog.getobject, map(getattr, brains, ('data_record_id_',)*len(brains)))
        except:
            return []

    def cu_catalog_object(self, ob):
        """ catalog an object """
        catalog = self.getGlossaryCatalog()
        try:
            ob_path = self.__build_catalog_path(ob)
            catalog.catalog_object(ob, ob_path)
        except Exception, error:
            print self.debug(error)

    def cu_uncatalog_object(self, ob):
        """ uncatalog an object """
        catalog = self.getGlossaryCatalog()
        try:
            catalog.uncatalog_object(self.__build_catalog_path(ob))
        except Exception, error:
            print self.debug(error)

    def cu_recatalog_object(self, ob):
        """ recatalog an object """
        try:
            catalog = self.getGlossaryCatalog()
            ob_path = self.__build_catalog_path(ob)
            catalog.uncatalog_object(ob_path)
            self.cu_catalog_object(ob)
        except Exception, error:
            print self.debug(error)
            
    def cu_getIndexes(self):
        """ return a list with all ZCatalog indexes """
        catalog = self.getGlossaryCatalog()
        return catalog.index_objects()

    def cu_reindexCatalogIndex(self, name, REQUEST):
        """ reindex an index from ZCatalog """
        catalog = self.getGlossaryCatalog()
        catalog.reindexIndex(name, REQUEST)

    def cu_get_cataloged_objects(self, meta_type=None, approved=0, howmany=-1, sort_on='bobobase_modification_time', 
        sort_order='reverse', path=''):
        """ return objects from catalog """
        results = []
        filter = {}
        filter['path'] = path
        if approved == 1:
            filter['approved'] = 1
        if sort_on != '':
            filter['sort_on'] = sort_on
            if sort_order != '':
                filter['sort_order'] = sort_order
        if meta_type:
            filter['meta_type'] = self.utConvertToList(meta_type)
        results = self.__searchCatalog(filter)
        if howmany != -1:
            results = results[:howmany]
        results = self.__get_objects(results)
        return results

    def utEliminateDuplicates(self, p_objects):
        """Eliminate duplicates from a list of objects (with ids)"""
        dict = {}
        for l_object in p_objects:
            dict[l_object.id] = l_object
        return dict.values()

    def cu_search_catalog(self, meta_type=None, query='', size=10000, language='English', definition=''):
        """ search catalog """
        catalog = self.getGlossaryCatalog()
        command= "catalog(meta_type=" + str(meta_type) + ", " + language + "='" + query + "', definition='" + definition + "')"
        command_name= "catalog(meta_type=" + str(meta_type) + ", " + language + "='" + "" + "', definition='" + definition + "', name='" + query + "')"
        results = eval(command)
        results_name = eval(command_name)
        res = self.__get_objects(results)
        res.extend(self.__get_objects(results_name))
        return self.utEliminateDuplicates(res)[:int(size)]

    def cu_search_synonyms(self):
        """ return synonyms pointing to this element """
        results = []
        filter = {}

        filter['synonyms'] = self.absolute_url(1)
        filter['approved'] = [1, 'on']
        filter['meta_type'] = EEA_GLOSSARY_SYNONYM_METATYPE

        results = self.__searchCatalog(filter)
        results = self.__get_objects(results)
        return results