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
#$Id: EEAGlossaryNews.py,v 1.4 2004/05/17 11:08:40 finrocvs Exp $

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports
from EEAGlossary_constants import *

manage_addGlossaryNews_html = DTMLFile('dtml/EEAGlossaryNews/add', globals())

def manage_addGlossaryNews(self, id, title='', news_date='', description='', glossary='', REQUEST=None):
    """ adds a new EEAGlossaryNews object """
    ob = EEAGlossaryNews(id, title, news_date, description, glossary)
    self._setObject(id, ob)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


class EEAGlossaryNews(SimpleItem):
    """ EEAGlossaryNews """

    meta_type=EEA_GLOSSARY_NEWS_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/news.gif'

    manage_options = (
        {'label':'Properties',                      'action':'manage_properties_html'},
        {'label':'Undo',                       'action':'manage_UndoForm'},
        {'label':'Ownership',         'action':'manage_owner'},)

    security = ClassSecurityInfo()

    def __init__(self, id, title, news_date, description, glossary):
        """ constructor """
        self.id = id
        self.title = title
        self.news_date = news_date
        self.description = description
        self.glossary = glossary

    def manage_news_properties(self, title='', news_date='', description='', glossary='', REQUEST=None):
        """ folder properties """
        self.title=title
        self.news_date=news_date
        self.description=description
        self.glossary=glossary
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('manage_properties_html?save=ok')

    manage_properties_html = DTMLFile("dtml/EEAGlossaryNews/properties", globals())

InitializeClass(EEAGlossaryNews)

