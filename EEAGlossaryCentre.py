# The contents of this file are subject to the Mozilla PublicloadINI
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
#$Id: EEAGlossaryCentre.py,v 1.22 2004/05/06 14:26:15 finrocvs Exp $

# python imports
import string
import whrandom

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware
import AccessControl.User
from Products.ZCatalog.ZCatalog import manage_addZCatalog, manage_addZCatalogForm

# product imports
import EEAGlossaryFolder
from EEAGlossary_utils import utils
from EEAGlossary_constants import *

manage_addGlossaryCentre_html = DTMLFile('dtml/EEAGlossaryCentre/add', globals())

def manage_addGlossaryCentre(self, id, title='', description='', REQUEST=None):
    """ Adds a new EEAGlossaryCentre object """
    ob = EEAGlossaryCentre(id, title, description)
    self._setObject(id, ob)
    obj = self._getOb(id)
    obj.loadProperties()
    obj._p_changed = 1
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryCentre(Folder, CatalogAware, utils):
    """ EEAGlossaryCentre """

    meta_type = EEA_GLOSSARY_CENTRE_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME

    manage_options =((Folder.manage_options[0],) +
                ({'label':'Properties',         'action':'manage_properties_html'},
                {'label':'View',                'action':'preview_html'},
                {'label':'Contexts Reference',  'action':'contexts_html'},
                {'label':'Check list',          'action':'check_list_html'},
                {'label':'Change Password',     'action':'change_pass_html'},
                {'label':'XML/RDF',             'action':'glossary_terms_rdf'},
                {'label':'All terms',           'action':'all_terms_html'},
                {'label':'Management',          'action':'management_page_html'},
                {'label':'Help',                'action':'manageHelp'},
                {'label':'Undo',                'action':'manage_UndoForm'},)
                )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        self.types_list = []
        self.languages_list = []
        self.subjects_list = []

        self.search_langs = []
        self.published = 0
        self.hidden_fields = []
        self.alpha_list = list(string.uppercase + string.digits)
        utils.__dict__['__init__'](self)

    def all_meta_types(self):
        """ Supported meta_types """
        meta_types = [{'name': EEA_GLOSSARY_FOLDER_METATYPE, 'action': 'manage_addGlossaryFolder_html'},]
        return meta_types

    manage_addGlossaryFolder_html = EEAGlossaryFolder.manage_addGlossaryFolder_html
    manage_addGlossaryFolder = EEAGlossaryFolder.manage_addGlossaryFolder

    #####################
    # LOAD PROPERTIES   #
    #####################
    def loadProperties(self):
        """ load the properties from engine """
        from copy import copy
        engine = self.getGlossaryEngine()
        self.languages_list = copy(engine.get_languages_list())
        self.subjects_list = copy(engine.get_subjects_list())
        self.types_list = copy(engine.get_types_list())

    #####################
    # BASIC FUNCTIONS   #
    #####################
    def getGlossaryEngine(self):
        """ """
        return self.unrestrictedTraverse(EEA_GLOSSARY_ENGINE_NAME, None)

    def getAuthenticatedUser(self):
        """ return the authenticated user """
        return self.REQUEST.AUTHENTICATED_USER.getUserName()

    def getAuthenticatedUserRoles(self):
        """ return the list of roles for authenticated user """
        return self.REQUEST.AUTHENTICATED_USER.getRoles()

    def style_css(self):
        """ return the css file from EEAGlossaryEngine """
        return self.getGlossaryEngine().style_css.read()

    def manageBasicProperties(self, title='', description='', published=0, REQUEST=None):
        """ manage basic properties for EEAGlossaryCentre """
        self.title = title
        self.description = description
        self.published = published
        self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')

    ##########################
    #   SUBJECTS FUNCTIONS   #
    ##########################
    def get_subjects_list(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.subjects_list, 'code')
        return self.subjects_list

    def set_subjects_list(self, code, name):
        """ set the languages """
        self.subjects_list.append({'code':code, 'name':name})

    def del_subject_from_list(self, code):
        """ remove a language from list """
        for subj_info in self.subjects_list:
            if subj_info['code'] == code:
                self.subjects_list.remove(subj_info)

    def get_subject_by_codes(self, codes):
        """ return the subjects list """
        results = []
        codes = self.utConvertToList(codes)
        for subj_info in self.subjects_list:
            if subj_info['code'] in codes:
                results.append(subj_info)
        return results

    def manageSubjectsProperties(self, ids=[], old_code='', code='', name='', REQUEST=None):
        """ manage subjects for EEAGlossaryCentre"""
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
    #   LANGUAGES FUNCTIONS  #
    ##########################
    def get_languages_list(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.languages_list, 'english_name')
        return self.languages_list

    def get_english_names(self):
        """ get the english name from languages list """
        results = []
        for k in self.get_languages_list():
            results.append(k['english_name'])
        return results

    def get_language_charset(self, language):
        """ get the charset for a specific language """
        for k in self.get_languages_list():
            if k['english_name'] == 'language':
                return k['charset']

    def set_languages_list(self, lang, charset, english_name):
        """ set the languages """
        self.languages_list.append({'lang':lang, 'charset':charset, 'english_name':english_name})

    def del_language_from_list(self, lang):
        """ remove a language from list """
        for lang_info in self.languages_list:
            if lang_info['lang'] == lang:
                self.languages_list.remove(lang_info)

    def get_unicode_langs(self):
        """ return the unicode languages list """
        return self.getGlossaryEngine().get_unicode_langs()

    def display_unicode_langs(self, language, charset=""):
        """ """
        if charset=="":
            return self.utToUTF8(language, self.get_language_charset(language))
        else:
            return self.utToUTF8(language, charset)

    def manageLanguagesProperties(self, ids='', lang='', charset='', english_name='', old_english_name='', REQUEST=None):
        """ manage languages for EEAGlossaryCentre """
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
                self.del_language_from_list(old_english_name)
                self.set_languages_list(lang, charset, english_name)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            for english_name in self.utConvertToList(ids):
                self.del_language_from_list(english_name)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4&save=ok')

    ##########################
    #   SEARCH FUNCTIONS     #
    ##########################
    def get_search_langs(self):
        return self.search_langs

    def set_search_langs(self, value):
        self.search_langs.append(value)

    def del_search_langs(self, value):
        self.search_langs.remove(value)

    def manageSearchProperties(self, ids='', language='', old_language='', REQUEST=None):
        """ maange the search languages for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            else:
                self.set_search_langs(language)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            else:
                self.del_search_langs(old_language)
                self.set_search_langs(language)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            for language in self.utConvertToList(ids):
                self.del_search_langs(language)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5&save=ok')

    ##########################
    #   TYPES FUNCTIONS      #
    ##########################
    def get_types_list(self):
        return self.types_list

    def set_types_list(self, value):
        self.types_list.append(value)

    def del_types_list(self, value):
        self.types_list.remove(value)

    def manageTypesProperties(self, old_type='', new_type='', ids='', REQUEST=None):
        """ manage the types properties for EEAGlossaryCentre """
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

    ################################
    # HIDDEN FIELDS FUNCTIONS      #
    ################################
    def get_hidden_list(self):
        return self.hidden_fields

    def set_hidden_list(self, value):
        self.hidden_fields.append(value)

    def del_hidden_list(self, value):
        self.hidden_fields.remove(value)

    def manageHiddenProperties(self, old_field='', field='', ids='', REQUEST=None):
        """ manage the hidden properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(field) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            else:
                self.set_hidden_list(field)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(field) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            else:
                self.del_hidden_list(old_field)
                self.set_hidden_list(field)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            for field in self.utConvertToList(ids):
                self.del_hidden_list(field)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6&save=ok')

    ################################
    #  ALPHA FIELDS FUNCTIONS      #
    ################################
    def get_alpha_list(self):
        return self.alpha_list

    def set_alpha_list(self, value):
        self.alpha_list.append(value)

    def del_alpha_list(self, value):
        self.alpha_list.remove(value)

    def manageAlphaProperties(self, old_alpha='', alpha='', ids='', REQUEST=None):
        """ manage the hidden properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(alpha) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.set_alpha_list(alpha)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(alpha) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.del_alpha_list(old_alpha)
                self.set_alpha_list(alpha)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            for alpha in self.utConvertToList(ids):
                self.del_alpha_list(alpha)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1&save=ok')

    #####################
    #   MANAGEMENT TABS #
    #####################
    manage_properties_html = DTMLFile('dtml/EEAGlossaryCentre/properties', globals())
    prop_basic_html = DTMLFile('dtml/EEAGlossaryCentre/properties_basic', globals())
    prop_alpha_html = DTMLFile('dtml/EEAGlossaryCentre/properties_alpha', globals())
    prop_types_html = DTMLFile('dtml/EEAGlossaryCentre/properties_types', globals())
    prop_subjects_html = DTMLFile('dtml/EEAGlossaryCentre/properties_subjects', globals())
    prop_languages_html = DTMLFile('dtml/EEAGlossaryCentre/properties_languages', globals())
    prop_search_html = DTMLFile('dtml/EEAGlossaryCentre/properties_search', globals())
    prop_hidden_html = DTMLFile('dtml/EEAGlossaryCentre/properties_hidden', globals())

    preview_html = DTMLFile('dtml/EEAGlossaryCentre/preview', globals())
    contexts_html = DTMLFile('dtml/EEAGlossaryCentre/contexts', globals())
    check_list_html = DTMLFile('dtml/EEAGlossaryCentre/checklist', globals())
    change_pass_html = DTMLFile('dtml/EEAGlossaryCentre/changepassword', globals())
    glossary_terms_rdf = ''
    all_terms_html = DTMLFile('dtml/EEAGlossaryCentre/allterms', globals())
    management_page_html = DTMLFile('dtml/EEAGlossaryCentre/administration', globals())

    help_html = DTMLFile("dtml/EEAGlossaryCentre/help", globals())
    help_contact_html = DTMLFile("dtml/EEAGlossaryCentre/help_contact", globals())

    manage_utf8_header = DTMLFile('dtml/EEAGlossaryCentre/utf8_header', globals())
    manage_utf8_footer = DTMLFile('dtml/EEAGlossaryCentre/utf8_footer', globals())
InitializeClass(EEAGlossaryCentre)