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
#$Id: toutf8.py,v 1.2 2004/05/12 17:21:09 finrocvs Exp $

#Python imports

class toUTF8:
    """ Class toUTF-8 """ 

    def __init__(self):
        """ """
        ##
        ## ISO-8859-4
        ##
        self.iso8859_4 = [
        # /* 0xa0 */
          0x00a0, 0x0104, 0x0138, 0x0156, 0x00a4, 0x0128, 0x013b, 0x00a7,
          0x00a8, 0x0160, 0x0112, 0x0122, 0x0166, 0x00ad, 0x017d, 0x00af,
        # /* 0xb0 */
          0x00b0, 0x0105, 0x02db, 0x0157, 0x00b4, 0x0129, 0x013c, 0x02c7,
          0x00b8, 0x0161, 0x0113, 0x0123, 0x0167, 0x014a, 0x017e, 0x014b,
        # /* 0xc0 */
          0x0100, 0x00c1, 0x00c2, 0x00c3, 0x00c4, 0x00c5, 0x00c6, 0x012e,
          0x010c, 0x00c9, 0x0118, 0x00cb, 0x0116, 0x00cd, 0x00ce, 0x012a,
        # /* 0xd0 */
          0x0110, 0x0145, 0x014c, 0x0136, 0x00d4, 0x00d5, 0x00d6, 0x00d7,
          0x00d8, 0x0172, 0x00da, 0x00db, 0x00dc, 0x0168, 0x016a, 0x00df,
        # /* 0xe0 */
          0x0101, 0x00e1, 0x00e2, 0x00e3, 0x00e4, 0x00e5, 0x00e6, 0x012f,
          0x010d, 0x00e9, 0x0119, 0x00eb, 0x0117, 0x00ed, 0x00ee, 0x012b,
        # /* 0xf0 */
          0x0111, 0x0146, 0x014d, 0x0137, 0x00f4, 0x00f5, 0x00f6, 0x00f7,
          0x00f8, 0x0173, 0x00fa, 0x00fb, 0x00fc, 0x0169, 0x016b, 0x02d9,
        ]

        ##
        ## ISO-8859-2
        ##
         
        self.iso8859_2 = [
        # /* 0xa0 */
          0x00a0, 0x0104, 0x02d8, 0x0141, 0x00a4, 0x013d, 0x015a, 0x00a7,
          0x00a8, 0x0160, 0x015e, 0x0164, 0x0179, 0x00ad, 0x017d, 0x017b,
        # /* 0xb0 */
          0x00b0, 0x0105, 0x02db, 0x0142, 0x00b4, 0x013e, 0x015b, 0x02c7,
          0x00b8, 0x0161, 0x015f, 0x0165, 0x017a, 0x02dd, 0x017e, 0x017c,
        # /* 0xc0 */
          0x0154, 0x00c1, 0x00c2, 0x0102, 0x00c4, 0x0139, 0x0106, 0x00c7,
          0x010c, 0x00c9, 0x0118, 0x00cb, 0x011a, 0x00cd, 0x00ce, 0x010e,
        # /* 0xd0 */
          0x0110, 0x0143, 0x0147, 0x00d3, 0x00d4, 0x0150, 0x00d6, 0x00d7,
          0x0158, 0x016e, 0x00da, 0x0170, 0x00dc, 0x00dd, 0x0162, 0x00df,
        # /* 0xe0 */
          0x0155, 0x00e1, 0x00e2, 0x0103, 0x00e4, 0x013a, 0x0107, 0x00e7,
          0x010d, 0x00e9, 0x0119, 0x00eb, 0x011b, 0x00ed, 0x00ee, 0x010f,
        # /* 0xf0 */
          0x0111, 0x0144, 0x0148, 0x00f3, 0x00f4, 0x0151, 0x00f6, 0x00f7,
          0x0159, 0x016f, 0x00fa, 0x0171, 0x00fc, 0x00fd, 0x0163, 0x02d9,
        ]

        self.cp1252 = [
        # Starts at 0x80
          0x20AC, 0x0000, 0x201A, 0x0192, 0x201E, 0x2026, 0x2020, 0x2021,
          0x02C6, 0x2030, 0x0160, 0x2039, 0x0152, 0x0000, 0x017D, 0x0000,
        # 0x90
          0x0000, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014,
          0x02DC, 0x2122, 0x0161, 0x203A, 0x0153, 0x0000, 0x017E, 0x0178,
        ]

    def toutf8(self, s, charset):
        """transfer to Unicode"""
        strlist = list(s)
        res = ""
        if (charset == 'iso-8859-7'):
            for ch in strlist:
                if ord(ch) >= 0xb4:
                    res = res + "&#" + `ord(ch) + 720` + ";"
                else:
                    res = res + ch

        elif (charset == 'iso-8859-5'):
            for ch in strlist:
                if ord(ch) >= 0xa0:
                    res = res + "&#" + `ord(ch) + 864` + ";"
                else:
                    res = res + ch

        elif (charset == 'iso-8859-4'):
            for ch in strlist:
                if ord(ch) >= 0xa0:
                    res = res + "&#" + `self.iso8859_4[ord(ch) - 0xa0]` + ";"
                else:
                    res = res + ch
        elif (charset == 'iso-8859-2'):
            for ch in strlist:
                if ord(ch) >= 0xa0:
                    res = res + "&#" + `self.iso8859_2[ord(ch) - 0xa0]` + ";"
                else:
                    res = res + ch
        else:               #Assume iso-8859-1 if unknown charset
            for ch in strlist:
                o = ord(ch)
                if o >= 0x80 and o <= 0x9f:
                    res = res + "&#" + `self.cp1252[o - 0x80]` + ";"
                elif o >= 0xa0:
                    res = res + "&#" + `ord(ch)` + ";"
                else:
                    res = res + ch
        return res