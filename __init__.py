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

import EEAGlossaryCentre
import EEAGlossaryNews
from ImageFile import ImageFile

def initialize(context):
    """ EEA Glossary """

    # Folder for the Glossary
    context.registerClass(
        EEAGlossaryCentre.EEAGlossaryCentre,
        constructors=(EEAGlossaryCentre.manage_addEEAGlossaryCentreForm,
                       EEAGlossaryCentre.manage_addEEAGlossaryCentre),
        icon='www/glossary.gif',
        )

    # Glossary News
    context.registerClass(
        EEAGlossaryNews.EEAGlossaryNews,
        constructors=(EEAGlossaryNews.manage_addEEAGlossaryNewsForm,
                       EEAGlossaryNews.manage_addEEAGlossaryNews),
        icon='www/glossarynews.gif',
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')

misc_ = {
    'OpenBook.gif':ImageFile('www/OpenBook.gif', globals()),
    'folder.gif':ImageFile('www/folder.gif', globals()),
#alec
    'line.gif':ImageFile('www/line.gif', globals()),
    'img_search_med.gif':ImageFile('www/img_search_med.gif', globals()),
    'img_search_small.gif':ImageFile('www/img_search_small.gif', globals()),
    'new.gif':ImageFile('www/new.gif', globals())
#/alec
#    "glossary.gif":     ImageFile("www/glossary.gif", globals()),
#    "glossarynews.gif":     ImageFile("www/glossarynews.gif", globals()),
}
