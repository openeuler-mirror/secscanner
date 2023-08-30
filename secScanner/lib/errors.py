# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''

class GenericError(Exception):
    """Base class for ease custom exceptions"""
    faultCode = 100
    fromFault = False

    def __str__(self):
        try:
            return str(self.args[0]['args'][0])
        except Exception:
            try:
                return str(self.args[0])
            except Exception:
                return str(self.__dict__)
class ConfigError(GenericError):
    """Raised when load of cve-ease configuration fails"""
    faultCode = 101

class RuntimeError(GenericError):
    """Raised when runtime error"""
    faultCode = 102

class NoDirError(GenericError):
    """Raised when input is not dir"""
    faultCode = 103

class CreateWorkdirError(GenericError):
    """Raised when create workdir error"""
    faultCode = 104