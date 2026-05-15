\# Timetabling ITCM



Modelo matemático para la programación eficiente de horarios académicos universitarios, aplicado a instancias reales del Instituto Tecnológico de Ciudad Madero.



Este repositorio contiene el código fuente, archivos de configuración, scripts de construcción de instancias, solver MILP y dashboard de validación utilizados para reproducir los experimentos del modelo de programación académica.



\## Objetivo



Automatizar la generación de horarios académicos universitarios mediante un modelo de programación entera mixta/binaria, considerando restricciones institucionales como:



\- No solapamiento de profesores.

\- No solapamiento de aulas.

\- No solapamiento de grupos.

\- Capacidad suficiente de aulas.

\- Asignación de aula única por curso.

\- Cumplimiento de sesiones requeridas.

\- Preferencia por aulas y laboratorios específicos.

\- Minimización del costo de afinidad docente-materia.



\## Instancias experimentales



Las pruebas principales fueron realizadas sobre:



| Instancia | Profesores | Aulas | Cursos (MG) | Eventos |

|---|---:|---:|---:|---:|

| Ingeniería en Sistemas Computacionales | 97 | 35 | 195 | 645 |

| Ingeniería Industrial | 121 | 75 | 311 | 936 |



\## Resultados principales



| Instancia | Estado | Tiempo (s) | MIP Gap (%) | Objetivo Z |

|---|---:|---:|---:|---:|

| Ingeniería en Sistemas Computacionales | Optimal | 37.47 | 10.73 | 14,442.051 |

| Ingeniería Industrial | Feasible (TimeLimit) | 600.34 | 84.88 | 72,950.000 |



Ambas soluciones obtuvieron cero solapes de aulas, profesores y grupos.



\## Requisitos



\- Python 3.10

\- IBM ILOG CPLEX Optimization Studio 22.1

\- Git

\- Windows 10/11 recomendado



\## Instalación rápida



Crear entorno virtual:



```bash

python -m venv .venv



Activar entorno en Windows:



```bash

.venv\\Scripts\\activate

```



Instalar dependencias:



```bash

pip install -r requirements.txt

```



Copiar archivo de configuración:



```bash

copy .env.example .env

```



Editar `.env` y configurar la ruta local de CPLEX:



```env

CPLEX\_BIN=C:\\Program Files\\IBM\\ILOG\\CPLEX\_Studio221\\cplex\\bin\\x64\_win64\\cplex.exe

```

