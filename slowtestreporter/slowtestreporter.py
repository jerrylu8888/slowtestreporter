import logging

from junitparser import JUnitXml, Failure
from tabulate import tabulate

THRESHOLD = 0.05
SLOW_ERROR_MSG = 'Test duration exceeded threshold'
FAIL_TEXT = 'FAIL'


def report_slow_tests(junit_file_path: str, xml_output_file_name: str, display_results: bool):
    """
    Takes a junit test results file and determines if there are any slow tests

    Args:
        junit_file_path (str) : The file path of the junit file results
        xml_output_file_name (str) : Output file name, if a junit file is to be produced. Do not include the file
                                    extension
        display_results (str) : Displays test results if set to true
    """
    junit_xml = JUnitXml.fromfile(junit_file_path)

    test_results, xml_output, passed = parse_test_results(junit_xml)
    average_test_duration = calculate_average_test_duration(junit_xml)

    if display_results:
        print(tabulate(test_results, headers=["Test", "Time (s)", "Result", "Message"]))
        logging.info('Average test duration: %s s', average_test_duration)

    if xml_output_file_name:
        xml_output.write(xml_output_file_name + '.xml')
        logging.info('junit file created: %s.xml', xml_output_file_name)


def parse_test_results(junit_xml: JUnitXml):
    test_results = []
    passed = True
    """
    IF TEST FAILED => FAILED
    IF TEST TOO SLOW => FAILED
    IF TEST TOO SLOW + FAILED => FAILED
    OTHERWISE => PASS
    """

    for suite in junit_xml:
        for testcase in suite:
            if testcase.time > THRESHOLD:
                result = FAIL_TEXT
                if testcase.result and testcase.result[0]:
                    testcase.result[0].message += ' ' + SLOW_ERROR_MSG
                else:
                    testcase.result = [Failure(SLOW_ERROR_MSG)]
                test_results.append([testcase.name, testcase.time, result, testcase.result[0].message])
                passed = False
            elif testcase.result and testcase.result[0]:
                result = FAIL_TEXT
                test_results.append([testcase.name, testcase.time, result, testcase.result[0].message])
                passed = False
            else:
                result = 'PASS'
                test_results.append([testcase.name, testcase.time, result])

    return test_results, junit_xml, passed


def calculate_average_test_duration(junit_xml: JUnitXml) -> float:
    test_count: float = 0
    total_duration: float = 0
    for suite in junit_xml:
        for testcase in suite:
            test_count += 1
            total_duration += testcase.time

    if test_count == 0:
        average = 0
    else:
        average = total_duration / test_count

    return average
