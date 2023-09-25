import requests
from base import DBModel
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer

import re
import json

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

def download(url):
    r = requests.get(url)
    name = url.split('/')[-1]
    with open('rpms/' + name, 'wb')as f:
        f.write(r.content)

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

    all_sample = session.query(ANAS).order_by(desc('id')).all()
    update_rpm = {}
    for take_a_sample in all_sample:
        if take_a_sample.cve == "[]":
            continue
        text = take_a_sample.product
        temp = re.sub('\'', '\"', text)
        product_json = json.loads(temp)
        if product_json[0]['name_version'] != 'Anolis OS 8':
            continue
        if 'product_package_info' in product_json[0]:
            package_info = product_json[0]['product_package_info']
        else:
            continue
        update_time = take_a_sample.publish_date.split()[0]
        if 'src' in package_info:
            package_src_name = package_info['src'][0]['rpm_name']
            if "kernel" in package_src_name:
                continue
            if 'Anolis' in package_src_name:
                continue
            package_src_url = package_info['src'][0]['rpm_url']
            if package_src_name in update_rpm:
                exist_update_time = update_rpm[package_src_name][0].split('-')
                cur_update_time = update_time.split('-')
                if cur_update_time[0] < exist_update_time[0]:
                    continue
                elif cur_update_time[0] > exist_update_time[0]:
                    update_rpm[package_src_name] = [update_time, package_src_url]
                else:
                    if cur_update_time[1] < exist_update_time[1]:
                        continue
                    elif cur_update_time[1] > exist_update_time[1]:
                        update_rpm[package_src_name] = [update_time, package_src_url]
                    else:
                        if cur_update_time[2] < exist_update_time[2]:
                            continue
                        else:
                            update_rpm[package_src_name] = [update_time, package_src_url]
            else:
                update_rpm[package_src_name] = [update_time, package_src_url]
        else:
            continue

    print("---------------------------------")
    sort_update_rpm = sorted(update_rpm)
    print(len(update_rpm))
    for i in sort_update_rpm:
        print("Start downloading ", i, update_rpm[i])
        download(update_rpm[i][1])


if __name__ == '__main__':
    main()
