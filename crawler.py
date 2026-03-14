from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
import json 
from bs4 import BeautifulSoup
import requests



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


def start_driver():
    
    # preliminar stuff starting those below
    global playwright, browser, context

    session = clear_cookies()

    playwright = sync_playwright().start() 
    browser = playwright.webkit.launch()
    context = browser.new_context()
    context.add_cookies(session)

    page = context.new_page()

    # sometimes playwright just cant access for no reason so it has to be done 2 times
    try:
        page.goto("https://admin-meia-entrada.netlify.app/dashboard/carteiras/dce_ifrs_restinga")
    except:
        page.goto("https://admin-meia-entrada.netlify.app/dashboard/carteiras/dce_ifrs_restinga")
    
    # goes to 'Em Produção' section of the page
    # try: 
    section_button = page.locator("button:has(span:has-text('Em Produção'))")
    section_button.wait_for()
    section_button.click()
    rows_per_page = page.locator("main div div div div div div div:has(p:has-text('Rows per page')) div div input")
    rows_per_page.click()
    select_rows_number = page.locator('div div div div div div div div div[value="100"][data-combobox-option="true"]')
    select_rows_number.click()


        # often this error occurs because the session cookies are expired
    # except TimeoutError:
    #     raise TimeoutError('You should try logging in again and updating your session cookies')

    # saves the state of the html
    with open('page.html', 'w') as p:  

        soup = BeautifulSoup(page.content(), "html.parser")
        soup = soup.prettify()
        p.write(soup)
    
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

        page.wait_for_timeout(5000)
        download_info.value.save_as("dne_list.pdf")



def get_email_info(page):

    all_rows = page.locator('div table tbody tr').all()
    for row in all_rows:

        try:
            row.click(timeout=5000)
        except TimeoutError:
            break

        div_has_name = page.locator("form div div div div:has(label:has-text('Nome'))")
        name = div_has_name.locator("div input[placeholder='Nome']").get_attribute('value')

        div_has_email = page.locator("form div div div div:has(label:has-text('Email'))")
        email = div_has_email.locator("div input[placeholder='Email']").get_attribute('value')

        print(f'{name}, {email}')

        close_detailed_info_button = page.locator("div section header button:has(svg)")
        close_detailed_info_button.click()



def main():

    page = start_driver()
    get_email_info(page)

    close_all(page)



if __name__ == "__main__":
    main()