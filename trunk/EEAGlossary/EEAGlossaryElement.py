# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with t4/28/2004he License. You may obtain a copy of
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
#$Id: EEAGlossaryElement.py,v 1.25 2004/05/06 14:17:35 finrocvs Exp $

# python imports
import string

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Products.ZCatalog.CatalogAwareness import CatalogAware

# product imports
from EEAGlossary_utils import utils
from EEAGlossary_constants import *

class ElementBasic:
    """ define the basic properties for EEAGlossaryElement"""

    def __init__(self, name, el_type, source, subjects, el_context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed):
        """ constructor"""

        self.name = name
        self.el_type = el_type
        self.source = source
        self.subjects = subjects
        self.el_context = el_context
        self.comment = comment
        self.used_for_1 = used_for_1
        self.used_for_2 = used_for_2
        self.definition = definition
        self.definition_source_url = definition_source_url
        self.disabled = disabled
        self.approved = approved
        self.long_definition = long_definition
        self.QA_needed = QA_needed

manage_addGlossaryElement_html = DTMLFile('dtml/EEAGlossaryElement/add', globals())

def manage_addGlossaryElement(self, id, name='', el_type='', source='', subjects=[], el_context='', comment='', 
    used_for_1='', used_for_2='',definition='', definition_source_url='', long_definition='', disabled=0, 
    approved=1, QA_needed=0, image_url='', flash_url='', links=[], actions=[], translations={}, REQUEST=None):

    """ Adds a new EEAGlossaryElement object """

    ob = EEAGlossaryElement(id, name, el_type, source, subjects, el_context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed, 
            image_url, flash_url, links, actions, translations)
    self._setObject(id, ob)
    element_obj = self._getOb(id)
    element_obj.load_translations_list()
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryElement(SimpleItem, CatalogAware, ElementBasic, utils):
    """ EEAGlossaryElement """

    meta_type = EEA_GLOSSARY_ELEMENT_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/element.gif'
    default_catalog = GLOSSARY_CATALOG_NAME

    manage_options = (
        {'label':'All Translations',        'action':'all_translations_html'},
        {'label':'Check Translation',       'action':'check_translation_html'},
        {'label':'Properties',              'action':'manage_properties_html'},
        {'label':"View",                    'action':'preview_html'},
        #{'label':'My props',                'action':'custom_properties_html'},
        {'label':'Convert to Synonym',      'action':'synonym_html'},
        {'label':'History',                 'action':'history_html'},
        {'label':'Undo',                    'action':'manage_UndoForm'},
        {'label':'Help',                    'action':'help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id, name, el_type, source, subjects, el_context, comment, used_for_1, used_for_2, definition, 
        definition_source_url, long_definition, disabled, approved, QA_needed,  image_url, flash_url, links, actions, translations):
        """ constructor """
        self.id = id
        self.image_url = image_url
        self.flash_url = flash_url
        self.links = links
        self.actions = actions
        self.translations = {}
        self.all_langs_list= {}
        self.history={}
        ElementBasic.__dict__['__init__'](self, name, el_type, source, subjects, el_context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed)

    def is_published (self):
        if self.approved and not self.disabled:
            return 1
        else:
            return 0

    def is_image_url (self):
        if not self.utIsEmptyString(self.image_url) and (not 'image_url' in self.REQUEST.PARENTS[2].hidden_fields):
            return 0
        else:
            return 1

    def is_long_definition (self):
        if not self.utIsEmptyString(self.long_definition) and (not 'long_definition' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0

    def is_defintion_source (self):
        if not self.utIsEmptyString(self.definition_source_url) and (not 'definition_source_url' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0

    def check_allowed_translations(self, language):
        """ check if the authenticated user has the permission to change the translation"""
        role = 'QC ' + language
        if (role in self.getAuthenticatedUserRoles()) or self.REQUEST.AUTHENTICATED_USER.has_role(role, self):
            return 1
        return 0

    def load_translations_list (self):
        for lang in self.REQUEST.PARENTS[0].languages_list.keys():
            self.translations[lang] = ''

    def get_translations_languages(self):
        """ """
        languages = self.translations.keys()
        languages.sort()
        return languages

    def get_translations_result(self, language):
        """ """
        try:
            return self.translations[language]
        except KeyError, error:
            print error

    def get_unicode_langs(self):
        """ """
        return self.getGlossaryEngine().unicode_langs

    def display_unicode_langs(self, language, charset=""):
        """ """
        if charset=="":
            return self.utToUTF8(language, self.get_language_charset(language))
        else:
            return self.utToUTF8(language, charset)

    def convert_element(self, synonyms=[], REQUEST=None):
        """convert element to synonym"""
        synid = self.id
        ob=self.aq_parent
        ob.manage_delObjects(synid)
        ob.manage_addGlossarySynonym(synid, synonyms)
        if synonyms == []:
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('convert_to_synonym_html?syn=0')
        else:
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('convert_to_synonym_html')


    #####################
    #   MANAGEMENT TABS #
    #####################

    def manageBasicProperties(self, name='', el_type='', source=[], el_context='', comment='', used_for_1='', used_for_2='', definition='',
        definition_source_url='', subjects='', disabled=0, approved =0, long_definition='', QA_needed=0, REQUEST=None):
        """ manage basic properties for EEAGlossaryElement """
        self.name = name
        self.el_type = el_type
        self.source = source
        self.el_context = el_context
        self.comment = comment
        self.used_for_1 = used_for_1
        self.used_for_2 = used_for_2
        self.definition = definition
        self.definition_source_url = definition_source_url
        self.subjects = subjects
        self.disabled = disabled
        self.approved = approved
        self.long_definition = long_definition
        self.QA_needed = QA_needed
        self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')

    def manageMediaProperties(self, image_url='', flash_url='', REQUEST=None):
        """ manage media properties for EEAGlossaryElement """
        self.image_url = image_url
        self.flash_url = flash_url
        self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=1&save=ok')

    def manageLinksProperties(self, old_link='', link='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.links.append(link)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.links.remove(old_link)
                self.links.append(link)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for link in self.utConvertToList(ids):
                self.links.remove(link)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    def manageActionsProperties(self, old_action='', action='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.actions.append(action)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.actions.remove(old_action)
                self.actions.append(action)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for action in self.utConvertToList(ids):
                self.actions.remove(action)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    all_translations_html = DTMLFile("dtml/EEAGlossaryElement/all_translations", globals())
    check_translation_html = DTMLFile("dtml/EEAGlossaryElement/check_translation", globals())

    manage_properties_html = DTMLFile("dtml/EEAGlossaryElement/properties", globals())
    media_html = DTMLFile("dtml/EEAGlossaryElement/properties_media", globals())
    actions_html = DTMLFile("dtml/EEAGlossaryElement/properties_actions", globals())
    basic_html = DTMLFile("dtml/EEAGlossaryElement/properties_basic", globals())

    preview_html = DTMLFile("dtml/EEAGlossaryElement/preview", globals())
    custom_properties_html = DTMLFile("dtml/EEAGlossaryElement/custom_prop", globals())
    synonym_html = DTMLFile("dtml/EEAGlossaryElement/synonym", globals())
    convert_to_synonym_html = DTMLFile("dtml/EEAGlossaryElement/convert_to_synonym", globals())
    history_html = DTMLFile("dtml/EEAGlossaryElement/history", globals())
    index_html = DTMLFile("dtml/EEAGlossaryElement/index", globals())
    main_content_html = DTMLFile("dtml/EEAGlossaryElement/main_content", globals())

InitializeClass(EEAGlossaryElement)