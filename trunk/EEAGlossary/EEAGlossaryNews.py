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
#$Id: EEAGlossaryNews.py,v 1.3 2004/05/17 08:54:19 finrocvs Exp $

# Zope imports
from Globals import DTMLFile, MessageDialog, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports

manage_addEEAGlossaryNewsForm = DTMLFile('dtml/EEAGlossaryNews_add', globals())
def manage_addEEAGlossaryNews(self, id, title, description,  glossary='', news_date='', REQUEST=None):
    """ Adds a new EEAGlossaryNews object """

    ob = EEAGlossaryNews(id, title, news_date,  description, glossary)
    self._setObject(id, ob)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)


class EEAGlossaryNews(SimpleItem):
    """ EEAGlossaryNews """

    meta_type='EEA Glossary News'
    security = ClassSecurityInfo()

    def __init__(self, id, title, news_date, description, glossary):
        """ constructor  for EEAGlossaryNews"""
        self.id = id
        self.title = title
        self.news_date = news_date
        self.description = description
        self.glossary = glossary

    content = DTMLFile('dtml/EEAGlossaryNews_content', globals())

InitializeClass(EEAGlossaryNews)

