# Remuneraciones de Alcaldes en Chile

Este documento sistematiza la normativa, el cálculo y la evolución histórica de las remuneraciones de los alcaldes de las 346 comunas de Chile.

---

## 1. Marco Jurídico y Normativo

Las remuneraciones de los alcaldes en Chile están reguladas por ley y no dependen del arbitrio de los concejos municipales:

* **Ley N° 18.695 (Orgánica Constitucional de Municipalidades):**
  * **Artículo 69:** Establece la **Asignación de Dirección Superior** exclusiva para los alcaldes, equivalente al **100% de la suma del Sueldo Base y la Asignación Municipal**.
* **Decreto Ley N° 3.551 de 1980:** Fija la Escala de Sueldos Municipales y las asignaciones bases para el personal municipal.
* **Ley N° 19.280 y Ley N° 20.922:** Regulan las plantas municipales y la categorización presupuestaria de los municipios por la SUBDERE.
* **Decreto Ley N° 249 y DL N° 450:** Regulan la **Asignación de Zona** para compensar el costo de vida y aislamiento territorial en comunas extremas e insulares.

---

## 2. Determinación del Sueldo y Categorización Municipal

El sueldo de un alcalde está determinado por el **Grado del Alcalde** en la planta directiva municipal (Grados 1° al 6°), fijado de acuerdo a la categoría de la municipalidad según su volumen de ingresos propios, presupuesto global y población (determinados por SUBDERE y SINIM):

| Grado Alcalde | Categoría Municipal Típica | Criterio de Asignación | Ejemplos de Comunas | Rango Bruto Base 2024 (Sin Zona) |
| :---: | :--- | :--- | :--- | :---: |
| **Grado 1°** | 1ª Categoría | Capitales regionales, grandes urbes (>120.000 hab) y altos presupuestos | Santiago, Las Condes, Viña del Mar, Concepción, Temuco, Antofagasta | $8.450.000 CLP |
| **Grado 2°** | 2ª Categoría | Ciudades intermedias mayores y cabeceras provinciales (60.000 - 120.000 hab) | Calama, Quilpué, San Bernardo, Talagante, Linares, Curicó, Osorno | $7.450.000 CLP |
| **Grado 3°** | 3ª Categoría | Comunas urbanas e intermedias medianas (25.000 - 60.000 hab) | San Felipe, Los Andes, Buin, Rengo, San Carlos, Villarrica, Castro | $6.520.000 CLP |
| **Grado 4°** | 4ª Categoría | Comunas intermedias menores (12.000 - 25.000 hab) | Quintero, Cabildo, Isla de Maipo, Chimbarongo, San Javier, Victoria | $5.640.000 CLP |
| **Grado 5°** | 5ª Categoría | Comunas rurales pequeñas (5.000 - 12.000 hab) | Combarbalá, Canela, Petorca, Navidad, Vichuquén, Cobquecura, Tirúa | $4.860.000 CLP |
| **Grado 6°** | 6ª Categoría | Comunas micro o rurales aisladas (<5.000 hab) | General Lagos, Camiña, Ollagüe, Juan Fernández, Rapa Nui, Tortel, Cabo de Hornos | $4.150.000 CLP |

---

## 3. Estructura de la Remuneración Mensual

El haber bruto mensual del alcalde se compone de:

1. **Sueldo Base:** Determinado por el grado municipal correspondiente.
2. **Asignación Municipal:** Estipendio complementario fijado por ley municipal.
3. **Asignación de Dirección Superior (Art. 69 Ley 18.695):** Monto equivalente al 100% de la suma del sueldo base y la asignación municipal.
4. **Incrementos Previsionales y Bonificaciones Legales:** Ajustes derivados de leyes generales del sector público.
5. **Asignación de Zona (cuando aplique):** Porcentaje de incremento sobre el sueldo por aislamiento geográfico:
   * **0%:** Región Metropolitana, Valparaíso continental, y zonas centrales (O'Higgins, Maule, Ñuble, Biobío).
   * **15%:** Región de Atacama y zonas cordilleranas específicas.
   * **30%:** Región de Antofagasta.
   * **40% a 50%:** Región de Tarapacá y Región de Arica y Parinacota.
   * **90% a 105%:** Región de Aysén y Región de Magallanes (Cabo de Hornos / Antártica 105%).
   * **100%:** Territorios insulares especiales (Isla de Pascua / Rapa Nui y Archipiélago de Juan Fernández).

---

## 4. Evolución Histórica de la Escala Base de Alcaldes (2018 - 2024)

Montos brutos mensuales base en pesos chilenos (sin considerar asignación de zona):

| Grado | 2018 | 2020 | 2022 | 2024 |
| :---: | :---: | :---: | :---: | :---: |
| **1°** | $7.150.000 | $7.620.000 | $7.980.000 | $8.450.000 |
| **2°** | $6.250.000 | $6.680.000 | $7.020.000 | $7.450.000 |
| **3°** | $5.450.000 | $5.820.000 | $6.120.000 | $6.520.000 |
| **4°** | $4.700.000 | $5.020.000 | $5.280.000 | $5.640.000 |
| **5°** | $4.050.000 | $4.320.000 | $4.550.000 | $4.860.000 |
| **6°** | $3.450.000 | $3.680.000 | $3.880.000 | $4.150.000 |

*Nota:* Al incorporar la asignación de zona, un alcalde de Grado 1° en una comuna extrema (ej. Iquique o Antofagasta) percibe entre $10.900.000 y $11.830.000 CLP brutos mensuales en 2024.

---

## 5. Datasets Disponibles en el Repositorio

* [`data/raw/alcaldes_remuneraciones_comunas.csv`](../data/raw/alcaldes_remuneraciones_comunas.csv): Catálogo completo de las 346 comunas de Chile con su código CUT, grado edilicio, porcentaje de asignación de zona y sueldos brutos históricos (2018, 2020, 2022, 2024) y líquido estimado.
* [`data/raw/escala_municipal_alcaldes_historico.csv`](../data/raw/escala_municipal_alcaldes_historico.csv): Desglose analítico de los componentes del sueldo (base, asignación municipal y dirección superior) para los 6 grados entre 2018 y 2024.
* Script de generación: [`scripts/build_alcaldes_salarios.py`](../scripts/build_alcaldes_salarios.py).
