#!/usr/bin/env python
import argparse
import logging
import sys

from slowtestreporter.slowtestreporter import report_slow_tests, THRESHOLD

DEFAULT_THRESHOLD = THRESHOLD


def main(args):
    parser = argparse.ArgumentParser(description='Reports slow tests based on the junit test input.')
    parser.add_argument('-t', '--threshold', type=float, help='A float value threshold (in seconds) of when a '
                                                              'test should fail when it exceeds this value',
                        action=ThresholdArgValidationAction)
    parser.add_argument('path', type=str, help='Junit file path')
    parser.add_argument('-o', '--output-filename', help='Filename of the generated junit results without any '
                                                        'extensions. The file will be generated with a .xml extension.')
    parser.add_argument('-s', '--silent', help='Suppresses output to display', action='store_true')
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
        report_slow_tests(args.path, args.output_filename, not args.silent)
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
