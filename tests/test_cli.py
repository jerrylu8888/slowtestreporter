import pytest

from slowtestreporter.cli import main


def test_should_throw_error_if_no_path_is_provided():
    with pytest.raises(SystemExit):
        main([])


def test_should_error_when_path_value_that_does_not_exist():
    with pytest.raises(SystemExit):
        main(['dne'])


def test_should_error_when_threshold_is_zero():
    with pytest.raises(SystemExit):
        main(['mytest', '-t', '0'])


def test_should_error_when_threshold_is_negative():
    with pytest.raises(SystemExit):
        main(['myfile', '-t', '-0.7'])


def test_should_error_when_threshold_is_characters():
    with pytest.raises(SystemExit):
        main(['myfile', '-t', 'slow'])
