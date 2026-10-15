# data/

Estructura de almacenamiento de datos:

## `raw/`
Datos en formato original y catálogos de referencia obtenidos de fuentes oficiales del Estado:
- `division_politico_electoral.csv`: División territorial y político-electoral de Chile con identificadores normalizados (BCN SIIT).
- `remuneraciones_politicos_historico.csv`: Serie histórica (2018-2026) de remuneraciones brutas y líquidas de Presidentes, Ministros, Subsecretarios, Parlamentarios y Expresidentes (CADP / Transparencia Activa).
- `asignaciones_gastos_politicos.csv`: Catálogo de asignaciones operacionales (personal, consultorías, sedes, bencina, peajes, arriendo de autos, chofer, pasajes y viáticos) del Consejo Resolutivo de Asignaciones y Senado.
- `distritos_gastos_operacionales.csv`: Matriz de gastos operacionales y suplementos geográficos para los 28 distritos de diputados.

## `processed/`
Datasets estructurados, limpios y relacionales:
- `division_territorial_electoral.csv`: Matriz desnormalizada completa con todos los identificadores (`REG-XX`, `CIRC-XX`, `DIST-XX`, `COM-XXXXX`).
- `dim_regiones.csv`: Dimensión de las 16 regiones de Chile.
- `dim_circunscripciones.csv`: Dimensión de las 16 circunscripciones senatoriales.
- `dim_distritos.csv`: Dimensión de los 28 distritos de diputados.
- `dim_comunas.csv`: Dimensión de las 346 comunas con su código CUT de 5 dígitos del INE.

## Privacidad y Normativa (Ley N° 19.628)
No se almacena ni procesa información sensible privada (RUT personal, domicilios particulares, teléfonos privados o antecedentes médicos).
