# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2012 CERN.
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

from invenio.dbquery import \
    run_sql, \
    CFG_DATABASE_NAME

depends_on = ['invenio_release_1_1_0']


def info():
    return "Change of rnk*R and idx*R tables to add type index"


def do_upgrade():
    all_tables = [t[0] for t in run_sql("SHOW TABLES LIKE 'idx%R'")] + \
                 [t[0] for t in run_sql("SHOW TABLES LIKE 'rnk%R'")]
    for table in all_tables:
        create_statement = run_sql('SHOW CREATE TABLE %s' % table)[0][1]
        if 'KEY `type`' not in create_statement:
            run_sql("ALTER TABLE %s ADD INDEX type (type)" % (table,))


def estimate():
    """  Estimate running time of upgrade in seconds (optional). """
    count_rows = run_sql("SELECT SUM(TABLE_ROWS) FROM INFORMATION_SCHEMA.TABLES "
                         "WHERE TABLE_SCHEMA = '%s' "
                         "AND (TABLE_NAME like 'idx%%R' or TABLE_NAME like 'rnk%%R')"
                         % (CFG_DATABASE_NAME,))[0][0]
    return count_rows / 1000


def pre_upgrade():
    pass


def post_upgrade():
    pass