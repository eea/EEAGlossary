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
#$Id: EEAGlossaryElement.py,v 1.32 2004/05/10 15:37:01 finrocvs Exp $

# python imports
import string

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports
from EEAGlossary_utils import utils
from EEAGlossary_utils import catalog_utils

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
    element_obj.subjects = self.get_subject_by_codes(subjects)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryElement(SimpleItem, ElementBasic, utils, catalog_utils):
    """ EEAGlossaryElement """

    meta_type = EEA_GLOSSARY_ELEMENT_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/element.gif'

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
        self.translations = []
        self.all_langs_list= {}
        self.history=[]
        ElementBasic.__dict__['__init__'](self, name, el_type, source, [], el_context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed)

    def is_published (self):
        return (self.approved and not self.disabled)

    def is_image_url (self):
        return not (self.utIsEmptyString(self.image_url) or 'image_url' in self.get_hidden_list())

    def is_long_definition (self):
        return not (self.utIsEmptyString(self.long_definition) or 'long_definition' in self.get_hidden_list())

    def is_definition_source(self):
        return not (self.utIsEmptyString(self.definition_source_url) or 'definition_source_url' in self.get_hidden_list())

    ############################
    #     SUBJECTS FUNCTIONS   #
    ############################
    def code_in_subjects(self, code):
        """ check if code is in the list """
        for subj_info in self.subjects:
            if subj_info['code'] == code:
                return 1
        return 0

    def get_subjects(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.subjects, 'code')
        return self.subjects

    def set_subjects(self, code, name):
        """ set the languages """
        append = self.subjects.append
        append({'code':code, 'name':name})

    def del_subject(self, code):
        """ remove a language from list """
        for subj_info in self.subjects:
            if subj_info['code'] == code:
                self.subjects.remove(subj_info)

    ############################
    #     HISTORY FUNCTIONS    #
    ############################
    def get_history(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.history, 'lang')
        return self.history

    def set_history(self, lang, translation):
        """ set the languages """
        self.history.append({'lang':lang, 'trans':translation,'time':self.utISOFormat(), 'user':self.getAuthenticatedUser()})

    def del_history(self, lang):
        """ remove a language from history list """
        for hist_info in self.history:
            if hist_info['lang'] == lang:
                self.history.remove(hist_info)

    ############################
    #  TRANSLATIONS FUNCTIONS  #
    ############################
    def check_allowed_translations(self, language):
        """ check if the authenticated user has the permission to change the translation"""
        role = EEA_GLOSSARY_ROLES_PREFIX + language
        if (role in self.getAuthenticatedUserRoles()) or self.REQUEST.AUTHENTICATED_USER.has_role(role, self):
            return 1
        return 0

    def get_translation_by_language(self, language):
        """ get translation by language """
        for trans_info in self.get_translations_list():
            if trans_info['language'] == language:
                return trans_info['translation']

    def get_translations_list(self):
        """ get the languages """
        self.utSortListOfDictionariesByKey(self.translations, 'language')
        return self.translations

    def check_if_no_translations(self):
        """ check if translations['translation'] != '':"""
        for trans_info in self.get_translations_list():
            if trans_info['translation']!='':
                return 1
        return 0

    def set_translations_list(self, language, translation):
        """ set the languages """
        self.translations.append({'language':language, 'translation':translation})

    def remove_translation_from_list(self, language):
        """ remove a language from list """
        for lang_info in self.translations:
            if lang_info['language'] == language:
                self.translations.remove(lang_info)

    def del_translation_by_language(self, language):
        """ remove a translation from list """
        for lang_info in self.translations:
            if lang_info['language'] == language:
                lang_info['translation'] = ''

    def del_translation_by_translation(self, translation):
        """ remove a translation from list """
        for lang_info in self.translations:
            if lang_info['translation'] == translation:
                lang_info['translation'] = ''

    def load_translations_list (self):
        for lang in self.get_english_names():
            self.set_translations_list(lang, '')

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

    def manageTranslations(self, lang_code='', translation='', REQUEST=None):
        """ save translation for a language"""
        if not lang_code:
            return 
        if self.check_allowed_translations(lang_code):
            #charset = self.get_language_charset(lang_code)
            #encode_translation = self.display_unicode_langs(translation, charset)
            self.set_history(lang_code, translation)
            self.remove_translation_from_list(lang_code)
            self.set_translations_list(lang_code, translation)
            self._p_changed = 1
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('check_translation_html')

    #####################
    #  BASIC PROPERTIES #
    #####################
    def manageBasicProperties(self, name='', el_type='', source=[], el_context='', comment='', used_for_1='', used_for_2='', definition='',
        definition_source_url='', subjects=[], disabled=0, approved =0, long_definition='', QA_needed=0, REQUEST=None):
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
        self.subjects = self.get_subject_by_codes(subjects)
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

    #######################
    #  LINKS PROPERTIES   #
    #######################
    def get_links(self):
        return self.links

    def set_link(self, value):
        self.links.append(value)

    def del_link(self, value):
        self.links.remove(value)

    def manageLinksProperties(self, old_link='', link='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.set_link(link)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.del_link(old_link)
                self.set_link(link)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for link in self.utConvertToList(ids):
                self.del_link(link)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    #######################
    #  ACTIONS PROPERTIES #
    #######################
    def get_actions(self):
        return self.actions

    def set_action(self, value):
        self.actions.append(value)

    def del_action(self, value):
        self.actions.remove(value)

    def manageActionsProperties(self, old_action='', action='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.set_action(action)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                self.del_action(old_action)
                self.set_action(action)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            for action in self.utConvertToList(ids):
                self.del_action(action)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    def manage_afterAdd(self, item, container):
        """ This method is called, whenever _setObject in ObjectManager gets called."""
        SimpleItem.inheritedAttribute('manage_afterAdd')(self, item, container)
        self.cu_catalog_object(self.getGlossaryCatalog(), self)

    def manage_beforeDelete(self, item, container):
        """ This method is called, when the object is deleted. """
        SimpleItem.inheritedAttribute('manage_beforeDelete')(self, item, container)
        self.cu_uncatalog_object(self.getGlossaryCatalog(), self)

    #####################
    #   MANAGEMENT TABS #
    #####################
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

    definition_html = DTMLFile("dtml/EEAGlossaryElement/definition", globals())

InitializeClass(EEAGlossaryElement)