import json
from docx import Document
from docx.shared import Pt
from tkinter import filedialog
from datetime import datetime

def generate_report():
    # Wczytaj dane z pliku JSON
    json_path = "data/temp_cart.json"
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    # Otwórz okno wyboru ścieżki zapisu
    save_path = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Dokument Word", "*.docx")],
        title="Zapisz raport jako"
    )

    if not save_path:
        print("Zapis anulowany przez użytkownika.")
        return

    doc = Document()

    # Styl domyślny
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10)

    # Nagłówek
    doc.add_heading('Wycena', 0)
    doc.add_paragraph(f'Data: {datetime.today().strftime("%d.%m.%Y")}')
    doc.add_paragraph(f'Nazwa klienta: {data.get("client_name", "-")}')
    doc.add_paragraph("")  # odstęp

    # Tabela - nagłówki
    headers = [
        "L.P.", "Typ", "Średnica", "Ø Trzonka", "L [mm]", "Ilość ostrzy", "Cięcie",
        "Ilość szt.", "Cena ostrzenia", "Wartość ostrzenia",
        "Powłoka", "Cena powłoki", "Wartość powłoki", "Cena cięcia", "Wartość cięcia", "Uwagi"
    ]

    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h

    # Sumy
    sum_sharpening = 0
    sum_cutting = 0
    sum_coating = 0

    # Tabela - dane
    for i, item in enumerate(data['items'], start=1):
        p = item['params']
        qty = item['quantity']
        sharpening = item['sharpening_price']
        cutting = item['cutting_price']
        coating = item['coating_price']

        total_sharpening = sharpening * qty
        total_cutting = cutting * qty
        total_coating = coating * qty

        sum_sharpening += total_sharpening
        sum_cutting += total_cutting
        sum_coating += total_coating

        row_cells = table.add_row().cells
        row_cells[0].text = str(i)
        row_cells[1].text = p.get("Typ", "-")
        row_cells[2].text = p.get("Srednica", "-")
        row_cells[3].text = p.get("fiChwyt", "-")
        row_cells[4].text = p.get("Długość całkowita", "-") if "Długość całkowita" in p else "-"
        row_cells[5].text = p.get("Ilosc ostrzy", "-")
        row_cells[6].text = p.get("ciecie", "-")
        row_cells[7].text = str(qty)
        row_cells[8].text = f"{sharpening:.2f} PLN"
        row_cells[9].text = f"{total_sharpening:.2f} PLN"
        row_cells[10].text = p.get("Powloka", "-")
        row_cells[11].text = f"{coating:.2f} PLN" if coating else "-"
        row_cells[12].text = f"{total_coating:.2f} PLN" if coating else "-"
        row_cells[13].text = f"{cutting:.2f} PLN" if cutting else "-"
        row_cells[14].text = f"{total_cutting:.2f} PLN" if cutting else "-"
        row_cells[15].text = ""  # Placeholder na uwagi

    doc.add_paragraph("")  # odstęp

    # Podsumowanie
    doc.add_paragraph("Podsumowanie kosztów:")
    doc.add_paragraph(f"• Suma ostrzenia: {sum_sharpening:.2f} PLN")
    doc.add_paragraph(f"• Suma cięcia: {sum_cutting:.2f} PLN")
    doc.add_paragraph(f"• Suma powlekania: {sum_coating:.2f} PLN")
    doc.add_paragraph(f"• Wartość całkowita: {sum_sharpening + sum_cutting + sum_coating:.2f} PLN")

    # Zapisz plik
    doc.save(save_path)
    print(f"Raport zapisany: {save_path}")
