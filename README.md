# Slow Test Reporter
Slow Test Reporter reads JUnit test result files and reports any slow running tests.

## Installation
`pip install slowtestreporter`

## Usage

    $ slowtestreporter --help
    usage: slowtestreporter [-h] [-t THRESHOLD] [-o OUTPUT_FILENAME] [-s] path
    
    Reports slow tests based on the junit test input.
    
    positional arguments:
      path                  Junit file path
    
    optional arguments:
      -h, --help            show this help message and exit
      -t THRESHOLD, --threshold THRESHOLD
                            A float value threshold (in seconds) of when a test should fail when it exceeds this value
      -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
                            Filename of the generated junit results without any extensions. The file will be generated with a .xml extension.
      -s, --silent          Suppresses output to display


