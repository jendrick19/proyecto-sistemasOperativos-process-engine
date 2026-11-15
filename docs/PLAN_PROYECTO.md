# OS-ProcessEngine — Definición del proyecto (15 personas · 2 semanas · Python en Windows)

## Contexto
El enunciado (`OS-ProcessEngine Motor de Abstracción, Planificación de CPU y Rendimiento de Procesos.pdf`) pide un simulador modular del subsistema de procesos: PCB y estados POSIX, algoritmos de planificación de CPU comparados con cargas CPU-bound / I/O-bound, IPC real con pipes y memoria compartida, costo del context switch, y una defensa con demo en vivo (efecto convoy, Round Robin) y preguntas de auditoría (context switch, starvation / Uninterruptible Sleep, integridad de buffers IPC).
Decisiones del usuario: **Python**, **2 semanas**, equipo en **Windows**, **15 personas**.


> Riesgo: el PDF dice "lenguaje moderno de sistemas". Python es válido si se justifica con tipado estricto (mypy --strict), IPC real del SO (`multiprocessing` usa pipes y memoria compartida nativos de Windows) y medición con `perf_counter_ns`. Recomendación: confirmar con el docente el primer día.

## Stack tecnológico

| Área | Herramienta / librería | Uso |
|---|---|---|
| Lenguaje | Python 3.12 | Base del proyecto |
| Entorno | `uv` (o venv + pip) | Entorno y dependencias idénticas en Windows |
| Stdlib núcleo | `dataclasses`, `enum`, `abc`, `typing`, `heapq`, `collections.deque` | PCB, estados, colas de planificación |
| Stdlib IPC | `multiprocessing` (`Pipe`, `shared_memory.SharedMemory`, `Lock`, `Semaphore`, `Event`, `Process`) | Pipes y memoria compartida reales, sincronización |
| Stdlib medición | `time.perf_counter_ns`, `tracemalloc`, `logging`, `tomllib` | Overhead real, detección de fugas, logs, escenarios en TOML |
| CLI | `typer` | Comandos `run`, `compare`, `ipc-demo`, `stress` |
| Visualización en vivo | `rich` (Live, Table, Progress) | Dashboard de colas, estados y métricas en tiempo real |
| Gráficos | `matplotlib` | Diagrama de Gantt y gráficas comparativas exportadas a PNG |
| Validación | `pydantic` v2 | Validar escenarios/entradas inválidas (robustez) |
| Pruebas | `pytest`, `pytest-cov`, `pytest-timeout`, `hypothesis` | Unit, cobertura, detección de deadlocks, pruebas de propiedades |
| Calidad | `ruff` (lint + format), `mypy --strict`, `pre-commit` | Clean Code y tipado robusto |
| Colaboración | Git + GitHub (repo, Projects/Kanban, PRs, Actions CI en `windows-latest` y `ubuntu-latest`) | Flujo de trabajo |
| Diagramas | Mermaid en Markdown / draw.io | Diagrama de clases, de estados, de arquitectura |
| Presentación | Google Slides / PowerPoint | Defensa |

## Arquitectura (paquete `os_process_engine/`)
- **Simulación por eventos discretos con reloj en ticks** → resultados deterministas y exactos contra los casos de referencia.
- **IPC con procesos reales** del SO (no simulados) → responde la pregunta de integridad de buffers.

```
os_process_engine/
  core/        pcb.py, states.py (NEW, READY, RUNNING, WAITING, UNINTERRUPTIBLE_SLEEP, SUSPENDED_READY/BLOCKED, TERMINATED),
               state_machine.py (transiciones válidas), process_table.py, cpu_mode.py (User/Kernel), syscalls.py (fork, exec, wait, exit, kill, read, write), clock.py
  scheduling/  base.py (Scheduler ABC), fcfs.py, sjf.py, srtf.py, priority.py (+aging), round_robin.py, mlfq.py,
               dispatcher.py (context switch con costo configurable), medium_term.py (swap in/out)
  ipc/         pipe_channel.py, shared_buffer.py (buffer circular productor-consumidor), sync.py
  workloads/   generator.py (CPU-bound / I/O-bound / mixto, semilla fija), scenarios/*.toml (convoy, rr_quantum, starvation, stress)
  metrics/     collector.py (espera, retorno, respuesta, throughput, % CPU, overhead CS), report.py (tabla/CSV), gantt.py
  cli/         main.py (typer), dashboard.py (rich)
  engine.py    bucle principal: reloj → llegadas → planificador → dispatcher → E/S → métricas
tests/         espejo de los módulos + tests/reference_cases/ (ejercicios resueltos a mano)
docs/          ARQUITECTURA.md, DECISIONES.md, diagramas, guion de defensa
```

Respuestas de auditoría que el diseño garantiza:
- **Context switch**: el `Dispatcher` guarda/restaura el contexto del PCB (PC, registros simulados), suma `cs_cost` ticks al reloj y los contabiliza como overhead; además mide el costo real con `perf_counter_ns`.
- **Starvation**: aging en Prioridad, boost periódico en MLFQ, quantum en RR. **Uninterruptible Sleep**: estado D no interrumpible por `kill`, sale solo por evento de fin de E/S; watchdog que alerta si supera un umbral.
- **Integridad IPC**: buffer circular en `SharedMemory` protegido con `Lock` + semáforos `empty/full`; cierre y `unlink()` garantizados con `try/finally` / context managers; pruebas de estrés con N productores/consumidores y `pytest-timeout`.

## Organización: 15 personas = 1 coordinación + 5 escuadras de 3 (incluye al coordinador en la escuadra 5)

| Escuadra | Módulo | Responsabilidad |
|---|---|---|
| E1 Núcleo | `core/` | PCB, máquina de estados, tabla de procesos, modos User/Kernel, syscalls simuladas con manejo de errores |
| E2 Planificación | `scheduling/` | 6 algoritmos, dispatcher, context switch, planificador a mediano plazo |
| E3 IPC | `ipc/` | Pipes, memoria compartida, sincronización, demo productor-consumidor |
| E4 Métricas y cargas | `workloads/`, `metrics/` | Generador de cargas, escenarios, métricas, Gantt, casos de referencia calculados a mano |
| E5 Integración, QA y defensa | `engine.py`, `cli/`, CI, `docs/` | Motor, CLI/dashboard, CI, revisión de PRs, documentación, presentación |

Cada escuadra nombra 1 líder; los 5 líderes + coordinador hacen un stand-up diario de 15 min.

## Lista de tareas

**Coordinación / E5 (Días 1–2: base para todos)**
- [ ] Crear repo GitHub, ramas protegidas (`main` solo por PR con 1 aprobación), tablero Kanban
- [ ] Esqueleto del paquete, `pyproject.toml`, `uv`, ruff, mypy strict, pre-commit
- [ ] CI GitHub Actions (lint + mypy + pytest en Windows y Ubuntu)
- [ ] **Contratos de interfaz** acordados con los líderes: `PCB`, `ProcessState`, `Scheduler` (ABC: `add`, `next`, `on_tick`, `preempt?`), `Event`, `MetricsCollector`
- [ ] Guía de contribución (convención de commits, docstrings, nombres)

**E1 Núcleo**
- [ ] `PCB` (pid, ppid, estado, prioridad, PC, registros, burst restante, tiempos de llegada/inicio/fin, E/S pendiente)
- [ ] Enum de estados + tabla de transiciones válidas; excepción `InvalidTransitionError`
- [ ] `ProcessTable` (alta, baja, búsqueda, árbol padre-hijo, zombies/huérfanos)
- [ ] Modo dual: trap User→Kernel en cada syscall, registro de cambios de modo
- [ ] Syscalls simuladas `fork/exec/wait/exit/kill/read/write` con validación de entradas inválidas
- [ ] Tests unitarios (transiciones válidas/ inválidas, syscalls con errores)

**E2 Planificación**
- [ ] `Scheduler` base + FCFS, SJF, SRTF
- [ ] Prioridad (apropiativa/no) con aging
- [ ] Round Robin con quantum configurable
- [ ] MLFQ (3 colas, boost periódico)
- [ ] `Dispatcher` con costo de context switch y conteo de cambios
- [ ] Planificador a mediano plazo (suspender/reanudar por carga)
- [ ] Tests contra casos de referencia de E4

**E3 IPC**
- [ ] `PipeChannel` sobre `multiprocessing.Pipe` (envío de mensajes, cierre limpio)
- [ ] `SharedBuffer` circular sobre `SharedMemory` + `Lock` + semáforos
- [ ] Demo productor-consumidor con N procesos
- [ ] Manejo de recursos: `unlink`, timeouts, procesos huérfanos
- [ ] Tests de estrés de carreras/deadlocks (`pytest-timeout`, `hypothesis`) y fugas (`tracemalloc`)

**E4 Métricas y cargas**
- [ ] Generador de cargas con semilla (CPU-bound, I/O-bound, mixto)
- [ ] Escenarios TOML: convoy, comparación de quantum, starvation, estrés masivo
- [ ] `MetricsCollector`: espera, retorno, respuesta, throughput, uso de CPU, % overhead
- [ ] Reporte en tabla/CSV + Gantt y gráficas con matplotlib
- [ ] 5+ casos de referencia resueltos a mano (de la guía de la Unidad I) como tests de precisión

**E5 Integración**
- [ ] `engine.py` (bucle de simulación por eventos)
- [ ] CLI `typer`: `run --algo rr --quantum 4 --scenario convoy`, `compare`, `ipc-demo`, `stress`
- [ ] Dashboard `rich` en vivo (colas, estados, métricas)
- [ ] Pruebas de integración end-to-end
- [ ] Docs: arquitectura, diagramas de clases/estados, decisiones de diseño
- [ ] Presentación + guion de demo + banco de preguntas de auditoría

## Cronograma (2 semanas)
| Días | Fase | Meta |
|---|---|---|
| 1–2 | Arranque | Repo, CI, contratos de interfaz congelados, confirmar Python con el docente |
| 3–7 | Desarrollo paralelo | Cada escuadra entrega su módulo con tests (≥80 % cobertura) |
| 8–10 | Integración | Motor + CLI + escenarios funcionando; casos de referencia en verde |
| 11–12 | Endurecimiento | Estrés, fugas, carreras, entradas inválidas, limpieza de código, docs |
| 13–14 | Defensa | Slides, 2 ensayos completos de demo, simulacro de preguntas (todos deben poder explicar cualquier módulo) |

## Reglas de trabajo
- Rama por tarea (`feat/e2-round-robin`), PR pequeño, 1 revisión de otra escuadra, CI en verde para fusionar.
- Todo tipado (mypy strict), docstrings en español con vocabulario de SO, sin `print` (usar `logging`).
- Una issue por tarea de la lista, asignada a una persona, con etiqueta de escuadra.

