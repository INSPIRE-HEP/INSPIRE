# -*- coding: utf-8 -*-
##
## $Id$
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2011, 2015, 2016, 2018 CERN.
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
"""
BibFormat element - Prints authors

"""


def format_element(
        bfo, limit, separator='; ',
        extension='[...]',
        print_links="yes",
        print_affiliations='no',
        affiliation_prefix=' (',
        affiliation_suffix=')',
        print_affiliation_first='no',
        interactive="no",
        highlight="no",
        affiliations_separator=" ; ",
        name_last_first="yes",
        collaboration="yes",
        id_links="no",
        markup="html",
        link_extension="no",
):

    """
    Prints the list of authors of a record.

    @param limit the maximum number of authors to display
    @param separator the separator between authors.
    @param extension a text printed if more authors than 'limit' exist
    @param print_links if yes, prints the authors as HTML link to their
           publications
    @param print_affiliations if yes, make each author name followed by
           its affiliation
    @param affiliation_prefix prefix printed before each affiliation
    @param affiliation_suffix suffix printed after each affiliation
    @param print_affiliation_first if 'yes', affiliation is printed before
           the author
    @param interactive if yes, enable user to show/hide authors when there
           are too many (html + javascript)
    @param highlight highlights authors corresponding to search query if set
           to 'yes'
    @param affiliations_separator separates affiliation groups
    @param name_last_first if yes (default) print last, first  otherwise
           print first last
    @param collaboration if yes (default) uses collaboration name in place
           of long author list, if available
    @param id_links if yes (default = no) prints link based on INSPIRE IDs
           if available - only used if print_links = yes
    @param markup html (default) or latex or bibtex controls small markup
           differences
    @param link_extension if 'yes' link the extension to the detailed
           record page

    """
    from urllib import quote
    from cgi import escape
    import re
    from invenio.messages import gettext_set_language
    from invenio.config import CFG_SITE_RECORD

    try:
        from invenio.config import CFG_BASE_URL
    except ImportError:
        from invenio.config import CFG_SITE_URL
        CFG_BASE_URL = CFG_SITE_URL

    _ = gettext_set_language(bfo.lang)    # load the right message language

    # regex for parsing last and first names and initials
    re_last_first = re.compile(
        r'^(?P<last>[^,]+)\s*,\s*(?P<first_names>[^\,]*)(?P<extension>\,?.*)$')
    re_initials = re.compile(r'(?P<initial>\w)([\w`\']+)?.?\s*', re.UNICODE)
    re_tildehyph = re.compile(
        ur'(?<=\.)~(?P<hyphen>[\u002D\u00AD\u2010-\u2014-])(?=\w)', re.UNICODE)
    re_coll = re.compile(r'\s*collaborations?', re.IGNORECASE)

    bibrec_id = bfo.control_field("001")
    authors = []
    lastauthor = ''
    only_corporate_author = False
    authors = bfo.fields('100__', repeatable_subfields_p=True)
    authors.extend(bfo.fields('700__', repeatable_subfields_p=True))

    # If there are no authors check for corporate author in 110__a field
    if len(authors) == 0:
        authors = bfo.fields('110__', repeatable_subfields_p=True)
        if len(authors) > 0:
            only_corporate_author = True
        # For corporate authors we don't want to reverse names order
        name_last_first = 'yes'
        # And we don't want to create links
        print_links = 'no'

    # authors is a list of dictionaries, count only those with names
    # e.g. naive count of this
    # [{'a': ['Toge, Nobu']},
    #  {'u': ['Kek, High Energy Accelerator Research Organization']},
    #  {'u': ['1-1 Oho, Tsukuba-Shi, Ibaraki-Ken, 305 Japan']}]
    # would be 3, but there is only 1 author
    nb_authors = len([au for au in authors if 'a' in au])

    if markup == 'bibtex':
        # skip editors
        authors = [au for au in authors if 'a' in au
                   and not ('e' in au and 'ed.' in au['e'])]
        nb_authors = len(authors)

    # Limit num of authors, so that we do not process
    # the authors that will not be shown. This can only
    # be done in non-interactive mode, as interactive mode
    # allows to show all of them.
    if limit.isdigit() and nb_authors > int(limit) \
            and interactive != "yes":
        authors = authors[:1]

    # Process authors to add link, affiliation and highlight
    for author in authors:
        if 'a' in author:
            # There should not be repeatable subfields here
            author['a'] = author['a'][0]
            if highlight == 'yes':
                from invenio import bibformat_utils
                author['a'] = bibformat_utils.highlight(author['a'],
                                                        bfo.search_pattern)

            # check if we need to reverse last, first
            # we don't try to reverse it if it isn't stored with a comma.
            first_last_match = re_last_first.search(author['a'])
            author['display'] = author['a']

            if name_last_first.lower() == "no":
                if first_last_match:
                    author['display'] = "%s %s%s" % (
                        first_last_match.group('first_names'),
                        first_last_match.group('last'),
                        first_last_match.group('extension'),)

            # for latex we do initials only (and assume first last)
            if markup == 'latex':
                if first_last_match:
                    first = re_initials.sub(
                        r'\g<initial>.~',
                        unicode(first_last_match.group('first_names'), 'utf8'))
                    first = re_tildehyph.sub(r'\g<hyphen>', first)
                    author['display'] = first + \
                        first_last_match.group('last') + \
                        first_last_match.group('extension')

            # custom name handling for bibtex
            if markup == 'bibtex':
                if first_last_match:
                    junior = first_last_match.group('extension')
                    if re.search(r'\b([JS]r\.)?$', junior) or \
                            re.search('([IV]{2,})$', junior):
                        author['display'] = "%s%s, %s" % (
                            first_last_match.group('last'),
                            junior,
                            first_last_match.group('first_names'),)
                    else:
                        author['display'] = "%s, %s%s" % (
                            first_last_match.group('last'),
                            first_last_match.group('first_names'),
                            junior,)

                    # avoid trailing comma for single name author
                    author['display'] = author['display'].rstrip(', ')

                    # multi-letter initial (in particular Russian Yu., Ya. ...)
                    # http://usefulenglish.ru/vocabulary/russian-names-in-english-en
                    author['display'] = re.sub(
                        r'\bY([aeou])\.',
                        r'{\\relax Y\1}.', author['display'])

            if print_links.lower() == "yes":
                # if there is an ID, search using that.
                id_link = ''
                if id_links == "yes" and 'i' in author:
                    author['i'] = author['i'][0]  # possible to have more IDs?
                    id_link = '<a class="authoridlink" href="' + \
                              CFG_BASE_URL + \
                              '/search?ln=' + bfo.lang + \
                              '&amp;p=100__i:' + escape(author['i']) + \
                              '+or+700__i:' + escape(author['i']) +\
                              '">' + escape("(ID Search)") + '</a> '

                author['display'] = '<a class="authorlink" href="' + \
                                    CFG_BASE_URL + \
                                    '/author/profile/' + quote(author['a']) + \
                                    '?recid=' + bibrec_id + \
                                    '&amp;ln=' + bfo.lang + \
                                    '">' + escape(author['display'])+'</a>' + \
                                    id_link

        if print_affiliations == "yes":
            if 'e' in author:
                author['e'] = affiliation_prefix + \
                    affiliations_separator.join(author['e']) + \
                    affiliation_suffix

            if 'u' in author:
                author['ilink'] = [
                    '<a class="afflink" href="' +
                    CFG_BASE_URL +
                    '/search?cc=Institutions&amp;p=institution:' +
                    quote('"' + string + '"') +
                    '&amp;ln=' + bfo.lang +
                    '">' +
                    string.lstrip() +
                    '</a>' for string in author['u']
                ]
                author['u'] = affiliation_prefix + \
                    affiliations_separator.join(author['ilink']) + \
                    affiliation_suffix

#
#  Consolidate repeated affiliations
#

    last = ''
    authors.reverse()
    for author in authors:
        if 'u' not in author:
            author['u'] = ''
        #print 'this->'+ author['a']+'\n'
        if last == author['u']:
            author['u'] = ''
        else:
            last = author['u']

    authors.reverse()

    # Flatten author instances
    if print_affiliations == 'yes':
        # 100__a (100__e)  700__a (100__e) (100__u)
        if print_affiliation_first.lower() != 'yes':
            authors = [author.get('display', '') + author.get('e', '') +
                       author.get('u', '') for author in authors]
        else:
            authors = [author.get('u', '') + author.get('display', '')
                       for author in authors]
    else:
        authors = [author.get('display', '')
                   for author in authors if 'display' in author]

    # link the extension to detailed record
    if link_extension == 'yes' and interactive != 'yes':
        extension = '<a class="authorlink" href="' +  \
            CFG_BASE_URL + '/' + CFG_SITE_RECORD + '/' + str(bfo.recID) \
            + '">' + extension + '</a>'

    # Detect Collaborations:
    if collaboration == "yes":
        colls = []
        for coll in bfo.fields("710__g"):
            if coll not in colls:
                colls.append(coll)
    else:
        colls = []

    if colls:
        short_coll = False
        colls = [re_coll.sub('', coll) for coll in colls]
        if print_links.lower() == "yes":
            colls = ['<a class="authorlink" href="' +
                     CFG_BASE_URL + '/search' +
                     '?p=collaboration:' + quote("'" + coll + "'") +
                     '&amp;ln=' + bfo.lang +
                     '">'+escape(coll)+'</a>' for coll in colls]

        noncollabterms = ('group', 'task force', 'consortium', 'team')
        noncolls = []
        truecolls = []
        for coll in colls:
            lcoll = coll.lower()
            noncoll = False
            for term in noncollabterms:
                if term in lcoll:
                    noncolls.append(coll)
                    noncoll = True
                    break
            if noncoll is False:
                truecolls.append(coll)

        coll_display = " and ".join(truecolls)
        if truecolls and not coll_display.endswith("aboration"):
            coll_display += " Collaboration"
            if len(truecolls) > 1:
                coll_display += 's'
        if truecolls and noncolls:
            coll_display += ' and '
        if noncolls:
            coll_display += ' and '.join(noncolls)
        if nb_authors > 1:
            if markup in ('latex', 'bibtex'):
                coll_display = authors[0] + extension + " [" + \
                    coll_display + "]"
            elif interactive == "yes":
                coll_display += " (" + authors[0] + " "
                extension += ")"
            else:  # html
                coll_display += " (" + authors[0] + extension + ")"
        elif nb_authors == 1:
            short_coll = True
            if markup in ('latex', 'bibtex'):
                coll_display = authors[0] + " [" + coll_display + "]"
            else:  # html
                if not only_corporate_author:
                    coll_display += " (" + authors[0] + \
                                    " for the collaboration)"
        elif nb_authors == 0:
            short_coll = True
            if markup in ('latex', 'bibtex'):
                coll_display = "[" + coll_display + "]"

    # Start outputting, depending on options and number of authors
    if colls and (interactive != "yes" or short_coll):
        return coll_display

    if limit.isdigit() and nb_authors > int(limit) and interactive != "yes":
        return separator.join(authors[:int(limit)]) + lastauthor + \
            extension

    elif interactive == "yes" and \
            ((colls and not short_coll) or
             (limit.isdigit() and nb_authors > int(limit))):
        out = '''
        <script>
        function toggle_authors_visibility(){
            var more = document.getElementById('more');
            var link = document.getElementById('link');
            var extension = document.getElementById('extension');
            if (more.style.display=='none'){
                more.style.display = '';
                extension.style.display = 'none';
                link.innerHTML = "%(show_less)s"
            } else {
                more.style.display = 'none';
                extension.style.display = '';
                link.innerHTML = "%(show_more)s"
            }
            link.style.color = "rgb(204,0,0);"
        }

        function set_up(){
            var extension = document.getElementById('extension');
            extension.innerHTML = '%(extension)s';
            toggle_authors_visibility();
        }

        </script>
        ''' % {'show_less': _("Hide"),
               'show_more': _("Show all %i authors") % nb_authors,
               'extension': extension}

#        out += '<a name="show_hide" />'
        if colls:
            show = coll_display
            more = separator + separator.join(authors[1:]) + ')'
        else:
            show = separator.join(authors[:int(limit)])
            more = separator + separator.join(authors[int(limit):len(authors)])

        out += show
        out += '<span id="more" style="">' + more + '</span>'
        out += '<span id="extension"></span>'
        out += '&nbsp;&nbsp;<small><i><a id="link" href="#"' + \
               ' style="color:green;background:white;" onclick="toggle_authors_visibility()" ' + \
               ' style="color:rgb(204,0,0);"></a></i></small>'
        out += '<script>set_up()</script>'
        return out
    elif nb_authors > 0:
        if markup in ('latex', 'bibtex'):
            if nb_authors > 1:
                lastauthor = ' and ' + authors.pop()
        return separator.join(authors) + lastauthor

# we know the argument is unused, thanks
# pylint: disable=W0613


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable=W0613
