###########
# imports #
###########
import base64

################
# default data #
################
messages = []
messages.append("""<?xml version="1.0" encoding="utf-8"?>\n<export>""")

glossary_objects = ["GlossaryFolder", "GlossaryElement", "GlossarySynonym"]
additional_objects =["GlossaryNews", "GlossaryCenter"]
glossary_objects.extend(additional_objects)

root = container.restrictedTraverse('/')

####################
# export functions #
####################
def exportGlossaryContent(glossary_center):
    for item in glossary_center.objectValues(glossary_objects):
        if item.meta_type == "GlossaryFolder":
            messages.append('%s' % (exportGlossaryFolder(item)))

            for glossary_item in item.objectValues(["GlossaryElement", "GlossarySynonym"]):
                if glossary_item.meta_type == "GlossaryElement":
                    messages.append('%s' % (exportGlossaryElement(glossary_item)))
                elif glossary_item.meta_type == "GlossarySynonym":
                     messages.append('%s' % (exportGlossarySynonym(glossary_item)))

            messages.append('\n</GFolder>')

def exportGlossaryFolder(p_item):
    #folders start
    l_temp = ''
    l_temp += '\n<GFolder'

    #folders properties
    l_temp += ' id="%s"' % utXmlEncode(p_item.id)
    l_temp += ' title="%s"' % utXmlEncode(p_item.title)
    l_temp += ' description="%s"' % utXmlEncode(p_item.description)
    l_temp += '>'
    return l_temp

def exportGlossaryElement(p_item):
    #elements start
    l_temp = ''
    l_temp += '\n<GElement'

    #elements properties
    l_temp += ' id="%s"' % utXmlEncode(p_item.id)
    l_temp += ' name="%s"' % utXmlEncode(p_item.name)
    l_temp += ' type="%s"' % utXmlEncode(p_item.type) #selection
    l_temp += ' source="%s"' % utXmlEncode(p_item.source)
    l_temp += ' context="%s"' % utXmlEncode(p_item.context)
    l_temp += ' comment="%s"' % utXmlEncode(p_item.comment) #text
    l_temp += ' used_for_1="%s"' % utXmlEncode(p_item.used_for_1)
    l_temp += ' used_for_2="%s"' % utXmlEncode(p_item.used_for_2)
    l_temp += ' definition="%s"' % utXmlEncode(p_item.definition) #text
    l_temp += ' definition_source="%s"' % utXmlEncode(p_item.definition_source)
    l_temp += ' subjects="%s"' % utXmlEncode(p_item.subjects) #multiple select
    l_temp += ' disabled="%s"' % utXmlEncode(p_item.disabled) #boolean
    l_temp += ' approved="%s"' % utXmlEncode(p_item.approved) #boolean
    l_temp += ' long_definition="%s"' % utXmlEncode(p_item.long_definition) #text
    l_temp += ' QA_needed="%s"' % utXmlEncode(p_item.QA_needed) #boolean
    l_temp += ' definition_source_url="%s"' % utXmlEncode(p_item.definition_source_url)
    l_temp += ' definition_source_year="%s"' % utXmlEncode(p_item.definition_source_year)
    l_temp += ' definition_source_org="%s"' % utXmlEncode(p_item.definition_source_org)
    l_temp += ' definition_source_org_full_name="%s"' % utXmlEncode(p_item.definition_source_org_full_name)

    #elements translations
    l_temp += ' Bulgarian="%s"' % utXmlEncode(p_item.Bulgarian)
    l_temp += ' Croatian="%s"' % utXmlEncode(p_item.Croatian)
    l_temp += ' Czech="%s"' % utXmlEncode(p_item.Czech)
    l_temp += ' Danish="%s"' % utXmlEncode(p_item.Danish)
    l_temp += ' Dutch="%s"' % utXmlEncode(p_item.Dutch)
    l_temp += ' English="%s"' % utXmlEncode(p_item.English)
    l_temp += ' Estonian="%s"' % utXmlEncode(p_item.Estonian)
    l_temp += ' Finnish="%s"' % utXmlEncode(p_item.Finnish)
    l_temp += ' French="%s"' % utXmlEncode(p_item.French)
    l_temp += ' German="%s"' % utXmlEncode(p_item.German)
    l_temp += ' Greek="%s"' % utXmlEncode(p_item.Greek)
    l_temp += ' Hungarian="%s"' % utXmlEncode(p_item.Hungarian)
    l_temp += ' Icelandic="%s"' % utXmlEncode(p_item.Icelandic)
    l_temp += ' Italian="%s"' % utXmlEncode(p_item.Italian)
    l_temp += ' Latvian="%s"' % utXmlEncode(p_item.Latvian)
    l_temp += ' Lithuanian="%s"' % utXmlEncode(p_item.Lithuanian)
    l_temp += ' Macedonian="%s"' % utXmlEncode(p_item.Macedonian)
    l_temp += ' Polish="%s"' % utXmlEncode(p_item.Polish)
    l_temp += ' Portuguese="%s"' % utXmlEncode(p_item.Portuguese)
    l_temp += ' Romanian="%s"' % utXmlEncode(p_item.Romanian)
    l_temp += ' Russian="%s"' % utXmlEncode(p_item.Russian)
    l_temp += ' Serbian="%s"' % utXmlEncode(p_item.Serbian)
    l_temp += ' Slovak="%s"' % utXmlEncode(p_item.Slovak)
    l_temp += ' Slovenian="%s"' % utXmlEncode(p_item.Slovenian)
    l_temp += ' Spanish="%s"' % utXmlEncode(p_item.Spanish)
    l_temp += ' Swedish="%s"' % utXmlEncode(p_item.Swedish)
    l_temp += ' Turkish="%s"' % utXmlEncode(p_item.Turkish)
    l_temp += ' Norwegian="%s"' % utXmlEncode(p_item.Norwegian)
    l_temp += ' Maltese="%s"' % utXmlEncode(p_item.Maltese)

    #elements end
    l_temp += ' />'
    return l_temp

def exportGlossarySynonym(p_item):
    #synonyms start
    l_temp = ''
    l_temp = '\n<GSynonym>'

    #synonyms properties
    #...to be completed

    #synonyms end
    l_temp+=' \n</GSynonym>'
    return l_temp

def utXmlEncode(p_string):
    """Encode some special chars"""
    l_tmp = str(p_string)
    l_tmp = l_tmp.replace('&', '&amp;')
    l_tmp = l_tmp.replace('<', '&lt;')
    l_tmp = l_tmp.replace('"', '&quot;')
    l_tmp = l_tmp.replace('\'', '&apos;')
    l_tmp = l_tmp.replace('>', '&gt;')
    return l_tmp

##################
# script content #
##################
for glossary_center in root.objectValues("GlossaryCenter"):
    if glossary_center.id==glossary_center_id:
        exportGlossaryContent(glossary_center)

messages.append("""\n</export>""")
print ''.join(messages)
return printed