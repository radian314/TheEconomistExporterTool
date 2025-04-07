from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
import os
import PyPDF2

def welcome_msg():
    print("Hej! Napisalem skrypt ktory sciaga i laczy w jeden PDF najnowsze wydanie The Economist do ktorego mamy legalny ale niewygodny dostep z SGH.")
    print("Wymaga zalogowania sie, stad nie ma watpliwosci, ze uzywany jest jedynie na uzytek wlasny ;)")
    print("Powinien dzialac zarowno na Macu jak i na Windowsie, jak ktos uzywa Linuxa to sam sobie poradzi :p")
    print("Zostal spowolniony poniekad celowo, bo stronka wykrywa, ze to automatyzacja")
    print("Czasami tez wystepuja zdwojone strony, ale no trundo nie chce mi sie wiecej go optymalizowac xd")
    print("")

def open_browser_instance(name, download_dir):    # Opens APP
    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument("start-maximized")
    browser_options.add_argument("--disable-backgrounding-occluded-windows")

    # Changes the download directory to the one specified by the user
    prefs = {
        "download.default_directory" : f"{download_dir}",
        "prompt_for_download" : False,
        "plugins.always_open_pdf_externally" : True,
    }
    browser_options.add_experimental_option("prefs", prefs)
    # Necessary to keep browser instance open
    browser_options.add_experimental_option("detach", True) 

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = browser_options)

    # Opens web_page in browser instance
    driver.get(name)    
    return driver

def remove_last_page(input_pdf_path, output_pdf_path):
    # Open the original PDF file
    time.sleep(1)
    with open(input_pdf_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)

        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Get the total number of pages
        num_pages = len(pdf_reader.pages)

        # Copy all the pages except the last one
        for page_num in range(num_pages - 1):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        # Write the result to a new PDF file
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def merge_pdfs(pdf1_path, pdf2_path, output_path):
    # Create a PdfWriter object
    writer = PyPDF2.PdfWriter()

    # Open and read the first PDF
    with open(pdf1_path, 'rb') as pdf1_file:
        reader1 = PyPDF2.PdfReader(pdf1_file)
        # Add all pages from the first PDF to the writer
        for page_num in range(len(reader1.pages)):
            page = reader1.pages[page_num]
            writer.add_page(page)

    # Open and read the second PDF
    with open(pdf2_path, 'rb') as pdf2_file:
        reader2 = PyPDF2.PdfReader(pdf2_file)
        # Add all pages from the second PDF to the writer
        for page_num in range(len(reader2.pages)):
            page = reader2.pages[page_num]
            writer.add_page(page)

    # Write the combined pages to the output PDF
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)


if __name__ == '__main__':

    welcome_msg()
    working_dir = input("Podaj sciezke do folderu w ktorym chcesz docelowo miec plik z calym The Economist: ")
    website_address = r'https://omnis-sgh.primo.exlibrisgroup.com/permalink/48OMNIS_WSE/1103dcg/alma993285616307664'

    browser = open_browser_instance(website_address, working_dir)


    try:
        first_button = WebDriverWait(browser, 6).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#getit_link1_0 > div > prm-full-view-service-container > div.section-body > div > prm-alma-viewit > prm-alma-viewit-items > md-list > div > md-list-item > div.in-element-dialog-context.layout-row.flex > div.md-list-item-text.layout-wrap.layout-row.flex > div > div > a")))
        first_button.click()  # Click the button
        print("Initial button clicked.")
    except TimeoutException:
        print("Could not find the cookie consent button.")

    # Switch to new tab which opens after first_button click
    WebDriverWait(browser, 5).until(EC.number_of_windows_to_be(2))
    assert len(browser.window_handles) == 2
    browser.switch_to.window(browser.window_handles[1]) 

    # Gives it a second
    browser.implicitly_wait(35)
    time.sleep(30)
    browser.implicitly_wait(35)

    # Finds cookie accept banner
    element = WebDriverWait(browser, 7).until(EC.visibility_of_element_located((By.ID, "onetrust-banner-sdk")))

    # Accepts / rejects the cookie banner
    try:
        accept_button = WebDriverWait(browser, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-reject-all-handler']")))
        accept_button.click()  # Click the cookie reject button
        print("Cookie consent button clicked.")
    except TimeoutException:
        print("Could not find the cookie consent button.")
    
    # Enters the first page of the magazine (Contents Table)
    table_of_contents = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, f"//a[@title='Table of Contents']")))
    table_of_contents.click()

    # #### TO_DO #### Zbierz info o wydaniu itp
    Title = "The Economist"

    # Will turn to zero on the last page
    flag_to_continue = 1
    # First page will be formatted differently
    first = 1
    # Path to the final version of the file
    path_to_final_file = working_dir

    while(flag_to_continue):
        # Finds and clicks the download button
        download_button = WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.XPATH, f"//a[@title='Pobierz plik PDF']")))
        download_button.click()

        # First file processing
        if first:
            file_counter = 1
            while file_counter:
                for file in os.listdir(working_dir):
                    path_to_file = os.path.join(working_dir, file)
                    if (not file.endswith(".tmp")) and (not file.endswith(".crdownload")) and os.path.isfile(path_to_file) and file.endswith(".pdf") and (not file.startswith(".com.google.Chrome")):
                        output_pdf_path = os.path.join(working_dir, f"{Title}.pdf")
                        # Use bulletproof function
                        remove_last_page(path_to_file, output_pdf_path)

                        # Clean up old file
                        os.remove(path_to_file)

                        # Save path for future merging
                        path_to_final_file = output_pdf_path

                        file_counter = 0  # exit loop

        if not first:
            file_counter = 1
            while file_counter:
                for file in os.listdir(working_dir):
                    path_to_file = os.path.join(working_dir, file)
                    if (path_to_file != path_to_final_file) and (not file.endswith(".tmp")) and (
                    not file.endswith(".crdownload")) and os.path.isfile(path_to_file) and file.endswith(".pdf") and (not file.startswith(".com.google.Chrome")):
                        # Clean next file
                        temp_cleaned_file = os.path.join(working_dir, "temp_cleaned.pdf")
                        remove_last_page(path_to_file, temp_cleaned_file)

                        # Merge temp_cleaned + final
                        temp_merged = os.path.join(working_dir, "temp_merged.pdf")
                        merge_pdfs(path_to_final_file, temp_cleaned_file, temp_merged)

                        # Cleanup
                        os.remove(path_to_file)
                        os.remove(path_to_final_file)
                        os.remove(temp_cleaned_file)

                        # Rename merged to final
                        os.rename(temp_merged, path_to_final_file)

                        file_counter = 0

        # Gdyby wykryli ze automatyzacja
        try:
            popupclose = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Close Sugerowane')]")))
            popupclose.click()
        except TimeoutException:
            pass

        # Szuka guzika do przejscia do nastepnej strony
        try:
            next_page_nav = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, f"//a[@id='nextLink']")))
            next_page_nav.click()
        except TimeoutException:
            flag_to_continue = 0
        first = 0
    print("Program zakonczyl sie pomyslnie")
        