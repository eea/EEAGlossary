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
#$Id: EEAGlossaryCentre.py,v 1.21 2004/05/05 20:23:21 finrocvs Exp $

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
    engine = obj.getGlossaryEngine()
    obj.languages_list = engine.languages
    obj.subjects_list = engine.subjects
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
        self.subjects_list = {}
        self.translations = []
        self.history = []
        self.languages_list = {}
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

    ##########################
    #   MANAGEMENT FUNCTIONS #
    ##########################

    def manageBasicProperties(self, title='', description='', published=0, REQUEST=None):
        """ manage basic properties for EEAGlossaryCentre """
        self.title = title
        self.description = description
        self.published = published
        self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')

    def manageSubjectsProperties(self, ids=[], old_code='', code='', name='', REQUEST=None):
        """ manage subjects for EEAGlossaryCentre"""
        if self.utAddObjectAction(REQUEST):
            if string.strip(code) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.subjects_list[code] = name
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(code) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                del self.subjects_list[old_code]
                self.subjects_list[code] = name
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for subj in self.utConvertToList(ids):
                del self.subjects_list[subj]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3&save=ok')

    def manageLanguagesProperties(self, ids='', lang='', charset='', english_name='', old_english_name='', REQUEST=None):
        """ manage languages for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(lang)=='' or string.strip(charset)=='' or string.strip(english_name)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            else:
                self.languages_list[english_name] = (lang, charset)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(lang)=='' or string.strip(charset)=='' or string.strip(english_name)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            else:
                del self.languages_list[old_english_name]
                self.languages_list[english_name] = (lang, charset)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            for english_name in self.utConvertToList(ids):
                del self.languages_list[english_name]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4&save=ok')

    def manageSearchProperties(self, ids='', language='', old_language='', REQUEST=None):
        """ maange the search languages for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            else:
                self.search_langs.append(language)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(language) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            else:
                self.search_langs.remove(old_language)
                self.search_langs.append(language)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5')
            for language in self.utConvertToList(ids):
                self.search_langs.remove(language)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=5&save=ok')

    def manageTypesProperties(self, old_type='', new_type='', ids='', REQUEST=None):
        """ manage the types properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(new_type) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.types_list.append(new_type)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(new_type) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.types_list.remove(old_type)
                self.types_list.append(new_type)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            for type in self.utConvertToList(ids):
                self.types_list.remove(type)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    def manageHiddenProperties(self, old_field='', field='', ids='', REQUEST=None):
        """ manage the hidden properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(field) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            else:
                self.hidden_fields.append(field)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(field) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            else:
                self.hidden_fields.remove(old_field)
                self.hidden_fields.append(field)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            for field in self.utConvertToList(ids):
                self.hidden_fields.remove(field)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6&save=ok')

    def manageAlphaProperties(self, old_alpha='', alpha='', ids='', REQUEST=None):
        """ manage the hidden properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(alpha) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.alpha_list.append(alpha)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(alpha) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            else:
                self.alpha_list.remove(old_alpha)
                self.alpha_list.append(alpha)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1')
            for alpha in self.utConvertToList(ids):
                self.alpha_list.remove(alpha)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1&save=ok')

    def get_subjects_list (self):
        """gets subjects list in alphabetical order """
        subjects_values = self.subjects_list.values()
        subjects_values.sort()
        return subjects_values

    def get_languages_list(self):
        """ """
        languages_values = self.languages_list.keys()
        languages_values.sort()
        return languages_values

    def get_language_charset(self, language):
        """ get the charset for a specific language """
        try:
            return self.languages_list[language][1]
        except KeyError, error:
            print error

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