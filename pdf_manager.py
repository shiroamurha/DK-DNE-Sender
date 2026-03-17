from pypdf import PdfReader, PdfWriter
from io import BytesIO
from utils import debug
from shutil import rmtree



def extract_dnes_from_list():

    dne_list = PdfReader("./DNEs/dne_list.pdf")

    for i, page in enumerate(dne_list.pages):

        temp_buffer = BytesIO() # this is needed to translate a pdfwriter to a pdfreader 
        dne = PdfWriter()

        dne.add_page(page)
        dne.write(temp_buffer)

        temp_buffer.seek(0)
        text_from_dne = PdfReader(temp_buffer).pages[0].extract_text()

        # 5th line from the text, replaces all spaces for nothing and makes all uppercase. ex.: 'JOAODASILVA'
        name_from_dne = text_from_dne.split('\n')[5].replace(' ', '').upper()

        with open(f"./DNEs/{name_from_dne}.pdf", "wb") as file:
            dne.write(file)
        
debug('Done extracting and renaming DNEs from list.')



def delete_all_temp_files():
    rmtree(r'./DNEs')
    debug('All DNEs deleted.')




if __name__ == "__main__":
    
    extract_dnes_from_list()