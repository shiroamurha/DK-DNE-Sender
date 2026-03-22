import crawler
import pdf_manager
import email_sender
from utils import *



def main():

    start = debug('========================== STARTING DK DNE SENDER ==========================')

    debug('Starting CRAWLER')
    name_to_email = crawler.crawl()

    filename_to_email = {}

    for key in name_to_email:
        filename_to_email[padronize(key)] = name_to_email.get(key)
    
    debug('Starting PDF MANAGER')
    all_filenames_list = pdf_manager.extract_dnes_from_list()
    all_emails_sent_to = []
    
    logs = get_logs()

    for filename in all_filenames_list:

        if filename not in logs[0]['already_sent_dnes']:

            email_to_send = filename_to_email.get(filename[:15])
            name_to_send = get_key_by_value(name_to_email, email_to_send)

            email_sender.send_dne_by_email(email_to_send, name_to_send, filename)
            debug(f'Nome: {name_to_send} - email {email_to_send} - arquivo: {filename}')
            all_emails_sent_to.append(email_to_send)
            #break
            
    logger(logs, all_filenames_list, all_emails_sent_to)
    
    pdf_manager.delete_all_dnes()
    
    end = debug('=============== END - ALL DONE SUCCESSFUL ===============')
    debug(f'SCRIPT TOTAL DURATION: {str((end - start).total_seconds())[:-4]} seconds')

if __name__ == "__main__":
    main()
    