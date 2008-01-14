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
# The Original Code is EEAGlossary version 1.0.0
#
# The Initial Developer of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Finsiel Romania
# Antonio De Marinis, EEA
# Cornel Nitu, Finsiel Romania


# python imports
import string

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports
from EEAGlossary_utils import utils
from EEAGlossary_utils import catalog_utils
from toutf8 import toUTF8
from EEAGlossary_constants import *

class ElementBasic:
    """ define the basic properties for EEAGlossaryElement """

    def __init__(self, name, el_type, source, el_context, comment,
            definition, definition_source_publ, definition_source_publ_year, definition_source_url, 
            definition_source_org, definition_source_org_fullname, long_definition):
        """ constructor """

        self.name = name
        self.el_type = el_type
        self.source = source
        self.el_context = el_context
        self.comment = comment
        self.definition = definition

        self.definition_source_publ = definition_source_publ
        self.definition_source_publ_year = definition_source_publ_year
        self.definition_source_url = definition_source_url
        self.definition_source_org = definition_source_org
        self.definition_source_org_fullname = definition_source_org_fullname

        self.long_definition = long_definition

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

InitializeClass(ElementBasic)

manage_addGlossaryElement_html = DTMLFile('dtml/EEAGlossaryElement/add', globals())

def manage_addGlossaryElement(self, name='', el_type='', source='', subjects=[], el_context='',
    comment='', definition='', definition_source_publ='', definition_source_publ_year='', 
    definition_source_url='', definition_source_org='', definition_source_org_fullname='',
    long_definition='', disabled=0, approved=1, QA_needed=0, image_url='', flash_url='',
    links=[], actions=[], translations={}, synonym=[], id='', bad_translations=[], REQUEST=None):
    """ adds a new EEAGlossaryElement object """
    #remove the spaces from name
    if id == '':  id = self.ut_makeId(name)
    ob = EEAGlossaryElement(id, name, el_type, source, subjects, el_context, comment,
            definition, definition_source_publ, definition_source_publ_year, definition_source_url, 
            definition_source_org, definition_source_org_fullname, long_definition, disabled, approved, QA_needed, 
            image_url, flash_url, links, actions, translations, synonym, bad_translations)
    self._setObject(id, ob)
    element_obj = self._getOb(id)
    element_obj.subjects = self.get_subject_by_codes(subjects)
    element_obj.load_translations_list()
    element_obj.set_translations_list('English', element_obj.name)

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
        {'label':'Help',                    'action':'element_help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id, name, el_type, source, subjects, el_context, comment, definition, 
            definition_source_publ, definition_source_publ_year, definition_source_url, definition_source_org, 
            definition_source_org_fullname, long_definition, disabled, approved, QA_needed,  image_url, flash_url, 
            links, actions, translations, synonym, bad_translations):
        """ constructor """
        self.id = id
        self.image_url = image_url
        self.flash_url = flash_url
        self.links = links
        self.actions = actions
        self.all_langs_list= {}
        self.history={}
        self.subjects = subjects
        self.disabled = disabled
        self.approved = approved
        self.QA_needed = QA_needed
        self.synonym = synonym
        self.bad_translations = bad_translations
        ElementBasic.__dict__['__init__'](self, name, el_type, source, el_context, comment, 
            definition, definition_source_publ, definition_source_publ_year, definition_source_url, 
            definition_source_org, definition_source_org_fullname, long_definition)

    def is_published(self):
        """ test if current element is published """
        return (self.approved and (not self.disabled))

    def is_image_url(self):
        """ test if the current element has an image URL """
        return not (self.utIsEmptyString(self.image_url) or 'image_url' in self.get_hidden_list())

    def is_long_definition(self):
        """ test if the current element has a long definition """
        return not (self.utIsEmptyString(self.long_definition) or 'long_definition' in self.get_hidden_list())

    def is_definition_source(self):
        """ test if the current element has a definition source """
        #return not self.utIsEmptyString(self.definition_source_publ)
        return not (self.utIsEmptyString(self.definition_source_publ) or 'definition_source_publ' in self.get_hidden_list())

    def is_duplicate(self, p_id):
        """test if is the same element"""
        return p_id == self.id

    def has_synonyms(self):
        """ test if this element has any synonym """
        return len(self.getSynonyms())

    def getSynonyms(self):
        """ returns list of synonyms for this element. 
        Also known as 'Use For' relation in thesauri system and 'alternative label' in ontology systems."""
        return self.cu_search_synonyms()

    def getDefinitionSource(self):
        """ returns a human readable string describing the original source of term definitions. """
        return self.definition_source_publ;


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
    def get_history_by_language(self, language):
        """ get the languages """
        try:
            history = self.history[language]
            self.utSortListOfDictionariesByKey(history, 'time', 1)
            return history
        except:
            return []

    def set_history(self, lang, translation):
        """ set the languages """
        try:
            self.history[lang].append({'trans':translation,'time':self.utISOFormat(), 'user':self.getAuthenticatedUser()})
        except KeyError:
            self.history[lang] = [{'trans':translation,'time':self.utISOFormat(), 'user':self.getAuthenticatedUser()}]

    ############################
    #  TRANSLATIONS FUNCTIONS  #
    ############################
    def check_allowed_translations(self, language):
        """ check if the authenticated user has the permission to change the translation """
        role = EEA_GLOSSARY_ROLES_PREFIX + language
        if (role in self.getAuthenticatedUserRoles()) or self.REQUEST.AUTHENTICATED_USER.has_role(role, self):
            return 1
        return 0

    def get_translation_by_language(self, language):
        """ get translation by language """
        try:    return self.utUtf8Encode(getattr(self, language))
        except: return ''

    def check_if_no_translations(self):
        """ check if translations['translation'] != '': """
        for lang in self.get_english_names():
            if getattr(self, lang) != '':
                return 1
        return 0

    def set_translations_list(self, language, translation):
        """ set the languages """
        setattr(self, language, translation)

    def del_translation_by_language(self, language):
        """ remove a translation from list """
        setattr(self, language, '')

    def load_translations_list (self):
        """ load languages """
        for lang in self.get_english_names():
            setattr(self, lang, '')

    def convert_element(self, synonyms=[], REQUEST=None):
        """convert element to synonym """
        synid = self.id
        synau = self.absolute_url(1)
        synname=self.name
        synapproved=self.approved
        syndisabled=self.disabled
        folder=self.aq_parent
        #delete old element before adding synonym with same id
        folder.manage_delObjects(synid)
        folder.manage_addGlossarySynonym(synid, synonyms)
        synobject=folder._getOb(synid)
        #preserve old element metadata
        synobject.manageSynonymOtherProperties(synname, syndisabled, synapproved)
        folder.utElementSynAdd([],synau)
        if synonyms == []:
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('convert_to_synonym_html?syn=0')
        else:
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('convert_to_synonym_html')

    def manageTranslations(self, lang_code='', translation='', REQUEST=None):
        """ save translation for a language """
        if not lang_code:
            return REQUEST.RESPONSE.redirect('check_translation_html')
        if self.check_allowed_translations(lang_code):
            self.set_history(lang_code, translation)
            self.set_translations_list(lang_code, translation)
            self.cu_recatalog_object(self)
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('check_translation_html')

    #####################
    #  BASIC PROPERTIES #
    #####################
    def manageBasicProperties(self, name='', el_type='', source=[], el_context='', comment='', definition='', 
            definition_source_publ='', definition_source_publ_year='', definition_source_url='', definition_source_org='', 
            definition_source_org_fullname='', subjects=[], disabled=0, approved =0, long_definition='', QA_needed=0, REQUEST=None):
        """ manage basic properties for EEAGlossaryElement """
        self.name = name
        self.el_type = el_type
        self.source = source
        self.el_context = el_context
        self.comment = comment
        self.definition = definition
        self.definition_source_url = definition_source_url
        self.subjects = self.get_subject_by_codes(subjects)
        self.disabled = disabled
        self.approved = approved
        self.definition_source_publ = definition_source_publ
        self.definition_source_publ_year = definition_source_publ_year
        self.definition_source_url = definition_source_url
        self.definition_source_org = definition_source_org
        self.definition_source_org_fullname = definition_source_org_fullname
        self.long_definition = long_definition
        self.QA_needed = QA_needed
        self._p_changed = 1
        self.cu_recatalog_object(self)
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
        """ return links """
        return self.links

    def set_link(self, value):
        """ set a link """
        self.links.append(value)

    def del_link(self, value):
        """ delete a link """
        self.links.remove(value)

    def manageLinksProperties(self, old_link='', link='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.set_link(link)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(link) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.del_link(old_link)
                self.set_link(link)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            for link in self.utConvertToList(ids):
                self.del_link(link)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    #######################
    #  ACTIONS PROPERTIES #
    #######################
    def get_actions(self):
        """ return actions """
        return self.actions

    def set_action(self, value):
        """ set an action """
        self.actions.append(value)

    def del_action(self, value):
        """ delete an action """
        self.actions.remove(value)

    def manageActionsProperties(self, old_action='', action='', ids='', REQUEST=None):
        """ manage actions properties for EEAGlossaryElement """
        if self.utAddObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.set_action(action)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(action) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            else:
                self.del_action(old_action)
                self.set_action(action)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2')
            for action in self.utConvertToList(ids):
                self.del_action(action)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=2&save=ok')

    def manage_afterAdd(self, item, container):
        """ this method is called, whenever _setObject in ObjectManager gets called """
        SimpleItem.inheritedAttribute('manage_afterAdd')(self, item, container)
        self.cu_catalog_object(self)

    def manage_beforeDelete(self, item, container):
        """ this method is called, when the object is deleted """
        if self.meta_type == EEA_GLOSSARY_ELEMENT_METATYPE:
            self.utSynonymElDel()
        else:
            self.utElementSynDel()
        SimpleItem.inheritedAttribute('manage_beforeDelete')(self, item, container)
        self.cu_uncatalog_object(self)

    #####################
    #   MANAGEMENT TABS #
    #####################
    all_translations_html = DTMLFile("dtml/EEAGlossaryElement/all_translations", globals())
    check_translation_html = DTMLFile("dtml/EEAGlossaryElement/check_translation", globals())
    manage_properties_html = DTMLFile("dtml/EEAGlossaryElement/properties", globals())
    media_html = DTMLFile("dtml/EEAGlossaryElement/properties_media", globals())
    actions_html = DTMLFile("dtml/EEAGlossaryElement/properties_actions", globals())
    basic_html = DTMLFile("dtml/EEAGlossaryElement/properties_basic", globals())
    view_languages_html = DTMLFile("dtml/EEAGlossaryElement/view_languages", globals())
    view_elements_html = DTMLFile("dtml/EEAGlossaryElement/view_elements", globals())
    view_box_html = DTMLFile("dtml/EEAGlossaryElement/view_box", globals())

    element_help_html = DTMLFile("dtml/EEAGlossaryElement/help", globals())

    preview_html = DTMLFile("dtml/EEAGlossaryElement/preview", globals())
    custom_properties_html = DTMLFile("dtml/EEAGlossaryElement/custom_prop", globals())
    synonym_html = DTMLFile("dtml/EEAGlossaryElement/synonym", globals())
    convert_to_synonym_html = DTMLFile("dtml/EEAGlossaryElement/convert_to_synonym", globals())
    history_html = DTMLFile("dtml/EEAGlossaryElement/history", globals())
    index_html = DTMLFile("dtml/EEAGlossaryElement/index", globals())
    main_content_html = DTMLFile("dtml/EEAGlossaryElement/main_content", globals())
    show_related_html = DTMLFile("dtml/EEAGlossaryElement/show_related", globals())

    definition_html = DTMLFile("dtml/EEAGlossaryElement/definition", globals())
    

InitializeClass(EEAGlossaryElement)