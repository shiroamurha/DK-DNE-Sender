from pypdf import PdfReader, PdfWriter

dne_list = PdfReader("./DNEs/dne_list.pdf")


for i, page in enumerate(dne_list.pages):

    dne = PdfWriter()
    dne.add_page(page)

    with open(f"./DNEs/{i+1}.pdf", "wb") as on_file:
        dne.write(on_file)

    with open(f"./DNEs/{i+1}_extracted_text.txt", "w") as file:
        saved_dne = PdfReader(f"./DNEs/{i+1}.pdf")
        file.write(saved_dne.pages[0].extract_text())