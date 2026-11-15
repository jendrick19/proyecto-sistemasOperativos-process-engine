from __future__ import annotations

import pytest

from os_process_engine.core.clock import Clock


def test_empieza_en_cero() -> None:
    assert Clock().now == 0


def test_puede_empezar_en_otro_tick() -> None:
    assert Clock(start=5).now == 5


def test_avanza_de_uno_en_uno_por_defecto() -> None:
    clock = Clock()
    clock.advance()
    clock.advance()
    assert clock.now == 2


def test_avanza_varios_ticks_y_devuelve_el_tick_nuevo() -> None:
    clock = Clock()
    assert clock.advance(4) == 4
    assert clock.advance(3) == 7


def test_avanzar_cero_no_cambia_nada() -> None:
    clock = Clock(start=3)
    clock.advance(0)
    assert clock.now == 3


def test_no_puede_retroceder() -> None:
    clock = Clock(start=10)
    with pytest.raises(ValueError, match="negativo"):
        clock.advance(-1)
    assert clock.now == 10  # el error no debe dejar el reloj modificado


def test_no_puede_empezar_negativo() -> None:
    with pytest.raises(ValueError):
        Clock(start=-1)


@pytest.mark.parametrize("valor", [1.5, "3", True, None])
def test_rechaza_valores_que_no_son_enteros(valor: object) -> None:
    with pytest.raises(TypeError):
        Clock().advance(valor)  # type: ignore[arg-type]


def test_reset_vuelve_a_cero() -> None:
    clock = Clock(start=8)
    clock.reset()
    assert clock.now == 0


def test_now_es_solo_lectura() -> None:
    clock = Clock()
    with pytest.raises(AttributeError):
        clock.now = 5  # type: ignore[misc]


def test_repr_muestra_el_tick() -> None:
    assert repr(Clock(start=2)) == "Clock(now=2)"
