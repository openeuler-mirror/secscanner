import requests
from base import DBModel
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
url = ' https://anas.openanolis.cn/api/securitydata/errata.json'
class ANAS(DBModel):
    __tablename__ = 'OpenAnolisANAS'

    id = Column('id', Integer, primary_key=True)
    advisory_id = Column('advisory_id', Text)
    advisory_type = Column('advisory_type', Text)
    severity = Column('severity', Text)
    publish_date = Column('publish_date', Text)
    synpopsis = Column('synpopsis', Text)
    description = Column('description', Text)
    solution = Column('solution', Text)
    issue = Column('issue', Text)
    source = Column('source', Text)
    modules = Column('modules', Text)
    product = Column('product', Text)
    cve = Column('cve', Text)

    def format_output(self):
        print(f"advisory_id: {self.advisory_id}")
        print(f"severity: {self.severity}")
        print(f"description: {self.description}")

def main():
    r = requests.get(url)
    for i in r.json():
        for j in i:
            print(j)
            print(i[j])
    engine = create_engine('sqlite:///cvedatabase.db', echo=False)
    DBModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = r.json()
    for i in data:
        if session.query(ANAS).filter_by(advisory_id=f"{i['advisory_id']}").first():
            continue
        anas = ANAS()
        anas.advisory_id = i['advisory_id']
        anas.advisory_type = i['advisory_type']
        anas.severity = i['severity']
        anas.publish_date = i['publish_date']
        anas.synpopsis = i['synpopsis']
        anas.description = i['description']
        anas.solution = i['solution']
        anas.issue = i['issue']
        anas.source = i['source']
        anas.modules = str(i['modules'])
        anas.product = str(i['product'])
        anas.cve = str(i['cve'])
        session.add(anas)
        session.commit()
if __name__ == '__main__':
    main()
