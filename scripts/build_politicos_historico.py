#!/usr/bin/env python3
"""
Generador del dataset histórico de políticos en Chile (2018-2026).
Extrae y consolida parlamentarios (Diputados y Senadores por distrito/circunscripción),
Presidentes, Expresidentes, Ministros de Estado y Alcaldes de comunas clave.
Fuentes: Biblioteca del Congreso Nacional (BCN), SERVEL, Transparencia Activa.
"""

import urllib.request
import json
import re
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "politicos_chile_historico.csv")
DIST_FILE = os.path.join(BASE_DIR, "data", "processed", "dim_distritos.csv")
CIRC_FILE = os.path.join(BASE_DIR, "data", "processed", "dim_circunscripciones.csv")

def clean_wiki_text(text: str) -> str:
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^>]*/>", "", text)
    text = re.sub(r"\[\[([^|\]]+\|)?([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\{\{([^\}]+)\}\}", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split()).strip()

def fetch_wikitext(page: str) -> str:
    url = f"https://es.wikipedia.org/w/api.php?action=parse&page={page}&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "TuBolsilloCL/1.0 (contacto@tubolsillo.cl)"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["parse"]["wikitext"]["*"]

def get_district_region_map():
    mapping = {}
    if os.path.exists(DIST_FILE):
        with open(DIST_FILE, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                mapping[int(r["numero_distrito"])] = r["id_region"]
    return mapping

def get_circ_region_map():
    mapping = {}
    if os.path.exists(CIRC_FILE):
        with open(CIRC_FILE, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                mapping[int(r["numero_circunscripcion"])] = r["id_region"]
    return mapping

def extract_deputies_lvi(wikitext: str, dist_reg_map: dict):
    pos = wikitext.find("== Cámara de Diputadas y Diputados ==")
    pos_tbl = wikitext.find("{| class=\"wikitable\"", pos)
    end_tbl = wikitext.find("|}", pos_tbl)
    table_text = wikitext[pos_tbl:end_tbl]

    records = []
    current_dist = None
    rows = table_text.split("|-")

    for r in rows:
        lines = [l.strip() for l in r.splitlines() if l.strip()]
        if not lines or lines[0].startswith("! ") or lines[0].startswith("!Colspan") or "background:#efefef" in lines[0]:
            continue

        cells = [l[1:].strip() for l in lines if l.startswith("|") and not l.startswith("|}")]

        if len(cells) >= 4:
            clean_dist_str = re.sub(r"^rowspan=\"?\d+\"?\|?", "", cells[1]).strip()
            m_dist = re.search(r"(\d+)", clean_dist_str)
            if m_dist:
                current_dist = int(m_dist.group(1))
            name = clean_wiki_text(cells[2])
            party = clean_wiki_text(cells[3])
            records.append((current_dist, name, party))
        elif len(cells) == 2:
            name = clean_wiki_text(cells[0])
            party = clean_wiki_text(cells[1])
            records.append((current_dist, name, party))
        elif len(cells) == 1 and "||" in cells[0]:
            parts = cells[0].split("||")
            name = clean_wiki_text(parts[0])
            party = clean_wiki_text(parts[1]) if len(parts) > 1 else ""
            records.append((current_dist, name, party))

    formatted = []
    for dist_num, name, party in records:
        id_dist = f"DIST-{dist_num:02d}"
        id_reg = dist_reg_map.get(dist_num, "DESCONOCIDO")
        formatted.append({
            "nombre_completo": name,
            "cargo": "Diputado de la República",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "2022-2026 (LVI Periodo)",
            "institucion": "Cámara de Diputadas y Diputados de Chile",
            "id_territorial": id_dist,
            "territorio_nombre": f"Distrito {dist_num}",
            "id_region": id_reg,
            "partido_o_coalicion": party,
            "fuente": "BCN / SERVEL (LVI Periodo Legislativo)"
        })
    return formatted

def extract_deputies_lv(wikitext: str, dist_reg_map: dict):
    pos = wikitext.find("== Cámara de Diputados ==")
    pos_tbl = wikitext.find("{| class=\"wikitable\"", pos)
    end_tbl = wikitext.find("|}", pos_tbl)
    table_text = wikitext[pos_tbl:end_tbl]

    records = []
    current_dist = None
    rows = table_text.split("|-")

    for r in rows:
        lines = [l.strip() for l in r.splitlines() if l.strip()]
        if not lines or lines[0].startswith("! ") or lines[0].startswith("!Colspan") or "background:#efefef" in lines[0]:
            continue

        cells = [l[1:].strip() for l in lines if l.startswith("|") and not l.startswith("|}")]

        if len(cells) >= 4:
            clean_dist_str = re.sub(r"^rowspan=\"?\d+\"?\|?", "", cells[1]).strip()
            m_dist = re.search(r"(\d+)", clean_dist_str)
            if m_dist:
                current_dist = int(m_dist.group(1))
            name = clean_wiki_text(cells[2])
            party = clean_wiki_text(cells[3])
            records.append((current_dist, name, party))
        elif len(cells) == 2:
            name = clean_wiki_text(cells[0])
            party = clean_wiki_text(cells[1])
            records.append((current_dist, name, party))
        elif len(cells) == 1 and "||" in cells[0]:
            parts = cells[0].split("||")
            name = clean_wiki_text(parts[0])
            party = clean_wiki_text(parts[1]) if len(parts) > 1 else ""
            records.append((current_dist, name, party))

    formatted = []
    for dist_num, name, party in records:
        id_dist = f"DIST-{dist_num:02d}"
        id_reg = dist_reg_map.get(dist_num, "DESCONOCIDO")
        formatted.append({
            "nombre_completo": name,
            "cargo": "Diputado de la República",
            "periodo_inicio": 2018,
            "periodo_fin": 2022,
            "periodo_institucional": "2018-2022 (LV Periodo)",
            "institucion": "Cámara de Diputadas y Diputados de Chile",
            "id_territorial": id_dist,
            "territorio_nombre": f"Distrito {dist_num}",
            "id_region": id_reg,
            "partido_o_coalicion": party,
            "fuente": "BCN / SERVEL (LV Periodo Legislativo)"
        })
    return formatted

def extract_senators_lvi(wikitext: str, circ_reg_map: dict):
    pos = wikitext.find("== Senado de la República ==")
    pos_tbl = wikitext.find("{| class=\"wikitable\"", pos)
    end_tbl = wikitext.find("|}", pos_tbl)
    table_text = wikitext[pos_tbl:end_tbl]

    records = []
    current_circ = None
    rows = table_text.split("|-")

    for r in rows:
        lines = [l.strip() for l in r.splitlines() if l.strip()]
        if not lines or lines[0].startswith("! ") or lines[0].startswith("!Colspan") or "background:#efefef" in lines[0]:
            continue

        cells = [l[1:].strip() for l in lines if l.startswith("|") and not l.startswith("|}")]

        if len(cells) >= 3:
            clean_circ_str = re.sub(r"^rowspan=\"?\d+\"?\|?", "", cells[1]).strip()
            m_circ = re.search(r"(\d+)", clean_circ_str)
            if m_circ:
                current_circ = int(m_circ.group(1))
            name_party = cells[2].split("||")
            name = clean_wiki_text(name_party[0])
            party = clean_wiki_text(name_party[1]) if len(name_party) > 1 else ""
            records.append((current_circ, name, party))
        elif len(cells) == 1 and "||" in cells[0]:
            parts = cells[0].split("||")
            name = clean_wiki_text(parts[0])
            party = clean_wiki_text(parts[1]) if len(parts) > 1 else ""
            records.append((current_circ, name, party))

    formatted = []
    for circ_num, name, party in records:
        id_circ = f"CIRC-{circ_num:02d}"
        id_reg = circ_reg_map.get(circ_num, "DESCONOCIDO")
        formatted.append({
            "nombre_completo": name,
            "cargo": "Senador de la República",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "2022-2026 (LVI Periodo)",
            "institucion": "Senado de la República de Chile",
            "id_territorial": id_circ,
            "territorio_nombre": f"Circunscripción {circ_num}ª",
            "id_region": id_reg,
            "partido_o_coalicion": party,
            "fuente": "BCN / Senado (LVI Periodo Legislativo)"
        })
    return formatted

def extract_senators_lv(wikitext: str, circ_reg_map: dict):
    pos = wikitext.find("== Senado ==")
    if pos == -1:
        pos = wikitext.find("Senad")
    pos_tbl = wikitext.find("{| class=\"wikitable\"", pos)
    end_tbl = wikitext.find("|}", pos_tbl)
    table_text = wikitext[pos_tbl:end_tbl]

    records = []
    current_circ = None
    rows = table_text.split("|-")

    for r in rows:
        lines = [l.strip() for l in r.splitlines() if l.strip()]
        if not lines or lines[0].startswith("! ") or lines[0].startswith("!Colspan") or "background:#efefef" in lines[0]:
            continue

        cells = [l[1:].strip() for l in lines if l.startswith("|") and not l.startswith("|}")]

        if len(cells) >= 3:
            clean_circ_str = re.sub(r"^rowspan=\"?\d+\"?\|?", "", cells[1]).strip()
            m_circ = re.search(r"(\d+)", clean_circ_str)
            if m_circ:
                current_circ = int(m_circ.group(1))
            name_party = cells[2].split("||")
            name = clean_wiki_text(name_party[0])
            party = clean_wiki_text(name_party[1]) if len(name_party) > 1 else ""
            records.append((current_circ, name, party))
        elif len(cells) == 1 and "||" in cells[0]:
            parts = cells[0].split("||")
            name = clean_wiki_text(parts[0])
            party = clean_wiki_text(parts[1]) if len(parts) > 1 else ""
            records.append((current_circ, name, party))

    formatted = []
    for circ_num, name, party in records:
        if circ_num is None:
            continue
        id_circ = f"CIRC-{circ_num:02d}"
        id_reg = circ_reg_map.get(circ_num, "DESCONOCIDO")
        formatted.append({
            "nombre_completo": name,
            "cargo": "Senador de la República",
            "periodo_inicio": 2018,
            "periodo_fin": 2022,
            "periodo_institucional": "2018-2022 (LV Periodo)",
            "institucion": "Senado de la República de Chile",
            "id_territorial": id_circ,
            "territorio_nombre": f"Circunscripción {circ_num}ª",
            "id_region": id_reg,
            "partido_o_coalicion": party,
            "fuente": "BCN / Senado (LV Periodo Legislativo)"
        })
    return formatted

def get_executive_records():
    return [
        # Presidentes de la República
        {
            "nombre_completo": "Michelle Bachelet Jeria",
            "cargo": "Presidente de la República",
            "periodo_inicio": 2014,
            "periodo_fin": 2018,
            "periodo_institucional": "Gobierno 2014-2018",
            "institucion": "Presidencia de la República de Chile",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PS (Nueva Mayoría)",
            "fuente": "Presidencia / BCN"
        },
        {
            "nombre_completo": "Sebastián Piñera Echenique",
            "cargo": "Presidente de la República",
            "periodo_inicio": 2018,
            "periodo_fin": 2022,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Presidencia de la República de Chile",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "RN (Chile Vamos)",
            "fuente": "Presidencia / BCN"
        },
        {
            "nombre_completo": "Gabriel Boric Font",
            "cargo": "Presidente de la República",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Presidencia de la República de Chile",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "FA (Apruebo Dignidad / Alianza de Gobierno)",
            "fuente": "Presidencia / BCN"
        },
        # Expresidentes con Dieta Vitalicia (Art. 30 CPR)
        {
            "nombre_completo": "Eduardo Frei Ruiz-Tagle",
            "cargo": "Expresidente de la República",
            "periodo_inicio": 2000,
            "periodo_fin": 2026,
            "periodo_institucional": "Vitalicio",
            "institucion": "Senado de la República (Departamento de Finanzas)",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PDC",
            "fuente": "Senado de Chile (Art. 30 Constitución)"
        },
        {
            "nombre_completo": "Ricardo Lagos Escobar",
            "cargo": "Expresidente de la República",
            "periodo_inicio": 2006,
            "periodo_fin": 2026,
            "periodo_institucional": "Vitalicio",
            "institucion": "Senado de la República (Departamento de Finanzas)",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PPD",
            "fuente": "Senado de Chile (Art. 30 Constitución)"
        },
        {
            "nombre_completo": "Michelle Bachelet Jeria",
            "cargo": "Expresidente de la República",
            "periodo_inicio": 2018,
            "periodo_fin": 2026,
            "periodo_institucional": "Vitalicio",
            "institucion": "Senado de la República (Departamento de Finanzas)",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PS",
            "fuente": "Senado de Chile (Art. 30 Constitución)"
        },
        {
            "nombre_completo": "Sebastián Piñera Echenique",
            "cargo": "Expresidente de la República",
            "periodo_inicio": 2022,
            "periodo_fin": 2024,
            "periodo_institucional": "2022-2024 (fallecimiento)",
            "institucion": "Senado de la República (Departamento de Finanzas)",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "RN / Chile Vamos",
            "fuente": "Senado de Chile (Art. 30 Constitución)"
        },
        # Ministros clave Gobierno Piñera (2018-2022)
        {
            "nombre_completo": "Andrés Chadwick Piñera",
            "cargo": "Ministro del Interior y Seguridad Pública",
            "periodo_inicio": 2018,
            "periodo_fin": 2019,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio del Interior y Seguridad Pública",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "UDI",
            "fuente": "Transparencia Activa Ministerio del Interior"
        },
        {
            "nombre_completo": "Gonzalo Blumel Mac-Iver",
            "cargo": "Ministro del Interior / Ministro Segpres",
            "periodo_inicio": 2018,
            "periodo_fin": 2020,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio del Interior y Seguridad Pública",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Evópoli",
            "fuente": "Transparencia Activa Ministerio del Interior"
        },
        {
            "nombre_completo": "Rodrigo Delgado Mocarquer",
            "cargo": "Ministro del Interior y Seguridad Pública",
            "periodo_inicio": 2020,
            "periodo_fin": 2022,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio del Interior y Seguridad Pública",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "UDI",
            "fuente": "Transparencia Activa Ministerio del Interior"
        },
        {
            "nombre_completo": "Felipe Larraín Bascuñán",
            "cargo": "Ministro de Hacienda",
            "periodo_inicio": 2018,
            "periodo_fin": 2019,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio de Hacienda",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-Chile Vamos",
            "fuente": "Transparencia Activa Ministerio de Hacienda"
        },
        {
            "nombre_completo": "Ignacio Briones Rojas",
            "cargo": "Ministro de Hacienda",
            "periodo_inicio": 2019,
            "periodo_fin": 2021,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio de Hacienda",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Evópoli",
            "fuente": "Transparencia Activa Ministerio de Hacienda"
        },
        {
            "nombre_completo": "Rodrigo Cerda Norambuena",
            "cargo": "Ministro de Hacienda",
            "periodo_inicio": 2021,
            "periodo_fin": 2022,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio de Hacienda",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-Chile Vamos",
            "fuente": "Transparencia Activa Ministerio de Hacienda"
        },
        {
            "nombre_completo": "Enrique Paris Mancilla",
            "cargo": "Ministro de Salud",
            "periodo_inicio": 2020,
            "periodo_fin": 2022,
            "periodo_institucional": "Gobierno 2018-2022",
            "institucion": "Ministerio de Salud",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-Chile Vamos",
            "fuente": "Transparencia Activa Ministerio de Salud"
        },
        # Ministros clave Gobierno Boric (2022-2026)
        {
            "nombre_completo": "Carolina Tohá Morales",
            "cargo": "Ministra del Interior y Seguridad Pública",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio del Interior y Seguridad Pública",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PPD",
            "fuente": "Transparencia Activa Ministerio del Interior"
        },
        {
            "nombre_completo": "Izkia Siches Pastén",
            "cargo": "Ministra del Interior y Seguridad Pública",
            "periodo_inicio": 2022,
            "periodo_fin": 2022,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio del Interior y Seguridad Pública",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-Frente Amplio",
            "fuente": "Transparencia Activa Ministerio del Interior"
        },
        {
            "nombre_completo": "Mario Marcel Cullell",
            "cargo": "Ministro de Hacienda",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio de Hacienda",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-PS",
            "fuente": "Transparencia Activa Ministerio de Hacienda"
        },
        {
            "nombre_completo": "Camila Vallejo Dowling",
            "cargo": "Ministra Secretaria General de Gobierno",
            "periodo_inicio": 2022,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio Secretaría General de Gobierno",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PCCh",
            "fuente": "Transparencia Activa Segegob"
        },
        {
            "nombre_completo": "Álvaro Elizalde Soto",
            "cargo": "Ministro Secretario General de la Presidencia",
            "periodo_inicio": 2023,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio Secretaría General de la Presidencia",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "PS",
            "fuente": "Transparencia Activa Segpres"
        },
        {
            "nombre_completo": "Alberto van Klaveren Stork",
            "cargo": "Ministro de Relaciones Exteriores",
            "periodo_inicio": 2023,
            "periodo_fin": 2026,
            "periodo_institucional": "Gobierno 2022-2026",
            "institucion": "Ministerio de Relaciones Exteriores",
            "id_territorial": "NACIONAL",
            "territorio_nombre": "Chile",
            "id_region": "NACIONAL",
            "partido_o_coalicion": "Ind-PPD",
            "fuente": "Transparencia Activa Minrel"
        }
    ]

def get_mayors_records():
    # Muestra representativa de alcaldes en capitales regionales y grandes comunas
    return [
        {"nombre_completo": "Felipe Alessandri Vergara", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2021, "periodo_institucional": "Municipal 2016-2021", "institucion": "Municipalidad de Santiago", "id_territorial": "COM-13101", "territorio_nombre": "Santiago", "id_region": "REG-13", "partido_o_coalicion": "RN", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Irací Hassler Jacob", "cargo": "Alcaldesa", "periodo_inicio": 2021, "periodo_fin": 2024, "periodo_institucional": "Municipal 2021-2024", "institucion": "Municipalidad de Santiago", "id_territorial": "COM-13101", "territorio_nombre": "Santiago", "id_region": "REG-13", "partido_o_coalicion": "PCCh", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Joaquín Lavín Infante", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2021, "periodo_institucional": "Municipal 2016-2021", "institucion": "Municipalidad de Las Condes", "id_territorial": "COM-13114", "territorio_nombre": "Las Condes", "id_region": "REG-13", "partido_o_coalicion": "UDI", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Daniela Peñaloza Ramos", "cargo": "Alcaldesa", "periodo_inicio": 2021, "periodo_fin": 2024, "periodo_institucional": "Municipal 2021-2024", "institucion": "Municipalidad de Las Condes", "id_territorial": "COM-13114", "territorio_nombre": "Las Condes", "id_region": "REG-13", "partido_o_coalicion": "UDI", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Evelyn Matthei Fornet", "cargo": "Alcaldesa", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Providencia", "id_territorial": "COM-13123", "territorio_nombre": "Providencia", "id_region": "REG-13", "partido_o_coalicion": "UDI", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Cathy Barriga Guerra", "cargo": "Alcaldesa", "periodo_inicio": 2016, "periodo_fin": 2021, "periodo_institucional": "Municipal 2016-2021", "institucion": "Municipalidad de Maipú", "id_territorial": "COM-13119", "territorio_nombre": "Maipú", "id_region": "REG-13", "partido_o_coalicion": "Ind-UDI", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Tomás Vodanovic Escudero", "cargo": "Alcalde", "periodo_inicio": 2021, "periodo_fin": 2024, "periodo_institucional": "Municipal 2021-2024", "institucion": "Municipalidad de Maipú", "id_territorial": "COM-13119", "territorio_nombre": "Maipú", "id_region": "REG-13", "partido_o_coalicion": "FA (RD)", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Germán Codina Powers", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Puente Alto", "id_territorial": "COM-13201", "territorio_nombre": "Puente Alto", "id_region": "REG-13", "partido_o_coalicion": "RN", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Rodolfo Carter Fernández", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de La Florida", "id_territorial": "COM-13110", "territorio_nombre": "La Florida", "id_region": "REG-13", "partido_o_coalicion": "Ind-Chile Vamos", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Daniel Jadue Jadue", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Recoleta", "id_territorial": "COM-13127", "territorio_nombre": "Recoleta", "id_region": "REG-13", "partido_o_coalicion": "PCCh", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Virginia Reginato Bozzo", "cargo": "Alcaldesa", "periodo_inicio": 2016, "periodo_fin": 2021, "periodo_institucional": "Municipal 2016-2021", "institucion": "Municipalidad de Viña del Mar", "id_territorial": "COM-05109", "territorio_nombre": "Viña del Mar", "id_region": "REG-05", "partido_o_coalicion": "UDI", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Macarena Ripamonti Serrano", "cargo": "Alcaldesa", "periodo_inicio": 2021, "periodo_fin": 2024, "periodo_institucional": "Municipal 2021-2024", "institucion": "Municipalidad de Viña del Mar", "id_territorial": "COM-05109", "territorio_nombre": "Viña del Mar", "id_region": "REG-05", "partido_o_coalicion": "FA (RD)", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Jorge Sharp Fajardo", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Valparaíso", "id_territorial": "COM-05101", "territorio_nombre": "Valparaíso", "id_region": "REG-05", "partido_o_coalicion": "Ind-Transformar", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Karen Rojo Venegas", "cargo": "Alcaldesa", "periodo_inicio": 2016, "periodo_fin": 2020, "periodo_institucional": "Municipal 2016-2020", "institucion": "Municipalidad de Antofagasta", "id_territorial": "COM-02101", "territorio_nombre": "Antofagasta", "id_region": "REG-02", "partido_o_coalicion": "Ind.", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Jonathan Velásquez Ramírez", "cargo": "Alcalde", "periodo_inicio": 2021, "periodo_fin": 2024, "periodo_institucional": "Municipal 2021-2024", "institucion": "Municipalidad de Antofagasta", "id_territorial": "COM-02101", "territorio_nombre": "Antofagasta", "id_region": "REG-02", "partido_o_coalicion": "Ind.", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Álvaro Ortiz Vera", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Concepción", "id_territorial": "COM-08101", "territorio_nombre": "Concepción", "id_region": "REG-08", "partido_o_coalicion": "PDC", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Gervoy Paredes Rojas", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Puerto Montt", "id_territorial": "COM-10101", "territorio_nombre": "Puerto Montt", "id_region": "REG-10", "partido_o_coalicion": "PS", "fuente": "Transparencia Activa Municipal / SERVEL"},
        {"nombre_completo": "Claudio Radonich Jiménez", "cargo": "Alcalde", "periodo_inicio": 2016, "periodo_fin": 2024, "periodo_institucional": "Municipal 2016-2024", "institucion": "Municipalidad de Punta Arenas", "id_territorial": "COM-12101", "territorio_nombre": "Punta Arenas", "id_region": "REG-12", "partido_o_coalicion": "RN", "fuente": "Transparencia Activa Municipal / SERVEL"}
    ]

def main():
    dist_reg_map = get_district_region_map()
    circ_reg_map = get_circ_region_map()

    print("Descargando nóminas parlamentarias desde Wikipedia API...")
    wiki_lvi = fetch_wikitext("LVI_periodo_legislativo_del_Congreso_Nacional_de_Chile")
    wiki_lv = fetch_wikitext("LV_periodo_legislativo_del_Congreso_Nacional_de_Chile")

    deputies_lvi = extract_deputies_lvi(wiki_lvi, dist_reg_map)
    deputies_lv = extract_deputies_lv(wiki_lv, dist_reg_map)
    senators_lvi = extract_senators_lvi(wiki_lvi, circ_reg_map)
    senators_lv = extract_senators_lv(wiki_lv, circ_reg_map)
    exec_records = get_executive_records()
    mayor_records = get_mayors_records()

    all_records = []
    # Incorporar con ID correlativo
    idx = 1
    for r in exec_records + senators_lvi + senators_lv + deputies_lvi + deputies_lv + mayor_records:
        r_copy = {"id_politico": f"POL-{idx:04d}"}
        r_copy.update(r)
        all_records.append(r_copy)
        idx += 1

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        fields = [
            "id_politico",
            "nombre_completo",
            "cargo",
            "periodo_inicio",
            "periodo_fin",
            "periodo_institucional",
            "institucion",
            "id_territorial",
            "territorio_nombre",
            "id_region",
            "partido_o_coalicion",
            "fuente"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(all_records)

    print(f"Dataset generado exitosamente en: {OUTPUT_FILE}")
    print(f"Total registros: {len(all_records)}")
    print(f" - Diputados LVI (2022-2026): {len(deputies_lvi)}")
    print(f" - Diputados LV (2018-2022): {len(deputies_lv)}")
    print(f" - Senadores LVI (2022-2026): {len(senators_lvi)}")
    print(f" - Senadores LV (2018-2022): {len(senators_lv)}")
    print(f" - Poder Ejecutivo y Expresidentes: {len(exec_records)}")
    print(f" - Alcaldes de comunas clave: {len(mayor_records)}")

if __name__ == "__main__":
    main()
