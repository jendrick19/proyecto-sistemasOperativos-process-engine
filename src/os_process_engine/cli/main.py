"""Punto de entrada de la CLI: ``osengine``.

Dueño: E5 Integración.
"""

from __future__ import annotations

import typer

from os_process_engine import __version__

app = typer.Typer(help="OS-ProcessEngine: simulador de procesos, planificación de CPU e IPC.")


@app.callback()
def main() -> None:
    """OS-ProcessEngine."""


@app.command()
def version() -> None:
    """Muestra la versión instalada."""
    typer.echo(f"OS-ProcessEngine v{__version__}")


if __name__ == "__main__":
    app()
