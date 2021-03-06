# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2018, 2019 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Return link with ROR ID(s)
"""


def format_element(bfo, style='', separator='; '):
    """
    This is the default format for formatting ROR IDs.
    @param separator: the separator between ROR IDs.
    @param style: CSS class of the link
    """

    BASEURL = 'https://ror.org/'

    ror_ids = set()

    tags = bfo.fields("035__")
    for item in tags:
        if item.get('9', '').upper() == 'ROR' and \
           item.get('a', '').startswith(BASEURL):
            ror_ids.add(item.get('a'))

    if style != "":
        style = 'class="{0}"'.format(style)

    links = ['<a {0} href="{1}">{2}</a>'.format(style, ror, ror)
             for ror in ror_ids]
    return separator.join(links)


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
