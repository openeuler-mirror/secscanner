from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker
from base import DBModel
import requests
import json
from cve import CVE
from cvrf import CVRF
#######################################################################
#check data in cvedatabase
#######################################################################
# engine = create_engine('sqlite:///cvedatabase.db', echo=False)
# Session = sessionmaker(bind=engine)
# session = Session()
# for i in range(20):
#     our_sample = session.query(CVE).filter_by(id=f'{i+1}').first()
#     if type(our_sample) == CVE:
#         print(our_sample.id)
#         print(our_sample.cveId)
# session.close()
#######################################################################
#check data in cvrfdatabase
#######################################################################
engine = create_engine('sqlite:///cvedatabase.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

for i in range(20):
    our_sample = session.query(CVRF).filter_by(id=f'{i+1}').first()
    if type(our_sample) == CVRF:
        print(our_sample.securityNoticeNo)
        print(our_sample.cveId)
        print(our_sample.cveThreat)
session.close()
testmap = {}
testmap['gdb'] = []
print(testmap['gdb'])
testmap['gdb'].append('rpm1')
testmap['gdb'].append('rpm1')
testmap['gdb'].append('rpm1')
print(testmap['gdb'])