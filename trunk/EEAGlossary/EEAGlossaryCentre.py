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
#$Id: EEAGlossaryCentre.py,v 1.3 2004/05/03 11:36:22 finrocvs Exp $

# python imports
import string
import whrandom

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder
from Products.ZCatalog.CatalogAwareness import CatalogAware
#alec
import AccessControl.User
from Products.ZCatalog.ZCatalog import manage_addZCatalog, manage_addZCatalogForm
#from OFS.ObjectManager import ObjectManager
#/alec

# product imports
import EEAGlossaryFolder
import EEAGlossaryElement

#import EEAGlossaryElementSynonym


manage_addEEAGlossaryCentreForm = DTMLFile('dtml/EEAGlossaryCentre_add', globals())

def manage_addEEAGlossaryCentre(self, id, title='', description='', REQUEST=None):
    """ Adds a new EEAGlossaryCentre object """
    ob = EEAGlossaryCentre(id, title, description)
    self._setObject(id, ob)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)



class EEAGlossaryCentre(Folder, CatalogAware):
    """ EEAGlossaryCentre """

    meta_type='EEA Glossary Centre'
    product_name = 'EEAGlosary'

    manage_options =(
                (Folder.manage_options[0],) +
                #(Folder.manage_options[1],) +
                (Folder.manage_options[2],) + (
                {'label':'View [lucru_!!]',           'action':'preview'},
                {'label':'Contexts Reference',        'action':'contexts_table_man'},
                {'label':'Check list',                'action':'check_form'},
                {'label':'Change Password [OK_!]',    'action':'changePass'},
                {'label':'XML/RDF',                   'action':'glossaryterms.rdf'},
                {'label':'All terms',                 'action':'GlossaryElement'},) +
                (Folder.manage_options[4],) + (
                {'label':'Help [OK_]',                'action':'manageHelp'},
                {'label':'Management',                'action':'managementpage'},
                {'label':'Undo [OK_]',                'action':'manage_UndoForm'},)
#alec                (Folder.manage_options[5],) + (
#alec                {'label':'Undo[OK]',            'action':'manage_UndoForm'},)
                )

    security = ClassSecurityInfo()

    def __init__(self, id, title, description):
        """ constructor """
        self.id = id
        self.title = title
        self.description = description
        self.types_list = []
        self.subjects_list = []
        self.languages_list = languages_list
        self.search_langs = ''
        self.published = 0
        self.hidden_fields = ''
        self.alpha_list = string.ascii_uppercase + string.digits + 'other'
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

#alec
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
#/alec

#alec
    def GlossaryCentre_folder_list(self):
        """Return all 'EEA Glossary Folder' from a Centre"""
        ret=''
        lista=self.objectItems('EEA Glossary Folder')
        lista.sort()
        for i in lista:
            o=i[1]
            ret=ret+'&nbsp;<a href="'+o.absolute_url()+'">'+o.id+'</a>&nbsp;|'
        return ret
#/alec

#alec
    def term_tip(self):
        """Return a random 'EEA Glossary Element' """
        elements=[]
        for fobject in container.objectValues('EEA Glossary Folder'):
            for eobject in fobject.objectValues('EEA Glossary Element'):
                if eobject.isPublished:
                   elements.append(eobject)
        if len(elements) > 0:
            return whrandom.choice(elements)
        else:
            return None
#/alec

#alec
    def isEmptyString(self,MyStr='',REQUEST=None):
        """return true if a string contains only white characters"""
        if MyStr and len(MyStr)>0:
            transtab=string.maketrans('','')
            idx=string.translate(MyStr,transtab,string.whitespace)
            if len(idx)<1:
                return 1
            else:
                return 0
        else:
            return 1
#/alec

    #alec
    #def manageHelp(self, REQUEST=None):
        """."""
    #/alec

    def glossary_rdf(self, REQUEST=None):
        """ Glossary in RSS 1.0 format """

        RESPONSE = REQUEST.RESPONSE
        RESPONSE.setHeader('content-type', 'text/xml')

        return """<?xml version="1.0" encoding="ISO-8859-1" ?>
        <rdf:RDF
          xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
          xmlns:dc="http://purl.org/dc/elements/1.1/"
          xmlns="http://purl.org/rss/1.0/"
        >

        <channel rdf:about="http://glossary.eea.eu.int/">
        <title>""" + self.title_or_id() + """</title>
        <link>http://glossary.eea.eu.int/</link>
        <description>""" + self.description + """</description>
        <dc:language>en</dc:language>
        <dc:publisher>EEA (European Environment Agency)</dc:publisher>
        <dc:creator>Webmaster  (mailto:webmaster@eea.eu.int)</dc:creator>
        </channel>

        <image rdf:about="http://org.eea.eu.int/images/logosmall.jpg" >
            <title>EEA (European Environment Agency)</title>
            <link>http://www.eea.eu.int</link>
            <url>http://org.eea.eu.int/images/logosmall.jpg</url>
        </image>
        </rdf:RDF>"""

    contexts_table_man = DTMLFile('dtml/EEAGlossary_contexts_table_man', globals())
    about = DTMLFile('dtml/EEAGlossary_contexts_table_man', globals())
#alec    changePass_html = DTMLFile('dtml/EEAGlossaryCentre_ChangePassForm', globals())
    term_tip_box = DTMLFile('dtml/EEAGlossaryCentre_term_tip_box', globals())
    manageHelp = DTMLFile('dtml/EEAGlossaryCentre_manageHelp', globals())
    contact_Help = DTMLFile('dtml/EEAGlossaryCentre_contact_help', globals())

    file2 = DTMLFile('dtml/f2', globals())
#alec
    style_css = DTMLFile('dtml/EEAGlossary_StyleCSS', globals())
    preview = DTMLFile('dtml/EEAGlossaryCentre_preview', globals())
    index_html = DTMLFile('dtml/EEAGlossaryCentre_index', globals())
    changePass = DTMLFile('dtml/EEAGlossaryCentre_changePass', globals())
    term_tip_box = DTMLFile('dtml/EEAGlossaryCentre_term_tip_box', globals())
    completeGlossary = DTMLFile('dtml/EEAGlossary_Complete', globals())

    #changePassAction = DTMLFile('dtml/EEAGlossaryCentre_changePassAction', globals())
#/alec
InitializeClass(EEAGlossaryCentre)

