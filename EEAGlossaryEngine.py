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
#$Id: EEAGlossaryEngine.py,v 1.2 2004/05/04 13:32:26 finrocvs Exp $

# Zope imports
from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports
from EEAGlossary_constants import *
from EEAGlossary_utils import utils
from parsers.languages_parser import languages_parser
from parsers.subjects_parser import subjects_parser

EngineID = EEA_GLOSSARY_ENGINE_NAME

class EEAGlossaryEngine(SimpleItem, utils):
    """ EEAGlossaryEngine """

    meta_type = EEA_GLOSSARY_ENGINE_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME
    icon = 'misc_/EEAGlossary/engine.gif'

    manage_options =({'label':'Help', 'action':'help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id):
        """ constructor """
        self.id = EngineID
        self.languages = {}
        #self.translations = {}
        self.subjects = {}
        self.roles = {}

    def load_roles_list(self):
        """ """
        pass

    def load_languages_list(self):
        """loads languages & history properties defaults"""
        from os.path import join
        languages_obj = languages_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary', 'config', 'languages.xml'))
        languages_handler, error = languages_obj.parseContent(content)
        for lang in languages_handler.languages:
            self.languages[lang.english_name] = (lang.lang, lang.charset)
            #self.translations.append(lang.english_name)
            #self.history.append(lang.english_name)
        self._p_changed = 1

    def load_subjects_list (self):
        """loads subjects properties defaults"""
        from os.path import join
        subjects_obj = subjects_parser()
        content = self.utOpenFile(join(SOFTWARE_HOME, 'Products','EEAGlossary','config', 'subjects.xml'))
        subjects_handler, error = subjects_obj.parseContent(content)
        for code in subjects_handler.subjects:
            self.subjects[code.code] = code.name
        self._p_changed = 1

    help_html = DTMLFile("dtml/EEAGlossaryEngine/help", globals())

InitializeClass(EEAGlossaryEngine)