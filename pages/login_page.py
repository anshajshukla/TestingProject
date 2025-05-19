"""
Page Object Model for the Login Page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import DEFAULT_TIMEOUT

class LoginPage:
    """
    Page Object for the login page.
    Contains element locators and page-specific methods.
    """
    # Element locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-msg")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    
    def __init__(self, driver):
        """
        Initialize the Login Page with a WebDriver instance.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    def open(self, base_url):
        """
        Open the login page.
        
        Args:
            base_url: Base URL of the application
        """
        self.driver.get(f"{base_url}/login")
        # Wait for the page to load
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        
    def enter_username(self, username):
        """
        Enter username in the username field.
        
        Args:
            username: Username to enter
        """
        self.driver.find_element(*self.USERNAME_FIELD).clear()
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)
    
    def enter_password(self, password):
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter
        """
        self.driver.find_element(*self.PASSWORD_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
    
    def click_login(self):
        """
        Click the login button.
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
    
    def login(self, username, password):
        """
        Perform complete login action.
        
        Args:
            username: Username to enter
            password: Password to enter
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self):
        """
        Get the error message text.
        
        Returns:
            str: Error message text
        """
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed.
        
        Returns:
            bool: True if error message is displayed, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except:
            return False
    
    def click_forgot_password(self):
        """
        Click the forgot password link.
        """
        self.driver.find_element(*self.FORGOT_PASSWORD_LINK).click()
