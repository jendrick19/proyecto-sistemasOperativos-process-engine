# Guía de contribución

## Flujo de trabajo
1. Toma una issue del tablero y asígnatela.
2. Crea una rama desde `main`: `feat/e2-round-robin`, `fix/e3-unlink-shm`, `docs/e5-diagramas`.
3. Commits pequeños con [Conventional Commits](https://www.conventionalcommits.org/es/):
   `feat(scheduling): agregar Round Robin`, `test(ipc): estrés productor-consumidor`.
4. Antes del PR: `ruff check . ; ruff format . ; mypy ; pytest` (todo en verde).
5. Abre el PR enlazando la issue (`Closes #12`). Pide revisión a **alguien de otra escuadra**.
6. Se fusiona con 1 aprobación y CI en verde. Nadie hace push directo a `main`.

## Reglas de código
- Tipado completo (`mypy --strict`). Nada de `Any` sin justificación.
- Docstrings en español con vocabulario de SO (PCB, ráfaga, quantum, context switch...).
- Sin `print` en la librería: usa `logging`. Solo la CLI imprime (con `rich`).
- Errores con excepciones propias y mensajes claros; nunca `except:` vacío.
- Recursos (pipes, memoria compartida, procesos) siempre con `with` o `try/finally`.
- Cada función pública nueva viene con su test.
- Tiempos en *ticks* enteros; la simulación debe ser determinista (semilla fija).

## Interfaces entre escuadras
Las definen los 5 líderes en la reunión del día 2 (PCB, estados, eventos, `Scheduler`,
métricas). Una vez acordadas, se listan aquí y quedan congeladas:
agregar algo = avisar en el chat de líderes; renombrar o quitar = acuerdo de los 5 líderes.

| Archivo | Escuadra dueña | Estado |
|---|---|---|
| _por definir_ | | |
