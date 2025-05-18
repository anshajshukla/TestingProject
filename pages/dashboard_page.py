"""
Page Object Model for the Dashboard Page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import DEFAULT_TIMEOUT

class DashboardPage:
    """
    Page Object for the dashboard page.
    Contains element locators and page-specific methods.
    """
    # Element locators
    ACCOUNT_SUMMARY = (By.ID, "account-summary")
    ACCOUNT_BALANCE = (By.ID, "account-balance")
    TRANSFER_BTN = (By.ID, "transfer-btn")
    TRANSACTION_HISTORY_BTN = (By.ID, "transaction-history-btn")
    PROFILE_BTN = (By.ID, "profile-btn")
    LOGOUT_BTN = (By.ID, "logout-btn")
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-message")
    NOTIFICATION_BELL = (By.ID, "notification-bell")
    NOTIFICATION_COUNT = (By.CLASS_NAME, "notification-count")
    
    def __init__(self, driver):
        """
        Initialize the Dashboard Page with a WebDriver instance.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    def is_loaded(self):
        """
        Check if the dashboard page is loaded.
        
        Returns:
            bool: True if dashboard page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_SUMMARY))
            return True
        except:
            return False
    
    def get_account_balance(self):
        """
        Get the account balance text.
        
        Returns:
            str: Account balance text
        """
        return self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_BALANCE)).text
    
    def click_transfer(self):
        """
        Click the transfer button.
        """
        self.driver.find_element(*self.TRANSFER_BTN).click()
    
    def click_transaction_history(self):
        """
        Click the transaction history button.
        """
        self.driver.find_element(*self.TRANSACTION_HISTORY_BTN).click()
    
    def click_profile(self):
        """
        Click the profile button.
        """
        self.driver.find_element(*self.PROFILE_BTN).click()
    
    def logout(self):
        """
        Click the logout button.
        """
        self.driver.find_element(*self.LOGOUT_BTN).click()
    
    def get_welcome_message(self):
        """
        Get the welcome message text.
        
        Returns:
            str: Welcome message text
        """
        return self.wait.until(EC.visibility_of_element_located(self.WELCOME_MESSAGE)).text
    
    def get_notification_count(self):
        """
        Get the notification count.
        
        Returns:
            int: Notification count
        """
        try:
            count_text = self.driver.find_element(*self.NOTIFICATION_COUNT).text
            return int(count_text)
        except:
            return 0
    
    def click_notification_bell(self):
        """
        Click the notification bell.
        """
        self.driver.find_element(*self.NOTIFICATION_BELL).click()
