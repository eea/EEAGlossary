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
# The Original Code is EEAGlossary version 1.0.0
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
#$Id: EEAGlossaryFolder.py,v 1.19 2004/05/17 08:54:19 finrocvs Exp $

# python imports
import whrandom

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware
import Products

# product imports
import EEAGlossaryElement
import EEAGlossarySynonym
from EEAGlossary_utils import utils
from EEAGlossary_constants import *

manage_addGlossaryFolder_html = DTMLFile('dtml/EEAGlossaryFolder/add', globals())

def manage_addGlossaryFolder(self, id, title='', description='', REQUEST=None):
    """ adds a new EEAGlossaryFolder object """
    ob = EEAGlossaryFolder(id, title, description)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryFolder(Folder, utils):
    """ EEAGlossaryFolder """

    meta_type = EEA_GLOSSARY_FOLDER_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = "misc_/EEAGlossary/folder.gif"

    manage_options = ((Folder.manage_options[0],) +
                ({'label':'View',       'action':'preview_html'},
                {'label':'Properties',  'action':'manage_properties_html'},
                {'label':'Subobjects',  'action':'manage_subobjects_html'},
                {'label':'Undo',        'action':'manage_UndoForm'},
                {'label':'Help',        'action':'folder_help_html'},)
                )

    meta_types = (
        {'name': EEA_GLOSSARY_ELEMENT_METATYPE, 'action': 'manage_addGlossaryElement_html', 'product': EEA_GLOSSARY_PRODUCT_NAME},
        {'name': EEA_GLOSSARY_SYNONYM_METATYPE, 'action': 'manage_addGlossarySynonym_html', 'product': EEA_GLOSSARY_PRODUCT_NAME},
        )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        self.adt_meta_types = []

    manage_addGlossaryElement_html = EEAGlossaryElement.manage_addGlossaryElement_html
    manage_addGlossaryElement = EEAGlossaryElement.manage_addGlossaryElement
    manage_addGlossarySynonym_html = EEAGlossarySynonym.manage_addGlossarySynonym_html
    manage_addGlossarySynonym = EEAGlossarySynonym.manage_addGlossarySynonym


    ##########################
    #   OTHER FUNCTIONS #
    ##########################
    def get_object_list(self):
        """ return all id sorted objects from a folder """
        id_lst = []
        obj_lst = []
        for obj in self.objectValues([EEA_GLOSSARY_ELEMENT_METATYPE,EEA_GLOSSARY_SYNONYM_METATYPE]):
            id_lst.append(obj.id)
        id_lst.sort()
        for term in id_lst:
            ob = self._getOb(term)
            obj_lst.append(ob)
        return obj_lst

    ##########################
    #   META TYPES FUNCTIONS #
    ##########################
    def all_meta_types(self):
        """ what can you put inside me """
        global metatypes 
        metatypes = self.adt_meta_types
        if len(metatypes) > 0:
            f = lambda x: x['name'] in metatypes
            return filter(f, Products.meta_types) + self.meta_types
        else:
            return self.meta_types

    def getMetaTypes(self):
        """ return meta_types list  """
        return [x['name'] for x in Products.meta_types]

    def manageSubobjects(self, REQUEST=None):
        """ update the additional meta types for all objects """
        subobjects = self.utConvertToList(REQUEST.get('subobjects', ''))
        self.adt_meta_types = subobjects
        self._p_changed = 1
        REQUEST.RESPONSE.redirect('manage_subobjects_html?save=ok')

    def manage_folder_properties(self, title='', description='', REQUEST=None):
        """ folder properties """
        self.title=title
        self.description=description
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')

    #####################
    #   MANAGEMENT TABS #
    #####################
    preview_html = DTMLFile('dtml/EEAGlossaryFolder/preview', globals())
    index_html = DTMLFile('dtml/EEAGlossaryFolder/index', globals())
    term_tip_box_html = DTMLFile('dtml/EEAGlossaryFolder/term_tip_box', globals())
    manage_properties_html = DTMLFile('dtml/EEAGlossaryFolder/properties', globals())
    manage_subobjects_html = DTMLFile('dtml/EEAGlossaryFolder/subobjects', globals())
    folder_help_html = DTMLFile("dtml/EEAGlossaryFolder/help", globals())

InitializeClass(EEAGlossaryFolder)