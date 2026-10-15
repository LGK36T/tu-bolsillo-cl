#!/usr/bin/env python3
"""
Script de extracción de la División Político-Electoral de Chile desde la BCN.
Fuente: Biblioteca del Congreso Nacional de Chile (BCN) - SIIT
URL: https://www.bcn.cl/siit/nuestropais/divisionelectoral/index.htm
"""

import urllib.request
import re
from html.parser import HTMLParser
import csv
import os

SOURCE_URL = "https://www.bcn.cl/siit/nuestropais/divisionelectoral/index.htm"
OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "raw", "division_politico_electoral.csv"
)

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="ignore")

class Cell:
    def __init__(self, tag, attrs, text, idcom=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.text = text
        self.idcom = idcom
        self.rowspan = int(self.attrs.get("rowspan", 1))
        self.colspan = int(self.attrs.get("colspan", 1))

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.current_row = None
        self.rows = []
        self.cell_tag = None
        self.cell_attrs = []
        self.cell_text = []
        self.current_idcom = None

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.current_row = []
        elif tag in ["td", "th"] and self.in_tbody:
            self.cell_tag = tag
            self.cell_attrs = attrs
            self.cell_text = []
            self.current_idcom = None
        elif tag == "a" and self.cell_tag is not None:
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            m = re.search(r"idcom=(\d+)", href)
            if m:
                self.current_idcom = m.group(1)

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_tbody = False
        elif tag == "tr" and self.in_tbody:
            if self.current_row is not None and len(self.current_row) > 0:
                self.rows.append(self.current_row)
            self.current_row = None
        elif tag in ["td", "th"] and self.in_tbody:
            txt = " ".join("".join(self.cell_text).split())
            if self.current_row is not None:
                self.current_row.append(
                    Cell(self.cell_tag, self.cell_attrs, txt, self.current_idcom)
                )
            self.cell_tag = None
            self.current_idcom = None

    def handle_data(self, data):
        if self.cell_tag is not None:
            self.cell_text.append(data)

def parse_circunscripcion(text: str):
    m = re.search(r"(\d+ª)\s*(?:(\d+)\s*Senadores)?", text, re.IGNORECASE)
    if m:
        circ = m.group(1)
        senadores = m.group(2) if m.group(2) else ""
        return circ, senadores
    return text, ""

def parse_distrito(text: str):
    m = re.search(r"(?:N°\s*)?(\d+)\s*(?:(\d+)\s*Diputados)?", text, re.IGNORECASE)
    if m:
        dist = f"Distrito {m.group(1)}"
        diputados = m.group(2) if m.group(2) else ""
        return dist, diputados
    return text, ""

def main():
    print(f"Descargando datos desde: {SOURCE_URL}...")
    html = fetch_html(SOURCE_URL)

    match = re.search(
        r'<table class="table table-bordered table-condensed RS_CONTENT">(.*?)</table>',
        html,
        re.DOTALL | re.IGNORECASE
    )
    if not match:
        raise ValueError("No se encontró la tabla de división electoral en la página.")

    table_content = match.group(1)
    parser = TableParser()
    parser.feed(table_content)

    num_rows = len(parser.rows)
    num_cols = 4
    grid = [[None for _ in range(num_cols)] for _ in range(num_rows)]

    for r_idx, row in enumerate(parser.rows):
        c_idx = 0
        for cell in row:
            while c_idx < num_cols and grid[r_idx][c_idx] is not None:
                c_idx += 1
            if c_idx >= num_cols:
                break
            for r_offset in range(cell.rowspan):
                for c_offset in range(cell.colspan):
                    target_r = r_idx + r_offset
                    target_c = c_idx + c_offset
                    if target_r < num_rows and target_c < num_cols:
                        grid[target_r][target_c] = cell
            c_idx += cell.colspan

    # Generar registros CSV
    records = []
    for r_idx in range(num_rows):
        reg_cell = grid[r_idx][0]
        circ_cell = grid[r_idx][1]
        dist_cell = grid[r_idx][2]
        com_cell = grid[r_idx][3]

        region = reg_cell.text if reg_cell else ""
        circ_raw = circ_cell.text if circ_cell else ""
        dist_raw = dist_cell.text if dist_cell else ""
        comuna = com_cell.text if com_cell else ""
        raw_idcom = com_cell.idcom if com_cell else ""

        circunscripcion, senadores = parse_circunscripcion(circ_raw)
        distrito, diputados = parse_distrito(dist_raw)

        # Código Único Territorial (CUT) a 5 dígitos
        codigo_cut = raw_idcom.zfill(5) if raw_idcom else ""

        records.append({
            "region": region,
            "circunscripcion": circunscripcion,
            "senadores_circunscripcion": senadores,
            "distrito": distrito,
            "diputados_distrito": diputados,
            "comuna": comuna,
            "codigo_comuna_cut": codigo_cut
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "region",
            "circunscripcion",
            "senadores_circunscripcion",
            "distrito",
            "diputados_distrito",
            "comuna",
            "codigo_comuna_cut"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Exportación completada exitosamente.")
    print(f"Total registros: {len(records)}")
    print(f"Archivo guardado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
