# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2014, 2020 CERN.
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
	Returns template subject and content for:
	a HEP record ticket
"""
def get_template_data(record):
	from invenio.config import CFG_SITE_URL, CFG_LABS_HOSTNAME
	from invenio.bibrecord import record_get_field_value, record_get_field_values

	recid = record_get_field_value(record,'001','','','')
	report_numbers = record_get_field_values('037','_','_','a')
	postfix =''
	if report_numbers:
		postfix = ' '
	queue = "HEP_cor"
	subject = "%s%s(#%s)" % ( ' '.join(report_numbers), postfix, recid)
	content = """
Curate record here: https://%s/workflows/edit_article/%s

                    %s/record/edit/#state=edit&recid=%s
""" % (CFG_LABS_HOSTNAME, recid, CFG_SITE_URL, recid)
	return (queue, subject, content)
