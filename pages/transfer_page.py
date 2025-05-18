"""
Page Object Model for the Transfer Page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.config import DEFAULT_TIMEOUT

class TransferPage:
    """
    Page Object for the transfer page.
    Contains element locators and page-specific methods.
    """
    # Element locators
    FROM_ACCOUNT_DROPDOWN = (By.ID, "from-account")
    TO_ACCOUNT_DROPDOWN = (By.ID, "to-account")
    AMOUNT_FIELD = (By.ID, "transfer-amount")
    DESCRIPTION_FIELD = (By.ID, "transfer-description")
    TRANSFER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CANCEL_BUTTON = (By.ID, "cancel-transfer")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        """
        Initialize the Transfer Page with a WebDriver instance.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
    
    def is_loaded(self):
        """
        Check if the transfer page is loaded.
        
        Returns:
            bool: True if transfer page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.FROM_ACCOUNT_DROPDOWN))
            return True
        except:
            return False
    
    def select_from_account(self, account_number):
        """
        Select the from account from the dropdown.
        
        Args:
            account_number: Account number to select
        """
        from_dropdown = Select(self.driver.find_element(*self.FROM_ACCOUNT_DROPDOWN))
        from_dropdown.select_by_visible_text(account_number)
    
    def select_to_account(self, account_number):
        """
        Select the to account from the dropdown.
        
        Args:
            account_number: Account number to select
        """
        to_dropdown = Select(self.driver.find_element(*self.TO_ACCOUNT_DROPDOWN))
        to_dropdown.select_by_visible_text(account_number)
    
    def enter_amount(self, amount):
        """
        Enter the transfer amount.
        
        Args:
            amount: Amount to transfer
        """
        self.driver.find_element(*self.AMOUNT_FIELD).clear()
        self.driver.find_element(*self.AMOUNT_FIELD).send_keys(str(amount))
    
    def enter_description(self, description):
        """
        Enter the transfer description.
        
        Args:
            description: Transfer description
        """
        self.driver.find_element(*self.DESCRIPTION_FIELD).clear()
        self.driver.find_element(*self.DESCRIPTION_FIELD).send_keys(description)
    
    def click_transfer(self):
        """
        Click the transfer button.
        """
        self.driver.find_element(*self.TRANSFER_BUTTON).click()
    
    def click_cancel(self):
        """
        Click the cancel button.
        """
        self.driver.find_element(*self.CANCEL_BUTTON).click()
    
    def get_success_message(self):
        """
        Get the success message text.
        
        Returns:
            str: Success message text
        """
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)).text
    
    def get_error_message(self):
        """
        Get the error message text.
        
        Returns:
            str: Error message text
        """
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
    
    def perform_transfer(self, from_account, to_account, amount, description=""):
        """
        Perform complete transfer action.
        
        Args:
            from_account: Source account number
            to_account: Destination account number
            amount: Amount to transfer
            description: Optional transfer description
        """
        self.select_from_account(from_account)
        self.select_to_account(to_account)
        self.enter_amount(amount)
        if description:
            self.enter_description(description)
        self.click_transfer()
