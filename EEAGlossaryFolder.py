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
# Anton Cupcea, Finsiel Romania
# Alex Ghica, Finsiel Romania

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware
from Products import meta_types

# product imports
import EEAGlossaryElement
from EEAGlossary_utils import MyUtils

#constants
manage_addEEAGlossaryFolderForm = DTMLFile('dtml/EEAGlossaryFolder_add', globals())

def manage_addEEAGlossaryFolder (self, id, title, description, REQUEST=None):
    """ Adds a new EEAGlossaryFolder object """
    ob = EEAGlossaryFolder(id, title, description)
    self._setObject(id, ob)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryFolder(Folder,MyUtils):
    """ EEAGlossaryFolder """

    meta_type='EEA Glossary Folder'
    product_name = 'EEAGlosary'
    icon = 'misc_/EEAGlossary/folder.gif'
    security = ClassSecurityInfo()

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
        {'id':'description', 'type':'text', 'mode':'w'},
        )
    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description

    manage_addEEAGlossaryFolderForm = manage_addEEAGlossaryFolderForm
    manage_addEEAGlossaryFolder = manage_addEEAGlossaryFolder
    manage_addEEAGlossaryElementForm = EEAGlossaryElement.manage_addEEAGlossaryElementForm
    manage_addEEAGlossaryElement = EEAGlossaryElement.manage_addEEAGlossaryElement

    manage_options = (
                (Folder.manage_options[0],) +
                ({'label':'View [lucru_!!!]',         'action':'preview'},) +
#alec                (Folder.manage_options[2],) +
                (Folder.manage_options[4],) + (
                {'label':'Properties [OK_!]',         'action':'manage_propertiesForm'},
                {'label':'Undo [OK_]',                'action':'manage_UndoForm'},
                {'label':'Help[OK_]',                 'action':'manageHelpF'},)
                )

    def all_meta_types(self):
        """ Supported meta_types """
#alec        types = ['User Folder', 'Script (Python)', 'DTML Method','ZCatalog', 'ZTabs', 'Version']
        y = [
#alec            {'name': 'EEAGlossaryFolder', 'action':'manage_addEEAGlossaryFolderForm'},
            {'name': 'EEAGlossaryElement', 'action':'manage_addEEAGlossaryElementForm'},
            {'name': 'EEAGlossarySynonym', 'action':'manage_addEEAGlossarySynonymForm'}
         ]
#alec        for x in meta_types:
#alec            if x['name'] in types:
#alec                y.append(x)
        return y

#alec
    def IsEmptyFolder():
        """returns 0 if is an empty folder"""
        for eobject in self.objectValues(['EEA Glossary Element','EEA Glossary Synonym']):
            if (eobject.approved and not eobject.disabled):
                return 1
        return 0
#/alec

#alec
    def GlossaryFolder_parent_list(self):
        """returns parent"""
        ret='<a href="'+self.REQUEST.PARENTS[1].absolute_url()+'">' \
            +'<img src="misc_/EEAGlossary/OpenBook.gif" BORDER=0></a>&nbsp;<a href="'+ \
            self.REQUEST.PARENTS[1].absolute_url()+'">'+self.REQUEST.PARENTS[1].title_or_id()+'</a>'
        return ret
#/alec

    index_html = DTMLFile('dtml/EEAGlossaryFolder_index', globals())
    preview = DTMLFile('dtml/EEAGlossaryFolder_preview', globals())
    IsEmpty = DTMLFile('dtml/EEAGlossaryFolder_IsEmpty', globals())
    manageHelpF = DTMLFile('dtml/EEAGlossaryCentre_manageHelp', globals())

InitializeClass(EEAGlossaryFolder)
