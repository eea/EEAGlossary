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
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#
#

from xml.sax.handler import ContentHandler
from xml.sax import *
from Products.EEAGlossary.EEAGlossary_utils import utils
from types import StringType
from cStringIO import StringIO


class folder_struct:
    """ """
    def __init__(self, id):
        """ """
        self.id = id

class element_struct:
    """ """
    def __init__(self, id):
        """ """
        self.id = id

class synonym_struct:
    """ """
    def __init__(self, id):
        """ """
        self.id = id

class old_product__handler(ContentHandler, utils):
    """ """

    def __init__(self):
        """ """
        self.folders = []
        self.elements = []
        self.synonyms = []

    def startElement(self, name, attrs):
        """ """
        if name == 'export':
            self.folders.append('folder')

    def endElement(self, name):
        """ """
        pass

class old_product_parser:

    def __init__(self):
        """ """
        pass
        
    def parseContent(self, file):
        # Create a parser
        parser = make_parser()
        chandler = old_product__handler()
        # Tell the parser to use our handler
        parser.setContentHandler(chandler)
        # Don't load the DTD from the Internet
        try:
            parser.setFeature(handler.feature_external_ges, 0)
        except:
            pass
        inputsrc = InputSource()

        if type(file) is StringType:
            inputsrc.setByteStream(StringIO(file))
        else:
            filecontent = file.read()
            inputsrc.setByteStream(StringIO(filecontent))
        parser.parse(inputsrc)
        return chandler
        
        try:
            if type(file) is StringType:
                inputsrc.setByteStream(StringIO(file))
            else:
                filecontent = file.read()
                inputsrc.setByteStream(StringIO(filecontent))
            parser.parse(inputsrc)
            return chandler
        except:
            return None