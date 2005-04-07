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
#$Id$


from DateTime import DateTime
from types import UnicodeType, StringType
import string
from xml.sax import make_parser, handler, InputSource
from cStringIO import StringIO
from Globals import MessageDialog

#product imports
from EEAGlossary_utils import utils
from parsers.tmx_parser import tmx_parser
from parsers.old_product_parser import old_product_parser

class glossary_export:
    """ """
    
    def __init__(self):
        """ constructor """

    def xliff_header(self, folders, language):
        """ return the xliff header """
        
        results = []
        r_append = results.append   #alias for append function. For optimization purposes
        # Generate the XLIFF file header
        if folders == '/':
            folders='all'
        else:
            folders = string.split(folders, '/')[-1]
        self.REQUEST.RESPONSE.setHeader('Content-Type', 'application/data; charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s_%s_%s.xliff"' % (self.id, folders, language))
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
        """ Exports the content to an XLIFF file """
        from types import UnicodeType
        results_list = []
        results = []
        terms = []
        r_append = results_list.append   #alias for append function. For optimization purposes
        if not published:
            terms.extend(self.get_published('/%s' % folder))
        else:
            terms.extend(self.get_all_objects('/%s' % folder))
        results_list.extend(self.xliff_header(folder, language))
        for term in terms:
            term.get_translation_by_language('English')
            #translation = term.get_translation_by_language(language)
            if language in self.get_unicode_langs():
                translation = self.convertWinCodesToHTMLCodes(term.get_translation_by_language(language))
            else:
                translation = self.display_unicode_langs(term.get_translation_by_language(language), charset=self.get_language_charset(language))
            r_append('<trans-unit id="%s">' % term.id)
            r_append('<source>%s</source>' % term.get_translation_by_language('English'))
            r_append('<target>%s</target>' % translation)
            if term.definition:
                pass #r_append('<note>%s</note>' % term.definition)
            r_append('</trans-unit>')
        results_list.extend(self.xliff_footer())
        for x in results_list:
            if type(x) is UnicodeType:
                results.append(x.encode('utf-8'))
            else:
                results.append(x)
        return '\r\n'.join(results)

    def tmx_export(self, folder='/', published=0, REQUEST=None):
        """ Exports the content to a TMX file """
        results = []
        results_list=[]
        terms=[]
        r_append = results_list.append
        if published:
            terms.extend(self.get_published('/%s' % folder))
        else:
            terms.extend(self.get_all_objects('/%s' % folder))

        results_list.extend(self.tmx_header(folder))

        for term in terms:
            r_append('<tu tuid="%s">' % term.id)
            for language in self.get_english_names():
                translation = term.get_translation_by_language(language)
                if language in self.get_unicode_langs():
                    r_append('<tuv xml:lang="%s">' % language)
                    r_append('<seg>%s</seg></tuv>' % self.convertWinCodesToHTMLCodes(translation))
                else:
                    r_append('<tuv xml:lang="%s">' % language)
                    r_append('<seg>%s</seg></tuv>' % self.display_unicode_langs(translation,self.get_language_charset(language)))
            r_append('</tu>')
            r_append('')

        results_list.extend(self.tmx_footer())
        for x in results_list:
            if type(x) is UnicodeType:
                results.append(x.encode('utf-8'))
            else:
                results.append(x)
        return '\r\n'.join(results)

    def tmx_header(self, folders):
        """ return the tmx header """
        r=[]
        r_append = r.append
        if folders == '/':
            folders='all'
        else:
            folders = string.split(folders, '/')[-1]
        self.REQUEST.RESPONSE.setHeader('Content-type', 'application/data; charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s_%s.tmx"' % (self.id, folders))
        r_append('<?xml version="1.0" encoding="utf-8"?>')
        r_append('<!DOCTYPE tmx SYSTEM "http://www.lisa.org/tmx/tmx14.dtd">')
        r_append('<tmx version="1.4">')
        r_append('<header')
        r_append(' creationtool="EEAGlossary"')
        r_append(' creationtoolversion="1.x"')
        r_append(' datatype="plaintext"')
        r_append(' segtype="paragraph"')
        r_append(' adminlang="English"')
        r_append(' srclang="English"')
        r_append(' o-encoding="utf-8"')

        r.append('>')
        r.append('</header>')
        r.append('<body>')
        r.append('')
        return r

    def tmx_footer(self):
        """ return the tmx footer """
        r=[]
        r_append = r.append
        r_append('</body>')
        r_append('</tmx>')
        return r

    ##################
    #   tmx import   #
    ##################

    def tmx_import(self, file, REQUEST=None):
        """ Imports a TMX file """
        
        from types import UnicodeType, StringType
        import string
        from xml.sax import make_parser, handler, InputSource
        from cStringIO import StringIO

        parser = tmx_parser()

        #parse the tmx information
        chandler = parser.parseContent(file)

        if chandler is None:
            return MessageDialog(title = 'Parse error',
             message = 'Unable to parse TMX file' ,  action = 'manage_main',)
                        
        l_list = chandler.TMXContent.keys()
        l_list.sort()
        for k in l_list:
            folder_id = self.utf8_to_latin1(string.upper(k[:1]))
            folder = self.unrestrictedTraverse(folder_id, None)
            if folder is None:
                try:
                    self.manage_addGlossaryFolder(folder_id)
                    folder = self._getOb(folder_id)
                except Exception, error:
                    print error
            elem_ob = folder._getOb(k, None)
            if elem_ob is not None:
                for lang,trans in chandler.TMXContent[k].items():
                    if trans != '':
                        elem_ob.set_translations_list(lang, trans.encode('utf-8'))
                        elem_ob.set_history(lang, trans.encode('utf-8'))
                elem_ob.cu_recatalog_object(elem_ob)
            else:
                try:
                    elem_name = self.utf8_to_latin1(chandler.TMXContent[k]['English'])
                    folder.manage_addGlossaryElement(elem_name, '', '', [], '', '', '', '', '', 
                    'dataservice, http://dataservice.eea.eu.int', '', 0, 1, 0, '', '', [], [], {})
                except Exception, error:
                    print error
                elem_ob = folder._getOb(k, None)
                if elem_ob is not None:
                    for lang,trans in chandler.TMXContent[k].items():
                        elem_ob.set_translations_list(lang, trans.encode('utf-8'))
                        elem_ob.set_history(lang, trans.encode('utf-8'))
                    elem_ob.cu_recatalog_object(elem_ob)


    ##########################
    #   old product import   #
    ##########################

    def old_product_import(self, file, REQUEST=None):
        """ Imports from XML (old product format) """

        from types import UnicodeType, StringType
        import string
        from xml.sax import make_parser, handler, InputSource
        from cStringIO import StringIO

        synonym_list = []

        parser = old_product_parser()

        #parse the xml information
        chandler = parser.parseContent(file)

        if chandler is None:
            return MessageDialog(title = 'Parse error',
             message = 'Unable to parse file' ,  action = 'manage_main',)

        l_content = chandler.content

        for l_item in l_content:

            if l_item.glossary_type == 'folder':
                try:
                    self.manage_addGlossaryFolder(l_item.id, l_item.title, l_item.description)
                except:
                    print 'folder error: %s' % l_item.id

            elif l_item.glossary_type == 'element':
                l_parent_folder = self.unrestrictedTraverse(l_item.id_folder, None)
                try:
                    #creates element object with base properties
                    l_parent_folder.manage_addGlossaryElement(
                                l_item.translations['English'],
                                l_item.type,
                                l_item.source,
                                self.get_subject_by_name(self.utSplitToList(l_item.subjects, ',')),
                                l_item.context,
                                l_item.comment,
                                l_item.definition,
                                'dataservice, http://dataservice.eea.eu.int',
                                l_item.definition_source_year,
                                l_item.definition_source_url,
                                l_item.definition_source_org,
                                l_item.definition_source_org_full_name,
                                l_item.long_definition,
                                self.utConvertToInt(l_item.disabled),
                                self.utConvertToInt(l_item.approved),
                                self.utConvertToInt(l_item.QA_needed),
                                '', #image_url
                                '', #flash_url
                                [], #links
                                [], #actions
                                {}, #translations
                                [], #synonym
                                l_item.id)

                    #translations
                    elem_ob = l_parent_folder._getOb(l_item.id, None)
                    for lang,trans in l_item.translations.items():
                        elem_ob.set_translations_list(lang, trans)
                        elem_ob.set_history(lang, trans)

                    #catalog object
                    elem_ob.cu_recatalog_object(elem_ob)
                except:
                    print 'elem error: %s' % l_item.id
            elif l_item.glossary_type == 'synonym':
                synonym_list.append(l_item)

        for l_item in synonym_list:
            if l_item.glossary_type == 'synonym':
                l_parent_folder = self.unrestrictedTraverse(l_item.id_folder, None)
                try:
                    #synonyms base properties
                    l_parent_folder.manage_addGlossarySynonym(
                                l_item.id,
                                [])

                    #synonym relations
                    synonym_ob = l_parent_folder._getOb(l_item.id, None)
                    if string.strip(l_item.synonyms) != '':
                        synonym_ob.manageSynonymProperties(l_item.synonyms)

                    #synonyms other properties
                    synonym_ob.manageSynonymOtherProperties(
                                l_item.name,
                                l_item.disabled,
                                l_item.approved)
                except:
                    print 'synonym error: %s' % l_item.id
        print 'done'