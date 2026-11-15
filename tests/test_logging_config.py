from __future__ import annotations

import io
import logging

import pytest

from os_process_engine.logging_config import configure_logging


def test_formato_con_tick() -> None:
    out = io.StringIO()
    configure_logging("DEBUG", stream=out)
    logging.getLogger("os_process_engine.prueba").info("PID %d listo", 3, extra={"tick": 12})
    assert out.getvalue() == "[t=12] INFO  os_process_engine.prueba: PID 3 listo\n"


def test_sin_tick_muestra_guion() -> None:
    out = io.StringIO()
    configure_logging("INFO", stream=out)
    logging.getLogger("os_process_engine").warning("sin reloj")
    assert out.getvalue().startswith("[t=-] WARNING")


def test_respeta_el_nivel() -> None:
    out = io.StringIO()
    configure_logging("warning", stream=out)
    logging.getLogger("os_process_engine").info("no debe salir")
    assert out.getvalue() == ""


def test_llamar_dos_veces_no_duplica_mensajes() -> None:
    out = io.StringIO()
    configure_logging("INFO", stream=out)
    configure_logging("INFO", stream=out)
    logging.getLogger("os_process_engine").info("una vez")
    assert out.getvalue().count("una vez") == 1


def test_nivel_invalido() -> None:
    with pytest.raises(ValueError, match="inválido"):
        configure_logging("VERBOSE")
