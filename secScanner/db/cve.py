# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from secScanner.db.base import DBModel
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer

class CVE(DBModel):
    __tablename__ = 'OpenEulerCVE'
    __table_args__ = {'extend_existing': True}
    id = Column('id', Integer, primary_key=True)

    cveId = Column('cveId', Text)
    summary = Column('summary', Text)
    level = Column('level', Text) # type



    cvsssCoreNVD = Column('cvsssCoreNVD', Text)
    cvsssCoreOE = Column('cvsssCoreOE', Text)

    attackVectorNVD = Column('attackVectorNVD', Text)
    attackVectorOE = Column('attackVectorOE', Text)

    attackComplexityNVD = Column('attackComplexityNVD', Text)
    attackComplexityOE = Column('attackComplexityOE', Text)

    privilegesRequiredNVD = Column('privilegesRequiredNVD', Text)
    privilegesRequiredOE = Column('privilegesRequiredOE', Text)

    userInteractionNVD = Column('userInteractionNVD', Text)
    userInteractionOE = Column('userInteractionOE', Text)

    scopeNVD = Column('scopeNVD', Text)
    scopeOE = Column('scopeOE', Text)

    confidentialityNVD = Column('confidentialityNVD', Text)
    confidentialityOE = Column('confidentialityOE', Text)

    integrityNVD = Column('integrityNVD', Text)
    integrityOE = Column('integrityOE', Text)

    availabilityNVD = Column('availabilityNVD', Text)
    availabilityOE = Column('availabilityOE', Text)

    status = Column('status', Text)

    announcementTime = Column('announcementTime', Text)
    createTime = Column('createTime', Text)
    updateTime = Column('updateTime', Text)
    packageName = Column('packageName', Text)

    extra_data = Column('extra_data', Text)
    COLUMN = [
        "id",

        "cveId",
        "summary",
        "level",

        "cvsssCoreNVD",
        "cvsssCoreOE",

        "attackVectorNVD",
        "attackVectorOE",

        "attackComplexityNVD",
        "attackComplexityOE",

        "privilegesRequiredNVD",
        "privilegesRequiredOE",

        "userInteractionNVD",
        "userInteractionOE",

        "scopeNVD",
        "scopeOE",

        "confidentialityNVD",
        "confidentialityOE",

        "integrityNVD",
        "integrityOE",

        "availabilityNVD",
        "availabilityOE",

        "status",

        "announcementTime",
        "createTime",
        "updateTime",
        "packageName",

        "extra_data",
    ]


