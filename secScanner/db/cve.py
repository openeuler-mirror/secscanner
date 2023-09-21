# -*- coding: utf-8 -*-

"""
 (c) 2023 - Copyright CTyunOS Inc

 Authors:
   youyifeng <youyf2@chinatelecom.cn>

"""

from base import DBModel
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer

class CVE(DBModel):
    __tablename__ = 'OpenEulerCVE'
    id = Column('id', Integer, primary_key=True)
    announcementTime = Column('announcementTime', Text)
    cveId = Column('cveId', Text)
    cvsssCoreNVD = Column('cvsssCoreNVD', Text)
    cvsssCoreOE = Column('cvsssCoreOE', Text)
    status = Column('status', Text)
    summary = Column('summary', Text)
    createTime = Column('createTime', Text)
    updateTime = Column('updateTime', Text)
    packageName = Column('packageName', Text)

    COLUMN = [
        "id",
        "announcementTime",
        "cveId",
        "cvsssCoreNVD",
        "cvsssCoreOE",
        "packageName",
        "status",
        "summary",
        "createTime",
        "updateTime",
    ]

