# Fuentes de Información

## Biblioteca del Congreso Nacional de Chile (BCN) - SIIT

- **Origen:** https://www.bcn.cl/siit/nuestropais/divisionelectoral/index.htm
- **Descripción:** División político-electoral oficial de Chile (16 regiones, 16 circunscripciones senatoriales, 28 distritos de diputados y 346 comunas con códigos CUT).
- **Archivo de datos:** `data/raw/division_politico_electoral.csv`
- **Script de extracción:** `scripts/extract_bcn_division.py`

### Estructura de `division_politico_electoral.csv`

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `region` | string | Nombre de la región |
| `circunscripcion` | string | Circunscripción senatorial (ordinal) |
| `senadores_circunscripcion` | int | Número de senadores electos |
| `distrito` | string | Identificador del distrito |
| `diputados_distrito` | int | Número de diputados electos |
| `comuna` | string | Nombre de la comuna |
| `codigo_comuna_cut` | string | Código Único Territorial (5 dígitos) |
