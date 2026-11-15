"""Prueba mínima para que el CI tenga algo que ejecutar. Bórrenla cuando haya pruebas reales."""

from __future__ import annotations

from typer.testing import CliRunner

from os_process_engine import __version__
from os_process_engine.cli.main import app


def test_cli_version() -> None:
    result = CliRunner().invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output
