import json
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from tkinter import filedialog
from datetime import datetime
from config.utils import resource_path

def generate_report():
    json_path = resource_path("data/temp_cart.json")
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Dokument Word", "*.docx")],
        title="Zapisz raport jako"
    )
    if not save_path:
        print("Zapis anulowany.")
        return

    doc = Document()

    # Ustaw minimalne marginesy
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(0.3)
    section.right_margin = Inches(0.3)
    total_width_cm = 21.0 - 0.6 * 2  # A4 szerokość - marginesy boczne

    # Czcionka
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(6)

    # Dodajemy dzisiejszą datę przed nazwą firmy
    today = datetime.today().strftime("%d.%m.%Y")
    date_para = doc.add_paragraph()
    date_run = date_para.add_run(f"Świdnica, {today}")
    date_run.font.size = Pt(8)

    # Górny wiersz z nazwą klienta i logo
    top_table = doc.add_table(rows=1, cols=2)

    # Komórka z nazwą klienta
    client_cell = top_table.cell(0, 0)
    client_para = client_cell.paragraphs[0]
    client_run = client_para.add_run(data.get("client_name", "--"))
    client_run.bold = True
    client_run.font.size = Pt(14)  # większy rozmiar czcionki dla nazwy klienta

    # Dodanie dwóch kolejnych linii
    for _ in range(2):
        client_cell.add_paragraph("..........................................................")

    logo_cell = top_table.cell(0, 1)
    logo_para = logo_cell.paragraphs[0]
    logo_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    try:
        logo_para.add_run().add_picture(resource_path("img/logo.png"), width=Inches(2))
    except:
        logo_para.add_run("Brak logo")

    doc.add_paragraph()

    # Tabela danych
    headers = [
        "L.P.", "Typ", "Ø OD", "Ø Chw.", "L [mm]",
        "Ilość ostrzy", "Cięcie", "Ilość szt.",
        "Cena ostrzenia", "Wartość ostrzenia",
        "Powłoka", "Cena powłoki", "Wartość powłoki", "Uwagi"
    ]
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.autofit = False

    # Wyznaczenie szerokości kolumn
    fixed_widths_cm = {
        0: 0.8,
        1: 2.0,
        2: 1.0,
        3: 1.0,
        4: 1.0,
        5: 1.0,
        6: 1.0,
        7: 1.0
    }
    remaining_columns = list(range(8, 14))  # pozostałe
    used_width = sum(fixed_widths_cm.values())
    remaining_width = total_width_cm - used_width
    equal_width = remaining_width / len(remaining_columns)

    column_widths_cm = {}
    column_widths_cm.update(fixed_widths_cm)
    for i in remaining_columns:
        column_widths_cm[i] = equal_width

    # Nagłówki
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Dane
    sum_qty = 0
    sum_sharpening = 0
    sum_coating = 0

    for i, item in enumerate(data['items'], start=1):
        p = item['params']
        qty = item['quantity']
        sharpen = item['sharpening_price']
        coat = item['coating_price']

        val_sharpen = sharpen * qty
        val_coat = coat * qty

        sum_qty += qty
        sum_sharpening += val_sharpen
        sum_coating += val_coat

        row = table.add_row().cells
        values = [
            str(i), p.get("Typ", "-"), p.get("Srednica", "-"),
            p.get("fiChwyt", "-"), p.get("Długość całkowita", "-"),
            p.get("Ilosc ostrzy", "-"), p.get("ciecie", "-"), str(qty),
            f"{sharpen:.2f} PLN", f"{val_sharpen:.2f} PLN",
            p.get("Powloka", "-"), f"{coat:.2f} PLN" if coat else "-",
            f"{val_coat:.2f} PLN" if coat else "-", ""
        ]

        for col, val in enumerate(values):
            cell = row[col]
            para = cell.paragraphs[0]
            para.text = val
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Pusta linia
    table.add_row()

    # Rząd podsumowań
    summary_row = table.add_row().cells
    summary_row[7].text = str(sum_qty)
    summary_row[9].text = f"{sum_sharpening:.2f} PLN"
    summary_row[12].text = f"{sum_coating:.2f} PLN"

    for i in [7, 9, 12]:
        summary_row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Rząd łącznej sumy
    total_row = table.add_row().cells
    total_label_cell = total_row[11]
    total_label_cell.text = "Suma:"
    total_label_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    total_value_cell = total_row[12]
    total_value_cell.text = f"{sum_sharpening + sum_coating:.2f} PLN"
    total_value_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Ustawienia szerokości kolumn
    for i, col in enumerate(table.columns):
        width_cm = column_widths_cm.get(i, 1.5)  # Domyślna szerokość 1.5 cm, jeśli nie określono
        try:
            col.width = Inches(width_cm / 2.54)  # Ustaw szerokość kolumny, a nie pojedynczych komórek
        except Exception as e:
            print(f"Błąd przy ustawianiu szerokości kolumny {i}: {str(e)}")

    doc.save(save_path)
    print(f"Raport zapisany: {save_path}")
