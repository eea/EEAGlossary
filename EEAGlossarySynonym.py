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


# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
#from Products.ZCatalog.CatalogAwareness import CatalogAware

# product imports

import GlossaryElement
#constants

manage_addEEAGlossarySynonymForm = DTMLFile('dtml/EEAGlossarySynonym_add', globals())

def manage_addEEAGlossarySynonym (self, id, title, description, REQUEST=None):
    """ Adds a new EEAGlossaryElementSynonym object """
    ob = EEAGlossarySynonym(id, title, description)
    self._setObject(id, ob)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)



class EEAGlossarySynonym(SimpleItem):
    """ EEAGlossaryFolder """

    meta_type='EEA Glossary Synonym'
    product_name = 'EEAGlosary'

    security = ClassSecurityInfo()

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
        {'id':'description', 'type':'text', 'mode':'w'},
        )

    #manage_options = Folder.manage_options[:2]

    manage_options =(
                (Folder.manage_options[0],) +
                ({'label':'All translations', 'action':'viewTranslations'}),
                #(Folder.manage_options[1],) +
                ({'label':'View',                        'action':'index_html'},) +
                (Folder.manage_options[2],) +
                (Folder.manage_options[5],) + (
                {'label':'Help',                        'action':'manageHelp'},)
                )

    index_html = DTMLFile("dtml/EEAGlossaryFolder_index", globals())

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description


InitializeClass(EEAGlossaryFolder)
