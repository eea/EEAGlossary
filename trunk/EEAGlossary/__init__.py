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
#$Id$

from ImageFile import ImageFile

import EEAGlossaryCentre
import EEAGlossaryNews
import EEAGlossaryEngine

EngineID = EEAGlossaryEngine.EngineID

def initialize(context):
    """ EEA Glossary """

    #add EEAGlossaryEngine
    app = context._ProductContext__app
    global Engine

    if hasattr(app, EngineID):
        Engine = getattr(app, EngineID)
    else:
        try:
            oEngine = EEAGlossaryEngine.EEAGlossaryEngine(id=EngineID)
            app._setObject(EngineID, oEngine)
            get_transaction().note('Added EEAGlossaryEngine')
            get_transaction().commit()
        except:
            pass
        Engine = getattr(app, EngineID)
    assert Engine is not None

    # Folder for the Glossary
    context.registerClass(
        EEAGlossaryCentre.EEAGlossaryCentre,
        constructors=(EEAGlossaryCentre.manage_addGlossaryCentre_html,
                       EEAGlossaryCentre.manage_addGlossaryCentre),
        icon='www/glossary.gif',
        )

    # Glossary News
    context.registerClass(
        EEAGlossaryNews.EEAGlossaryNews,
        constructors=(EEAGlossaryNews.manage_addGlossaryNews_html,
                       EEAGlossaryNews.manage_addGlossaryNews),
        icon='www/news.gif',
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')

misc_ = {
    'glossary.gif':ImageFile('www/glossary.gif', globals()),
    'element.gif':ImageFile('www/element.gif', globals()),
    'synonym.gif':ImageFile('www/synonym.gif', globals()),
    'folder.gif':ImageFile('www/folder.gif', globals()),
    'engine.gif':ImageFile('www/engine.gif', globals()),
    'line.gif':ImageFile('www/line.gif', globals()),
    'img_search_med.gif':ImageFile('www/img_search_med.gif', globals()),
    'img_search_small.gif':ImageFile('www/img_search_small.gif', globals()),
    'news.gif':ImageFile('www/news.gif', globals()),
    'new.gif':ImageFile('www/new.gif', globals()),

    #new glossary style
    'ico_searchhelp.gif':ImageFile('www/ico_searchhelp.gif', globals()),
    's_lefttop.gif':ImageFile('www/s_lefttop.gif', globals()),
    's_lefttop.gif':ImageFile('www/s_lefttop.gif', globals()),
    's_toplines.gif':ImageFile('www/s_toplines.gif', globals()),
    's_righttop.gif':ImageFile('www/s_righttop.gif', globals()),
    's_leftbottom.gif':ImageFile('www/s_leftbottom.gif', globals()),
    's_bottomlines.gif':ImageFile('www/s_bottomlines.gif', globals()),
    's_rightbottom.gif':ImageFile('www/s_rightbottom.gif', globals()),
    's_bcktop.gif':ImageFile('www/s_bcktop.gif', globals()),
    's_bckbottom.gif':ImageFile('www/s_bckbottom.gif', globals()),
    'searchGloss_butt.gif':ImageFile('www/searchGloss_butt.gif', globals()),
    'category.gif':ImageFile('www/category.gif', globals()),
    'dotted.gif':ImageFile('www/dotted.gif', globals()),
    'note_ico.gif':ImageFile('www/note_ico.gif', globals()),
    'separ.gif':ImageFile('www/separ.gif', globals()),
    'search_ico.gif':ImageFile('www/search_ico.gif', globals()),
    'related_ico.gif':ImageFile('www/related_ico.gif', globals())
}
