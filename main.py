import time

import data
import helpers

from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução")

    def _start_comfort_flow(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)


    def setup_method    (self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage (self.driver)
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

    def test_set_route(self):
        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO

    def test_select_plan(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.click_comfort_active()

    def test_fill_phone_number(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        self.page.click_number_text(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in self.page.numero_confirmado()

    def test_fill_card(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        self.page.click_comfort_active()
        self.page.open_payment_method()
        self.page.click_add_card()
        self.page.fill_card_number(data.CARD_NUMBER)
        self.page.fill_card_code(data.CARD_CODE)
        self.page.confirm_add_card()
        self.page.check_card_added()
        self.page.close_button()
        self.page.confirm_cartao()
        assert "Cartão" in self.page.confirm_cartao()

    def test_comment_for_driver(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.click_comfort_active()
        self.page.click_comment_button()
        self.page.fill_comment_field(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_comment_value() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.click_comfort_active()
        self.page.click_blanket_toggle()

    def test_order_2_ice_creams(self):
        munbers_of_ice_creams = 2
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.click_comfort_active()
        self.page.add_two_icecreams()
        assert self.page.get_icecream_value() == 2

    def test_car_search_model_appears(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()

        self.page.click_number_text(data.PHONE_NUMBER)

        self.page.open_payment_method()
        self.page.click_add_card()
        self.page.fill_card_number(data.CARD_NUMBER)
        self.page.fill_card_code(data.CARD_CODE)
        self.page.confirm_add_card()
        self.page.check_card_added()
        self.page.close_button()
        self.page.confirm_cartao()

        self.page.click_comment_button()
        self.page.fill_comment_field(data.MESSAGE_FOR_DRIVER)

        self.page.click_blanket_toggle()

        self.page.add_two_icecreams()

        self.page.call_taxi()
        assert "Buscar carro" in self.page.pop_up_show()


    def teardown_class(cls):
        cls.driver.quit()
