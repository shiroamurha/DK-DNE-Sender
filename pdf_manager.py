from pypdf import PdfReader, PdfWriter
from io import BytesIO
from utils import debug
from shutil import rmtree



def extract_dnes_from_list():

    all_filenames_list = []
    dne_list = PdfReader("./DNEs/dne_list.pdf")

    for i, page in enumerate(dne_list.pages):
        
        if i%2 == 0: # only the odd pages (reversed because of i starting on 0)
            temp_buffer = BytesIO() # this is needed to translate a pdfwriter to a pdfreader 
            dne = PdfWriter()

            dne.add_page(page)
            dne.add_page(dne_list.pages[i+1]) # adding the next page that would not be parsed, but will be at the yield file

            dne.write(temp_buffer)

            temp_buffer.seek(0)
            dne_read = PdfReader(temp_buffer)
            text_from_dne = dne_read.pages[0].extract_text()
    
            # 5th line from the text, replaces all spaces for nothing and makes all uppercase. ex.: 'JOAODASILVA'
            name_from_dne = text_from_dne.split('\n')[5].replace(' ', '').upper()
            all_filenames_list.append(name_from_dne)

            with open(f"./DNEs/{name_from_dne}.pdf", "wb") as file:
                dne.write(file)
        
    debug('Done extracting and renaming DNEs from list.')
    return all_filenames_list



def delete_all_dnes():
    rmtree(r'./DNEs')
    debug('All DNEs deleted.')



if __name__ == "__main__":
    
    extract_dnes_from_list()