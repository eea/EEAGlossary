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
# Cornel Nitu, Finsiel Romania
#
#
#$Id: EEAGlossarySynonym.py,v 1.18 2004/05/13 11:41:23 finrocvs Exp $

#python imports
import string

# Zope imports
from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo

# product imports
from EEAGlossaryElement import EEAGlossaryElement
from EEAGlossary_utils import utils
from EEAGlossary_constants import *

manage_addGlossarySynonym_html = DTMLFile('dtml/EEAGlossarySynonym/add', globals())

def manage_addGlossarySynonym(self, id, synonyms=[], REQUEST=None):
    """ Adds a new EEAGlossaryElementSynonym object """
    ob = EEAGlossarySynonym(id, synonyms)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossarySynonym(EEAGlossaryElement, utils):
    """ EEAGlossaryFolder """

    meta_type = EEA_GLOSSARY_SYNONYM_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/synonym.gif'

    manage_options = (
        {'label':'All Translations',    'action':'all_translations_html'},
        {'label':'Check Translation',               'action':'check_translation_html'},
        {'label':'Properties',                      'action':'manage_properties_html'},
        {'label':"View",                            'action':'preview_html'},
        {'label':'History',             'action':'history_html'},
        {'label':'Help',                       'action':'help_html'},
        {'label':'Undo',                       'action':'manage_UndoForm'},
        {'label':'Synonym Properties',         'action':'synonym_properties_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id, synonyms):
        """ constructor """
        self.id = id
        self.synonyms = self.utConvertToList(synonyms)
        EEAGlossaryElement.__dict__['__init__'](self, id, '', '', '', [], '', '', '', '', '', 
            '', '', 0, 0, 0, '', '', [], [], {})

    #####################
    #   MANAGEMENT TABS #
    #####################
    def manageSynonymProperties(self, old_synonym='', new_synonym='', ids='', REQUEST=None):
        """ manage the synonym properties for EEAGlossarySynonym """
        if self.utAddObjectAction(REQUEST):
            if string.strip(new_synonym) == '':
                return REQUEST.RESPONSE.redirect('synonym_properties_html')
            else:
                self.synonyms.append(new_synonym)
                self._p_changed = 1
        elif self.utUpdateObjectAction(REQUEST):
            if string.strip(new_synonym) == '':
                return REQUEST.RESPONSE.redirect('synonym_properties_html')
            else:
                self.synonyms.remove(old_synonym)
                self.synonyms.append(new_synonym)
                self._p_changed = 1
        elif self.utDeleteObjectAction(REQUEST):
            if not ids or len(ids) == 0:
                return REQUEST.RESPONSE.redirect('synonym_properties_html')
            for synonym in self.utConvertToList(ids):
                self.synonyms.remove(synonym)
            self._p_changed = 1
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('synonym_properties_html')

    def manageSynonymOtherProperties(self, name, disabled=0, approved=0, REQUEST=None):
        """ manage other synonym properties for EEAGlossarySynonym """
        self.name = name
        self.disabled = disabled
        self.approved = approved
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')

    manage_properties_html = DTMLFile("dtml/EEAGlossarySynonym/properties", globals())
    index_html = DTMLFile("dtml/EEAGlossarySynonym/index", globals())
    main_content_html = DTMLFile("dtml/EEAGlossarySynonym/main_content", globals())
    synonym_properties_html = DTMLFile("dtml/EEAGlossarySynonym/synonym_properties", globals())
    short_info_html = DTMLFile("dtml/EEAGlossarySynonym/short_info", globals())
    view_box_html = DTMLFile("dtml/EEAGlossarySynonym/view_box", globals())

InitializeClass(EEAGlossarySynonym)
