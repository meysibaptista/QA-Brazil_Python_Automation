
from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

class UrbanRoutesPage:
    # Seção De e Para
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Fluxo de chamada de taxi
    taxi_option = (By.XPATH, "//button[contains(text(), 'Chamar')]")
    comfort_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    comfort_active = (By.XPATH, "//div[contains(@class,'tcard') and contains(@class,'active')]//div[text()='Comfort']")

    # Preencher número de telefone
    phone_button = (By.XPATH, "//div[@class='np-button']//div[contains(text(), 'Número de telefone')]")
    phone_input_field = (By.ID, "phone")

    # Preencher número de cartão
    payment_method_button = (By.XPATH, "//div[@class='pp-text' and text()='Método de pagamento']")
    add_card_button = (By.XPATH,"//div[contains(@class,'pp-title') and text()='Adicionar cartão']")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH,"//div[contains(@class,'card-code-input')]//input[@id='code']")
    confirm_add_card_button = (By.XPATH, "//button[@type='submit' and contains(text(),'Adicionar')]")

    # Preencher comentário
    comment_label = (By.CSS_SELECTOR, 'label[for="comment"]')
    comment_field = (By.ID, 'comment')

    # Cobertores e lençois
    blanket_toggle = (By.XPATH, "//div[text()='Cobertor e lençóis']/following-sibling::div")

    # Escolher quantidade de sorvete
    icecream_plus = (By.XPATH, "//div[text()='Sorvete']/following::div[@class='counter-plus'][1]")
    icecream_value = (By.XPATH, "//div[text()='Sorvete']/following::div[@class='counter-value'][1]")

    def __init__ (self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

# POM
    def _find (self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def _click (self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)
    # Adress

    def _get_text(selfself, locator):
        return self._find(locator).text

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def enter_locations(self, from_text, to_text):
        self._type(self.from_field, from_text)
        self._type(self.to_field, to_text)

    def get_from_location(self):
        return self._get_value(self.from_field)

    def get_to_location(self):
        return self._get_value(self.to_field)

    # Chamar Táxi
    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option).click()

    def click_comfort_icon(self):
        self.driver.find_element(*self.comfort_icon).click()

    def click_comfort_active(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.comfort_active)
            )
            return True
        except:
            return False

    # Preencher telefone
    def click_phone_button(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.phone_button)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._click(self.phone_button)

    def fill_phone_field(self, phone_number):
        self._type(self.phone_input_field, phone_number)

    def get_phone_value(self):
        return self._get_value(self.phone_input_field)

    # Preencher cartão
    def open_payment_method(self):
        btn = self.wait.until(
            EC.element_to_be_clickable(self.payment_method_button)
        )
        btn.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Adicionar cartão')]")
            )
        )

    def click_add_card(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Adicionar cartão']")
            )
        )

        add_card = self.driver.find_element(
            By.XPATH,
            "//div[text()='Adicionar cartão']"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            add_card
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "number")
            )
        )

    def fill_card_number(self, number):
        field = self.wait.until(EC.visibility_of_element_located(self.card_number_field))
        field.click()
        field.clear()
        field.send_keys(number)
        field.send_keys(Keys.TAB)

    def fill_card_code(self, code):
        field = self.wait.until(EC.visibility_of_element_located(self.card_code_field))
        field.click()
        field.clear()
        field.send_keys(code)
        field.send_keys(Keys.TAB)
        self.driver.execute_script("document.activeElement.blur();")

    def fill_card_code(self, code):
        fields = self.driver.find_elements(By.ID, "code")

        visible_field = next(
            field for field in fields
            if field.is_displayed()
        )
        visible_field.clear()
        visible_field.send_keys(code)
        self.driver.execute_script("document.activeElement.blur();")

    def confirm_add_card(self):
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Adicionar')]")
            )
        )

        btn.click()
        self.driver.save_screenshot("after_click.png")

    def check_card_added(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Cartão') or contains(text(),'card') or contains(text(),'Visa')]")
            )
        )


    # Comentário motorista
    def click_comment_button(self):
        label = self.wait.until(
            EC.element_to_be_clickable(self.comment_label)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
        label.click()
    def fill_comment_field(self, text):
        field = self.wait.until(
            EC.visibility_of_element_located(self.comment_field)
        )
        field.clear()
        field.send_keys(text)

    def get_comment_value(self):
        field = self.wait.until(
            EC.visibility_of_element_located(self.comment_field)
        )
        return field.get_attribute("value")

    # Adicionar cobertores e lençois
    def click_blanket_toggle(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.blanket_toggle)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    # Adicionar quantidade de sorvete
    def add_two_icecreams(self):
        plus_button = self.wait.until(
            EC.element_to_be_clickable(self.icecream_plus)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_button)
        plus_button.click()
        plus_button.click()

    def get_icecream_value(self):
        value = self.wait.until(
            EC.visibility_of_element_located(self.icecream_value)
        )
        return int(value.text)