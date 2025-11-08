# -*- coding: utf-8 -*-
from secScanner.db.base import DBModel
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
import requests

def parse_cvss_vector(cvss_vector, metric=None):
    # 定义字段名称和值的映射关系
    metric_names = {
        "AV": "Attack Vector",
        "AC": "Attack Complexity",
        "PR": "Privileges Required",
        "UI": "User Interaction",
        "S": "Scope",
        "C": "Confidentiality Impact",
        "I": "Integrity Impact",
        "A": "Availability Impact"
    }

    value_mapping = {
        "AV": {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"},
        "AC": {"L": "Low", "H": "High"},
        "PR": {"N": "None", "L": "Low", "H": "High"},
        "UI": {"N": "None", "R": "Required"},
        "S": {"U": "Unchanged", "C": "Changed"},
        "C": {"N": "None", "L": "Low", "H": "High"},
        "I": {"N": "None", "L": "Low", "H": "High"},
        "A": {"N": "None", "L": "Low", "H": "High"}
    }

    # 分割输入字符串并过滤掉版本信息（CVSS:3.1）
    parts = cvss_vector.split("/")[1:]
    metrics_dict = {}  # 存储字段缩写到值的映射
    results = []       # 存储完整可读文本

    for part in parts:
        m, v = part.split(":")
        name = metric_names.get(m, m)
        mapping = value_mapping.get(m, {})
        # 处理所有 L 统一为 Low
        mapped_value = "Low" if v == "L" else mapping.get(v, v)
        metrics_dict[m] = mapped_value  # 存储到字典
        results.append(f"{name}: {mapped_value}")

    # 根据参数返回结果
    if metric:
        return metrics_dict.get(metric, None)  # 直接返回字段值（如 "Network"）
    else:
        return "\n".join(results)  # 返回完整文本

def scrapy_CSAF_index():
    try_time = 10
    api_url = 'https://dl-cdn.openeuler.openatom.cn/security/data/csaf/cve/index.txt'
    for try_index in range(try_time):
        try:
            response = requests.get(url=api_url, timeout=(10, 30))
        except Exception as e:
            print(f"scrapy from {api_url} error: {str(e)}!")
            if try_index == try_time - 1:
                print("try [%d] times failed! exit.")
                exit(1)
            print(" try again [%d/%d] " % (try_index + 1, try_time))
            continue
        break
    if response.status_code < 200 or response.status_code > 299:
        print("ret code no in [200,300)")
        exit(1)
    index_list = response.text.strip().strip('\r').split('\n')
    if 0 == len(index_list):
        print(" failed to get cvrf list")
        exit(1)
    return index_list

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


