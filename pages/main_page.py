from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы
    RUB_SUM = (By.ID, "rub-sum")
    RUB_RESERVED = (By.ID, "rub-reserved")
    USD_SUM = (By.ID, "usd-sum")
    EURO_SUM = (By.ID, "euro-sum")

    CARD_NUMBER_FIELD = (By.ID, "card-number")
    AMOUNT_FIELD = (By.ID, "amount")
    TRANSFER_BUTTON = (By.ID, "transfer-button")
    COMMISSION_LABEL = (By.ID, "commission")

    SUCCESS_MESSAGE = (By.ID, "success-message")
    ERROR_MESSAGE = (By.ID, "error-message")
    CARD_ERROR = (By.ID, "card-error")
    AMOUNT_ERROR = (By.ID, "amount-error")

    RUBLE_ACCOUNT_BUTTON = (By.XPATH, "//div[contains(text(), 'Рубли')]")
    EURO_ACCOUNT_BUTTON = (By.XPATH, "//div[contains(text(), 'Евро')]")

    def open(self, url="http://localhost:8000/?balance=30000&reserved=20001"):
        self.driver.get(url)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # Получить текст баланса
    def get_rub_balance(self):
        return self.wait_for_element(self.RUB_SUM).text

    def get_rub_reserved(self):
        return self.wait_for_element(self.RUB_RESERVED).text

    def get_usd_balance(self):
        return self.wait_for_element(self.USD_SUM).text

    def get_euro_balance(self):
        return self.wait_for_element(self.EURO_SUM).text

    # Работа с переводом
    def select_ruble_account(self):
        self.wait_for_element(self.RUBLE_ACCOUNT_BUTTON).click()

    def enter_card_number(self, card_number):
        self.wait_for_element(self.CARD_NUMBER_FIELD).send_keys(card_number)

    def enter_amount(self, amount):
        self.wait_for_element(self.AMOUNT_FIELD).send_keys(amount)

    def click_transfer_button(self):
        self.wait_for_element(self.TRANSFER_BUTTON).click()

    def get_commission(self):
        return self.wait_for_element(self.COMMISSION_LABEL).text

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        return self.wait_for_element(self.ERROR_MESSAGE).text

    def get_card_error(self):
        return self.wait_for_element(self.CARD_ERROR).text

    def get_amount_error(self):
        return self.wait_for_element(self.AMOUNT_ERROR).text

    def is_transfer_button_enabled(self):
        return self.wait_for_element(self.TRANSFER_BUTTON).is_enabled()

    def is_card_input_visible(self):
        return self.wait_for_element(self.CARD_NUMBER_FIELD).is_displayed()

    def is_amount_input_visible(self):
        return self.wait_for_element(self.AMOUNT_FIELD).is_displayed()

    def select_euro_account(self):
        self.wait_for_element(self.EURO_ACCOUNT_BUTTON).click()