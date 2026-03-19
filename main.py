import crawler
import pdf_manager
import email_sender
from utils import *



def main():

    debug('Starting CRAWLER')
    name_to_email = crawler.crawl()

    filename_to_email = {}

    for key in name_to_email:
        filename_to_email[padronize(key)] = name_to_email.get(key)
    
    debug('Starting PDF MANAGER')
    all_filenames_list = pdf_manager.extract_dnes_from_list()

    for filename in all_filenames_list:
        email_to_send = filename_to_email.get(filename[:15])
        name_to_send = get_key_by_value(name_to_email, email_to_send)

        email_sender.send_dne_by_email('alayouey@gmail.com', name_to_send, filename)
        debug(f'Nome: {name_to_send} - email {email_to_send} - arquivo: {filename}')
    
    pdf_manager.delete_all_dnes()
    

if __name__ == "__main__":
    main()
    