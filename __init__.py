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
#$Id: __init__.py,v 1.6 2004/05/04 13:32:26 finrocvs Exp $

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
        Engine.load_roles_list()
        Engine.load_languages_list()
        Engine.load_subjects_list()
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
        constructors=(EEAGlossaryNews.manage_addEEAGlossaryNewsForm,
                       EEAGlossaryNews.manage_addEEAGlossaryNews),
        icon='www/glossarynews.gif',
        )

    context.registerHelp()
    context.registerHelpTitle('Zope Help')

misc_ = {
    'element.gif':ImageFile('www/element.gif', globals()),
    'folder.gif':ImageFile('www/folder.gif', globals()),
    'engine.gif':ImageFile('www/engine.gif', globals()),
#alec
    'line.gif':ImageFile('www/line.gif', globals()),
    'img_search_med.gif':ImageFile('www/img_search_med.gif', globals()),
    'img_search_small.gif':ImageFile('www/img_search_small.gif', globals()),
    'new.gif':ImageFile('www/new.gif', globals())
}
