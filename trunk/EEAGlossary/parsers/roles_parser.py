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
#$Id: roles_parser.py,v 1.1 2004/05/03 20:05:32 finrocvs Exp $

from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO
import string

class roles_struct:
    """ """
    def __init__(self, name, permissions):
        """ """
        self.name = name
        self.permissions = permissions

class roles_handler(ContentHandler):
    """ """

    def __init__(self):
        """ """
        self.roles = []

    def startElement(self, name, attrs):
        """ """
        if name == 'role':
            self.roles.append(roles_struct(attrs['name'], self.splitToList(attrs['permissions']))

    def endElement(self, name):
        """ """
        pass

    def splitToList(self, s):
        """Gets a comma separated string and returns a list"""
        res = []
        if s!='':
            res = string.split(s, ',')
        return res

class roles_parser:
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