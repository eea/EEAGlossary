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
#$Id: EEAGlossaryEngine.py,v 1.1 2004/05/04 07:23:15 finrocvs Exp $

# Zope imports
from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

# product imports
from EEAGlossary_constants import *

EngineID = 'Engine'

class EEAGlossaryEngine(SimpleItem):
    """ EEAGlossaryEngine """

    meta_type = EEA_GLOSSARY_ENGINE_METATYPE
    product_name = EEA_GLOSSARY_PRODUCT_NAME

    manage_options =({'label':'Help', 'action':'help_html'},)

    security = ClassSecurityInfo()

    def __init__(self, id):
        """ constructor """
        self.id = EngineID

    def load_roles_list(self):
        """ """
        pass

    help_html = DTMLFile("dtml/EEAGlossaryEngine/help", globals())

InitializeClass(EEAGlossaryEngine)