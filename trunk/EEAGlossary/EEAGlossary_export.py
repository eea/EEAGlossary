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
#$Id: EEAGlossary_export.py,v 1.3 2004/05/28 10:53:13 finrocvs Exp $

from DateTime import DateTime

class glossary_export:
    """ """
    
    def __init__(self):
        """ constructor """

    def xliff_header(self, folders, language):
        """ return the xliff header """
        
        results = []
        r_append = results.append   #alias for append function. For optimization purposes
        # Generate the XLIFF file header
        self.REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml; charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s_%s_%s.xml"' % (self.id, folders, language))
        r_append('<?xml version="1.0" encoding="UTF-8"?>')
        r_append('<!DOCTYPE xliff SYSTEM "http://www.oasis-open.org/committees/xliff/documents/xliff.dtd">')
        r_append(u'<!-- XLIFF Format Copyright \xa9 OASIS Open 2001-2003 -->')
        r_append('<xliff version="1.0">')
        r_append('<file')
        r_append(' original="%s"' % self.absolute_url(1))
        r_append(' product-name="EEAGlossary"')
        r_append(' product-version="1.1.x"')
        r_append(' datatype="plaintext"')
        r_append(' source-language="English"')
        r_append(' target-language="%s"' % language)
        r_append(' date="%s"' % DateTime().HTML4())
        r_append('>')
        r_append('<body>')
        return results

    def xliff_footer(self):
        results = []
        r_append = results.append   #alias for append function. For optimization purposes
        r_append('</body>')
        r_append('</file>')
        r_append('</xliff>')
        return results

    def xliff_export(self, folder='/', language='', published=0, REQUEST=None):
        """ Exports the content of the EEAGlossary to an XLIFF file """
        results = []
        terms = []
        r_append = results.append   #alias for append function. For optimization purposes
        for folder in self.folder_list_sorted():
            if published:
                terms.extend(self.get_published('/%s' % folder))
            else:
                terms.extend(self.get_all_objects('/%s' % folder))
        results.extend(self.xliff_header(folder, language))
        for term in terms:
            #if language in self.get_unicode_langs():
            #    translation = term.get_translation_by_language(language)
            #else:
            #    translation = self.display_unicode_langs(term.get_translation_by_language(language), charset=self.get_language_charset(language))
            translation = term.get_translation_by_language(language)
            r_append('<trans-unit id="%s">' % term.id)
            r_append(' <source>%s</source>' % term.get_translation_by_language('English'))
            r_append(' <target>%s</target>' % translation)
            if term.definition:
                r_append(' <note>%s</note>' % term.definition)
            r_append('</trans-unit>')
        results.extend(self.xliff_footer())
        return '\r\n'.join(results)
