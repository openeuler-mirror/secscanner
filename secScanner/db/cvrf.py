# -*- coding: utf-8 -*-

"""
 (c) 2023 - Copyright CTyunOS Inc

 Authors:
   youyifeng <youyf2@chinatelecom.cn>

"""

from secScanner.db.base import DBModel
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
import re
import requests
import xml.etree.ElementTree as ET


class CVRF(DBModel):
    __tablename__ = 'OpenEulerCVRF'

    id = Column('id', Integer, primary_key=True)
    securityNoticeNo = Column('securityNoticeNo', Text)
    affectedComponent = Column('affectedComponent', Text)
    cveId = Column('cveId', Text)
    cveThreat = Column('cveThreat', Text)
    affectedProduct = Column('affectedProduct', Text)
    packageName = Column('packageName', Text)

    announcementTime = Column('announcementTime', Text)
    # description = Column('description', Text)
    # introduction = Column('introduction', Text)
    # referenceDocuments = Column('referenceDocuments', Text)
    # revisionHistory = Column('revisionHistory', Text)
    # subject = Column('subject', Text)
    # summary = Column('summary', Text)
    type = Column('type', Text)
    updateTime = Column('updateTime', Text)

    cvrf = Column('cvrf', Text)

    # packageHelperList = Column('packageHelperList', Text)
    # packageList = Column('packageList', Text)
    # referenceList = Column('referenceList', Text)
    # cveList = Column('cveList', Text)

    def format_output(self):
        print("""SecurityNoticeNo: %s
PackageName: %s
CVEID: %s
Affected Product: %s
""" % (
            self.securityNoticeNo,
            self.affectedComponent,
            self.cveId,
            self.affectedProduct
        ))

    @staticmethod
    def pretty_output_title():
        print("%-15s %-30s %-10s %-20s" % ("CVEID", "包名", "评分", "发布时间"))

    def pretty_output(self):
        print("%-15s %-30s %-10s %-20s" % (
            self.cveId,
            self.packageName,
            self.cvsssCoreNVD if self.cvsssCoreNVD else self.cvsssCoreOE,
            self.updateTime,
        ))

    def simple_output(self):
        print("""CVEID: %s
评分:%s 
包名: %s
发布时间: %s
详情链接: https://www.openeuler.org/zh/security/cve/detail/?cveId=%s&packageName=%s
""" % (
            self.cveId,
            self.cvsssCoreNVD if self.cvsssCoreNVD else self.cvsssCoreOE,
            self.packageName,
            self.updateTime,
            self.cveId,
            self.packageName,
        ))


class CVRFXML(object):
    def __init__(self, cvrf_xml):
        rawxmldata = cvrf_xml
        rawxmldata = re.sub(' xmlns="[^"]+"', '', rawxmldata, count=0)
        rawxmldata = re.sub(' xmlns:cvrf="[^"]+"', '', rawxmldata, count=0)
        rawxmldata = re.sub(' xml:lang="[^"]+"', '', rawxmldata, count=0)
        rawxmldata = rawxmldata.replace('&', '&amp;')
        self.ctyunos_cvrf_xml = cvrf_xml
        self.root = ET.fromstring(rawxmldata)
        # self.repos = repos

    def node_get_securityNoticeNo(self):
        # self.showNode(node)
        path = 'DocumentTracking/Identification/ID'
        ret = self.root.find(path)

        if ret is not None:
            # print(ret.text)
            return ret.text
        else:
            raise Exception("%s is None" % path)

    def node_get_summary(self):
        # self.showNode(node)
        path = 'DocumentNotes/Note'
        ret = self.root.findall(path)
        for node in ret:
            if "Title" in node.attrib and node.attrib["Title"] == 'Synopsis':
                return node.text

        raise Exception("%s is None" % path)

    def node_get_announcetime(self):
        # self.showNode(node)
        path = 'DocumentTracking/CurrentReleaseDate'
        ret = self.root.find(path)

        if ret is not None:
            return ret.text
        else:
            raise Exception("%s is None" % path)

    def node_get_introduction(self):
        # self.showNode(node)
        path = 'DocumentTitle'
        ret = self.root.find(path)

        if ret is not None:
            # print(ret.text)
            return ret.text
        else:
            raise Exception("%s is None" % path)

    def node_get_type(self):
        # self.showNode(node)
        path = 'DocumentNotes/Note'
        ret = self.root.findall(path)
        for node in ret:
            if "Title" in node.attrib and node.attrib["Title"] == 'Severity':
                return node.text

        raise Exception("%s is None" % path)

    def node_get_subject(self):
        # self.showNode(node)
        path = 'DocumentNotes/Note'
        ret = self.root.findall(path)
        for node in ret:
            if "Title" in node.attrib and node.attrib["Title"] == 'Topic':
                return node.text

        raise Exception("%s is None" % path)

    def node_get_description(self):
        # self.showNode(node)
        path = 'DocumentNotes/Note'
        ret = self.root.findall(path)
        for node in ret:
            if "Title" in node.attrib and node.attrib["Title"] == 'Description':
                return node.text

        raise Exception("%s is None" % path)

    def node_get_affectedComponent(self):
        # self.showNode(node)
        path = 'DocumentNotes/Note'
        ret = self.root.findall(path)
        for node in ret:
            if "Title" in node.attrib and node.attrib["Title"] == 'Affected Component':
                return node.text

        raise Exception("%s is None" % path)

    def showNode(self, node):
        print("tag: %s | attrib: %s | text: %s" % (node.tag, node.attrib, node.text))

    def node_get_reference_list(self):
        path = 'DocumentReferences/Reference'
        reference_list = []
        ret = self.root.findall(path)
        for node in ret:
            if "Type" in node.attrib and node.attrib["Type"] == 'Other':
                for child in node:
                    reference_list.append({
                        "url": child.text
                    })
        if len(reference_list) == 0:
            raise Exception("reference list is 0")
        return reference_list

    def node_get_cveId(self):
        path = 'Vulnerability/CVE'
        cve_list = []
        ret = self.root.findall(path)
        for node in ret:
            cve_list.append(node.text)
        if len(cve_list) == 0:
            raise Exception("cve list is 0")
        return cve_list

    def node_get_cveThreat(self):
        path = 'Vulnerability/Threats/Threat/Description'
        cveThreat_list = []
        ret = self.root.findall(path)
        for node in ret:
            cveThreat_list.append(node.text)
        if len(cveThreat_list) == 0:
            raise Exception("cvethreat list is 0")
        return cveThreat_list

    def node_get_packageName(self):

        path = 'ProductTree/Branch'
        pkg_dict = {

        }
        cpe_productid = {}
        ret = self.root.findall(path)

        for node in ret:
            if "Type" in node.attrib and node.attrib["Type"] == 'Product Name':
                for child in node:
                    productId = child.attrib["ProductID"]
                    cpe_productid[child.attrib["CPE"]] = child.attrib["ProductID"]
                    pkg_dict[productId] = {
                        "src": set(),
                        "aarch64": set(),
                        "x86_64": set(),
                        "noarch": set(),
                    }
        # print(json.dumps(cpe_productid, indent=4))
        for node in ret:
            if "Type" in node.attrib and node.attrib["Type"] == 'Package Arch':
                arch = node.attrib["Name"]
                if arch not in ("src", "noarch", "x86_64", "aarch64"):
                    raise Exception("arch %s does't support" % node.attrib["Name"])
                for child in node:
                    cpe = child.attrib["CPE"]
                    productId = cpe_productid[cpe]
                    # print("productId", productId, "cpe", cpe)
                    pkg_dict[productId][arch].add(child.text)
                    # print("add", child.text)

        for productId in pkg_dict:
            for arch in pkg_dict[productId]:
                pkg_dict[productId][arch] = list(pkg_dict[productId][arch])
                # print('pkg_dict[productId][arch]', pkg_dict[productId][arch])

        # print(json.dumps(pkg_dict, indent=4))

        return pkg_dict

    def node_get_affectedProduct(self):
        path = 'ProductTree/Branch'
        pkg_dict = set()
        ret = self.root.findall(path)
        for node in ret:
            if "Type" in node.attrib and node.attrib["Type"] == 'Product Name':
                for child in node:
                    pkg_dict.add(child.text)

        return list(pkg_dict)


class PRODUCT(DBModel):
    __tablename__ = 'OpenEulerProduct'

    id = Column('id', Integer, primary_key=True)
    productId = Column('productId', Text)
    srcfilename = Column('srcfilename', Text)
    packageName = Column('packageName', Text)
    packages = Column('packages', Text)
    # Foreign key to OpenEulerCVRF
    securityNoticeNo = Column('securityNoticeNo', Text)

def scrapy_CVRF_index():
    """
    :API: https://repo.openeuler.org/security/data/cvrf/index.txt
    :return: json
    """
    try_time = 10
    api_url = 'https://repo.openeuler.org/security/data/cvrf/index.txt'
    for try_index in range(try_time):
        try:
            response = requests.get(url=api_url, timeout=(10, 30))
        except Exception as e:
            print("scrapy from api '%s' error!" % api_url, str(e))
            if try_index == try_time - 1:
                print("try [%d] times failed! exit.")
                exit(1)
            print(" try again [%d/%d] " % (try_index + 1, try_time))
            continue
        break
    if response.status_code < 200 or response.status_code > 299:
        print("ret code no in [200,300)")
        exit(1)
    index_list = response.text.strip('\r').split('\n')
    if 0 == len(index_list):
        print("failed to get cvrf list")
        exit(1)
    index_list.pop()
    return index_list


def activate_session(session):
    """active sql session"""
    DBModel.metadata.create_all(bind=session.get_engine())
    db = session.new_session()
    return db

def purge_db(session):
    """clean all data model and recreate"""
    DBModel.metadata.drop_all(bind=session.get_engine())
    DBModel.metadata.create_all(bind=session.get_engine())
