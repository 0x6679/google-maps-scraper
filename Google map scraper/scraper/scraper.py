"""
This module contain the code for backend,
that will handle scraping process
"""

from bs4 import BeautifulSoup
from time import sleep
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import (
    WebDriverException,
    JavascriptException,
)
import sys
import threading
import undetected_chromedriver as uc
from .datasaver import DataSaver
from .settings import DRIVER_EXECUTABLE_PATH


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Backend:
    closeThread = threading.Event()

    timeout = 60

    def __init__(self, searchquery, outputformat, messageshowingfunc,  healdessmode):
        """
        params:

        search query: it is the value that user will enter in search query entry 
        outputformat: output format of file , selected by user
        messageshowingfunc: function refernece to function of frontend class to 
        outputpath: directory path where file will be stored after scraping
        headlessmode: it's value can be 0 and 1, 0 means unchecked box and 1 means checked

        """

        self.searchquery = searchquery  # search query that user will enter
        # it is a function used as api for transfering message form this backend to frontend
        self.messageshowing = messageshowingfunc

        self.headlessMode = healdessmode
        self.datasaver = DataSaver(
            outputformat=outputformat,
            messageshowfunc=messageshowingfunc,
        )

    def findelementwithwait(self, by, value):
        """we will use this function to find an element"""

        element = WebDriverWait(self.driver, self.timeout).until(
            Ec.visibility_of_element_located((by, value))
        )
        return element

    def openingurl(self, url: str):
        """
        To avoid internet connection error while requesting"""

        while True:
            if self.closeThread.is_set():
                self.driver.quit()
                return

            try:
                self.driver.get(url)
            except WebDriverException:
                sleep(5)
                continue
            else:
                break

    def parsing(self):
        """Our function to parse the html"""

        """This block will get element details sheet of a business. 
        Details sheet means that business details card when you click on a business in 
        serach results in google maps"""

        infoSheet = self.driver.execute_script(
            """return document.querySelector("[role='main']")""")
        #print(infoSheet)
        infoSheet_text = self.driver.execute_script(
        """return document.querySelector("[role='main']").textContent""")


        html_content = self.driver.execute_script(
        """return document.querySelector("[role='main']").innerHTML""")
        
        soup = BeautifulSoup(html_content, 'html.parser')

        def get_text_by_css_selector(selector):
            try:
                element = soup.select_one(selector)
                return element.text.strip() if element else None
            except Exception:
                return None

        data = {}
        try:
            data["Name"] = get_text_by_css_selector('h1.DUwDvf')
        except Exception:
            data["Name"] = None

        try:
            data["Rating"] = get_text_by_css_selector('div.F7nice span[aria-hidden="true"]')
        except Exception:
            data["Rating"] = None

        try:
            data["Total Reviews"] = get_text_by_css_selector('div.F7nice span[aria-label]')
        except Exception:
            data["Total Reviews"] = None

        try:
            data["Address"] = get_text_by_css_selector('button[aria-label^="Cím:"] div.Io6YTe')
        except Exception:
            data["Address"] = None

        try:
            data["Website"] = get_text_by_css_selector('a[aria-label^="Webhely:"] div.Io6YTe')
        except Exception:
            data["Website"] = None

        try:
            data["Phone"] = get_text_by_css_selector('button[aria-label^="Telefonszám:"] div.Io6YTe')
        except Exception:
            data["Phone"] = None

        self.finalData.append(data)
        print(data)



    def mainscraping(self):

        try:
            querywithplus = "+".join(self.searchquery.split())

            """
            link of page variable contains the link of page of google maps that user wants to scrape.
            We have make it by inserting search query in it
            """

            link_of_page = f"https://www.google.com/maps/search/{querywithplus}/"

            # ==========================================

            """ 
            We will use these links to find our required data from information fields of the business card
            To understand it , kindly see its use in parsing
            """
            self.comparingLinks = {
                "locationLink": """//www.gstatic.com/images/icons/material/system_gm/1x/place_gm_blue_24dp.png""",
                "phoneLink": """//www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png""",
                "websiteLink": """//www.gstatic.com/images/icons/material/system_gm/1x/public_gm_blue_24dp.png""",
            }

            """
            In this empty list our records will be append, we will make pandas dataframe from it
            """
            self.finalData = []

            """Starting our browser"""

            options = uc.ChromeOptions()

            if self.headlessMode == 1:
                options.headless = True

            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

            self.messageshowing(
                custom=True,
                value="Wait checking for driver...\nIf you don't have webdriver in your machine it will install it",
            )
            try:
                if DRIVER_EXECUTABLE_PATH is not None:
                    self.driver = uc.Chrome(
                        driver_executable_path=DRIVER_EXECUTABLE_PATH, options=options)

                else:
                    self.driver = uc.Chrome(options=options)

            except NameError:
                self.driver = uc.Chrome(options=options)

            self.driver.maximize_window()
            self.messageshowing(custom=True, value="Opening browser...")
            self.driver.implicitly_wait(self.timeout)

            # ====================================

            self.openingurl(url=link_of_page)
            #sleep(10000)
            
            try:
                # Wait until the button is clickable using the full XPath
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/div[3]'))
                )
                # Scroll into view and click using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                self.driver.execute_script("arguments[0].click();", button)
            except Exception as e:
                print(f"An error occurred: {e}")
            
            self.messageshowing(custom=True, value="Working start...")

            sleep(1)
            scrollAbleElement = self.driver.execute_script(
                """return document.querySelector("[role='feed']")"""
            )

            """In case search results are not available"""
            if scrollAbleElement is None:
                self.messageshowing(noresultfound=True)

            else:
                last_height = 0

                while True:
                    if self.closeThread.is_set():
                        self.driver.quit()
                        return

                    """Scroll down to the bottom."""
                    self.driver.execute_script(
                        "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                        scrollAbleElement,
                    )
                    time.sleep(2)

                    # Wait to load the page.

                    # get new scroll height and compare with last scroll height.
                    new_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight", scrollAbleElement
                    )
                    if new_height == last_height:
                        """checking if we have reached end of the list"""

                        script = f"""
                        const endingElement = document.querySelector(".PbZDve ");
                        return endingElement;
                        """
                        endAlertElement = self.driver.execute_script(
                            script)  # to know that we are at end of list or not

                        if endAlertElement is None:
                            """if it returns empty list its mean we are not at the end of list"""
                            try:  # sometimes google maps load results when a result is clicked
                                self.driver.execute_script(
                                    "array=document.getElementsByClassName('hfpxzc');array[array.length-1].click();"
                                )
                            except JavascriptException:
                                pass
                        else:

                            break
                    else:
                        last_height = new_height

                allResultsListSoup = BeautifulSoup(
                    scrollAbleElement.get_attribute('outerHTML'), 'html.parser')

                allResultsAnchorTags = allResultsListSoup.find_all(
                    'a', class_='hfpxzc')

                """all the links of results"""
                allResultsLinks = [anchorTag.get(
                    'href') for anchorTag in allResultsAnchorTags]

                for resultLink in allResultsLinks:
                    if self.closeThread.is_set():
                        self.driver.quit()
                        return

                    self.openingurl(url=resultLink)
                    self.parsing()

            """
        Handling all errors.If any error occurs like user has closed the self.driver and if 'no such window' error occurs
            """
        except Exception as e:
            import traceback
            traceback.print_exc()

            try:
                self.messageshowing(interruptionerror=True, exception=str(e))

                try:
                    self.driver.quit()
                    self.driver.close()
                except:  # if browser is always closed
                    pass

                try:
                    self.datasaver.save(self.finalData, self.searchquery)
                except:
                    pass
            except RuntimeError:
                sys.exit()

        else:  # if not any error occured, will save the data smoothly
            self.driver.close()
            self.driver.quit()


            self.datasaver.save(self.finalData, self.searchquery)

