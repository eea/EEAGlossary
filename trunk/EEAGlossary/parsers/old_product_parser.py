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
    def __init__(self, glossary_type, id, title, description):
        """ """
        self.glossary_type = glossary_type
        self.id = id
        self.title = title
        self.description = description

class element_struct:
    """ """
    def __init__(self, glossary_type, id_folder, id, type, source, context, comment,
                       used_for_1, used_for_2, definition, definition_source, subjects,
                       disabled, approved, long_definition, QA_needed, definition_source_url,
                       definition_source_year, definition_source_org, definition_source_org_full_name,
                       translations):
        """ """
        self.glossary_type = glossary_type
        self.id_folder = id_folder
        self.id = id
        self.type = type
        self.source = source
        self.context = context
        self.comment = comment
        self.used_for_1 = used_for_1
        self.used_for_2 = used_for_2
        self.definition = definition
        self.definition_source = definition_source
        self.subjects = subjects
        self.disabled = disabled
        self.approved = approved
        self.long_definition = long_definition
        self.QA_needed = QA_needed
        self.definition_source_url = definition_source_url
        self.definition_source_year = definition_source_year
        self.definition_source_org = definition_source_org
        self.definition_source_org_full_name = definition_source_org_full_name
        self.translations = translations

class synonym_struct:
    """ """
    def __init__(self, glossary_type, id_folder, id, name, disabled, approved, synonyms):
        """ """
        self.glossary_type = glossary_type
        self.id_folder = id_folder
        self.id = id
        self.name = name
        self.disabled = disabled
        self.approved = approved
        self.synonyms = synonyms

class old_product__handler(ContentHandler, utils):
    """ """

    def __init__(self):
        """ """
        self.content = []
        self.current_folder = ''

    def startElement(self, name, attrs):
        """ """
        if name == 'GFolder':
            self.current_folder = (attrs['id']).encode('utf-8')
            self.content.append(folder_struct('folder', self.current_folder, (attrs['title']).encode('utf-8'), (attrs['description']).encode('utf-8')))
        if name == 'GElement':
            #GlossaryElement's translations
            l_translations = {}
##            l_translations['Bulgarian'] = (attrs['Bulgarian']).encode('utf-8')
##            l_translations['Crotian'] = (attrs['Crotian']).encode('utf-8')
##            l_translations['Czech'] = (attrs['Czech']).encode('utf-8')
#            l_translations['Danish'] = attrs['Danish']
#            l_translations['Dutch'] = attrs['Dutch']
            l_translations['English'] = (attrs['English']).encode('utf-8')
##            l_translations['Estonian'] = (attrs['Estonian']).encode('utf-8')
#            l_translations['Finnish'] = attrs['Finnish']
#            l_translations['French'] = attrs['French']
#            l_translations['German'] = attrs['German']
##            l_translations['Greek'] = (attrs['Greek']).encode('utf-8')
##            l_translations['Hungarian'] = (attrs['Hungarian']).encode('utf-8')
#            l_translations['Icelandic'] = attrs['Icelandic']
#            l_translations['Italian'] = attrs['Italian']
#            l_translations['Latvian'] = attrs['Latvian']
#            l_translations['Lithuanian'] = attrs['Lithuanian']
##            l_translations['Macedonian'] = (attrs['Macedonian']).encode('utf-8')
##            l_translations['Maltese'] = (attrs['Maltese']).encode('utf-8')
#            l_translations['Norwegian'] = attrs['Norwegian']
##            l_translations['Polish'] = (attrs['Polish']).encode('utf-8')
#            l_translations['Portuguese'] = attrs['Portuguese']
##            l_translations['Romanian'] = (attrs['Romanian']).encode('utf-8')
##            l_translations['Russian'] = (attrs['Russian']).encode('utf-8')
##            l_translations['Serbian'] = (attrs['Serbian']).encode('utf-8')
            l_translations['Slovak'] = (attrs['Slovak']).encode('utf-8')
#            l_translations['Slovenian'] = attrs['Slovenian']
#            l_translations['Spanish'] = attrs['Spanish']
#            l_translations['Swedish'] = attrs['Swedish']
#            l_translations['Turkish'] = attrs['Turkish']

            self.content.append(element_struct(
                            #GlossaryElement's descriptors
                            'element', #glossary internal type
                            self.current_folder, #parent folder

                            #GlossaryElement's properties
                            (attrs['id']).encode('utf-8'),
                            (attrs['type']).encode('utf-8'),
                            (attrs['source']).encode('utf-8'),
                            (attrs['context']).encode('utf-8'),
                            (attrs['comment']).encode('utf-8'),
                            (attrs['used_for_1']).encode('utf-8'),
                            (attrs['used_for_2']).encode('utf-8'),
                            (attrs['definition']).encode('utf-8'),
                            (attrs['definition_source']).encode('utf-8'),
                            (attrs['subjects']).encode('utf-8'),
                            (attrs['disabled']).encode('utf-8'),
                            (attrs['approved']).encode('utf-8'),
                            (attrs['long_definition']).encode('utf-8'),
                            (attrs['QA_needed']).encode('utf-8'),
                            (attrs['definition_source_url']).encode('utf-8'),
                            (attrs['definition_source_year']).encode('utf-8'),
                            (attrs['definition_source_org']).encode('utf-8'),
                            (attrs['definition_source_org_full_name']).encode('utf-8'),

                            #GlossaryElement's translations
                            l_translations))
        if name == 'GSynonym':
            self.content.append(synonym_struct(
                            #GlossarySynonym's descriptors
                            'synonym', #glossary internal type
                            self.current_folder, #parent folder

                            #GlossarySynonym's properties
                            (attrs['id']).encode('utf-8'),
                            (attrs['name']).encode('utf-8'),
                            (attrs['disabled']).encode('utf-8'),
                            (attrs['approved']).encode('utf-8'),
                            (attrs['synonyms']).encode('utf-8')))

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