#!/usr/bin/python3
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
import unittest
import platform
from secScanner.gconfig import *
g_init()
from secScanner.commands.basic import *

def check_python_version():
    python_version = platform.python_version().split('.')[0]
    if python_version == "3":
        return
    else:
        print('Invalid python version requested: %s' % python_version)

def add_tests(suite, test_class):
    #suite = unittest.TestSuite()
    # 加载测试类中的所有测试方法
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
    suite.addTests(tests)

    return tests.countTestCases()

    # 创建一个测试运行器来运行测试
    #runner = unittest.TextTestRunner(verbosity=0)
    #runner.run(suite)

def add_module_tests(benchmark, op_type, suite):
    print("Security Benchmark: %s, Type: %s" % (benchmark, op_type))

    pattern = r'Test[CS]([0-9]+)_.*\.py'
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "tests", "enhance", benchmark, op_type)
    CHECK_ITEMS = sorted(glob.glob( path + '/*' ))

    print("%4s\t%-30s\t%s" % ("Seq", "Module Name", "Num of TestCases"))
    print("-" * 70)
    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            if 1 <= s_num <= 1021 : # 范围验证
                module_name = os.path.splitext(os.path.basename(i))[0]
                module_path = os.path.dirname(i)
                sys.path.append(module_path)
                try:
                    module = __import__(module_name)
                    num = add_tests(suite, getattr(module, module_name))

                    print("[%02d]\t%-30s\t%3d" % (s_num, module_name, num))
                except ImportError as e:
                    print(f"Failed to import module {module_name}: {e}")
                    sys.exit(1)
                except AttributeError as e:
                    print(f"Module {module_name} does not have the required function: {e}")
                    sys.exit(1)


def test_check_sys():
        # clear the counter, make this function re-call-able.
    # these two counters are used for scan_show_result() function.
    suite = unittest.TestSuite()
    benchmarks = ["basic", "euler", "group", "level3"]
    op_types = ["check", "set"]

    for benchmark in benchmarks:
        for op_type in op_types:
            add_module_tests(benchmark, op_type, suite)
            print()
    '''
    pattern = r'TestC([0-9]+)_.*\.py'
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "tests", "enhance", "basic", "check")
    CHECK_ITEMS = sorted(glob.glob( path + '/*' ))

    print("%4s\t%-30s\t%s" % ("Seq", "Module Name", "Num of TestCases"))
    print("-" * 60)
    for i in CHECK_ITEMS:
        match = re.search(pattern, i)
        if match:
            s_num = int(match.group(1))
            if 1 <= s_num <= 60 : # 范围验证
                module_name = os.path.splitext(os.path.basename(i))[0]
                module_path = os.path.dirname(i)
                sys.path.append(module_path)
                try:
                    module = __import__(module_name)
                    num = add_tests(suite, getattr(module, module_name))

                    print("[%02d]\t%-30s\t%3d" % (s_num, module_name, num))
                except ImportError as e:
                    print(f"Failed to import module {module_name}: {e}")
                    sys.exit(1)
                except AttributeError as e:
                    print(f"Module {module_name} does not have the required function: {e}")
                    sys.exit(1)
    '''
    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)

if __name__ == "__main__":
    check_python_version()
    test_check_sys()
    
