import pytest
from pages.main_page import MainPage


# Тест 1: Проверка корректного отображения параметров URL
def test_display_url_parameters(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    assert page.get_rub_balance() == "30'000", "Рублевый баланс не отображается корректно"
    assert page.get_rub_reserved() == "20'001", "Резервная сумма не отображается корректно"


# Тест 2: Проверка корректного отображения валют
def test_currency_display(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    assert page.get_usd_balance() == "100", "Долларовый баланс не отображается корректно"
    assert page.get_euro_balance() == "300", "Евро баланс не отображается корректно"


# Тест 3: Проверка ограничения резервной суммы
def test_reserve_limit(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=35000")

    assert page.get_rub_balance() == "30'000", "Рублевый баланс не отображается корректно"
    assert page.get_rub_reserved() == "30'000", "Резерв должен быть ограничен балансом"


# Тест 4: Перевод с достаточными средствами
def test_successful_transfer(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("1000")
    page.click_transfer_button()

    assert page.get_success_message() == "Перевод принят", "Перевод не был успешно выполнен"


# Тест 5: Перевод с недостаточными средствами
def test_insufficient_funds_transfer(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=29000")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("2000")

    assert not page.is_transfer_button_enabled(), "Кнопка перевода должна быть неактивна"
    assert page.get_error_message() == "Недостаточно средств на счете", "Не отображено сообщение об ошибке"


# Тест 6: Корректность расчета комиссии (10%)
def test_commission_calculation(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("1000")

    assert page.get_commission() == "100 ₽", "Комиссия рассчитана некорректно"


# Тест 7: Ввод некорректного номера карты (17 цифр)
def test_invalid_card_number(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1234 5678 9012 3451 3")  # 17 цифр
    page.enter_amount("1000")

    assert page.get_card_error() == "Некорректный номер карты", "Не отображено сообщение об ошибке"


# Тест 8: Отрицательная сумма перевода
def test_negative_amount_transfer(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("-100")

    assert page.get_amount_error() == "Сумма перевода должна быть положительной", "Не отображено сообщение об ошибке"


# Тест 9: Максимальная сумма перевода
def test_max_transfer_amount(driver):
    page = MainPage(driver)
    page.open("http://localhost:8080/?balance=30000&reserved=0")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("30000")

    assert page.get_error_message() == "Недостаточно средств на счете", "Не отображено сообщение об ошибке"


# Тест 10: Перевод с нулевой резервной суммой
def test_transfer_with_zero_reserve(driver):
    page = MainPage(driver)
    page.open("http://localhost:8080/?balance=30000&reserved=0")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("10000")
    page.click_transfer_button()

    assert page.get_success_message() == "Перевод принят", "Перевод не был успешно выполнен"


# Тест 11: Перевод с длиной номера карты (16 символов)
def test_valid_card_length(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1234567890123456")
    page.enter_amount("1000")
    page.click_transfer_button()

    assert page.get_success_message() == "Перевод принят", "Перевод не был успешно выполнен"


# Тест 12: Минимальная сумма перевода и округление комиссии до 0
def test_minimum_transfer_rounding(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=1&reserved=0")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("1")
    page.click_transfer_button()

    assert page.get_success_message() == "Перевод принят", "Перевод не был успешно выполнен"


# Тест 13: Попытка перевода с евро или долларового счета
def test_foreign_currency_transfer_disabled(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_euro_account()

    assert not page.is_card_input_visible(), "Поле ввода номера карты должно быть скрыто"
    assert not page.is_amount_input_visible(), "Поле ввода суммы должно быть скрыто"


# Тест 14: Ввод пустого номера карты
def test_empty_card_number(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_amount("1000")

    assert not page.is_transfer_button_enabled(), "Кнопка перевода должна быть неактивна"


# Тест 15: Ввод букв вместо номера карты
def test_letters_in_card_number(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("abcd efgh ijkl mnop")

    assert page.get_card_error() == "Некорректный номер карты", "Не отображено сообщение об ошибке"


# Тест 16: Дробная сумма перевода
def test_fractional_amount(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("100.5")

    assert not page.is_transfer_button_enabled(), "Кнопка перевода должна быть неактивна"


# Тест 17: Сумма + комиссия превышает доступную сумму
def test_exceeding_balance(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("10001")

    assert page.get_error_message() == "Недостаточно средств на счете", "Не отображено сообщение об ошибке"


# Тест 18: Попытка перевода без выбора счета
def test_no_account_selected(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    card_input_visible = page.is_card_input_visible()
    amount_input_visible = page.is_amount_input_visible()
    transfer_button_enabled = page.is_transfer_button_enabled()

    assert not card_input_visible, "Поле ввода номера карты должно быть скрыто"
    assert not amount_input_visible, "Поле ввода суммы должно быть скрыто"
    assert not transfer_button_enabled, "Кнопка перевода должна быть неактивна"


# Тест 19: Ввод букв вместо суммы перевода
def test_letters_in_amount_field(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=30000&reserved=20001")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("dfsdfs")

    assert not page.is_transfer_button_enabled(), "Кнопка перевода должна быть неактивна"


# Тест 20: Перевод с минимальной суммой и комиссией 0
def test_minimal_amount_zero_commission(driver):
    page = MainPage(driver)
    page.open("http://localhost:8000/?balance=1&reserved=0")

    page.select_ruble_account()
    page.enter_card_number("1111 1111 1111 1111")
    page.enter_amount("1")
    page.click_transfer_button()

    assert page.get_success_message() == "Перевод принят", "Перевод не был успешно выполнен"