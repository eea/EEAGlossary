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
import whrandom
from os.path import join

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass, package_home
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
import AccessControl.User
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCTextIndex.ZCTextIndex import manage_addLexicon
import Products
from ZPublisher.HTTPRequest import record

# product imports
import EEAGlossaryFolder
from EEAGlossary_utils import utils
from toutf8 import toUTF8
from EEAGlossary_utils import catalog_utils
from EEAGlossary_export import glossary_export
from EEAGlossary_constants import *
from parsers.xliff_parser import xliff_parser

try:
    from Products.TextIndexNG2 import TextIndexNG
    TNG2_exists = 1
except:
    TNG2_exists = 0

manage_addGlossaryCentre_html = DTMLFile('dtml/EEAGlossaryCentre/add', globals())
def manage_addGlossaryCentre(self, id, title='', description='', max_related='', REQUEST=None):
    """ Adds a new EEAGlossaryCentre object """
    max_related = EEA_GLOSSARY_MAX_REALTED
    ob = EEAGlossaryCentre(id, title, description, max_related)
    self._setObject(id, ob)
    obj = self._getOb(id)
    obj.loadProperties()
    obj.addCatalog()
    obj.loadRDF()

    style_css = open(join(EEAGLOSSARY_PATH,'dtml','EEAGlossaryCentre','style_presentation.dtml'))
    content = style_css.read()
    style_css.close()
    ob.manage_addDTMLMethod('style_presentation_css', title='', file=content)

    file = open(join(EEAGLOSSARY_PATH, 'www', 'img_search_med.gif'), 'rb')
    content = file.read()
    file.close()
    ob.manage_addImage(id='search_img', title='Search Image - you can upload it from here', file='')
    img_ob = ob._getOb('search_img')
    img_ob.update_data(data=content)


    obj._p_changed = 1
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


class EEAGlossaryCentre(Folder, utils, catalog_utils, glossary_export, toUTF8):
    """ EEAGlossaryCentre """

    meta_type = EEA_GLOSSARY_CENTRE_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = "misc_/EEAGlossary/glossary.gif"

    manage_options =((Folder.manage_options[0],) +
                ({'label':'Properties',         'action':'manage_properties_html'},
                {'label':'View',                'action':'preview_html'},
                {'label':'Contexts Reference',  'action':'contexts_html'},
                {'label':'Check list',          'action':'check_list_html'},
                {'label':'Change Password',     'action':'change_pass_html'},
                {'label':'Export',              'action':'export_html'},
                {'label':'Import',              'action':'import_html'},
                {'label':'Management',          'action':'management_page_html'},
                {'label':'Translations',          'action':'translations_html'},
                {'label':'Help',                'action':'centre_help_html'},
                {'label':'Undo',                'action':'manage_UndoForm'},)
                )

    def __setstate__(self,state):
        """ """
        EEAGlossaryCentre.inheritedAttribute('__setstate__')(self, state)
        if not hasattr(self, 'max_related'):
            self.max_related = 10

    security = ClassSecurityInfo()

    def __init__(self, id, title, description, max_related):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        self.max_related = max_related
        self.types_list = []
        self.languages_list = []
        self.stop_words_list = []
        self.subjects_list = []

        self.search_langs = []
        self.published = 0
        self.hidden_fields = []
        self.alpha_list = list(string.uppercase + string.digits)
        self.contact_trans = {}
        self.contact_technic = {}
        utils.__dict__['__init__'](self)
        toUTF8.__dict__['__init__'](self)
        glossary_export.__dict__['__init__'](self)

    def all_meta_types(self, interfaces=None):
        """ Can contain any kind of objects plus EWFolder """
        meta_types = [
            {'name': EEA_GLOSSARY_FOLDER_METATYPE, 'action': 'manage_addGlossaryFolder_html', 'product': EEA_GLOSSARY_PRODUCT_NAME},
        ]
        for x in Products.meta_types:
            meta_types.append(x)
        return meta_types

    manage_addGlossaryFolder_html = EEAGlossaryFolder.manage_addGlossaryFolder_html
    manage_addGlossaryFolder = EEAGlossaryFolder.manage_addGlossaryFolder

    def getCenterId(self):
        """ """
        return self.id

    def getCenterURL(self, p_method):
        """ """
        return self.absolute_url(0) + '/' + p_method

    #####################
    # LOAD PROPERTIES   #
    #####################
    def addCatalog(self):
        """ add the default catalog """
        id_catalog = EEA_GLOSSARY_CATALOG_NAME
        glossary_catalog = ZCatalog(id_catalog)
        try:
            self._setObject(id_catalog, glossary_catalog)
            self.__addLexicon(self._getOb(id_catalog))
        except: pass
        catalog_obj = self._getOb(id_catalog)

        #create indexes
        for lang in self.get_english_names():
            if TNG2_exists:
                index_extra = record()
                index_extra.default_encoding = 'utf-8'
                try:    catalog_obj.manage_addIndex(lang, 'TextIndexNG2',index_extra)
                except:    pass
            else:
                try: self.__addZCTextIndex(lang, catalog_obj)
                except: pass

        try: self.__addZCTextIndex('definition', catalog_obj)
        except: pass
        try: self.__addZCTextIndex('name', catalog_obj)
        except: pass
        try: self.__addZCTextIndex('title', catalog_obj)
        except: pass

        try: catalog_obj.addIndex('approved', 'FieldIndex')
        except: pass
        try: catalog_obj.addIndex('bobobase_modification_time', 'FieldIndex')
        except: pass
        try: catalog_obj.addIndex('id', 'FieldIndex')
        except: pass
        try: catalog_obj.addIndex('meta_type', 'FieldIndex')
        except: pass
        try: catalog_obj.addIndex('path', 'PathIndex')
        except: pass
        try: catalog_obj.addIndex('synonyms', 'KeywordIndex')
        except: pass

        #deprecated, used for Zope 2.6.4
        try: catalog_obj.addIndex('definition', 'TextIndex')
        except: pass
        try: catalog_obj.addIndex('name', 'TextIndex')
        except: pass
        try: catalog_obj.addIndex('title', 'TextIndex')
        except: pass

       #create metadata
        try: catalog_obj.addColumn('id')
        except: pass
        try: catalog_obj.addColumn('title')
        except: pass
        try: catalog_obj.addColumn('meta_type')
        except: pass
        try: catalog_obj.addColumn('bobobase_modification_time')
        except: pass
        try: catalog_obj.addColumn('summary')
        except: pass
        try: catalog_obj.addColumn('name')
        except: pass

    def __addZCTextIndex(self, name, catalog):
        #Add a ZCTextIndex
        p_extras = MyData()
        p_extras.doc_attr = name
        p_extras.index_type = 'Okapi BM25 Rank'
        p_extras.lexicon_id = 'Lexicon'
        catalog.addIndex(name, 'ZCTextIndex', p_extras)

    def __addLexicon(self, catalog):
        #It adds a default lexicon with 'Lexicon' id.
        elements = []
        wordSplitter = MyData()
        wordSplitter.group = 'Word Splitter'
        wordSplitter.name = 'HTML aware splitter'

        caseNormalizer = MyData()
        caseNormalizer.group = 'Case Normalizer'
        caseNormalizer.name = 'Case Normalizer'

        stopWords = MyData()
        stopWords.group = 'Stop Words'
        stopWords.name = 'Remove listed stop words only'

        elements.append(wordSplitter)
        elements.append(caseNormalizer)
        elements.append(stopWords)
        id = 'Lexicon'
        title = 'Default Lexicon'

        manage_addLexicon(catalog, id, title, elements)

    def loadProperties(self):
        """ load the properties from engine """
        from copy import copy
        engine = self.getGlossaryEngine()
        self.languages_list = copy(engine.get_languages_list())
        self.stop_words_list = copy(engine.get_stop_words_list())
        self.subjects_list = copy(engine.get_subjects_list())
        self.types_list = copy(engine.get_types_list())
        self.search_langs = copy(engine.get_searchable_langs())
        self.contact_trans = copy(engine.get_translation_persons())
        self.contact_technic = copy(engine.get_contact_persons())

    ######################
    # TEST PERMISSIONS   #
    ######################
    def getAuthenticatedUser(self):
        """ return the authenticated user """
        return self.REQUEST.AUTHENTICATED_USER.getUserName()

    def getAuthenticatedUserRoles(self):
        """ return the list of roles for authenticated user """
        return self.REQUEST.AUTHENTICATED_USER.getRoles()

    def is_AuthenticatedUserRoles(self):
        """ test if Quality Controller in roles"""
        return 'Quality Controller' in self.getAuthenticatedUserRoles()

    def canManageGlossary(self):
        """ test if the user can manage the glossary"""
        return ('Manager' in self.getAuthenticatedUserRoles()) or ('GlossaryManager' in self.getAuthenticatedUserRoles())

    def isManager(self):
        """test if the user has manager role """
        return 'Manager' in self.getAuthenticatedUserRoles()

    #####################
    # BASIC FUNCTIONS   #
    #####################
    def getGlossaryEngine(self):
        """ return the glossary engine object """
        return self.unrestrictedTraverse(EEA_GLOSSARY_ENGINE_NAME, None)

    def getGlossaryCatalog(self):
        """ return the glossary catalog object """
        return self._getOb(EEA_GLOSSARY_CATALOG_NAME)

    def manageBasicProperties(self, title='', description='', published=0, max_related=10, REQUEST=None):
        """ manage basic properties for EEAGlossaryCentre """
        self.title = title
        self.description = description
        self.published = published
        self.max_related = max_related
        self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=0&save=ok')

    ##########################
    #   CONTACT  FUNCTIONS   #
    ##########################

    def get_contact_persons(self):
        """ return the technic persons list"""
        return self.contact_technic

    def get_translation_persons(self):
        """ return the translation persons list"""
        return self.contact_trans

    def manageTechnicProperties(self, ids=[], old_email='', email='', phone='', name='', REQUEST=None):
        """ manage tecnical contacts for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            else:
                self.contact_technic[email] = (name, phone)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            else:
                del self.contact_technic[old_email]
                self.contact_technic[email] = (name, phone)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            for email in self.utConvertToList(ids):
                del self.contact_technic[email]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7&save=ok')

    def manageTranslatorProperties(self, ids=[], old_email='', email='', phone='', name='', REQUEST=None):
        """ manage translator contacts for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            else:
                self.contact_trans[email] = (name, phone)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(email) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            else:
                del self.contact_trans[old_email]
                self.contact_trans[email] = (name, phone)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7')
            for email in self.utConvertToList(ids):
                del self.contact_trans[email]
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=7&save=ok')

    #########################
    #   STOP WORD FUNCTIONS #
    #########################
    def get_stop_words_list(self):
        """ get the stop words """
        self.utSortListOfDictionariesByKey(self.stop_words_list, 'stop_word')
        return self.stop_words_list

    def get_stop_words(self):
        """ return the words list """
        word_list = []
        l_list = self.get_stop_words_list()
        for word in l_list:
            word_list.append(word['stop_word'])
        return word_list

    def set_stop_words_list(self, text):
        """ set the stop words """
        append = self.stop_words_list.append
        append({'stop_word':text})

    def del_stop_words_from_list(self, stop_word):
        """ remove a stop word from list """
        for word in self.stop_words_list:
            if word['stop_word'] == stop_word:
                self.stop_words_list.remove(word)

    def check_stop_words_exists(self, text):
        """ check if this stop word exists """
        ret = 1
        for stop_word in self.stop_words_list:
            if stop_word['stop_word'] == text:
                ret = 0
        return ret

    def manageStopWordsProperties(self, ids='', stop_word='', old_stop_word='', REQUEST=None):
        """ manage stop words for EEAGlossaryEngine """
        if self.utAddObjectAction(REQUEST):
            if string.strip(stop_word)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=8')
            else:
                if self.check_stop_words_exists(stop_word):
                    self.set_stop_words_list(stop_word)
                    self._p_changed = 1
                else:
                    return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=8')
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(stop_word)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=8')
            else:
                self.del_stop_words_from_list(old_stop_word)
                self.set_stop_words_list(stop_word)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=8')
            for word in self.utConvertToList(ids):
                self.del_stop_words_from_list(word)
                self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=8&save=ok')


    ##########################
    #   SUBJECTS FUNCTIONS   #
    ##########################
    def get_subjects_list(self):
        """ get the subjects """
        self.utSortListOfDictionariesByKey(self.subjects_list, 'code')
        return self.subjects_list

    def set_subjects_list(self, code, name):
        """ set the subjects """
        self.subjects_list.append({'code':code, 'name':name})

    def del_subject_from_list(self, code):
        """ remove a subjects from list """
        for subj_info in self.subjects_list:
            if subj_info['code'] == code:
                self.subjects_list.remove(subj_info)

    def get_subject_by_name(self, names):
        """ return corresponding codes """
        results = []
        names = self.utConvertToList(names)
        for subj_info in self.subjects_list:
            if subj_info['name'] in names:
                results.append(subj_info['code'])
        return results

    def get_subject_by_codes(self, codes):
        """ return the subjects list """
        results = []
        codes = self.utConvertToList(codes)
        for subj_info in self.subjects_list:
            if subj_info['code'] in codes:
                results.append(subj_info)
        return results

    def check_subjects_exists(self, code):
        """ check if this subject exists """
        ret = 1
        for l_code in self.subjects_list:
            if l_code['code'] == code:
                ret = 0
        return ret

    def manageSubjectsProperties(self, ids=[], old_code='', code='', name='', REQUEST=None):
        """ manage subjects for EEAGlossaryCentre"""
        if self.utAddObjectAction(REQUEST):
            if string.strip(code) == '' or string.strip(name) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
            else:
                if self.check_subjects_exists(code):
                    self.set_subjects_list(code, name)
                    self._p_changed = 1
                else:
                    return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=3')
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

    def get_language_codes(self):
        """ get the codes from languages list """
        results = []
        for k in self.get_languages_list():
            results.append(k['lang'])
        return results

    def get_language_code(self, language):
        """ get the charset for a specific language """
        for k in self.get_languages_list():
            if k['english_name'] == language:
                return k['lang']

    def get_language_by_code(self, lang_code):
        """ get the english name given the code """
        for k in self.get_languages_list():
            if k['lang'] == lang_code:
                return k['english_name']

    def get_language_charset(self, language):
        """ get the charset for a specific language """
        for k in self.get_languages_list():
            if k['english_name'] == language:
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
        """ display unicode languages """
        if charset=="":
            return self.toutf8(language, self.get_language_charset(language))
        else:
            return self.toutf8(language, charset)

    def check_language_exists(self, english_name):
        """ check if this language exists """
        ret = 1
        for eng_lang in self.languages_list:
            if eng_lang['english_name'] == english_name:
                ret = 0
        return ret

    def manageLanguagesProperties(self, ids='', lang='', charset='', english_name='', old_english_name='', REQUEST=None):
        """ manage languages for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(lang)=='' or string.strip(charset)=='' or string.strip(english_name)=='':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
            else:
                if self.check_language_exists(english_name):
                    self.set_languages_list(lang, charset, english_name)
                    self._p_changed = 1
                else:
                    return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=4')
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
        """ return the searchable languages list"""
        return self.search_langs

    def set_search_langs(self, value):
        """ set the searchable languages list"""
        self.search_langs.append(value)

    def del_search_langs(self, value):
        """ delete from searchable languages list"""
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
        """ return the types list """
        return self.types_list

    def set_types_list(self, value):
        """ set the types list """
        self.types_list.append(value)

    def del_types_list(self, value):
        """ delete from types list """
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
        """ return the hidden properties list """
        return self.hidden_fields

    def set_hidden_list(self, value):
        """ set the hidden properties list """
        self.hidden_fields.append(value)

    def del_hidden_list(self, value):
        """ remove from hidden fields list """
        self.hidden_fields.remove(value)

    def check_hidden_exists(self, field):
        """ check if this hidden field exists """
        ret = 1
        for l_field in self.hidden_fields:
            if l_field == field:
                ret = 0
        return ret

    def manageHiddenProperties(self, old_field='', field='', ids='', REQUEST=None):
        """ manage the hidden properties for EEAGlossaryCentre """
        if self.utAddObjectAction(REQUEST):
            if string.strip(field) == '':
                return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
            else:
                if self.check_hidden_exists(field):
                    self.set_hidden_list(field)
                    self._p_changed = 1
                else:
                    return REQUEST.RESPONSE.redirect('manage_properties_html?pagetab=6')
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
        """ return the alpha list """
        return self.alpha_list

    def set_alpha_list(self, value):
        """ set the alpha list """
        self.alpha_list.append(value)

    def del_alpha_list(self, value):
        """ remove from alpha list """
        self.alpha_list.remove(value)

    def manageAlphaProperties(self, old_alpha='', alpha='', ids='', REQUEST=None):
        """ manage the alpha list for EEAGlossaryCentre """
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

    ######################################
    # GLOSSARY ADMINISTRATION FUNCTIONS  #
    ######################################
    def get_not_approved(self):
        """.return the elements&synonyms not approved """
        lst_not_approved = []
        append = lst_not_approved.append
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if (not obj.approved):
                append(obj)
        return lst_not_approved

    def get_approved(self):
        """.return the elements&synonyms approved """
        lst_approved = []
        append = lst_approved.append
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if obj.approved:
                append(obj)
        return lst_approved

    def get_disabled(self):
        """.return the elements&synonyms disabled """
        lst_disabled = []
        append = lst_disabled.append
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if obj.disabled:
                append(obj)
        return lst_disabled

    def get_not_disabled(self):
        """ return the elements&synonym not disabled """
        not_disabled_terms = 0
        not_disabled_concepts = 0
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if (obj.disabled == 0) and (obj.meta_type == EEA_GLOSSARY_ELEMENT_METATYPE):
                not_disabled_concepts += 1
            if obj.disabled == 0:
                not_disabled_terms += 1
        return [not_disabled_terms, not_disabled_concepts]

    def get_not_published(self):
        """.return the elements&synonyms not published """
        lst_not_published = []
        append = lst_not_published.append
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if (not obj.approved or obj.disabled):
                append(obj)
        return lst_not_published

    def get_published(self, path=''):
        """.return the elements&synonyms published """
        lst_published = []
        append = lst_published.append
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order='', path=path):
            if (obj.approved and not obj.disabled):
                append(obj)
        return lst_published
        
    def get_terms_stats(self):
        """ return the stats for all elements&synonyms"""
        published_terms = 0
        published_concepts = 0
        not_disabled_terms = 0
        not_disabled_concepts = 0
        for obj in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order=''):
            if (not obj.disabled and obj.approved):
                published_terms += 1
            if (not obj.disabled) and (obj.approved) and (obj.meta_type == EEA_GLOSSARY_ELEMENT_METATYPE):
                published_concepts += 1
            if (not obj.disabled) and (obj.meta_type == EEA_GLOSSARY_ELEMENT_METATYPE):
                not_disabled_concepts += 1
            if not obj.disabled:
                not_disabled_terms += 1
        return [published_terms, published_concepts, not_disabled_terms, not_disabled_concepts]
 

    ######################################
    # GLOSSARY FUNCTIONALITIES FUNCTIONS #
    ######################################
    def searchGlossary(self, query='', size=10000, language='English', definition='*', REQUEST=None):
        """ search glossary """
        results = self.cu_search_catalog([EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE],
                                         self.utToUtf8(query), size, language, self.utToUtf8(definition))
        return (language, query, results)

    def random_from_catalog(self, folders=''):
        """a random element from catalog """
        if len(folders):
            folder = whrandom.choice(folders)
            return self.random_from_folder('/'+folder.absolute_url(1))
        else: return ''
#        folder = whrandom.choice(folders)
#        return self.random_from_folder('/'+folder.absolute_url(1))

    def random_from_folder(self, folder=''):
        """ a random element from a GlossaryFolder """
        elements=[]
        append = elements.append
        for obj in self.cu_get_cataloged_objects(meta_type=EEA_GLOSSARY_ELEMENT_METATYPE, path=folder):
            if obj.is_published() and obj.definition:
                append(obj)
        if len(elements) > 0:
            return whrandom.choice(elements)
        else:
            return None

    def change_pass_action(self,REQUEST=None):
        """Change Password for current Zope user"""
        domains = REQUEST.AUTHENTICATED_USER.getDomains()
        roles = REQUEST.AUTHENTICATED_USER.getRoles()
        name = REQUEST.AUTHENTICATED_USER.getUserName()
        password = REQUEST.new_password
        confirm = REQUEST.new_password_confirm
        self.acl_users._changeUser(name,password,confirm,roles,domains,REQUEST=None)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('change_pass_html?save=ok')

    def folder_list_sorted(self):
        """ Return all the folders, sorted"""
        results = []
        for l_folder in self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_FOLDER_METATYPE], sort_on='id', sort_order=''):
            if len(l_folder.objectValues([EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE])) > 0:

                for k in l_folder.objectValues([EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE]):
                    if k.is_published():
                        results.append(l_folder)
                        break

        return results

    def get_all_objects (self, path=''):
        """ return sorted objects by name """
        return self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE], sort_on='id', sort_order='', path=path)
        
    def get_all_elements(self):
        """ return sorted objects by name """
        return self.cu_get_cataloged_objects(meta_type=[EEA_GLOSSARY_ELEMENT_METATYPE,], sort_on='id', sort_order='')

    def get_all_elements_by_type(self):
        """ return sorted elements by name """
        elem_lst=[]
        elem_lst = self.cu_get_cataloged_objects(meta_type=EEA_GLOSSARY_ELEMENT_METATYPE, sort_on='id', sort_order='')
        return elem_lst

    def reindexCatalog(self, REQUEST=None):
        """ reindex the catalog """
        try:
            indexes = self.cu_getIndexes()
            for index in indexes:
                self.cu_reindexCatalogIndex(index.id, REQUEST)
            return 1
        except:
            return 0

    def buildGlossary(self, glossary_table, REQUEST=None):
        """ build glossary -- initial phase """
        tiny = self.unrestrictedTraverse(glossary_table, None)
        transtab = string.maketrans('/ ','__')
        #return the columns names from tiny table
        cols = string.split(tiny.cols_text(), ' ')
        obj = mapTiny()
        for item in tiny.getRows():
            for col in cols:
                if string.upper(col) == EEA_TINYTABLE_ENTRY:
                    col_info = eval("item.%s" % col)
                    #Replace danish characters to the old ones.
                    #entry = string.replace(col_info,'?,'ae')
                    #entry = string.replace(entry,'?,'aa')
                    #entry = string.replace(entry,'','oe')
                    obj.entry = col_info
                    if obj.entry != '':
                        #Set default values to empty string.
                        folder_id = string.upper(obj.entry[:1])
                        folder = self.unrestrictedTraverse(folder_id, None)
                        if folder is None:
                            try:
                                self.manage_addGlossaryFolder(folder_id)
                                folder = self._getOb(folder_id)
                            except Exception, error:
                                print error
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION:
                    obj.definition = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION_SOURCE:
                    obj.definition_source = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION_SOURCE_PUBL:
                    obj.definition_source_publ = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION_SOURCE_PUBL_YEAR:
                    obj.definition_source_publ_year = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION_SOURCE_ORG:
                    obj.definition_source_org = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_DEFINITION_SOURCE_ORG_FULLNAME:
                    obj.definition_source_org_fullname = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_LONGDEFINITION:
                    obj.long_definition = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_ACRONYM:
                    obj.acronym = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_ACRONYM:
                    obj.acronym = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_USEFOR1:
                    obj.used_for_1 = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_USEFOR2:
                    obj.used_for_2 = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_ENTRY_TYPE:
                    obj.entry_type = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_SOURCE:
                    obj.source = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_CONTEXT:
                    obj.context = eval("item.%s" % col)
                elif string.upper(col) == EEA_TINYTABLE_COMMENT:
                    obj.comment = eval("item.%s" % col)
            if obj.entry != '':
                elem_id = self.ut_makeId(obj.entry)
                elem_ob = folder._getOb(elem_id, None)
                if elem_ob is None:
                    try:
                        folder.manage_addGlossaryElement(obj.entry, obj.entry_type, obj.source, [], obj.context, obj.comment, 
                            obj.definition, obj.definition_source_publ, obj.definition_source_publ_year, obj.definition_source, 
                            obj.definition_source_org, obj.definition_source_org_fullname, 
                            obj.long_definition, 0, 1, 0, '', '', [], [], {}, [])
                        elem_ob = folder._getOb(elem_id)
                    except Exception, error:
                        print error
                else:
                    try:
                        elem_ob.name = obj.entry
                        elem_ob.el_type = obj.entry_type
                        elem_ob.source = obj.source
                        elem_ob.el_context = obj.context
                        elem_ob.comment = obj.comment
                        elem_ob.definition = obj.definition
                        elem_ob.definition_source_publ = obj.definition_source_publ
                        elem_ob.definition_source_publ_year = obj.definition_source_publ_year
                        elem_ob.definition_source_url = obj.definition_source
                        elem_ob.definition_source_org = obj.definition_source_org
                        elem_ob.definition_source_org_fullname = obj.definition_source_org_fullname
                        elem_ob.cu_recatalog_object(elem_ob)
                    except:
                        pass
                if obj.used_for_1:
                    self.create_synonim(obj.used_for_1, elem_ob.absolute_url(1))
                if obj.used_for_2:
                    self.create_synonim(obj.used_for_2, elem_ob.absolute_url(1))
                if obj.acronym:
                    self.create_synonim(obj.acronym, elem_ob.absolute_url(1))
            obj.emptyObject()
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('build_glossary_html')

    def create_synonim(self, id, term_url):
        """ create a synonim given an id """
        folder_id = string.upper(id[:1])
        folder = self.unrestrictedTraverse(folder_id, None)
        if folder is None:
            try:
                self.manage_addGlossaryFolder(folder_id)
                folder = self._getOb(folder_id)
            except Exception, error:
                print error
        elem_ob = folder._getOb(self.ut_makeId(id), None)
        if elem_ob is None:
            try:
                folder.manage_addGlossarySynonym(self.ut_makeId(id), term_url)
            except Exception, error:
                print error
        else:
            #nothing yet for this momment
            pass

    def updateGlossary(self, glossary_table, REQUEST=None):
        """ update the glossary translations """
        tiny = self.unrestrictedTraverse(glossary_table, None)
        catalog = self.getGlossaryCatalog()
        transtab = string.maketrans('/ ','__')
        #return the columns names from tiny table
        cols = string.split(tiny.cols_text(), ' ')
        obj = mapTiny()
        lower = string.lower
        for item in tiny.getRows():
            for col in cols:
                cap_col = string.capitalize(col)
                low_col = string.lower(col)
                if string.upper(col) == EEA_TINYTABLE_ENTRY or cap_col == 'English' or low_col == 'en':
                    col_info = eval("item.%s" % col)
                    #Replace danish characters to the old ones.
                    #entry = string.replace(col_info,'?,'ae')
                    #entry = string.replace(entry,'?,'aa')
                    #entry = string.replace(entry,'','oe')
                    obj.entry = col_info
                    if obj.entry != '':
                        #Set default values to empty string.
                        folder_id = string.upper(obj.entry[:1])
                        folder = self.unrestrictedTraverse(folder_id, None)
                        if folder is None:
                            try:
                                self.manage_addGlossaryFolder(folder_id)
                                folder = self._getOb(folder_id)
                            except Exception, error:
                                print error
                elif cap_col in self.get_english_names():
                    col_info = eval("item.%s" % col)
                    obj.translations[cap_col] = col_info#self.display_unicode_langs(col_info,self.get_language_charset(cap_col))
                elif low_col in self.get_language_codes():
                    col_info = eval("item.%s" % col)
                    lang = self.get_language_by_code(low_col)
                    obj.translations[lang] = self.display_unicode_langs(col_info,self.get_language_charset(lang))
            if obj.entry != '':
                elem_ob = folder._getOb(self.ut_makeId(obj.entry), None)
                if elem_ob is not None:
                    for k,v in obj.translations.items():
                        elem_ob.set_translations_list(k, v)
                        elem_ob.set_history(k, v)
                    elem_ob.cu_recatalog_object(elem_ob)
                else:
                    try:
                        folder.manage_addGlossaryElement(obj.entry, '', '', [], '', '', '', '', '', 
                        'dataservice, http://dataservice.eea.eu.int', '', 0, 1, 0, '', '', [], [], {})
                    except Exception, error:
                        print error
                    elem_ob = folder._getOb(self.ut_makeId(obj.entry), None)
                    if elem_ob is not None:
                        for k,v in obj.translations.items():
                            #print self.get_language_charset(k)
                            #buf1 = self.display_unicode_langs(v, self.get_language_charset(k))
                            #print buf1
                            #print type(v)
                            #print v
                            #buf1 = self.convertWinCodesToHTMLCodes(v)
                            #buf2 = self.convertHTMLCodesToHex(v)
                            #print buf2
                            #print type(buf2)
                            #print buf2
                            #buf3 = v.encode('utf-8')
                            #print buf3
                            #print type(buf3)
                            #print buf2
                            #print buf3
                            #print buf3
                            elem_ob.set_translations_list(k, v)
                            elem_ob.set_history(k, v)
                        elem_ob.cu_recatalog_object(elem_ob)
            obj.emptyObject()
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('update_trans_html')

    def xliff_import(self, file, REQUEST=None):
        """ XLIFF is the XML Localization Interchange File Format
            designed by a group of software providers.
            It is specified by www.oasis-open.org
        """

        parser = xliff_parser()

        #parse the xliff information
        chandler = parser.parseHeader(file)

        if chandler is None:
            return MessageDialog(title = 'Parse error',
             message = 'Unable to parse XLIFF file' ,
             action = 'manage_main',)

        header_info = chandler.getFileTag()
        #get the target language
        target_language = [x for x in header_info if x[0]=='target-language'][0][1]

        body_info = chandler.getBody() #return a dictionary {id: (source, target)}
        obj = mapTiny()
        for elem_id, translation in body_info.items():
            if elem_id!='':
                folder_id = self.utf8_to_latin1(string.upper(elem_id[:1]))
                folder = self.unrestrictedTraverse(folder_id, None)
                if folder is None:
                    try:
                        self.manage_addGlossaryFolder(folder_id)
                        folder = self._getOb(folder_id)
                    except Exception, error:
                        print error
                if target_language in self.get_english_names():
                    obj.entry = self.utf8_to_latin1(translation['source'])
                    obj.translations[target_language] = translation['target']
                    #self.display_unicode_langs(translation['target'],self.get_language_charset(target_language))
                    #charset = self.get_language_charset(target_language)
                if obj.entry!='':
                    elem_ob = folder._getOb(self.ut_makeId(obj.entry), None)
                    if elem_ob is not None:
                        for k,v in obj.translations.items():
                            elem_ob.set_translations_list(k, v.encode('utf-8'))
                            elem_ob.set_history(k, v.encode('utf-8'))
                        elem_ob.cu_recatalog_object(elem_ob)
                    else:
                        try:
                            folder.manage_addGlossaryElement(obj.entry, '', '', [], '', '', '', '', '', 
                            'dataservice, http://dataservice.eea.eu.int', '', 0, 1, 0, '', '', [], [], {})
                        except Exception, error:
                            print error
                        elem_ob = folder._getOb(self.ut_makeId(obj.entry), None)
                        if elem_ob is not None:
                            for k,v in obj.translations.items():
                                elem_ob.set_translations_list(k, v.encode('utf-8'))
                                elem_ob.set_history(k, v.encode('utf-8'))
                            elem_ob.cu_recatalog_object(elem_ob)
            obj.emptyObject()
        if REQUEST is not None:
             return MessageDialog(title = 'Messages imported', message = 'Terms successfully imported' ,
             action = 'import_html',)

    def style_console_css(self):
        """ return the css file from EEAGlossaryEngine """
        return self.getGlossaryEngine().style_console_css.read()

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
    prop_contact_html = DTMLFile("dtml/EEAGlossaryCentre/properties_contact", globals())
    prop_stop_words_html = DTMLFile("dtml/EEAGlossaryCentre/properties_stop_words", globals())

    preview_html = DTMLFile('dtml/EEAGlossaryCentre/preview', globals())
    index_html = DTMLFile('dtml/EEAGlossaryCentre/index', globals())

    search_html = DTMLFile('dtml/EEAGlossaryCentre/search_box', globals())
    search_help_html = DTMLFile('dtml/EEAGlossaryCentre/search_help', globals())

    not_approved_html = DTMLFile('dtml/EEAGlossaryCentre/administration_not_approved', globals())
    approved_html = DTMLFile('dtml/EEAGlossaryCentre/administration_approved', globals())
    disabled_html = DTMLFile('dtml/EEAGlossaryCentre/administration_disabled', globals())
    not_published_html = DTMLFile('dtml/EEAGlossaryCentre/administration_not_published', globals())
    published_html = DTMLFile('dtml/EEAGlossaryCentre/administration_published', globals())
    terms_stats_html = DTMLFile('dtml/EEAGlossaryCentre/administration_terms_stats', globals())
    export_html = DTMLFile('dtml/EEAGlossaryCentre/administration_export', globals())
    all_terms_view_html = DTMLFile('dtml/EEAGlossaryCentre/all_terms', globals())

    import_html = DTMLFile('dtml/EEAGlossaryCentre/administration_import', globals())

    term_tip_box_html = DTMLFile('dtml/EEAGlossaryCentre/term_tip_box', globals())
    contexts_html = DTMLFile('dtml/EEAGlossaryCentre/contexts', globals())
    contexts_view_html = DTMLFile('dtml/EEAGlossaryCentre/contexts_view', globals())
    check_list_html = DTMLFile('dtml/EEAGlossaryCentre/checklist', globals())
    change_pass_html = DTMLFile('dtml/EEAGlossaryCentre/changepassword', globals())
    glossary_terms_rdf = DTMLFile('dtml/EEAGlossaryCentre/glossary_rdf', globals())
    all_terms_html = DTMLFile('dtml/EEAGlossaryCentre/all_terms_view', globals())

    management_page_html = DTMLFile('dtml/EEAGlossaryCentre/administration', globals())
    reindex_html = DTMLFile('dtml/EEAGlossaryCentre/administration_reindex', globals())
    build_glossary_html = DTMLFile('dtml/EEAGlossaryCentre/administration_build', globals())
    update_trans_html = DTMLFile('dtml/EEAGlossaryCentre/administration_trans', globals())

    centre_help_html = DTMLFile("dtml/EEAGlossaryCentre/centre_help", globals())
    help_html = DTMLFile("dtml/EEAGlossaryCentre/help", globals())
    help_contact_html = DTMLFile("dtml/EEAGlossaryCentre/help_contact", globals())

    translations_list_html = DTMLFile("dtml/EEAGlossaryCentre/administration_translations_list", globals())
    translations_html = DTMLFile("dtml/EEAGlossaryCentre/administration_translations", globals())

    manage_utf8_header = DTMLFile('dtml/EEAGlossaryCentre/utf8_header', globals())
    manage_utf8_footer = DTMLFile('dtml/EEAGlossaryCentre/utf8_footer', globals())

    #####################
    #   SKOS Functions  #
    #####################
    def loadRDF(self):
        """ loads rdf files """
        from os.path import join
        from Products.PythonScripts.PythonScript import manage_addPythonScript

        file_content = open(join(EEAGLOSSARY_PATH, 'rdfs', 'EEAGlossary_skos.spy'), 'r').read()
        manage_addPythonScript(self, 'skos.rdf')
        self._getOb('skos.rdf').write(file_content)

    def GetElementsInfo(self):
        """ """
        result=[]
        folder_list = self.folder_list_sorted()
        for folder in folder_list:
            elems=folder.get_object_list()
            result.extend(elems)
        return result

InitializeClass(EEAGlossaryCentre)


class mapTiny:
    def __init__(self):
        """ """
        self.entry = ''
        self.definition = ''
        self.acronym = ''
        self.used_for_1 = ''
        self.used_for_2 = ''
        self.entry_type = ''
        self.source = ''
        self.context = ''
        self.comment = ''
        self.definition = ''
        self.definition_source = ''
        self.long_definition = ''
        self.translations = {}

    def emptyObject(self):
        """ """
        self.entry = ''
        self.definition = ''
        self.acronym = ''
        self.used_for_1 = ''
        self.used_for_2 = ''
        self.entry_type = ''
        self.source = ''
        self.context = ''
        self.comment = ''
        self.definition = ''
        self.definition_source = ''
        self.long_definition = ''
        self.translations = {}

class MyData: pass
