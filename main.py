from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

ACCOUNT_EMAIL = "YOUR_EMAIL"
ACCOUNT_PASSWORD = "YOUR_PASSWORD"
PHONE = "YOUR_NUMBER"


chrome_driver_path = "CHROME_DRIVER_PATH"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&keywords=web%20developer")
driver.maximize_window()
signin = driver.find_element_by_css_selector(".nav__button-secondary")
signin.click()

#Login
time.sleep(5)
username = driver.find_element_by_css_selector("#username")
username.send_keys(ACCOUNT_EMAIL)
password = driver.find_element_by_name("session_password")
password.send_keys(ACCOUNT_PASSWORD)
password.send_keys(Keys.ENTER)

time.sleep(5)

all_job_listings = driver.find_elements_by_css_selector(".job-card-container--clickable")

for listing in all_job_listings:
    listing.click()
    time.sleep(2)

    #Try to Locate the apply button,if can't locate then skip the job
    try:
        apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
        apply_button.click()
        time.sleep(5)

        #Filling Empty Phone Field
        phone_number = driver.find_element_by_class_name("fb-single-line-text__input")
        if phone_number.text == "":
            phone_number.send_keys(PHONE)

        submit_button = driver.find_element_by_css_selector("footer button")

        #If submit button is a "Next" button multistep form skip it
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
            discard_button.click()
            print("Complex application,skipped.")

        else:
            submit_button.click()


        #Close window after submitting the application
        time.sleep(2)
        close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
        close_button.click()

        #If already applied to a job or if job is no longer accepting aplication,then skip.
    except NoSuchElementException:
        print("No application button,skipped")
        continue

time.sleep(5)
driver.quit()