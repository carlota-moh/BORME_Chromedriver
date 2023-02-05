def create_webdriver(prefs):
    """
    Function used to create Chrome webdriver used by selenium

    INPUTS:
    -prefs: dictionary
        Contains drivers additional preferences

    RETURNS:
    -driver:
        Selenium Chromedriver
    """
    from selenium import webdriver

    # load options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument('--headless') # uncomment to run headless
    options.add_experimental_option('prefs', prefs)

    # create driver
    driver = webdriver.Chrome(options=options)
    return driver

def load_url(driver, url, logger):
    import time
    from selenium.common.exceptions import StaleElementReferenceException, InvalidArgumentException
    try:
        driver.get(url)
        time.sleep(1)
        logger.debug("Loaded %s" % url)
            
    except StaleElementReferenceException:
        pass
    
    except InvalidArgumentException:
        logger.critical("Invalid URL")

def load_date(driver, date, ID, logger):
    """
    Function used to interact with date field and load
    data corresponding to a particular date

    -INPUTS:
    -driver:
        Selenium driver
    -date: string
        Date to be passed. Must be formated as "MMDDYYYY"
    -ID: string
        ID of the HTML field to interact with
    """
    import time
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    date_field = driver.find_element(By.ID, ID)

    try:
        date_field.send_keys(date, Keys.ENTER)
        time.sleep(2) 
    except:
        logger.error('Input field not found')

def click_dropdown(driver, XPATH, logger):
    import sys
    """
    Function used for interacting with dropdown object

    INPUTS:
    -driver:
        Selenium driver
    -XPATH: string
        XML path used to locate dropdown
    """
    from selenium.webdriver.common.by import By

    try:
        dropdown = driver.find_element(By.XPATH, XPATH)
        dropdown.click()
    except:
        logger.crticañ("There is no data for this particular date")
        sys.exit()


def get_url(driver, desired_name, logger):  
    """
    Get desired URL from a list of elements

    INPUTS:
    -driver:
        Selenium driver
    -desired_name: 
        Name of the desired element for which url
        needs to be fetched
    """
    from selenium.webdriver.common.by import By

    links = driver.find_elements(By.TAG_NAME, 'a')
    for l in links:
        if l.text == desired_name:
           url = l.get_attribute('href')
           load_url(driver, url, logger) 
        else:
            continue

def move_to_folder(old_directory, new_directory, logger):
    """
    Function used to move elements from one folder to another

    INPUTS:
    -old_directory: string
        Name of the old directory, which contains file(s) to be
        reallocated

    -new_directory: string
        Name of the new directory, in which file(s) is to be placed
    """
    import time
    import glob
    import os

    got_file = False   
    # Grab current filename
    while got_file == False:
        try: 
            current_file = glob.glob(old_directory+'*')[0]
            got_file = True
        except:
            logger.debug("File is not yet downloaded")
            time.sleep(15)

    # Create new filename
    filename = glob.glob(old_directory+'*')[0].split('/')[-1]
    destination = new_directory+filename

    # Move file to new destination
    os.rename(current_file, destination)
    logger.debug("Moved %s to %s" % (current_file, destination))

def find_links(driver, li_class):
    """
    Function used for finding links contained within a list

    INPUTS:
    -driver: 
        Selenium driver

    -li_class: string
        Name of the list attribute for which to search for

    RETURNS:
    -links: list
        list of urls contained inside the li element
    """
    from selenium.webdriver.common.by import By

    lis = driver.find_elements(By.XPATH, ('//li[@class="{}"]').format(li_class))
    links = [l.find_element(By.TAG_NAME, 'a').get_attribute('href') for l in lis]
    return links

def download_data(driver, default_download_dir, dir_XPATH, logger):
    """
    Function used for downloading PDF and XML documents

    INPUTS:
    -driver:
        Selenium driver
    
    -default_download_dir: string
        Path to the directory where data is to be downloaded
    
    -dir_XPATH: string
        XPATH within the HTML corresponding to the section
        headers, for which download directories need to be
        created
    """
    import os
    import time
    import requests
    from selenium.webdriver.common.by import By
    from utils import dir_maker

    # Find elements containing directory names
    dirs = driver.find_elements(By.XPATH, dir_XPATH)
    dirnames = [d.text.replace(' ', '_') for d in dirs]

    # For each subsection
    for name, dir in zip(dirnames, dirs):
        # Create new directory to store pdfs
        dir_maker(directory=name)
        new_path = os.getcwd()+'/'+name+'/'

        # Get doc URLs
        ul = dir.find_element(By.XPATH, './following-sibling::*')
        lis = ul.find_elements(By.TAG_NAME, 'li')
        dispo_docs = [l for l in lis if l.get_attribute('class') == "puntoHTML"]
        urls = [l.find_element(By.TAG_NAME, 'a').get_attribute('href') for l in dispo_docs]

        for url in urls:
            load_url(driver, url, logger)

            # Get pdf
            pdf_url = find_links(driver=driver, li_class="puntoPDF")[0]
            load_url(driver, pdf_url, logger)
            time.sleep(3)
            logger.debug("Downloaded %s" % pdf_url)
            move_to_folder(old_directory=default_download_dir, new_directory=new_path, logger=logger)

            # Get XML
            xml_url = find_links(driver=driver, li_class="puntoXML")[0]
            xml_name = xml_url.split('=')[-1]
            
            response = requests.get(xml_url)
            if response.status_code == 200:
                with open(default_download_dir+xml_name+'.xml', "wb") as f:
                    f.write(response.content)
            else:
                logger.warning("Something went wrong. Response code: {} for {}".format(response.status_code,
                                                                                       xml_name))
            move_to_folder(old_directory=default_download_dir, new_directory=new_path, logger=logger)
            
            # Go back to repeat process
            driver.back()
            logger.info("Returning to %s" % driver.current_url)
            time.sleep(0.5)        

def run_spider(default_download_dir, date, url):
    import time
    import logging
    from selenium.common.exceptions import StaleElementReferenceException
    from utils import dir_remover

    # Initialize logger
    logger = logging.getLogger("spider")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = "./logs/spider.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    # Create a console handler with a higher log level.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    # Modify the handlers log format to your convenience.
    handler_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(handler_format)
    console_handler.setFormatter(handler_format)
    # Finally, add the handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    prefs = {
    "download.default_directory": default_download_dir,
    "download.prompt_for_download": False, # To auto download the file
    "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
    }

    driver = create_webdriver(prefs=prefs)
    logger.info("Loaded driver")

    # Load URL
    load_url(driver, url, logger)
    time.sleep(2)
    logger.info("Loaded url")

    # load date
    date_id = 'fechaBORME'
    load_date(driver=driver, date=date, ID=date_id, logger=logger)
    logger.debug("Using %s as date" % date)

    # Click on dropdown
    dropdown_path = '//label[@data-toggle="dropdown"]'
    click_dropdown(driver=driver, XPATH=dropdown_path, logger=logger)
    logger.info("Clicking on dropdown")

    # Navigate to section 2
    section2 = 'SECCIÓN SEGUNDA. Anuncios y avisos legales'
    try:
        get_url(driver=driver, desired_name=section2, logger=logger)
        logger.info("Navigated to %s" % section2)
    except StaleElementReferenceException:
        pass

    time.sleep(2)

    # Download PDFs
    subsections_xpath = '//h4'
    download_data(driver=driver, default_download_dir=default_download_dir,\
                  dir_XPATH=subsections_xpath, logger=logger)

    # remove default downloads directory
    try:
        dir_remover(directory=default_download_dir)
    except OSError:
        logger.warning("Could not move a file from download directory.\
                        Please relocate it manually")

if __name__ == '__main__':
    import sys
    import os
    from utils import dir_maker

    arguments = sys.argv
    input_date = str(arguments[-1])
    
    # Reformat date appropriately
    YYYY = input_date[:4]
    MM = input_date[4:6]
    DD = input_date[-2:]
    date = MM+DD+YYYY

    # Create downloads directory
    download_name = 'downloads'
    dir_maker(download_name)
    download_dir = os.getcwd()+download_name+'/'

    # url
    url = 'https://www.boe.es/diario_borme/'

    # run spider
    run_spider(default_download_dir=download_dir, date=date, url=url)
