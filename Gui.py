import time
import customtkinter as ctk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from Subject import App


universities = {
    "University of Patras": "https://eclass.upatras.gr/",
    "National and Kapodistrian University of Athens": "https://eclass.uoa.gr/",
    "Aristotle University of Thessaloniki": "https://eclass.auth.gr/",
    "National Technical University of Athens": "https://mycourses.ntua.gr/",
    "University of Crete": "https://eclass.edc.uoc.gr/",
    "University of Ioannina": "https://eclass.uoi.gr/",
    "University of Thessaly": "https://eclass.uth.gr/",
    "University of the Aegean": "https://eclass.aegean.gr/",
}

def get_university_names(universities):
    return list(universities.keys())

university_names = get_university_names(universities)

class EclassAllFileDownloader(ctk.CTk):

    WIDTH = 480
    HEIGHT = 360

    def __init__(self):
        super().__init__()
        self.selected_university = universities["University of Patras"]
        self.clear_inputs = None
        self.root = ctk.CTk()
        self.root.iconbitmap("images/logo.ico")
        self.root.title("Eclass All File Downloader")
        self.root.geometry(
            f"{EclassAllFileDownloader.WIDTH}x{EclassAllFileDownloader.HEIGHT}+800+300")
        self.root.resizable(False,False)

        self.myFrame = ctk.CTkFrame(master=self.root)
        self.myFrame.grid(row=0, column=0, sticky="nsew")
        # Configure the grid to expand the frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.eclassLabel = ctk.CTkLabel(master=self.myFrame, text='URL:')
        self.eclass_url = ctk.CTkOptionMenu(master=self.myFrame,
            values=university_names,command=self.get_url)
        self.eclassLabel.grid(row=2, column=0)
        self.eclass_url.grid(row=2, column=1, pady=10, padx=20, sticky="ew")
        self.eclass_url.set("University of Patras")

        self.subjectLabel = ctk.CTkLabel(master=self.myFrame, text='Subject:')
        self.subjectInput = ctk.CTkEntry(master=self.myFrame, width=200, placeholder_text="Type in the subject:")
        self.subjectInput.bind("<Return>", lambda event: self.usernameInput.focus_set())
        self.subjectLabel.grid(row=3, column=0)
        self.subjectInput.grid(row=3, column=1, pady=10)

        self.usernameLabel = ctk.CTkLabel(master=self.myFrame, text='Username:')
        self.usernameInput = ctk.CTkEntry(master=self.myFrame, width=200, placeholder_text="Enter your username:")
        self.usernameInput.bind(
            "<Return>", lambda event: self.passwordInput.focus_set())
        self.usernameLabel.grid(row=6, column=0)
        self.usernameInput.grid(row=6, column=1, pady=10)

        self.passwordLabel = ctk.CTkLabel(master=self.myFrame, text='Password:')
        self.passwordInput = ctk.CTkEntry(master=self.myFrame, width=200, placeholder_text="Enter your password:", show='*')
        self.passwordInput.bind("<Return>", 
                                lambda event: self.download_all_files())
        self.passwordLabel.grid(row=8, column=0)
        self.passwordInput.grid(row=8, column=1, pady=10)

        self.checkButton = ctk.CTkSwitch(
            master=self.myFrame, text="Show password", command=self.toggle_show_password)
        self.checkButton.grid(row=9, column=1)

        self.myButton = ctk.CTkButton(
            master=self.myFrame, 
            text="Initialize Process", command=lambda: self.download_all_files())
        self.myButton.grid(row=10, column=0, pady=20, columnspan=2)
        
        self.label_mode = ctk.CTkLabel(master=self.myFrame, text="Appearance Mode:")
        self.label_mode.grid(row=12, column=0, pady=0, padx=20, sticky="ew")

        self.optionmenu_1 = ctk.CTkOptionMenu(master=self.myFrame,
            values=["Dark", "Light", "System"],command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=12, column=1, pady=10, padx=20, sticky="ew")
        self.optionmenu_1.set("System")
        
        self.myFrame.bind("<Return>", 
            lambda event: self.download_all_files())

        self.root.bind("<Command-q>", self.on_closing)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.var = 0
        
    def toggle_show_password(self):
        self.var += 1
        if self.var % 2:
            self.passwordInput.configure(show="")
        else:
            self.passwordInput.configure(show="*")
            
    def get_url(self, selected_university):
        self.selected_university = universities[selected_university]
        return self.selected_university
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def start(self, event=None):
        self.root.mainloop()

    def on_closing(self, event=0):
        self.root.destroy()

    def get_credentials(self):
        subject = self.subjectInput.get().strip()
        username = self.usernameInput.get().replace(" ", "")
        password = self.passwordInput.get().replace(" ", "")
        return subject, username, password

    def initialize_and_login(self, username, password, selected_university):
        # Initialize the webdriver
        try:
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        except WebDriverException as e:
            print(f"Error initializing WebDriver: {e}")
            return

        # Login
        try:
            driver.get(selected_university)
        except WebDriverException as e:
            print(f"Error navigating to URL: {e}")
            return 
        driver.implicitly_wait(0.5)

        scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[2]/div/div/div/div/div/div[1]/div[1]/a', "click")
        scraped_element_action(driver, "name", "j_username", "sendkeys", username)
        scraped_element_action(driver, "name", "j_password", "sendkeys", password)
        scraped_element_action(driver, "xpath", '//*[@id="loginButton"]', "click")

        return driver

    def disconnect_from_eclass(self, driver):
        scraped_element_action(driver, "xpath", '//*[@id="dropdownMenu1"]', "click")
        scraped_element_action(driver, "xpath", '//*[@id="profile_menu_dropdown"]/ul/li[9]', "click")


    def clear_input_fields(self, subjectInput, usernameInput, passwordInput):
        subjectInput.delete(0, ctk.END)
        usernameInput.delete(0, ctk.END)
        passwordInput.delete(0, ctk.END)

    def fetch_subjects(self, username, password):
        driver = self.initialize_and_login(username, password, self.selected_university)
        if driver is None:
            return
        
        # Navigate to the "Όλα τα μαθήματα" section
        scraped_element_action(driver, "link_text", "Όλα τα μαθήματα", "click")

        # Scrape all the subject names
        subjects = [element.text for element in driver.find_elements(By.XPATH, '//table/tbody/tr/td[1]/strong/a')]

        # Disconnect from eclass
        self.disconnect_from_eclass(driver)

        driver.quit()

        return subjects

    def download_all_files(self):
        subject, username, password = self.get_credentials()
        # If subject is empty, fetch all the subject names
        if not subject:
            subjects = list(self.fetch_subjects(username, password))
            if subjects:
                app = App(self.root, subject_var=subjects, callable_func=lambda: self.download_files_for_subject(app.get_subject(), 
                                                username, password, lambda clear_inputs: self.on_download_complete(clear_inputs, app)))
                app.start()
                print(self.clear_inputs)
                if self.clear_inputs:
                    app.on_closing()
            else:
                messagebox.showinfo("Info", "No subjects found")
            return
        # If subject is not empty, download the files for the subject
        self.download_files_for_subject(subject, username, password, self.on_download_complete)

    def download_files_for_subject(self, subject, username, password, callback=None):
        driver = self.initialize_and_login(username, password, self.selected_university)
        if driver is None:
            return

        try:
            subject_downloader(driver, subject)

        # Very common exception needs something else
        except NoSuchElementException:
            # Not enrolled, enroll and then download the files
            # Clicking Εγγραφη σε μάθημα
            scraped_element_action(driver, "link_text", "Εγγραφή σε μάθημα", "click")

            # Clicking Προπτυχιακό
            scraped_element_action(driver, "link_text", "Προπτυχιακό", "click")

            # Clicking the subject
            scraped_element_action(driver, "link_text", subject, "click")
            scraped_element_action(driver, "xpath", '//*[@id="passwordModal"]/span[2]', "click")
                
            # Clicking Χαρτοφυλάκιο
            scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[1]/nav/ol/li[1]/a', "click")
                
            # Downloading the files
            subject_downloader(driver, subject)
            
        # Disconnect from eclass
        self.disconnect_from_eclass(driver)
        driver.quit()
        self.clear_inputs = messagebox.askyesno("Clear Inputs", "Do you want to erase all the input data?")
        if callback:
            callback(self.clear_inputs)

    def on_download_complete(self, clear_inputs, app=None):
        self.clear_inputs = clear_inputs
        if self.clear_inputs:
            self.clear_input_fields(self.subjectInput, self.usernameInput, self.passwordInput)
            if app:
                app.on_closing()


def scraped_element_action(driver, TYPE, value_var, action, send_keys_value="", time_to_wait=0.5):
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

def sleep_time(duration):
    time.sleep(duration)
    
def subject_downloader(driver, subject):
    scraped_element_action(driver, "xpath", '//*[@id = "portfolio_lessons_wrapper"]/div[1]/a', "click")
    scraped_element_action(driver, "link_text", subject, "click")
    scraped_element_action(
        driver, "xpath", '//*[@id="header"]/button/span[1]', "click")
    scraped_element_action(driver, "link_text",'Έγγραφα', "click", time_to_wait=1)
    start_time = time.time()
    scraped_element_action(driver, "xpath", 
        '//*[@id="main-content"]/div/div/div[3]/div/div/div/div/a[2]/span', "click")
    end_time = time.time()
    time_to_download = end_time - start_time
    sleep_time(time_to_download)

if __name__ == '__main__':
    app = EclassAllFileDownloader()
    app.start()
