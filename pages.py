
from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from helpers import retrieve_phone_code
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
    number_text_locator = (By.CSS_SELECTOR, '.np-button')
    number_enter = (By.ID, 'phone')
    number_confirm = (By.CSS_SELECTOR, '.button.full')
    number_code = (By.ID, 'code')
    code_confirm = (By.XPATH, '//button[contains(text(),"Confirmar")]')
    number_finish = (By.CSS_SELECTOR, '.np-text')

    # Preencher número de cartão
    payment_method_button = (By.XPATH, "//div[@class='pp-text' and text()='Método de pagamento']")
    add_card_button = (By.XPATH,"//div[contains(@class,'pp-title') and text()='Adicionar cartão']")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH,"//div[contains(@class,'card-code-input')]//input[@id='code']")
    confirm_add_card_button = (By.XPATH, "//button[@type='submit' and contains(text(),'Adicionar')]")
    close_button_card = (By.CSS_SELECTOR, '.payment-picker.open .close-button')
    comfirm_card = (By.CSS_SELECTOR, '.pp-value-text')

    # Preencher comentário
    comment_label = (By.CSS_SELECTOR, 'label[for="comment"]')
    comment_field = (By.ID, 'comment')

    # Cobertores e lençois
    blanket_toggle = (By.XPATH, "//div[text()='Cobertor e lençóis']/following-sibling::div")

    # Escolher quantidade de sorvete
    icecream_plus = (By.XPATH, "//div[text()='Sorvete']/following::div[@class='counter-plus'][1]")
    icecream_value = (By.XPATH, "//div[text()='Sorvete']/following::div[@class='counter-value'][1]")

    # Model
    call_taxi_button = (By.CSS_SELECTOR, '.smart-button')
    pop_up = (By.CSS_SELECTOR, '.order-header-title')

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
    def click_number_text(self, telefone):
        self.driver.find_element(*self.number_text_locator).click() #Clica no número

        self.driver.find_element(*self.number_enter).send_keys(telefone)  #Digita o número

        self.driver.find_element(*self.number_confirm).click() #Confirma o número

        code = retrieve_phone_code(self.driver) #Digita o código
        code_input = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(self.number_code)
        )
        code_input.clear()
        code_input.send_keys(code)

        self.driver.find_element(*self.code_confirm).click()#Confirma

    def numero_confirmado(self):
        numero = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.number_finish))
        return numero.text

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

    def close_button(self):
        return self.driver.find_element(*self.close_button_card).click()

    def confirm_cartao(self):
        return self.driver.find_element(*self.comfirm_card).text


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

    # Model

    def call_taxi(self):
        self.driver.find_element(*self.call_taxi_button).click()

    def pop_up_show(self):
        pop_up = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.pop_up))
        return pop_up.text
