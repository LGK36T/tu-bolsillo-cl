#!/usr/bin/env python3
"""
Generador de identificadores estándar para la división territorial y electoral de Chile.
Crea datasets procesados y tablas de dimensiones en data/processed/.
"""

import csv
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FILE = os.path.join(BASE_DIR, "data", "raw", "division_politico_electoral.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def get_circ_num(circ_str: str) -> int:
    m = re.search(r"(\d+)", circ_str)
    return int(m.group(1)) if m else 0

def get_dist_num(dist_str: str) -> int:
    m = re.search(r"(\d+)", dist_str)
    return int(m.group(1)) if m else 0

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    with open(RAW_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    enriched_rows = []
    regiones_dict = {}
    circs_dict = {}
    distritos_dict = {}
    comunas_dict = {}

    for r in raw_rows:
        cut_comuna = r["codigo_comuna_cut"].zfill(5)
        if r["comuna"] == "Antártica" and cut_comuna == "12201":
            cut_comuna = "12202"
        cut_region = cut_comuna[:2]

        id_region = f"REG-{cut_region}"
        circ_num = get_circ_num(r["circunscripcion"])
        id_circ = f"CIRC-{circ_num:02d}"

        dist_num = get_dist_num(r["distrito"])
        id_dist = f"DIST-{dist_num:02d}"

        id_comuna = f"COM-{cut_comuna}"

        row_data = {
            "id_region": id_region,
            "codigo_cut_region": cut_region,
            "region": r["region"],
            "id_circunscripcion": id_circ,
            "circunscripcion": r["circunscripcion"],
            "senadores_circunscripcion": int(r["senadores_circunscripcion"]),
            "id_distrito": id_dist,
            "distrito": r["distrito"],
            "diputados_distrito": int(r["diputados_distrito"]),
            "id_comuna": id_comuna,
            "codigo_cut_comuna": cut_comuna,
            "comuna": r["comuna"]
        }
        enriched_rows.append(row_data)

        # Dimension Regiones
        if id_region not in regiones_dict:
            regiones_dict[id_region] = {
                "id_region": id_region,
                "codigo_cut_region": cut_region,
                "nombre_region": r["region"],
                "id_circunscripcion": id_circ
            }

        # Dimension Circunscripciones
        if id_circ not in circs_dict:
            circs_dict[id_circ] = {
                "id_circunscripcion": id_circ,
                "numero_circunscripcion": circ_num,
                "senadores": int(r["senadores_circunscripcion"]),
                "id_region": id_region
            }

        # Dimension Distritos
        if id_dist not in distritos_dict:
            distritos_dict[id_dist] = {
                "id_distrito": id_dist,
                "numero_distrito": dist_num,
                "diputados": int(r["diputados_distrito"]),
                "id_region": id_region
            }

        # Dimension Comunas
        if id_comuna not in comunas_dict:
            comunas_dict[id_comuna] = {
                "id_comuna": id_comuna,
                "codigo_cut_comuna": cut_comuna,
                "nombre_comuna": r["comuna"],
                "id_distrito": id_dist,
                "id_circunscripcion": id_circ,
                "id_region": id_region
            }

    # 1. Exportar division_territorial_electoral.csv en processed
    unified_file = os.path.join(PROCESSED_DIR, "division_territorial_electoral.csv")
    with open(unified_file, "w", encoding="utf-8", newline="") as f:
        fields = [
            "id_region", "codigo_cut_region", "region",
            "id_circunscripcion", "circunscripcion", "senadores_circunscripcion",
            "id_distrito", "distrito", "diputados_distrito",
            "id_comuna", "codigo_cut_comuna", "comuna"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(enriched_rows)

    # 2. Exportar dim_regiones.csv
    with open(os.path.join(PROCESSED_DIR, "dim_regiones.csv"), "w", encoding="utf-8", newline="") as f:
        fields = ["id_region", "codigo_cut_region", "nombre_region", "id_circunscripcion"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(regiones_dict.values(), key=lambda x: x["codigo_cut_region"]))

    # 3. Exportar dim_circunscripciones.csv
    with open(os.path.join(PROCESSED_DIR, "dim_circunscripciones.csv"), "w", encoding="utf-8", newline="") as f:
        fields = ["id_circunscripcion", "numero_circunscripcion", "senadores", "id_region"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(circs_dict.values(), key=lambda x: x["numero_circunscripcion"]))

    # 4. Exportar dim_distritos.csv
    with open(os.path.join(PROCESSED_DIR, "dim_distritos.csv"), "w", encoding="utf-8", newline="") as f:
        fields = ["id_distrito", "numero_distrito", "diputados", "id_region"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(distritos_dict.values(), key=lambda x: x["numero_distrito"]))

    # 5. Exportar dim_comunas.csv
    with open(os.path.join(PROCESSED_DIR, "dim_comunas.csv"), "w", encoding="utf-8", newline="") as f:
        fields = ["id_comuna", "codigo_cut_comuna", "nombre_comuna", "id_distrito", "id_circunscripcion", "id_region"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(comunas_dict.values(), key=lambda x: x["codigo_cut_comuna"]))

    print(f"Archivos procesados generados exitosamente en: {PROCESSED_DIR}")
    print(f" - Regiones: {len(regiones_dict)}")
    print(f" - Circunscripciones: {len(circs_dict)}")
    print(f" - Distritos: {len(distritos_dict)}")
    print(f" - Comunas: {len(comunas_dict)}")

if __name__ == "__main__":
    main()
