import time
import os
import getpass
import glob
import threading
from selenium.webdriver.common.by import By

################################################################################################################
####################################### Methods for scraping in the web  ######################################
################################################################################################################
class WebScraper:
    def __init__(self, driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver
        
    def get_download_path(self):
        if os.name == 'nt':  # For Windows
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        else:  # For Unix-based systems
            download_path = os.path.join("/home", getpass.getuser(), "Downloads")
        return download_path

    def wait_for_latest_file(self, download_path, download_complete_event):
        try:
            while True:
                list_of_files = glob.glob(download_path + '/*')
                if not list_of_files:
                    time.sleep(1)
                    continue
                latest_file = max(list_of_files, key=os.path.getctime)
                if os.path.splitext(latest_file)[1] not in ['.crdownload', '.part']:
                    if not os.path.exists(latest_file):  # Check if the file exists
                        continue
                    old_file_size = os.path.getsize(latest_file)
                    time.sleep(1)
                    if not os.path.exists(latest_file):  # Check if the file exists
                        continue
                    new_file_size = os.path.getsize(latest_file)
                    if old_file_size == new_file_size:  # If the file size has stopped increasing
                        break
        except Exception as e:
            print(f"An error occurred while waiting for the file to download: {e}")
        finally:
            download_complete_event.set()  # Signal that the download is complete
            
    def scraped_element_action(self, driver, TYPE, value_var, action, send_keys_value="", time_to_wait=0.5):
        scraped_element = None
        if TYPE == "xpath":
            scraped_element = driver.find_element(by=By.XPATH, value=value_var)
        elif TYPE == "link_text":
            scraped_element = driver.find_element(by=By.LINK_TEXT, value=value_var)
        elif TYPE == "name":
            scraped_element = driver.find_element(by=By.NAME, value=value_var)

        if scraped_element is not None:
            if action == "click":
                scraped_element.click()
            elif action == "sendkeys":
                scraped_element.send_keys(send_keys_value)
            driver.implicitly_wait(time_to_wait)
        else:
            print(f"No element found with {TYPE} = {value_var}")
        
    def subject_downloader(self, driver, subject, download_complete_event):
        download_path = self.get_download_path()
        self.scraped_element_action(driver, "xpath", '//*[@id = "portfolio_lessons_wrapper"]/div[1]/a', "click")
        self.scraped_element_action(driver, "link_text", subject, "click")
        self.scraped_element_action(
            driver, "xpath", '//*[@id="header"]/button/span[1]', "click")
        self.scraped_element_action(driver, "link_text",'Έγγραφα', "click", time_to_wait=1)
        self.scraped_element_action(driver, "xpath", 
            '//*[@id="main-content"]/div/div/div[3]/div/div/div/div/a[2]/span', "click")
        # Start a new thread to wait for the download to complete
        download_wait_thread = threading.Thread(target=self.wait_for_latest_file, args=(download_path, download_complete_event))
        download_wait_thread.start()
        download_wait_thread.join()  # Wait for the download to complete
