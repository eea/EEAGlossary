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
#$Id: EEAGlossaryElement.py,v 1.4 2004/05/03 11:36:22 finrocvs Exp $

# python imports
import string

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
#from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware

# product imports
import EEAGlossaryCentre
from EEAGlossary_utils import Utils

#constants
manage_addEEAGlossaryElementForm = DTMLFile('dtml/EEAGlossaryElement_add', globals())

def manage_addEEAGlossaryElement (self, id, name='', type='', source='', subjects=[], context='', comment='', used_for_1='', used_for_2='',
    definition='', definition_source_url='', long_definition='', disabled=0, approved=0, QA_needed=0, image_url='', flash_url='', links=[], actions=[], REQUEST=None):
    """ Adds a new EEAGlossaryElement object """
    ob = EEAGlossaryElement(id, name, type, source, subjects, context, comment, used_for_1, used_for_2, definition, 
        definition_source_url, long_definition, disabled, approved, QA_needed, image_url, flash_url, links, actions)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryElement(SimpleItem, CatalogAware, ElementBasic, Utils):
    """ EEAGlossaryElement """

    meta_type='EEA Glossary Element'
    product_name = 'EEAGlosary'
    icon = 'misc_/EEAGlossary/OpenBook.gif'
    default_catalog='GlossaryCatalog'

    manage_options = ((
        #{'label':'All Translations',        'action':'viewTranslations'},
        #{'label':'Check Translation',       'action':'transForm2'},
        #{'label':'Properties',              'action':'manage_properties'},
        {'label':"View [OK_!]",                    'action':'preview'},
        {'label':'History',                 'action':'viewHistory'},
        {'label':'Help [OK_]',                    'action':'manageHelpE'},
        {'label':'Undo [OK_]',                    'action':'manage_UndoForm'},
        {'label':'My props',                'action':'all_langs_list'},
        {'label':'Media',                   'action':'/propertysheets/Media/manage'},
        {'label':'Actions',                 'action':'/propertysheets/Actions/manage'},
        {'label':'Convert to Synonym',      'action':'convertToSynonymForm'},)
        )

    security = ClassSecurityInfo()

    def __init__(self, id, name, type, source, subjects, context, comment, used_for_1, used_for_2, definition, 
        definition_source_url, long_definition, disabled, approved, QA_needed,  image_url, flash_url, links, actions):
        """ constructor """
        self.id = id
        self.image_url = image_url
        self.flash_url = flash_url
        self.links = links
        self.actions = actions
        self.all_langs_list= {} #????????
        self.history={} #??????
        ElementBasic.__dict__['__init__'](self, name, type, source, subjects, context, comment, used_for_1, used_for_2, 
            definition, definition_source_url, long_definition, disabled, approved, QA_needed)

#    def loadINI (self):
#        """loads languages & history properties defaults"""
#        from os.path import join
#        try:
#            file=open(join(SOFTWARE_HOME, 'Products','EEAGlossary','EEAGlossary.ini'), 'r')
#            for line in file.readlines():
#                line=string.strip(line)
#                if line != '':
#                    key, value = string.split(line,'=')
#                    if key == 'History':
#                        self.history[value]=''
#                    if key == 'Translation':
#                        self.all_langs_list[value]=''
#            file.close()
#        except:
#            pass
#        return 1

#alec
    def isPublished (self):
        if self.approved and not self.disabled:
            return 1
        else:
            return 0
#/alec

#alec
    def isImageURL (self):
        if not self.isEmptyString(self.ImageURL) and (not 'ImageURL' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0
#/alec

#alec
    def isLong_Definition (self):
        if not self.isEmptyString(self.long_definition) and (not 'long_definition' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0
#/alec

#alec
    def isDefintion_Source (self):
        if not self.isEmptyString(self.definition_source_url) and (not 'definition_source' in self.REQUEST.PARENTS[2].hidden_fields):
            return 1
        else:
            return 0
#/alec

    index_html = DTMLFile("dtml/EEAGlossaryElement_index", globals())
    preview = DTMLFile("dtml/EEAGlossaryElement_preview", globals())
    main_content = DTMLFile("dtml/EEAGlossaryElement_main_content", globals())
    viewTranslations = DTMLFile("dtml/EEAGlossaryElement_viewTranslations", globals())
    manage_utf8_header = DTMLFile("dtml/EEAGlossaryElement_manage_utf8_header", globals())
    manage_utf8_footer = DTMLFile("dtml/EEAGlossaryElement_manage_utf8_footer", globals())
    transForm2 = DTMLFile("dtml/EEAGlossaryElement_transForm2", globals())
    manage_properties = DTMLFile("dtml/EEAGlossaryElement_manage_properties", globals())
    viewHistory = DTMLFile("dtml/EEAGlossaryElement_viewHistory", globals())
    manageHelpE = DTMLFile('dtml/EEAGlossaryCentre_manageHelp', globals())
#alec    new_entry_icon = DTMLFile("dtml/EEAGlossaryElement_new_entry_icon", globals())
#alec    status_view = DTMLFile("dtml/EEAGlossaryElement_status_view", globals())
#alec    isPublished = DTMLFile("dtml/EEAGlossaryElement_isPublished", globals())

InitializeClass(EEAGlossaryElement)


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
        self.used_for_1 = used_for_1    #????????
        self.used_for_2 = used_for_2    #????????
        self.definition = definition
        self.definition_source_url = definition_source_url
        self.disabled = disabled
        self.approved = approved
        self.long_definition = long_definition
        self.QA_needed = QA_needed  #?????