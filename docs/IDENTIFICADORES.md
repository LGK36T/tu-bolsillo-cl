# Sistema de Identificadores Territoriales y Electorales

El proyecto utiliza un sistema estructurado de códigos únicos para garantizar integridad referencial y facilitar el análisis relacional entre las distintas entidades del Estado de Chile.

---

## 1. Nomenclatura de Identificadores

| Entidad | Formato de ID | Rango / Cantidad | Base Normativa | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Regiones** | `REG-{CUT_2D}` | `REG-01` a `REG-16` (16) | Código Único Territorial (CUT) de 2 dígitos INE/BCN | `REG-13` (Metropolitana), `REG-05` (Valparaíso) |
| **Circunscripciones** | `CIRC-{NUM_2D}` | `CIRC-01` a `CIRC-16` (16) | Número senatorial (Ley N° 20.840) | `CIRC-07` (RM, 5 senadores), `CIRC-01` (Arica, 2 senadores) |
| **Distritos** | `DIST-{NUM_2D}` | `DIST-01` a `DIST-28` (28) | Número de distrito electoral de diputados | `DIST-10` (Santiago, 8 diputados), `DIST-28` (Magallanes, 3 diputados) |
| **Comunas** | `COM-{CUT_5D}` | `COM-01101` a `COM-16305` (346) | Código Único Territorial oficial de 5 dígitos del INE | `COM-15101` (Arica), `COM-13101` (Santiago), `COM-12201` (Cabo de Hornos), `COM-12202` (Antártica) |

---

## 2. Correspondencia Jerárquica

```text
[Región: REG-XX]
    └── [Circunscripción Senatorial: CIRC-XX]
            └── [Distrito Electoral: DIST-XX]
                    └── [Comuna: COM-XXXXX (CUT 5 dígitos)]
```

* Cada comuna pertenece unívocamente a exactamente un distrito electoral, una circunscripción senatorial y una región.
* En 14 de las 16 regiones, la circunscripción senatorial coincide geográficamente con los límites de la región.
* Cada distrito electoral agrupa entre 1 y 52 comunas pertenecientes a la misma región administrativa.

---

## 3. Tablas de Dimensiones Disponibles

En el directorio [`data/processed/`](../data/processed):
* [`dim_regiones.csv`](../data/processed/dim_regiones.csv): Catálogo de las 16 regiones con `id_region`, `codigo_cut_region`, `nombre_region` y enlace a su circunscripción.
* [`dim_circunscripciones.csv`](../data/processed/dim_circunscripciones.csv): Catálogo de las 16 circunscripciones con cantidad de senadores electos.
* [`dim_distritos.csv`](../data/processed/dim_distritos.csv): Catálogo de los 28 distritos con cantidad de diputados electos y su región.
* [`dim_comunas.csv`](../data/processed/dim_comunas.csv): Catálogo de las 346 comunas con su código CUT de 5 dígitos y llaves foráneas.
* [`division_territorial_electoral.csv`](../data/processed/division_territorial_electoral.csv): Matriz desnormalizada unificada con todos los identificadores.
