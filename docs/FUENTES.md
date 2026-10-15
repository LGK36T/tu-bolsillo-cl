# Fuentes de Información Oficiales

Este documento registra los portales, marcos regulatorios y organismos oficiales de los que se obtienen los datos de **Tu Bolsillo CL**.

---

## 1. División Territorial y Electoral

### Biblioteca del Congreso Nacional de Chile (BCN) — SIIT
* **Plataforma:** Sistema Integrado de Información Territorial (SIIT).
* **URL:** https://www.bcn.cl/siit/nuestropais/divisionelectoral/index.htm
* **Descripción:** Composición oficial de las 16 regiones, 16 circunscripciones senatoriales, 28 distritos de diputados y 346 comunas de Chile bajo la Ley N° 20.840.
* **Archivos asociados:**
  * Raw: [`data/raw/division_politico_electoral.csv`](../data/raw/division_politico_electoral.csv)
  * Procesados: [`data/processed/division_territorial_electoral.csv`](../data/processed/division_territorial_electoral.csv), [`data/processed/dim_regiones.csv`](../data/processed/dim_regiones.csv), [`data/processed/dim_circunscripciones.csv`](../data/processed/dim_circunscripciones.csv), [`data/processed/dim_distritos.csv`](../data/processed/dim_distritos.csv), [`data/processed/dim_comunas.csv`](../data/processed/dim_comunas.csv).
* **Scripts:** [`scripts/extract_bcn_division.py`](../scripts/extract_bcn_division.py) y [`scripts/build_territorial_ids.py`](../scripts/build_territorial_ids.py).

---

## 2. Remuneraciones y Dietas Políticas

### Presidencia de la República — Transparencia Activa
* **Plataforma:** Portal de Transparencia Activa Presidencia.
* **URL:** http://transparenciaactiva.presidencia.cl
* **Descripción:** Escala Única de Sueldos (DL N° 249), Asignación de Dirección Superior (Ley N° 19.863) y bonos de cumplimiento institucional (PMG, Ley N° 19.553) del Presidente de la República, Ministros y Subsecretarios.

### Cámara de Diputadas y Diputados de Chile — Transparencia
* **Plataforma:** Transparencia Activa - Dieta Parlamentaria.
* **URL:** https://www.camara.cl
* **Descripción:** Planillas oficiales de pago mensual de dietas brutas y líquidas de los 155 diputados de la República (Artículo 62 de la Constitución).

### Senado de la República — Transparencia Activa y Finanzas
* **Plataforma:** Portal de Transparencia del Senado.
* **URL:** https://www.senado.cl
* **Descripción:** Remuneraciones y dietas de los 50 senadores. Pagos mensuales, asignaciones de traslación y gastos de oficinas de los Expresidentes de la República bajo el Artículo 30 de la Constitución Política (Ley N° 19.672).

### Consejo de Alta Dirección Pública (CADP) y Comisión Técnica
* **Normativa:** Ley N° 21.233 (reforma constitucional) y Artículo 38 bis de la Constitución Política.
* **Descripción:** Resoluciones de rebaja del 25% de la dieta parlamentaria y rentas de ministros en 2020, y fijación periódica de remuneraciones de autoridades por comisión técnica autónoma.

---

## 3. Asignaciones Parlamentarias y Gastos Operacionales

### Consejo Resolutivo de Asignaciones Parlamentarias
* **Marco Legal:** Creado por la Ley N° 20.447 (año 2010).
* **Resolución clave:** Resolución N° 12 sistematizada y acuerdos complementarios anuales.
* **URL:** https://www.consejoresolutivo.cl
* **Descripción:** Fijación de montos, criterios de uso y topes máximos de fondos públicos destinados a:
  * Personal de apoyo (asesores territoriales, secretarias, administrativos).
  * Asesorías externas (consultorías e informes técnicos especializados).
  * Gastos operacionales (arriendo de sedes, combustible/bencina, peajes, vehículos con o sin chofer, pasajes aéreos y terrestres, alojamiento y viáticos en Valparaíso).
* **Archivos asociados:**
  * [`data/raw/remuneraciones_politicos_historico.csv`](../data/raw/remuneraciones_politicos_historico.csv)
  * [`data/raw/asignaciones_gastos_politicos.csv`](../data/raw/asignaciones_gastos_politicos.csv)
  * [`data/raw/distritos_gastos_operacionales.csv`](../data/raw/distritos_gastos_operacionales.csv)
* **Script:** [`scripts/generate_distritos_gastos.py`](../scripts/generate_distritos_gastos.py).
