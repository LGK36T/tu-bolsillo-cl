# tu-bolsillo-cl

Proyecto open source para la recopilación, normalización y análisis de datos públicos del Estado, territorio nacional y autoridades en Chile.

## Estado del proyecto

Versión actual: `0.0.3-pre-alpha`

## Módulos y Datasets Disponibles

El proyecto consolida datasets públicos en formatos abiertos (CSV) dentro de `data/raw/` y `data/processed/`:

1. **División Territorial y Electoral:**
   - 16 Regiones (`REG-01` a `REG-16`), 16 Circunscripciones Senatoriales (`CIRC-01` a `CIRC-16`), 28 Distritos Electorales (`DIST-01` a `DIST-28`) y 346 Comunas (`COM-01101` a `COM-16305` con Códigos Únicos Territoriales oficiales del INE).
   - Tablas dimensionales relacionales y matriz unificada en `data/processed/`.

2. **Remuneraciones y Dietas de Altos Cargos (2018-2026):**
   - Series históricas de remuneraciones brutas y líquidas del Presidente de la República, Expresidentes (Art. 30 de la Constitución), Ministros de Estado, Subsecretarios, Diputados y Senadores.
   - Impacto de la rebaja transitoria del 25% de la CADP (Ley N° 21.233 de 2020) y reajustes posteriores.

3. **Asignaciones Parlamentarias y Gastos Operacionales:**
   - Desglose de partidas normadas por el Consejo Resolutivo de Asignaciones Parlamentarias (Resolución N° 12): personal de apoyo, asesorías externas/consultoría, arriendo de sedes, combustible/bencina, peajes, arriendo de vehículos con o sin chofer, pasajes y viáticos/alojamiento.
   - Matriz de suplementos geográficos y costos operacionales para los 28 distritos.

4. **Sueldos Históricos de Alcaldes (346 Comunas, 2018-2024):**
   - Catálogo comunal de remuneraciones edilicias fijadas por la Escala Municipal (DL N° 3.551), Asignación de Dirección Superior (Ley N° 18.695 Art. 69), grados 1° al 6° y recargos por asignación de zona (DL N° 249 / 450).

5. **Catálogo de Políticos (439 Registros):**
   - Nómina de parlamentarios electos por distrito y circunscripción (periodos LV 2018-2022 y LVI 2022-2026), autoridades del Ejecutivo y alcaldes de capitales y comunas principales.

## Documentación Técnica

- [docs/FUENTES.md](docs/FUENTES.md): Registro de plataformas oficiales (BCN, SERVEL, Transparencia Activa, Consejo Resolutivo de Asignaciones, SUBDERE / SINIM, CADP).
- [docs/GASTOS_POLITICOS.md](docs/GASTOS_POLITICOS.md): Bases legales y operativas de dietas, pensiones vitalicias y asignaciones parlamentarias.
- [docs/ALCALDES_REMUNERACIONES.md](docs/ALCALDES_REMUNERACIONES.md): Metodología de cálculo, categorización municipal y escala de sueldos edilicios.
- [docs/IDENTIFICADORES.md](docs/IDENTIFICADORES.md): Estándar de nomenclatura de identificadores territoriales (`REG`, `CIRC`, `DIST`, `COM`).
- [docs/MARCO_LEGAL.md](docs/MARCO_LEGAL.md): Bases jurídicas de publicidad y probidad (Art. 8 Constitución, Ley 20.285) y directrices de privacidad de datos (Ley 19.628).

## Licencia

[MIT](LICENSE)
