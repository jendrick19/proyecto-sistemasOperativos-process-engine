"""Reloj global del simulador.

Dueño: E1 Núcleo (adelantado por E5).

El tiempo se mide en *ticks*: unidades enteras y abstractas. Un tick representa la unidad
mínima de trabajo de la CPU simulada (por ejemplo, 1 ms). Usar enteros evita errores de
redondeo y hace que los resultados coincidan exactamente con los ejercicios resueltos a mano.
"""

from __future__ import annotations


class Clock:
    """Reloj monótono: el tiempo solo avanza, nunca retrocede.

    Example:
        >>> clock = Clock()
        >>> clock.advance()
        1
        >>> clock.advance(3)
        4
        >>> clock.now
        4
    """

    def __init__(self, start: int = 0) -> None:
        """Crea el reloj en el tick ``start``.

        Raises:
            ValueError: si ``start`` es negativo.
        """
        self._now = self._validate(start, "start")

    @property
    def now(self) -> int:
        """Tick actual (solo lectura: se cambia con ``advance`` o ``reset``)."""
        return self._now

    def advance(self, ticks: int = 1) -> int:
        """Avanza el reloj ``ticks`` unidades y devuelve el nuevo tick actual.

        ``advance(0)`` está permitido y no cambia nada.

        Raises:
            ValueError: si ``ticks`` es negativo (el tiempo no puede retroceder).
        """
        self._now += self._validate(ticks, "ticks")
        return self._now

    def reset(self) -> None:
        """Vuelve el reloj a cero (para empezar otra simulación)."""
        self._now = 0

    def __repr__(self) -> str:
        return f"Clock(now={self._now})"

    @staticmethod
    def _validate(value: int, name: str) -> int:
        # bool es subclase de int en Python: se rechaza explícitamente (True no es un tick).
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} debe ser un entero, se recibió {type(value).__name__}")
        if value < 0:
            raise ValueError(f"{name} no puede ser negativo (se recibió {value})")
        return value
