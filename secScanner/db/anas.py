import requests
from base import DBModel
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
import re
import json
from bs4 import BeautifulSoup
import os
from datetime import datetime
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




 def check_rpm_link(packagename, rpm_name):
     rpm_list = rpm_name.split(packagename)
     if len(rpm_list) != 2:
         return False
     if rpm_list[0] != '':
         return False
     if rpm_list[1][0] == '-' and rpm_list[1][1].isdigit():
         return True
     return False
 def get_bclinux_srpm(package_src_names):
     # 定义目标网址
     global url
     OS_DISTRO = "8.2"
     url_list = [
         "https://mirrors.cmecloud.cn/anolis/" + OS_DISTRO + "/BaseOS/source/Packages/",
         "https://mirrors.cmecloud.cn/anolis/" + OS_DISTRO + "/AppStream/source/Packages/",
         "https://mirrors.cmecloud.cn/anolis/" + OS_DISTRO + "/PowerTools/source/Packages/"
     ]

     packages = {}
     found_packages = []
     packages_url = {}
     # 指定保存目录
     save_directory = "bclinux_srpm"  # 替换为实际的保存目录路径
     # 创建保存目录（如果不存在）
     os.makedirs(save_directory, exist_ok=True)
     downloaded_packages = set()  # 存储已下载的包的名称

     # 发送 GET 请求获取网页内容
     for url in url_list:
         # 发送 GET 请求获取网页内容
         response = requests.get(url)
         html_content = response.content

         # 使用 BeautifulSoup 解析网页内容
         soup = BeautifulSoup(html_content, "html.parser")

         # 提取所有 .src.rpm 文件链接、文件大小和日期
         file_rows = soup.find_all("tr")[1:]  # 跳过表头行
         for row in file_rows:
             columns = row.find_all("td")
             link = columns[0].find("a")["href"]
             file_size_str = columns[1].text
             upload_time_str = columns[2].text

             try:
                 file_size = float(file_size_str.split()[0])
                 upload_time = datetime.strptime(upload_time_str, "%Y-%m-%d %H:%M:%S")
                 package_name = None
                 for src_name in package_src_names:
                     if check_rpm_link(src_name, link):
                         package_name = src_name
                         found_packages.append(package_name)
                         break

                 # 检查是否存在相同的包名已被找到
                 if not package_name:
                     continue

                 if package_name in packages:
                     if upload_time > packages[package_name]["upload_time"]:
                         packages[package_name]["upload_time"] = upload_time
                         packages[package_name]["link"] = link
                         packages[package_name]["file_size"] = file_size
                 else:
                     packages[package_name] = {"upload_time": upload_time, "link": link, "file_size": file_size}

             except (ValueError, AttributeError):
                 print(f"无效的文件大小或上传时间，跳过链接: {link}")


         for package_name, package_info in packages.items():
             if package_name not in downloaded_packages:  # 检查包是否已经下载过
                 download_url = url + package_info["link"]
                 file_name = package_info["link"].split("/")[-1]
                 save_path = os.path.join(save_directory, file_name)
                 # response = requests.get(download_url)
                 # with open(save_path, "wb") as f:
                 #     f.write(response.content)
                 print(f"成功下载并保存 {file_name}")
                 downloaded_packages.add(package_name)  # 将已下载的包添加到集合中

     # 如果未找到任何软件包
     if not packages:
         print("未找到任何 .src.rpm 包")
     count = 0
     for i in downloaded_packages:
         if i in package_src_names:
             count = count + 1
     print(f"According to Anolis ANAS updated {len(package_src_names)} numbers of rpm packages, there are {count} packages found from cmcloud")

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
    get_bclinux_srpm(update_rpm) #download from cmcloud

if __name__ == '__main__':
    main()

