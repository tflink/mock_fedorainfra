#
# models.py - SQLAlchemy models for boji
#
# Copyright 2011, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Tim Flink <tflink@redhat.com>


from sqlalchemy import Table, Column, Integer, String, Date, Boolean
from sqlalchemy.orm import mapper
from mock_fedorainfra.database import Base

# this kind of works, needs to be a python date object instead of a string, though
# t_comment = mock_fedorainfra.models.BodhiComment('2000-01-23 12:34:56', 'update title', 'this is a comment', 'user23', 1, False)
class BodhiComment(Base):

    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    # SQLite has poor datetime support, just use a string for now
    date = Column(String)
    title = Column(String)
    text = Column(String)
    username = Column(String)
    karma = Column(Integer)
    send_email = Column(Boolean)

    def __init__(self, date, title, text, username, karma = 0, send_email = False):
        self.date = date
        self.title = title
        self.text = text
        self.username = username
        self.karma = karma
        self.send_email = send_email


    def __repr__(self):
        return "< BodhiComment('%s', '%s', '%s', '%s', '%d', '%s')>" % (self.date,
                    self.title, self.text, self.username, self.karma, str(self.send_email))
