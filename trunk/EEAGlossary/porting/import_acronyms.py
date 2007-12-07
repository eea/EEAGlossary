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
# Agency (EEA).  Portions created by Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Alex Ghica, Eau de Web
# Antonio De Marinis, EEA

def import_acr(context, REQUEST=None):
    import csv
    from os.path import join
    from Products.EEAGlossary.EEAGlossary_constants import EEAGLOSSARY_PATH

    reader = csv.reader(open(join(EEAGLOSSARY_PATH, 'porting', 'ACRONYMS.csv'), "rb"), csv.excel)
    for rec in reader:
        if rec:
            if context.check_subjects_exists(rec[0]):
                context.set_subjects_list(rec[0], rec[1])
                context._p_changed = 1

    return 'Done.'
