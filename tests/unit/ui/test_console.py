import textwrap

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture

from dvc.ui import Console


def test_write(capsys: CaptureFixture[str]):
    """Test that ui.write works."""
    console = Console(enable=True)
    message = "hello world"
    console.write(message)
    console.error_write(message)

    captured = capsys.readouterr()
    assert captured.out == f"{message}\n"
    assert captured.err == f"{message}\n"


@pytest.mark.parametrize(
    "isatty, expected_output",
    [
        (
            True,
            textwrap.dedent(
                """\
        {
          "hello": "world"
        }
    """
            ),
        ),
        (
            False,
            textwrap.dedent(
                """\
        {"hello": "world"}
        """
            ),
        ),
    ],
)
def test_write_json(
    capsys: CaptureFixture[str], mocker: MockerFixture, isatty, expected_output
):
    """Test that ui.write_json works."""

    console = Console(enable=True)
    mocker.patch.object(console, "isatty", return_value=isatty)
    message = {"hello": "world"}
    console.write_json(message)
    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_capsys_works(capsys: CaptureFixture[str]):
    """Sanity check that capsys can capture outputs from a global ui."""
    from dvc.ui import ui

    message = "hello world"
    ui.write(message)
    ui.error_write(message)

    captured = capsys.readouterr()
    assert captured.out == f"{message}\n"
    assert captured.err == f"{message}\n"
