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
# Alex Ghica, Finsiel Romania
#
#$Id: EEAGlossaryFolder.py,v 1.4 2004/05/03 13:19:48 finrocvs Exp $

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware
import Products

# product imports
import EEAGlossaryElement
from EEAGlossary_utils import Utils
from EEAGlossary_constants import *

manage_addGlossaryFolder_html = DTMLFile('dtml/EEAGlossaryFolder_add', globals())
def manage_addGlossaryFolder(self, id, title, description, REQUEST=None):
    """ Adds a new EEAGlossaryFolder object """
    ob = EEAGlossaryFolder(id, title, description)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryFolder(Folder, Utils):
    """ EEAGlossaryFolder """

    meta_type = EEA_GLOSSARY_FOLDER_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = "misc_/EEAGlossary/folder.gif"

    manage_options = (
                (Folder.manage_options[0],) +
                ({'label':'View',       'action':'preview'},) +
                (Folder.manage_options[4],) + (
                {'label':'Properties',       'action':'manage_propertiesForm'},
                {'label':'Subobjects',              'action':'manage_subobjects_html'},
                {'label':'Undo',              'action':'manage_UndoForm'},
                {'label':'Help',               'action':'manageHelpForm'},)
                )

    security = ClassSecurityInfo()

    meta_types = (
        {'name': EEA_GLOSSARY_ELEMENT_METATYPE, 'action': 'manage_addGlossaryElement_html', 'product': EEA_GLOSSARY_PRODUCT_NAME},
        {'name': EEA_GLOSSARY_SYNONYM_METATYPE, 'action': 'manage_addGlossarySynonym_html', 'product': EEA_GLOSSARY_PRODUCT_NAME},
        )

    manage_addGlossaryElement_html = EEAGlossaryElement.manage_addGlossaryElement_html
    manage_addGlossaryElement = EEAGlossaryElement.manage_addGlossaryElement

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        print "intre"
        self.adt_meta_types = []

    def all_meta_types(self):
        """ What can you put inside me? """
        global metatypes 
        metatypes = self.adt_meta_types
        if len(metatypes) > 0:
            f = lambda x: x['name'] in metatypes
            return filter(f, Products.meta_types) + self.meta_types
        else:
            return self.meta_types

    def getMetaTypes(self):
        return [x['name'] for x in Products.meta_types]

    def manageSubobjects(self, REQUEST=None):
        """ Update the additional meta types for all objects """
        subobjects = self.utConvertToList(REQUEST.get('subobjects', self.adt_meta_types))
        self.adt_meta_types = subobjects
        self._p_changed = 1
        REQUEST.RESPONSE.redirect('manage_subobjects_html?save=ok')


    def IsEmptyFolder(self):
        """returns 0 if is an empty folder"""
        for eobject in self.objectValues([EEA_GLOSSARY_ELEMENT_METATYPE, EEA_GLOSSARY_SYNONYM_METATYPE]):
            if (eobject.approved and not eobject.disabled):
                return 1
        return 0

    def GlossaryFolder_parent_list(self):
        """returns parent"""
        ret='<a href="'+self.REQUEST.PARENTS[1].absolute_url()+'">' \
            +'<img src="misc_/EEAGlossary/OpenBook.gif" BORDER=0></a>&nbsp;<a href="'+ \
            self.REQUEST.PARENTS[1].absolute_url()+'">'+self.REQUEST.PARENTS[1].title_or_id()+'</a>'
        return ret

    index_html = DTMLFile('dtml/EEAGlossaryFolder_index', globals())
    preview = DTMLFile('dtml/EEAGlossaryFolder_preview', globals())
    manage_subobjects_html = DTMLFile('dtml/EEAGlossaryFolder_subobjects', globals())
    #IsEmpty = DTMLFile('dtml/EEAGlossaryFolder_IsEmpty', globals())
    #manageHelpForm = DTMLFile('dtml/EEAGlossaryCentre_manageHelp', globals())

InitializeClass(EEAGlossaryFolder)
