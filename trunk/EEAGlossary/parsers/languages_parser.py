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
#$Id: languages_parser.py,v 1.2 2004/05/10 15:37:01 finrocvs Exp $

from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO


class languages_struct:
    """ """
    def __init__(self, lang, charset, english_name, unicode):
        """ """
        self.lang = lang
        self.charset = charset
        self.english_name = english_name
        self.unicode = unicode

class languages_handler(ContentHandler):
    """ """

    def __init__(self):
        """ """
        self.languages = []

    def startElement(self, name, attrs):
        """ """
        if name == 'language':
            self.languages.append(languages_struct(attrs['lang'].encode('latin-1'), attrs['charset'].encode('latin-1'), attrs['englishname'].encode('latin-1'), attrs['unicode'].encode('latin-1')))

    def endElement(self, name):
        """ """
        pass

class languages_parser:
    """ """

    def parseContent(self, content):
        """ """
        handler = languages_handler()
        parser = make_parser()
        parser.setContentHandler(handler)
        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(content))
        try:
            parser.parse(inpsrc)
            return (handler, '')
        except Exception, error:
            return (None, error)