import json 
from os import system
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
from bs4 import BeautifulSoup



def clear_cookies():

    raw_cookies = json.load(open('../dk_dne_session.json', 'r'))
    filtered_session = []

    for item in raw_cookies:
        keys = list(item.keys()).copy()
        for line in keys:
            if line not in ['name', 'value', 'domain', 'path']:
                del item[line]
    filtered_session = raw_cookies

    json.dump(filtered_session, open('../dk_dne_session.json', 'w'), indent=4)

    return filtered_session



def debug(content):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] > {content}')



def start_driver(entity):
    
    # preliminar stuff starting those below
    global playwright, browser, context

    session = clear_cookies()

    playwright = sync_playwright().start() 
    browser = playwright.webkit.launch()
    context = browser.new_context()
    context.add_cookies(session)

    page = context.new_page()

    debug('Driver, context and page initialized.')

    # sometimes playwright just cant access for no reason so it has to be done 2 times
    try:
        page.goto(f"https://admin-meia-entrada.netlify.app/dashboard/carteiras/{entity}")
    except:
        page.goto(f"https://admin-meia-entrada.netlify.app/dashboard/carteiras/{entity}")
    
    debug('URL resolved.')

    # goes to 'Em Produção' section of the page
    try: 
        section_button = page.locator("button:has(span:has-text('Em Produção'))")
        section_button.wait_for()
        section_button.click()

        rows_per_page = page.locator("main div div div div div div div:has(p:has-text('Rows per page')) div div input")
        rows_per_page.click()

        select_rows_number = page.locator('div div div div div div div div div[value="100"][data-combobox-option="true"]')
        select_rows_number.click()


        # often this error occurs because the session cookies are expired
    except TimeoutError as e:
        raise TimeoutError(f'{e}\n\nYou should try logging in again and updating your session cookies')

    debug('Section accessed. Set to 100 rows visualization')

    return page


    
def close_all(page):# aperta agora

        try:
            page.close()
        except:
            pass
        try:
            context.close()
        except:
            pass

        try:
            browser.close()
        except:
            pass
        
        try:
            playwright.dispose()
        except:
            pass



def download_dne_list(page):    

    with page.expect_download() as download_info:

        download_button = page.locator("button:has(span:has-text('BAIXAR TODAS '))")
        download_button.wait_for()
        download_button.click()
        debug('Downloading DNE List... ')

        system('mkdir DNEs')
        download_info.value.save_as("./DNEs/dne_list.pdf")
        debug('Done.')
        



def get_email_info(page):

    debug('Starting to get e-mail info. ')
    all_rows = page.locator('div table tbody tr').all()
    email_info = {}
    counter = 1

    for row in all_rows:

        # playwright creates nth's in lots of 10, but when there is no next nth element, it just dont resolves
        # so in general every click and wait for needs about 1000ms to resolve and if it delays more than 5s, it breaks the loop
        try:
            row.click(timeout=5000)
        except TimeoutError:
            break

        # was needed to get the whole tag tree to crawl precisely to those elements
        div_has_name = page.locator("form div div div div:has(label:has-text('Nome'))")
        name = div_has_name.locator("div input[placeholder='Nome']").get_attribute('value')

        div_has_email = page.locator("form div div div div:has(label:has-text('Email'))")
        email = div_has_email.locator("div input[placeholder='Email']").get_attribute('value')

        email_info[name] = email

        # closes the window of detailed info
        close_detailed_info_button = page.locator("div section header button:has(svg)")
        close_detailed_info_button.click()
        debug(f'Gotten email info no. {counter}')
        
        counter += 1

    return email_info



def save_html_state(page):

    with open('page.html', 'w') as p:  

        soup = BeautifulSoup(page.content(), "html.parser")
        soup = soup.prettify()
        p.write(soup)
    



def main():

    page = start_driver('dce_ifrs_restinga')
    download_dne_list(page)
    get_email_info(page)
    save_html_state(page)
    close_all(page)



if __name__ == "__main__":
    main()