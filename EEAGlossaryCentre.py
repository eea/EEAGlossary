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
#$Id: EEAGlossaryCentre.py,v 1.4 2004/05/03 12:19:22 finrocvs Exp $

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

#product imports
import EEAGlossaryFolder
import EEAGlossaryElement
#import EEAGlossaryElementSynonym
from EEAGlossary_constants import *

manage_addEEAGlossaryCentreForm = DTMLFile('dtml/EEAGlossaryCentre_add', globals())

def manage_addEEAGlossaryCentre(self, id, title='', description='', REQUEST=None):
    """ Adds a new EEAGlossaryCentre object """
    ob = EEAGlossaryCentre(id, title, description)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EEAGlossaryCentre(Folder, CatalogAware):
    """ EEAGlossaryCentre """

    meta_type = EEA_GLOSSARY_CENTRE_METATYPE
    product_name = 'EEAGlosary'

    manage_options =((Folder.manage_options[0],) +
                (Folder.manage_options[2],) + ({'label':'View [lucru_!!]',           'action':'preview'},
                {'label':'Contexts Reference',        'action':'contexts_table_man'},
                {'label':'Check list',                'action':'check_form'},
                {'label':'Change Password [OK_!]',    'action':'changePass'},
                {'label':'XML/RDF',                   'action':'glossaryterms.rdf'},
                {'label':'All terms',                 'action':'GlossaryElement'},) +
                (Folder.manage_options[4],) + ({'label':'Help [OK_]',                'action':'manageHelp'},
                {'label':'Management',                'action':'managementpage'},
                {'label':'Undo [OK_]',                'action':'manage_UndoForm'},)
                )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        self.types_list = []
        self.subjects_list = []
        self.languages_list = []
        self.search_langs = ''
        self.published = 0
        self.hidden_fields = ''
        self.alpha_list = string.uppercase + string.digits + 'other'
        #self.

    def all_meta_types(self):
        """ Supported meta_types """
        meta_types = [  {'name': 'EEAGlossaryFolder', 'action': 'manage_addEEAGlossaryFolderForm'},
            {'name': 'EEAGlossaryElement', 'action':'manage_addEEAGlossaryElementForm'},
            {'name': 'EEAGlossarySynonym', 'action':'manage_addEEAGlossarySynonymForm'},
            {'name': 'EEAGlossaryCatalog', 'action':'manage_addZCatalogForm'}
         ]
        return meta_types

    manage_addZCatalogForm = manage_addZCatalogForm
    manage_addZCatalog = manage_addZCatalog

    manage_addEEAGlossaryFolderForm = EEAGlossaryFolder.manage_addEEAGlossaryFolderForm
    manage_addEEAGlossaryFolder = EEAGlossaryFolder.manage_addEEAGlossaryFolder

    manage_addEEAGlossaryElementForm = EEAGlossaryElement.manage_addEEAGlossaryElementForm
    manage_addEEAGlossaryElement = EEAGlossaryElement.manage_addEEAGlossaryElement

    #manage_addEEAGlossaryElementSynonymForm = EEAGlossaryElement.manage_addEEAGlossaryElementSynonymForm
    #manage_addEEAGlossaryElementSynonym = EEAGlossaryElement.manage_addEEAGlossaryElementSynonym


    def loadINI (self):
        """loads languages & history properties defaults"""
        from os.path import join
        file = open(join(SOFTWARE_HOME, 'Products','EEAGlossary','languages.xml'), 'r')
        content = file.read()
        file.close()
        languages_handler, error = forms_parser.parseContent(content)
        for lang in languages_handler.languages:
            self.translations = english_name
            self.history = english_name
            print self.translations
            print self.history

    def changePass(self, REQUEST=None):
        """."""

    def glossary_terms_rdf(self, REQUEST=None):
        """."""

    def GlossaryElement(self, REQUEST=None):
        """."""

    def managementpage(self, REQUEST=None):
        """."""


    def changePassAction(self,REQUEST=None):
        """Change Password for current Zope user"""
        
        domains = REQUEST.AUTHENTICATED_USER.getDomains()
        roles = REQUEST.AUTHENTICATED_USER.getRoles()
        name = REQUEST.AUTHENTICATED_USER.getUserName()
        password = REQUEST.new_password
        confirm = REQUEST.new_password_confirm

        return self.acl_users._changeUser(name,password,confirm,roles,domains,REQUEST=None)
        #return MessageDialog(
        #           title  ='Illegal value',
        #           message='AAAA',
        #           action ='manage_main')



    def GlossaryCentre_folder_list(self):
        """Return all 'EEA Glossary Folder' from a Centre"""
        ret=''
        lista=self.objectItems(EEA_GLOSSARY_FOLDER_METATYPE)
        lista.sort()
        for i in lista:
            o=i[1]
            ret=ret+'&nbsp;<a href="'+o.absolute_url()+'">'+o.id+'</a>&nbsp;|'
        return ret

    def term_tip(self):
        """Return a random 'EEA Glossary Element' """
        elements=[]
        for fobject in container.objectValues(EEA_GLOSSARY_FOLDER_METATYPE):
            for eobject in fobject.objectValues(EEA_GLOSSARY_ELEMENT_METATYPE):
                if eobject.isPublished:
                   elements.append(eobject)
        if len(elements) > 0:
            return whrandom.choice(elements)
        else:
            return None

    contexts_table_man = DTMLFile('dtml/EEAGlossary_contexts_table_man', globals())
    about = DTMLFile('dtml/EEAGlossary_contexts_table_man', globals())
    changePass_html = DTMLFile('dtml/EEAGlossaryCentre_ChangePassForm', globals())
    term_tip_box = DTMLFile('dtml/EEAGlossaryCentre_term_tip_box', globals())
    manageHelp = DTMLFile('dtml/EEAGlossaryCentre_manageHelp', globals())
    contact_Help = DTMLFile('dtml/EEAGlossaryCentre_contact_help', globals())

    file2 = DTMLFile('dtml/f2', globals())

    style_css = DTMLFile('dtml/EEAGlossary_StyleCSS', globals())
    preview = DTMLFile('dtml/EEAGlossaryCentre_preview', globals())
    index_html = DTMLFile('dtml/EEAGlossaryCentre_index', globals())
    changePass = DTMLFile('dtml/EEAGlossaryCentre_changePass', globals())
    term_tip_box = DTMLFile('dtml/EEAGlossaryCentre_term_tip_box', globals())
    completeGlossary = DTMLFile('dtml/EEAGlossary_Complete', globals())

    #changePassAction = DTMLFile('dtml/EEAGlossaryCentre_changePassAction', globals())

InitializeClass(EEAGlossaryCentre)