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
#$Id: EEAGlossaryElement.py,v 1.11 2004/05/04 10:18:49 finrocvs Exp $

# python imports
import string

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Products.ZCatalog.CatalogAwareness import CatalogAware

# product imports
import EEAGlossaryCentre
from EEAGlossary_utils import utils
from EEAGlossary_constants import *

class ElementBasic:
    """ define the basic properties for EEAGlossaryElement"""

    def __init__(self, name, type, source, subjects, context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed):
        """ constructor"""

        self.name = name
        self.type = type
        self.source = source
        self.subjects = subjects
        self.context = context
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

def manage_addGlossaryElement(self, id, name='', type='', source='', subjects=[], context='', comment='', 
    used_for_1='', used_for_2='',definition='', definition_source_url='', long_definition='', disabled=0, 
    approved=1, QA_needed=0, image_url='', flash_url='', links=[], actions=[], REQUEST=None):

    """ Adds a new EEAGlossaryElement object """

    ob = EEAGlossaryElement(id, name, type, source, subjects, context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed, 
            image_url, flash_url, links, actions)
    self._setObject(id, ob)
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
        {'label':'My props',                'action':'custom_properties_html'},
        {'label':'Media',                   'action':'media_html'},
        {'label':'Actions',                 'action':'actions_html'},
        {'label':'Convert to Synonym',      'action':'synonym_html'},
        {'label':'History',                 'action':'history_html'},
        {'label':'Undo [OK]',                    'action':'manage_UndoForm'},
        {'label':'Help [OK]',                    'action':'help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id, name, type, source, subjects, context, comment, used_for_1, used_for_2, definition, 
        definition_source_url, long_definition, disabled, approved, QA_needed,  image_url, flash_url, links, actions):
        """ constructor """
        self.id = id
        self.image_url = image_url
        self.flash_url = flash_url
        self.links = links
        self.actions = actions
        self.all_langs_list= {}
        self.history={}
        ElementBasic.__dict__['__init__'](self, name, type, source, subjects, context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed)

    def is_published (self):
        if self.approved and not self.disabled:
            return 1
        else:
            return 0

    def is_image_url (self):
        if not self.utIsEmptyString(self.image_url) and (not 'image_url' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0

    def is_long_definition (self):
        if not self.utIsEmptyString(self.long_definition) and (not 'long_definition' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0

    def is_defintion_source (self):
        if not self.utIsEmptyString(self.definition_source_url) and (not 'definition_source' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0

    #####################
    #   MANAGEMENT TABS #
    #####################

    all_translations_html = DTMLFile("dtml/EEAGlossaryElement/all_translations", globals())
    check_translation_html = DTMLFile("dtml/EEAGlossaryElement/check_translation", globals())
    manage_properties_html = DTMLFile("dtml/EEAGlossaryElement/manage_properties", globals())
    preview_html = DTMLFile("dtml/EEAGlossaryElement/preview", globals())
    custom_properties_html = DTMLFile("dtml/EEAGlossaryElement/custom_prop", globals())
    media_html = DTMLFile("dtml/EEAGlossaryElement/media", globals())
    actions_html = DTMLFile("dtml/EEAGlossaryElement/actions", globals())
    synonym_html = DTMLFile("dtml/EEAGlossaryElement/synonym", globals())
    history_html = DTMLFile("dtml/EEAGlossaryElement/history", globals())
    help_html = DTMLFile("dtml/EEAGlossaryElement/help", globals())
    index_html = DTMLFile("dtml/EEAGlossaryElement/index", globals())
    main_content_html = DTMLFile("dtml/EEAGlossaryElement/main_content", globals())

InitializeClass(EEAGlossaryElement)