import pytest
from junitparser import TestCase, TestSuite, Error, JUnitXml

from slowtestreporter import slowtestreporter
from slowtestreporter.slowtestreporter import report_slow_tests

# Prevent pytest from trying to collect junitparser test objects as tests:
TestCase.__test__ = False
TestSuite.__test__ = False


def test_should_throw_exception_when_file_is_not_found():
    with pytest.raises(FileNotFoundError):
        report_slow_tests('filedoesnotexist.xml', 'my_results', False)


def test_should_throw_exception_when_no_file_provided():
    with pytest.raises(FileNotFoundError):
        report_slow_tests('', 'results', False)


def test_should_not_change_results_when_single_test_is_fast():
    case1 = TestCase('case1', 'Test', 0.01)
    case1.result = []
    suite = TestSuite('suite1')
    suite.add_testcase(case1)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    test_results, junit_xml = slowtestreporter.parse_test_results(xml)
    assert slowtestreporter.SLOW_ERROR_MSG not in test_results[0], 'Expected no slow test error'


def test_should_not_change_results_when_single_failed_test_is_fast():
    case1 = TestCase('case1', 'FailedTest', 0.01)
    case1.result = [Error('Error', 'Some error type')]
    suite = TestSuite('suite1')
    suite.add_testcase(case1)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    test_results, junit_xml = slowtestreporter.parse_test_results(xml)
    assert slowtestreporter.SLOW_ERROR_MSG not in test_results[0], 'Expected no slow test error despite failed test'


def test_should_keep_test_failed_when_single_failed_test_is_fast():
    case1 = TestCase('case1', 'FailedTest', 0.01)
    case1.result = [Error('Error', 'Some error type')]
    suite = TestSuite('suite1')
    suite.add_testcase(case1)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    test_results, junit_xml = slowtestreporter.parse_test_results(xml)
    assert slowtestreporter.FAIL_TEXT in test_results[0][2], 'Expected failed test to stay failed'


def test_should_report_slow_test_when_single_failed_test_is_slow():
    case1 = TestCase('case1', 'FailedTest', 7000)
    case1.result = [Error('Error', 'Some error type')]
    suite = TestSuite('suite1')
    suite.add_testcase(case1)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    test_results, junit_xml = slowtestreporter.parse_test_results(xml)
    assert slowtestreporter.FAIL_TEXT in test_results[0][2], 'Expected slow test error for failed and slow test'


def test_should_not_fail_average_calculation_when_no_test_suite():
    xml = JUnitXml()

    average_time = slowtestreporter.calculate_average_test_duration(xml)
    assert average_time == 0, 'Expected no failure when there is no test suite'


def test_should_calculate_average_time_for_single_test():
    case1 = TestCase('case1', 'Test', 0.01)
    case1.result = []
    suite = TestSuite('suite1')
    suite.add_testcase(case1)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    average_time = slowtestreporter.calculate_average_test_duration(xml)
    assert average_time == 0.01, 'Expected correct average test duration when calculated against single test case'


def test_should_calculate_average_time_for_two_test_cases():
    case1 = TestCase('case1', 'Test', 0.01)
    case1.result = []

    case2 = TestCase('case2', 'Test', 0.12)
    case2.result = []

    suite = TestSuite('suite1')
    suite.add_testcase(case1)
    suite.add_testcase(case2)

    xml = JUnitXml()
    xml.add_testsuite(suite)

    average_time = slowtestreporter.calculate_average_test_duration(xml)
    assert average_time == 0.065, 'Expected correct average test duration when calculated against 2 test cases'
