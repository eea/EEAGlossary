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
#$Id: EEAGlossaryCentre.py,v 1.14 2004/05/04 10:18:49 finrocvs Exp $

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
from parsers.languages_parser import languages_parser
from parsers.subjects_parser import subjects_parser
from EEAGlossary_constants import *

manage_addGlossaryCentre_html = DTMLFile('dtml/EEAGlossaryCentre/add', globals())

def manage_addGlossaryCentre(self, id, title='', description='', REQUEST=None):
    """ Adds a new EEAGlossaryCentre object """
    ob = EEAGlossaryCentre(id, title, description)
    self._setObject(id, ob)
    centre_obj = self._getOb(id)
    centre_obj.load_subjects_list()
    centre_obj.load_languages_list()
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
        self.languages_list = []
        self.search_langs = ''
        self.published = 0
        self.hidden_fields = []
        self.alpha_list = string.uppercase + string.digits + 'other'
        utils.__dict__['__init__'](self)

    def all_meta_types(self):
        """ Supported meta_types """
        meta_types = [{'name': EEA_GLOSSARY_FOLDER_METATYPE, 'action': 'manage_addGlossaryFolder_html'},]
        return meta_types

    manage_addGlossaryFolder_html = EEAGlossaryFolder.manage_addGlossaryFolder_html
    manage_addGlossaryFolder = EEAGlossaryFolder.manage_addGlossaryFolder

    def load_languages_list(self):
        """loads languages & history properties defaults"""
        from os.path import join
        languages_obj = languages_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary', 'config', 'languages.xml'))
        languages_handler, error = languages_obj.parseContent(content)
        for lang in languages_handler.languages:
            self.languages_list.append(lang.english_name)
            self.translations.append(lang.english_name)
            self.history.append(lang.english_name)

    def load_subjects_list (self):
        """loads subjects properties defaults"""
        from os.path import join
        subjects_obj = subjects_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary','config', 'subjects.xml'))
        subjects_handler, error = subjects_obj.parseContent(content)
        for code in subjects_handler.subjects:
            self.subjects_list[code.code] = code.name

    def get_subjects_list (self):
        """gets subjects list in alphabetical order """
        subjects_values = self.subjects_list.values()
        subjects_values.sort()
        return subjects_values

    ##########################
    #   MANAGEMENT FUNCTIONS #
    ##########################

    def manageProperties(self, title='', description='', alpha_list=[], types_list=[], subjects_list=[], 
        languages_list=[], search_langs=[], published=0, hidden_fields=[], REQUEST=None):
        """ manage properties for EEAGlossaryCentre """
        self.title = title
        self.description = description
        self.alpha_list = self.utConvertLinesToList(alpha_list)
        self.types_list = self.utConvertLinesToList(types_list)
        #self.subjects_list = self.utConvertLinesToList(subjects_list)
        self.languages_list = self.utConvertLinesToList(languages_list)
        self.search_langs = self.utConvertLinesToList(search_langs)
        self.published = published
        self.hidden_fields = self.utConvertLinesToList(hidden_fields)
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')


    #####################
    #   MANAGEMENT TABS #
    #####################

    manage_properties_html = DTMLFile('dtml/EEAGlossaryCentre/properties', globals())
    preview_html = DTMLFile('dtml/EEAGlossaryCentre/preview', globals())
    contexts_html = DTMLFile('dtml/EEAGlossaryCentre/contexts', globals())
    check_list_html = DTMLFile('dtml/EEAGlossaryCentre/checklist', globals())
    change_pass_html = DTMLFile('dtml/EEAGlossaryCentre/changepassword', globals())
    glossary_terms_rdf = ''
    all_terms_html = DTMLFile('dtml/EEAGlossaryCentre/allterms', globals())
    management_page_html = DTMLFile('dtml/EEAGlossaryCentre/administration', globals())

    style_css = DTMLFile('dtml/EEAGlossaryCentre/style', globals())

InitializeClass(EEAGlossaryCentre)