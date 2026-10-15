# Changelog

El proyecto sigue el estándar [Semantic Versioning (SemVer)](https://semver.org/), complementado con las siguientes etapas de ciclo de desarrollo:

- `pre-alpha`
- `alpha`
- `beta`
- `snapshot`
- `release`

## [Unreleased]

## [0.0.3-pre-alpha] - 2026-10-15

### Added
- Dataset histórico de sueldos de alcaldes para las 346 comunas de Chile 2018-2024 (`data/raw/alcaldes_remuneraciones_comunas.csv`).
- Dataset de referencia y componentes de la escala municipal de alcaldes Grados 1° al 6° (`data/raw/escala_municipal_alcaldes_historico.csv`).
- Documento técnico de análisis de sueldos edilicios: `docs/ALCALDES_REMUNERACIONES.md` (Ley 18.695 Art. 69, DL 3551, categorización municipal y asignaciones de zona).
- Actualización de fuentes oficiales con SINIM / SUBDERE y Transparencia Activa Municipal (CPLT) en `docs/FUENTES.md`.
- Script reproducible: `scripts/build_alcaldes_salarios.py`.
- Catálogo histórico de políticos en Chile 2018-2026 (`data/raw/politicos_chile_historico.csv`) con 439 registros vinculados a distritos, circunscripciones, comunas y país.
- Script de extracción desde BCN / SERVEL: `scripts/build_politicos_historico.py`.

## [0.0.2-pre-alpha] - 2026-10-15

### Added
- Sistema de identificadores únicos normalizados para entidades territoriales y electorales: `REG-XX`, `CIRC-XX`, `DIST-XX` y `COM-XXXXX`.
- Tablas dimensionales en `data/processed/`: `dim_regiones.csv`, `dim_circunscripciones.csv`, `dim_distritos.csv`, `dim_comunas.csv` y matriz unificada `division_territorial_electoral.csv`.
- Corrección de Código Único Territorial (CUT) para Cabo de Hornos (`12201`) y Antártica (`12202`).
- Dataset histórico de remuneraciones de altos cargos políticos 2018-2026 (`data/raw/remuneraciones_politicos_historico.csv`), cubriendo Presidentes, Ministros, Subsecretarios, Diputados, Senadores y Expresidentes de la República.
- Catálogo de asignaciones operacionales (`data/raw/asignaciones_gastos_politicos.csv`) detallando personal de apoyo, consultoría/asesorías externas, arriendo de sedes, combustible/bencina, peajes, vehículos con/sin chofer, pasajes y viáticos/alojamiento.
- Matriz de gastos operacionales y suplementos territoriales de los 28 distritos (`data/raw/distritos_gastos_operacionales.csv`).
- Documento técnico de análisis de gastos de cargos públicos: `docs/GASTOS_POLITICOS.md`.
- Documento de especificación de identificadores: `docs/IDENTIFICADORES.md`.
- Actualización de fuentes oficiales en `docs/FUENTES.md` (Consejo Resolutivo de Asignaciones, Senado, Cámara de Diputados, Presidencia, CADP).
- Scripts reproducibles: `scripts/build_territorial_ids.py` y `scripts/generate_distritos_gastos.py`.

## [0.0.1-pre-alpha] - 2026-10-15

### Added
- Estructura inicial del repositorio y directorios `data/raw`, `data/processed` y `docs`.
- Extracción de datos de división político-electoral desde BCN SIIT (`data/raw/division_politico_electoral.csv`).
- Script de extracción reproducible (`scripts/extract_bcn_division.py`).
- Documentación de fuentes oficiales (`docs/FUENTES.md`).
- Documentación de marco legal aplicable (`docs/MARCO_LEGAL.md`).
- Exclusión local de `chat-history/` en `.gitignore`.
