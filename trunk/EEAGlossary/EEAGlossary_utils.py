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
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#
#
#$Id: EEAGlossary_utils.py,v 1.32 2004/05/13 14:25:19 finrocvs Exp $

#Python imports
import string

#Zope imports
from Products.PythonScripts.standard import url_quote

#product imports
from EEAGlossary_constants import *

#constants
class utils:

    def __init__(self):
        pass

    def ut_makeId(self, p_name):
        """ """
        transtab=string.maketrans('/ +@','____')
        p_name = unicode(p_name, 'latin-1')
        p_name = string.lower(p_name.encode('ascii', 'replace'))
        return string.translate(p_name,transtab,'?&!;()<=>*#[]{}^~:|\/???$?%?')

    def element_list_sorted(self):
        """Return all 'EEA Glossary Element' from a Centre root"""
        lista=self.objectItems([EEA_GLOSSARY_SYNONYM_METATYPE, EEA_GLOSSARY_ELEMENT_METATYPE])
        lista.sort()
        return lista

    def utGetSynonyms(self):
        """ return elements found in synonyms """
        results = []
        cat_obj = self.cu_get_cataloged_objects(self.getGlossaryCatalog(), meta_type=EEA_GLOSSARY_ELEMENT_METATYPE)
        for obj in cat_obj:
            if obj.name in self.synonyms:
                results.append(obj)
        return results

    def utGetElement(self,p_name):
        """ return an element from catalog """
        cat_obj = self.cu_get_cataloged_objects(self.getGlossaryCatalog(), meta_type=EEA_GLOSSARY_ELEMENT_METATYPE)
        for obj in cat_obj:
            if obj.name == p_name:
                return obj

    def utIsSynonym(self):
        """ check if the object is a synonym"""
        return self.meta_type==EEA_GLOSSARY_SYNONYM_METATYPE

    def utCompare(self, x, y):
        """."""
        return cmp(string.lower(x[0]), string.lower(y[0]))

    def utAddObjectAction(self, REQUEST=None):
        """Check if adding an object"""
        res = 0
        if REQUEST:
            res = REQUEST.has_key('add')
        return res

    def utUpdateObjectAction(self, REQUEST=None):
        """Check if updating an object"""
        res = 0
        if REQUEST:
            res = REQUEST.has_key('update')
        return res

    def utDeleteObjectAction(self, REQUEST=None):
        """Check if deleting an object"""
        res = 0
        if REQUEST:
            res = REQUEST.has_key('delete')
        return res

    def utConvertToList(self, something):
        """Convert to list"""
        ret = something
        if type(something) is type(''):
            ret = [something]
        return ret

    def utSortList(self, list):
        """ sort a list """
        list.sort()
        return list

    def utConvertLinesToList(self, value):
        """Takes a value from a textarea control and returns a list of values"""
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
        """Takes a list of values and returns a value for a textarea control"""
        if len(values) == 0:
            return ''
        else:
            return string.join(values, '\r\n')
            
    def utUrlEncode(self, p_string):
        """Encode a string using url_encode"""
        return url_quote(p_string)

    def utISOFormat(self):
        """ return the currect time in ISO format """
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def utIsEmptyString(self, term='',REQUEST=None):
        """return true if a string contains only white characters"""
        if term and len(term)>0:
            if term.count(" ") == len(term):
                return 1
            return 0
        return 1

    def utGetROOT(self):
        """ get the ROOT object"""
        return self.unrestrictedTraverse(('',))

    def utOpenFile(self, path, mode='r'):
        file = open(path, mode)
        content = file.read()
        file.close()
        return content

    def utSortListOfDictionariesByKey(self, p_list, p_key, p_order=0):
        """ Sort a list of dictionary by key """
        if p_order==0:   #ascending
            p_list.sort(lambda x, y, param=p_key: cmp(x[param], y[param]))
        else:           #desceding
            p_list.sort(lambda x, y, param=p_key: cmp(y[param], x[param]))

    def utUtf8Encode(self, p_value):
            """ Encode a iven value to utf-8 """
            return unicode(str(p_value), 'latin-1').encode('utf8')

class catalog_utils:

    def __init__(self):
        """ """
        pass

    def __build_catalog_path(self, item):
        """Creates an id for the item to be added in catalog"""
        return '/'.join(item.getPhysicalPath())

    def __searchCatalog(self, catalog, criteria, path):
        """Search catalog"""
        return catalog(criteria, path)

    def __get_objects(self, catalog, brains):
        """ given the brains return the objects"""
        try:
            return map(catalog.getobject, map(getattr, brains, ('data_record_id_',)*len(brains)))
        except:
            return []

    def cu_catalog_object(self, catalog, ob):
        """ catalog an object """
        catalog.catalog_object(ob, self.__build_catalog_path(ob))
        try:
            catalog.catalog_object(ob, self.__build_catalog_path(ob))
        except:
            pass

    def cu_uncatalog_object(self, catalog, ob):
        """ uncatalog an object """
        try:
            catalog.uncatalog_object(self.__build_catalog_path(ob))
        except:
            pass

    def cu_recatalog_object(self, catalog, ob):
        """ recatalog an object """
        try:
            ob_path = self.__build_catalog_path(ob)
            catalog.uncatalog_object(ob_path)
            catalog.catalog_object(ob, ob_path)
        except:
            pass

    def cu_get_cataloged_objects(self, catalog, meta_type=None, approved=0, howmany=-1, sort_on='bobobase_modification_time', sort_order='reverse', path='/'):
        results = []
        filter = {}
        if approved == 1:
            filter['approved'] = 1
        if sort_on != '':
            filter['sort_on'] = sort_on
            if sort_order != '':
                filter['sort_order'] = sort_order
        if meta_type:
            filter['meta_type'] = self.utConvertToList(meta_type)
        results = self.__searchCatalog(catalog, filter, path)
        if howmany != -1:
            results = results[:howmany]
        results = self.__get_objects(catalog, results)
        return results

    def cu_search_catalog(self, catalog, meta_type=None, query='', size=10000, language='English', definition=''):
        """ """
        command= "catalog(meta_type=" + str(meta_type) + ", " + language + "='" + query + "', definition='" + definition + "')"
        results = eval(command)
        return self.__get_objects(catalog, results)