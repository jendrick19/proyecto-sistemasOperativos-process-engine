# OS-ProcessEngine

Motor de abstracción, planificación de CPU y rendimiento de procesos.
Proyecto Integrador de la Unidad I de Sistemas Operativos.

Simula el subsistema de gestión de procesos de un kernel: PCB y estados POSIX, modo
usuario/kernel, llamadas al sistema, planificadores (FCFS, SJF, SRTF, Prioridad con aging,
Round Robin, MLFQ), costo del cambio de contexto e IPC real con pipes y memoria compartida.

## Instalación (Windows)

Requisitos: Python 3.12 y Git.

```powershell
git clone <url-del-repo>
cd proyecto-sistemasOperativos-process-engine
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
pre-commit install
```

## Uso

```powershell
osengine --help
osengine version
```

## Verificar antes de abrir un PR

```powershell
ruff check . ; ruff format . ; mypy ; pytest
```

## Estructura

| Carpeta | Escuadra | Contenido |
|---|---|---|
| `src/os_process_engine/core/` | E1 Núcleo | PCB, estados, tabla de procesos, modos, syscalls |
| `src/os_process_engine/scheduling/` | E2 Planificación | Algoritmos, dispatcher, mediano plazo |
| `src/os_process_engine/ipc/` | E3 IPC | Pipes, memoria compartida, sincronización |
| `src/os_process_engine/workloads/`, `metrics/` | E4 Métricas | Cargas, escenarios TOML, métricas, Gantt |
| `src/os_process_engine/engine.py`, `cli/` | E5 Integración | Motor, CLI, dashboard |

Las interfaces entre módulos (PCB, estados, eventos, `Scheduler`, métricas) las definen los
líderes de escuadra en la reunión del día 2; quedan documentadas en `CONTRIBUTING.md`.

Ver [docs/PLAN_PROYECTO.md](docs/PLAN_PROYECTO.md) y [CONTRIBUTING.md](CONTRIBUTING.md).
