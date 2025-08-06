import json
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from tkinter import filedialog
from datetime import datetime
from config.utils import resource_path
from config.client_utils import get_client_data


def generate_report(client_name, main_app):
    json_path = resource_path("data/temp_cart.json")
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    # Pobierz dane klienta za pomocą get_client_data
    client_data = get_client_data(client_name.get(), main_app)

    # Przygotuj dane klienta, używając "......." dla pustych pól
    client_name_str = client_name.get().strip() if client_name.get().strip() and client_name.get() != "- -" else "......."
    client_address = client_data.get("address", "").strip() if client_data else "......."
    client_contact = client_data.get("contact", "").strip() if client_data else "......."

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
    style.font.size = Pt(14)  # Domyślna czcionka dla dokumentu

    # Dodajemy dzisiejszą datę przed nazwą firmy
    today = datetime.today().strftime("%d.%m.%Y")
    date_para = doc.add_paragraph()
    date_run = date_para.add_run(f"Świdnica, {today}")
    date_run.font.size = Pt(8)
    date_para.paragraph_format.space_after = Pt(8)  # Odstęp po dacie

    # Górny wiersz z nazwą klienta, adresem, kontaktem i logo
    top_table = doc.add_table(rows=1, cols=2)

    # Komórka z nazwą klienta, adresem i kontaktem
    client_cell = top_table.cell(0, 0)
    client_para = client_cell.paragraphs[0]
    client_run = client_para.add_run(client_name_str)
    client_run.bold = True
    client_run.font.size = Pt(14)
    client_para.paragraph_format.space_after = Pt(2)  # Minimalny odstęp po nazwie

    # Dodanie linii z adresem i kontaktem
    address_para = client_cell.add_paragraph(client_address)
    address_para.runs[0].font.size = Pt(14)
    address_para.paragraph_format.space_after = Pt(2)  # Minimalny odstęp po adresie

    contact_para = client_cell.add_paragraph(client_contact)
    contact_para.runs[0].font.size = Pt(14)
    contact_para.paragraph_format.space_after = Pt(2)  # Minimalny odstęp po kontakcie

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
        cell.paragraphs[0].runs[0].font.size = Pt(6)  # Czcionka nagłówków tabeli na 6 pt

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
            f"{val_coat:.2f} PLN" if coat else "-", p.get("Uwagi", "-")
        ]

        for col, val in enumerate(values):
            cell = row[col]
            para = cell.paragraphs[0]
            para.text = val
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.runs[0].font.size = Pt(6)  # Czcionka danych tabeli na 6 pt

    # Pusta linia
    table.add_row()

    # Rząd podsumowań
    summary_row = table.add_row().cells
    summary_row[7].text = str(sum_qty)
    summary_row[9].text = f"{sum_sharpening:.2f} PLN"
    summary_row[12].text = f"{sum_coating:.2f} PLN"

    for i in [7, 9, 12]:
        summary_row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        summary_row[i].paragraphs[0].runs[0].font.size = Pt(6)

    # Rząd łącznej sumy
    total_row = table.add_row().cells
    total_label_cell = total_row[11]
    total_label_cell.text = "Suma:"
    total_label_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    total_label_cell.paragraphs[0].runs[0].font.size = Pt(6)

    total_value_cell = total_row[12]
    total_value_cell.text = f"{sum_sharpening + sum_coating:.2f} PLN"
    total_value_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    total_value_cell.paragraphs[0].runs[0].font.size = Pt(6)

    # Ustawienia szerokości kolumn
    for i, col in enumerate(table.columns):
        width_cm = column_widths_cm.get(i, 1.5)  # Domyślna szerokość 1.5 cm, jeśli nie określono
        try:
            col.width = Inches(width_cm / 2.54)  # Ustaw szerokość kolumny
        except Exception as e:
            print(f"Błąd przy ustawianiu szerokości kolumny {i}: {str(e)}")

    doc.save(save_path)
    print(f"Raport zapisany: {save_path}")