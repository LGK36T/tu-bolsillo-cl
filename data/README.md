# data/

Estructura de almacenamiento de datos:

## `raw/`
Datos en formato original y catálogos de referencia obtenidos de fuentes oficiales del Estado:
- `division_politico_electoral.csv`: División territorial y político-electoral de Chile con identificadores normalizados (BCN SIIT).
- `remuneraciones_politicos_historico.csv`: Serie histórica (2018-2026) de remuneraciones brutas y líquidas de Presidentes, Ministros, Subsecretarios, Parlamentarios y Expresidentes (CADP / Transparencia Activa).
- `asignaciones_gastos_politicos.csv`: Catálogo de asignaciones operacionales (personal, consultorías, sedes, bencina, peajes, arriendo de autos, chofer, pasajes y viáticos) del Consejo Resolutivo de Asignaciones y Senado.
- `distritos_gastos_operacionales.csv`: Matriz de gastos operacionales y suplementos geográficos para los 28 distritos de diputados.
- `alcaldes_remuneraciones_comunas.csv`: Serie histórica de sueldos de alcaldes de las 346 comunas (2018-2024), grados municipales y asignaciones de zona (Ley 18.695 / CPLT / SUBDERE).
- `escala_municipal_alcaldes_historico.csv`: Escala municipal de referencia y desglose por grado (1° al 6°) de sueldo base, asignación municipal y dirección superior.
- `politicos_chile_historico.csv`: Catálogo histórico de 439 cargos políticos (2018-2026), incluyendo Presidentes, Expresidentes, Ministros, Diputados (períodos LV y LVI por distrito), Senadores y Alcaldes.

## `processed/`
Datasets estructurados, limpios y relacionales:
- `division_territorial_electoral.csv`: Matriz desnormalizada completa con todos los identificadores (`REG-XX`, `CIRC-XX`, `DIST-XX`, `COM-XXXXX`).
- `dim_regiones.csv`: Dimensión de las 16 regiones de Chile.
- `dim_circunscripciones.csv`: Dimensión de las 16 circunscripciones senatoriales.
- `dim_distritos.csv`: Dimensión de los 28 distritos de diputados.
- `dim_comunas.csv`: Dimensión de las 346 comunas con su código CUT de 5 dígitos del INE.

## Privacidad y Normativa (Ley N° 19.628)
No se almacena ni procesa información sensible privada (RUT personal, domicilios particulares, teléfonos privados o antecedentes médicos).
