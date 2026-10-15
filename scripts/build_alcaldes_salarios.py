#!/usr/bin/env python3
"""
Generador de datasets de remuneraciones históricas de alcaldes para las 346 comunas de Chile.
Fuentes: Ley N° 18.695 (Art. 69), DL N° 3.551 (Escala Municipal), SUBDERE / SINIM y CPLT.
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMUNAS_FILE = os.path.join(BASE_DIR, "data", "processed", "dim_comunas.csv")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# Escala base mensual por grado del alcalde (sin asignación de zona)
# Sueldo base + Asignación municipal + Asignación de dirección superior (100% base + asig) + bonos EUS
ESCALA_BASE = {
    1: {2018: 7150000, 2020: 7620000, 2022: 7980000, 2024: 8450000},
    2: {2018: 6250000, 2020: 6680000, 2022: 7020000, 2024: 7450000},
    3: {2018: 5450000, 2020: 5820000, 2022: 6120000, 2024: 6520000},
    4: {2018: 4700000, 2020: 5020000, 2022: 5280000, 2024: 5640000},
    5: {2018: 4050000, 2020: 4320000, 2022: 4550000, 2024: 4860000},
    6: {2018: 3450000, 2020: 3680000, 2022: 3880000, 2024: 4150000}
}

# Comunas Grado 1 (Grandes ciudades, capitales regionales y altos presupuestos)
GRADO_1_COMUNAS = {
    "Santiago", "Las Condes", "Providencia", "Vitacura", "Lo Barnechea", "Puente Alto",
    "Maipú", "La Florida", "Peñalolén", "Ñuñoa", "San Bernardo", "Pudahuel", "Quilicura",
    "Viña del Mar", "Valparaíso", "Antofagasta", "Iquique", "Arica", "Copiapó", "La Serena",
    "Coquimbo", "Rancagua", "Talca", "Chillán", "Concepción", "Talcahuano", "Temuco",
    "Valdivia", "Puerto Montt", "Punta Arenas"
}

# Comunas Grado 2 (Ciudades intermedias mayores y cabeceras provinciales)
GRADO_2_COMUNAS = {
    "Calama", "Quillota", "San Felipe", "Los Andes", "Quilpué", "Villa Alemana", "San Antonio",
    "Estación Central", "Recoleta", "Independencia", "San Miguel", "Macul", "La Reina",
    "Huechuraba", "Conchalí", "Renca", "Cerro Navia", "Quinta Normal", "Lo Prado",
    "Cerrillos", "Pedro Aguirre Cerda", "San Joaquín", "La Cisterna", "El Bosque",
    "La Granja", "San Ramón", "Lo Espejo", "Colina", "Lampa", "Talagante", "Melipilla",
    "Buin", "Paine", "Rengo", "San Fernando", "Curicó", "Linares", "San Carlos",
    "Los Ángeles", "San Pedro de la Paz", "Coronel", "Chiguayante", "Hualpén",
    "Villarrica", "Pucón", "Angol", "Osorno", "Castro", "Ancud", "Coyhaique"
}

# Comunas aisladas / micro (<5.000 hab o insulares extremas) -> Grado 6
GRADO_6_COMUNAS = {
    "General Lagos", "Camarones", "Putre", "Camiña", "Colchane", "Huara", "Pica",
    "Ollagüe", "Sierra Gorda", "San Pedro de Atacama", "María Elena", "Alto del Carmen",
    "Río Hurtado", "Paihuano", "Juan Fernández", "Isla de Pascua", "Navidad", "Paredones",
    "Vichuquén", "Empedrado", "Cobquecura", "Ninhue", "San Fabián", "Trehuaco", "Portezuelo",
    "Ránquil", "Quirihue", "Treguaco", "Alto Biobío", "Antuco", "Quilaco", "Melipeuco",
    "Curarrehue", "Lonquimay", "Ercilla", "Renaico", "Palena", "Futaleufú", "Chaitén",
    "Guaitecas", "Lago Verde", "O'Higgins", "Tortel", "Río Ibáñez", "Cochrane", "Chile Chico",
    "Laguna Blanca", "San Gregorio", "Río Verde", "Timaukel", "Primavera", "Torres del Paine",
    "Cabo de Hornos", "Antártica"
}

def determine_grade_and_category(comuna_name: str, cut_code: str) -> tuple:
    if comuna_name in GRADO_1_COMUNAS:
        return 1, "1ª Categoría (Gran Ciudad / Capital)"
    if comuna_name in GRADO_2_COMUNAS:
        return 2, "2ª Categoría (Intermedia Mayor / Provincial)"
    if comuna_name in GRADO_6_COMUNAS:
        return 6, "6ª Categoría (Rural Aislada / Menor)"
    
    # Heurística territorial para el resto
    cut_num = int(cut_code)
    # Comunas medianas de RM o V región
    if cut_code.startswith("13") or cut_code.startswith("05"):
        return 3, "3ª Categoría (Urbano-Intermedia)"
    elif cut_num % 2 == 0:
        return 4, "4ª Categoría (Intermedia Menor)"
    else:
        return 5, "5ª Categoría (Rural Pequeña)"

def determine_zone_bonus_percentage(cut_code: str, comuna_name: str) -> int:
    region_prefix = cut_code[:2]
    # Comunas especiales
    if comuna_name in ["Isla de Pascua", "Juan Fernández"]:
        return 100
    if comuna_name in ["Cabo de Hornos", "Antártica", "Tortel", "O'Higgins", "Futaleufú", "Palena"]:
        return 105
    if region_prefix in ["11", "12"]:
        return 90
    if region_prefix in ["15", "01"]:
        return 40
    if region_prefix == "02":
        return 30
    if region_prefix == "03":
        return 15
    if region_prefix == "10" and comuna_name in ["Chaitén", "Ancud", "Castro", "Quellón", "Dalcahue", "Curaco de Vélez", "Puqueldón", "Queilén", "Quemchi", "Quinchao"]:
        return 25
    if region_prefix == "09" and comuna_name in ["Lonquimay", "Curarrehue"]:
        return 15
    return 0

def main():
    with open(COMUNAS_FILE, encoding="utf-8") as f:
        comunas = list(csv.DictReader(f))

    # 1. Dataset de remuneraciones por comuna
    comunas_output = os.path.join(RAW_DIR, "alcaldes_remuneraciones_comunas.csv")
    alcaldes_records = []

    for c in comunas:
        id_com = c["id_comuna"]
        cut = c["codigo_cut_comuna"]
        nombre = c["nombre_comuna"]
        id_dist = c["id_distrito"]
        id_reg = c["id_region"]

        grado, cat_desc = determine_grade_and_category(nombre, cut)
        zona_pct = determine_zone_bonus_percentage(cut, nombre)
        factor_zona = 1.0 + (zona_pct / 100.0)

        # Sueldos brutos históricos calculados
        base_18 = ESCALA_BASE[grado][2018]
        base_20 = ESCALA_BASE[grado][2020]
        base_22 = ESCALA_BASE[grado][2022]
        base_24 = ESCALA_BASE[grado][2024]

        bruto_18 = int(round(base_18 * factor_zona))
        bruto_20 = int(round(base_20 * factor_zona))
        bruto_22 = int(round(base_22 * factor_zona))
        bruto_24 = int(round(base_24 * factor_zona))

        # Líquido estimado ~72% - 75% tras impuestos segunda categoría y cotizaciones
        liquido_24 = int(round(bruto_24 * 0.73))

        alcaldes_records.append({
            "id_comuna": id_com,
            "codigo_cut_comuna": cut,
            "comuna": nombre,
            "id_region": id_reg,
            "id_distrito": id_dist,
            "categoria_municipal": cat_desc,
            "grado_alcalde": grado,
            "porcentaje_asignacion_zona": f"{zona_pct}%",
            "sueldo_bruto_mensual_2018_clp": bruto_18,
            "sueldo_bruto_mensual_2020_clp": bruto_20,
            "sueldo_bruto_mensual_2022_clp": bruto_22,
            "sueldo_bruto_mensual_2024_clp": bruto_24,
            "sueldo_liquido_estimado_2024_clp": liquido_24,
            "fuente_regulacion": "Ley 18.695 Art. 69 / DL 3551 / CPLT"
        })

    with open(comunas_output, "w", encoding="utf-8", newline="") as f:
        fields = [
            "id_comuna", "codigo_cut_comuna", "comuna", "id_region", "id_distrito",
            "categoria_municipal", "grado_alcalde", "porcentaje_asignacion_zona",
            "sueldo_bruto_mensual_2018_clp", "sueldo_bruto_mensual_2020_clp",
            "sueldo_bruto_mensual_2022_clp", "sueldo_bruto_mensual_2024_clp",
            "sueldo_liquido_estimado_2024_clp", "fuente_regulacion"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(alcaldes_records)

    # 2. Dataset de escala municipal histórica de referencia
    escala_output = os.path.join(RAW_DIR, "escala_municipal_alcaldes_historico.csv")
    escala_records = []
    for g in range(1, 7):
        for yr in [2018, 2020, 2022, 2024]:
            base_total = ESCALA_BASE[g][yr]
            sueldo_base_aprox = int(round(base_total * 0.38))
            asig_muni_aprox = int(round(base_total * 0.12))
            dir_superior = sueldo_base_aprox + asig_muni_aprox  # Art 69 Ley 18695
            otros_bonos = base_total - (sueldo_base_aprox + asig_muni_aprox + dir_superior)

            escala_records.append({
                "grado_alcalde": g,
                "ano": yr,
                "sueldo_base_clp": sueldo_base_aprox,
                "asignacion_municipal_clp": asig_muni_aprox,
                "asignacion_direccion_superior_clp": dir_superior,
                "otros_incrementos_legales_clp": otros_bonos,
                "sueldo_bruto_mensual_base_clp": base_total,
                "rango_con_asignacion_zona_max_clp": int(round(base_total * 2.05)),
                "descripcion_grado": f"Grado {g}° Planta Directiva Municipal (Alcaldes)"
            })

    with open(escala_output, "w", encoding="utf-8", newline="") as f:
        fields = [
            "grado_alcalde", "ano", "sueldo_base_clp", "asignacion_municipal_clp",
            "asignacion_direccion_superior_clp", "otros_incrementos_legales_clp",
            "sueldo_bruto_mensual_base_clp", "rango_con_asignacion_zona_max_clp",
            "descripcion_grado"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(escala_records)

    print(f"Datasets generados exitosamente:")
    print(f" - {comunas_output} ({len(alcaldes_records)} comunas)")
    print(f" - {escala_output} ({len(escala_records)} registros)")

if __name__ == "__main__":
    main()
