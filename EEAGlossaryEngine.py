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
# The Original Code is EEAGlossary version 1.0.
#
# The Initial Developer of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#
#
#$Id: EEAGlossaryEngine.py,v 1.9 2004/05/11 11:38:36 finrocvs Exp $

import string

# Zope imports
from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
# product imports
from EEAGlossary_constants import *
from EEAGlossary_utils import utils
from parsers.languages_parser import languages_parser
from parsers.subjects_parser import subjects_parser
from parsers.roles_parser import roles_parser

EngineID = EEA_GLOSSARY_ENGINE_NAME

class EEAGlossaryEngine(SimpleItem, utils):
    """ EEAGlossaryEngine """

    meta_type = EEA_GLOSSARY_ENGINE_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/engine.gif'

    manage_options =({'label':'Properties', 'action':'manage_properties_html'},
                    {'label':'Help', 'action':'help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id):
        """ constructor """
        self.id = EngineID
        self.__languages_list = []
        self.__subjects_list = []
        self.__roles = {}
        self.__unicode_langs = []
        self.__search_langs = []
        self.__types_list = []
        self.trans_contact = {}
        self.technic_contact = {}

    def load_roles_list(self):
        """ """
        from os.path import join
        roles_obj = roles_parser()
        root_obj = self.utGetROOT()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary', 'config', 'roles.xml'))
        roles_handler, error = roles_obj.parseContent(content)
        for role in roles_handler.roles:
            self.set_roles(role.name, role.permissions)
            root_obj._addRole(role.name)
            root_obj.__of__(self).manage_role(role.name, role.permissions)
        self._p_changed = 1

    def load_languages_list(self):
        """loads languages & history properties defaults"""

        from os.path import join
        languages_obj = languages_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary', 'config', 'languages.xml'))
        languages_handler, error = languages_obj.parseContent(content)

        for lang in languages_handler.languages:
            self.set_languages_list(lang.lang, lang.charset, lang.english_name)
            if int(lang.unicode):
                self.set_unicode_langs(lang.english_name)
            if int(lang.searchable):
                self.set_searchable_langs(lang.english_name)
        self._p_changed = 1

    def load_subjects_list (self):
        """loads subjects properties defaults"""
        from os.path import join
        subjects_obj = subjects_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary','config', 'subjects.xml'))
        subjects_handler, error = subjects_obj.parseContent(content)
        for code in subjects_handler.subjects:
            self.set_subjects_list(code.code, code.name)
        self._p_changed = 1

    ######################
    # TYPES  FUNCTIONS   #
    ######################
    def get_types_list(self):
        return self.__types_list

    def set_types_list(self, value):
        self.__types_list.append(value)

    def del_types_list(self, value):
        self.__types_list.remove(value)

    def manageTypesProperties(self, old_type='', new_type='', ids='', REQUEST=None):
        """ manage the types properties for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(new_type) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.set_types_list(new_type)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(new_type) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.del_types_list(old_type)
                self.set_types_list(new_type)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            for type in self.utConvertToList(ids):
                self.del_types_list(type)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    ######################
    # UNICODE FUNCTIONS  #
    ######################
    def get_unicode_langs(self):
        return self.__unicode_langs

    def set_unicode_langs(self, value):
        self.__unicode_langs.append(value)

    def del_unicode_langs(self, value):
        self.__unicode_langs.remove(value)

    def manageUnicodeProperties(self, ids='', language='', old_language='', REQUEST=None):
        """ maange the unicode languages for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.set_unicode_langs(language)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.del_unicode_langs(old_language)
                self.set_unicode_langs(language)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            for language in self.utConvertToList(ids):
                self.del_unicode_langs(language)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1&save=ok')

    #########################
    # SEARCHABLE FUNCTIONS  #
    #########################
    def get_searchable_langs(self):
        return self.__search_langs

    def set_searchable_langs(self, value):
        self.__search_langs.append(value)

    def del_searchable_langs(self, value):
        self.__search_langs.remove(value)

    def manageSearchableProperties(self, ids='', language='', old_language='', REQUEST=None):
        """ maange the searchable languages for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.set_searchable_langs(language)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.del_searchable_langs(old_language)
                self.set_searchable_langs(language)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            for language in self.utConvertToList(ids):
                self.del_searchable_langs(language)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1&save=ok')

    ####################
    # ROLES FUNCTIONS  #
    ####################
    def set_roles(self, name, permissions):
        """ add a role in the dictionary """
        self.__roles[name] = permissions

    #######################
    # LANGUAGES FUNCTIONS #
    #######################
    def get_languages_list(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.__languages_list, 'english_name')
        return self.__languages_list

    def get_english_names(self):
        """ get the english name from languages list """
        results = []
        for k in self.get_languages_list():
            results.append(k['english_name'])
        return results

    def set_languages_list(self, lang, charset, english_name):
        """ set the languages """
        append = self.__languages_list.append
        append({'lang':lang, 'charset':charset, 'english_name':english_name})

    def del_language_from_list(self, lang):
        """ remove a language from list """
        for lang_info in self.__languages_list:
            if lang_info['lang'] == lang:
                self.__languages_list.remove(lang_info)

    def manageLanguagesProperties(self, ids='', lang='', charset='', english_name='', old_lang='', REQUEST=None):
        """ manage languages for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(lang)=='' or string.strip(charset)=='' or string.strip(english_name)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            else:
                self.set_languages_list(lang, charset, english_name)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(lang)=='' or string.strip(charset)=='' or string.strip(english_name)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            else:
                self.del_language_from_list(old_lang)
                self.set_languages_list(lang, charset, english_name)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            for lang in self.utConvertToList(ids):
                self.del_language_from_list(lang)
                self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4&save=ok')

    ######################
    # SUBJECTS FUNCTIONS #
    ######################
    def get_subjects_list(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.__subjects_list, 'code')
        return self.__subjects_list

    def set_subjects_list(self, code, name):
        """ set the languages """
        append = self.__subjects_list.append
        append({'code':code, 'name':name})

    def del_subject_from_list(self, code):
        """ remove a language from list """
        for subj_info in self.__subjects_list:
            if subj_info['code'] == code:
                self.__subjects_list.remove(subj_info)

    def manageSubjectsProperties(self, ids=[], old_code='', code='', name='', REQUEST=None):
        """ manage subjects for EEAGlossaryEngine"""
        if self.utAddObjectAction(REQUEST):
            if string.strip(code) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.set_subjects_list(code, name)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(code) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.del_subject_from_list(old_code)
                self.set_subjects_list(code, name)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for subj in self.utConvertToList(ids):
                self.del_subject_from_list(subj)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3&save=ok')

    ##########################
    #   CONTACT  FUNCTIONS   #
    ##########################
    def manageTechnicProperties(self, ids=[], old_email='', email='', phone='', name='', REQUEST=None):
        """ manage tecnical contacts for EEAGlossaryEngine"""
        if self.utAddObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            else:
                self.technic_contact[email] = (name, phone)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            else:
                del self.technic_contact[old_email]
                self.technic_contact[email] = (name, phone)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            for email in self.utConvertToList(ids):
                del self.technic_contact[email]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')

    def manageTranslatorProperties(self, ids=[], old_email='', email='', phone='', name='', REQUEST=None):
        """ manage translator contacts for EEAGlossaryEngine"""
        if self.utAddObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            else:
                self.trans_contact[email] = (name, phone)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            else:
                del self.trans_contact[old_email]
                self.trans_contact[email] = (name, phone)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0')
            for email in self.utConvertToList(ids):
                del self.trans_contact[email]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')


    ##########################
    #  MANAGEMENT FUNCTIONS  #
    ##########################
    def manage_afterAdd(self, item, container):
        """ """
        SimpleItem.inheritedAttribute('manage_afterAdd')(self, item, container)
        item.load_roles_list()
        item.load_languages_list()
        item.load_subjects_list()

    def manage_beforeDelete(self, item, container):
        """ This method is called, when the object is deleted. """
        SimpleItem.inheritedAttribute('manage_beforeDelete')(self, item, container)
        root_obj = self.utGetROOT()
        root_obj._delRoles(self.__roles.keys(), None)

    ##########
    # FORMS  #
    ##########
    help_html = DTMLFile("dtml/EEAGlossaryEngine/help", globals())
    manage_properties_html = DTMLFile("dtml/EEAGlossaryEngine/properties", globals())
    unicode_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_unicode", globals())
    types_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_types", globals())
    languages_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_languages", globals())
    subjects_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_subjects", globals())
    contact_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_contact", globals())
    search_prop_html = DTMLFile("dtml/EEAGlossaryEngine/properties_search", globals())
    style_css = DTMLFile('dtml/EEAGlossaryEngine/style', globals())

InitializeClass(EEAGlossaryEngine)