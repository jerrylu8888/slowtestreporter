#!/usr/bin/env python
import argparse
import logging
import sys

from junitparser import JUnitXml

from slowtestreporter.slowtestreporter import report_slow_tests, THRESHOLD, report_average_test_result

DEFAULT_THRESHOLD = THRESHOLD


def main(args):
    parser = argparse.ArgumentParser(description='Reports slow tests based on the junit test input.')
    parser.add_argument('-t', '--threshold', type=float, help='A float value threshold (in seconds) of when a '
                                                              'test should fail when it exceeds this value',
                        action=ThresholdArgValidationAction)
    parser.add_argument('-a', '--average-threshold', type=float, help='A float value threshold (in seconds) when the '
                                                                      'average duration check should fail',
                        action=ThresholdArgValidationAction)
    parser.add_argument('path', type=str, help='Junit file path')
    parser.add_argument('-o', '--output-filename', help='Filename of the generated junit results without file '
                                                        'extension. The file will be generated with a .xml extension.')
    parser.add_argument('-s', '--silent', help='Suppresses output to display', action='store_true')
    parser.add_argument('--exit-zero-duration-test', help='Force slow test report to use the exit status code 0 even '
                                                          'if there are test errors', action='store_true')
    parser.add_argument('--exit-zero-average-test', help='Force slow test report to use the exit status code 0 even '
                                                         'if there are test errors', action='store_true')
    args = parser.parse_args(args)

    if args.silent:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)
        print('JUNIT SLOW TEST REPORTER')
        print('========================')

    if not args.threshold:
        threshold = DEFAULT_THRESHOLD
        logging.info('Threshold not set, using default threshold: %ss', str(threshold))
    else:
        threshold = args.threshold
        logging.info('Threshold for slow tests: %ss', str(threshold))

    try:
        passed = report_slow_tests(args.path, args.output_filename, not args.silent)
        if not passed:
            logging.error('Tests failed threshold.')
            if not args.exit_zero_duration_test:
                raise SystemExit(1)

        if args.average_threshold:
            junit_xml = JUnitXml.fromfile(args.output_filename)
            average_duration_passed = report_average_test_result(args.average_threshold, junit_xml, not args.silent)
            if not args.exit_zero_average_test and not average_duration_passed:
                raise SystemExit(1)

    except FileNotFoundError:
        logging.error('Junit file input not found.')
        raise SystemExit(1)


class ThresholdArgValidationAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values <= 0:
            logging.error("Threshold cannot be less than or equal to zero.")
            raise SystemExit(1)
        setattr(namespace, self.dest, values)


if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit()
