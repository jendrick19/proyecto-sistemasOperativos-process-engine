"""Configuración de logging del proyecto.

Dueño: E5 Integración.

La librería nunca usa ``print``; cada módulo crea su logger y registra con el tick simulado::

    import logging
    log = logging.getLogger(__name__)
    log.info("PID %d pasa a READY", pid, extra={"tick": now})

Salida: ``[t=12] INFO  os_process_engine.scheduling.fcfs: PID 3 pasa a READY``.
Si no se pasa ``tick``, se muestra ``[t=-]``.
"""

from __future__ import annotations

import logging
import sys
from typing import TextIO

PACKAGE_LOGGER = "os_process_engine"
LOG_FORMAT = "[t=%(tick)s] %(levelname)-5s %(name)s: %(message)s"
VALID_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class _TickFilter(logging.Filter):
    """Pone ``tick='-'`` en los registros que no traen el tick simulado."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "tick"):
            record.tick = "-"
        return True


def configure_logging(level: str = "INFO", stream: TextIO | None = None) -> logging.Logger:
    """Configura el logger raíz del paquete y lo devuelve.

    Se puede llamar varias veces (por ejemplo desde la CLI y desde las pruebas): reemplaza
    el handler anterior en lugar de duplicar los mensajes.

    Args:
        level: Nivel mínimo, uno de ``VALID_LEVELS`` (no distingue mayúsculas).
        stream: Destino de los mensajes; por defecto ``sys.stderr``.

    Raises:
        ValueError: si ``level`` no es un nivel válido.
    """
    normalized = level.upper()
    if normalized not in VALID_LEVELS:
        raise ValueError(f"Nivel de log inválido: {level!r}. Use uno de {', '.join(VALID_LEVELS)}")

    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(_TickFilter())

    logger = logging.getLogger(PACKAGE_LOGGER)
    for old in list(logger.handlers):
        logger.removeHandler(old)
    logger.addHandler(handler)
    logger.setLevel(normalized)
    logger.propagate = False
    return logger
