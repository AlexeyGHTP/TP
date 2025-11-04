import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import json
import requests
from bs4 import BeautifulSoup as bs

class pars():
    def __init__(self):
        pass
    def pars_cb(self):
        url = 'https://cbr.ru/currency_base/daily/'
        try:
            page = requests.get(url)
        except:
            print("Страница недоступна!")
        soup = bs(page.text, "html.parser")
        table = soup.find('div', class_='table')
        rows = table.find_all('tr')
        self.list = {}
        date = soup.find("button", class_="datepicker-filter_button").text
        name = soup.find("span", class_="referenceable").text
        for index, i in enumerate(rows):
            local_t = i.find_all('td')
            if local_t != []:
                self.list[local_t[1].text] = [j.text for j in local_t[2:]]
                self.list[local_t[1].text][0] = int(self.list[local_t[1].text][0])
                self.list[local_t[1].text][2] = float(self.list[local_t[1].text][2].replace(",", "."))
        with open(f"{name}_{date}.json", "w", encoding="utf-8") as f:
            json.dump(self.list, f, ensure_ascii=False, indent=4)
pars = pars()
pars.pars_cb()
# Пример заглушки (замените на вашу реализацию)
def get_exchange_rate(from_curr: str, to_curr: str) -> float:
    # Пример фиксированных курсов (замените на реальный парсинг)
    from_curr_rub = pars.list[from_curr][2]/pars.list[from_curr][0]
    to_curr_rub = pars.list[to_curr][2]/pars.list[to_curr][0]
    return from_curr_rub/to_curr_rub

def get_supported_currencies():
    return pars.list.keys()

# === Streamlit UI ===
st.set_page_config(page_title="💱 Конвертер валют", page_icon="💱", layout="centered")

# Заголовок с акцентом
colored_header(
    label="💱 Конвертер валют",
    description="Мгновенно конвертируйте между валютами",
    color_name="blue-70",
)

add_vertical_space(1)

# Получаем список валют
currencies = get_supported_currencies()

# Выбор валют
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("Из валюты", currencies, index=0)

with col2:
    to_currency = st.selectbox("В валюту", currencies, index=1)

# Ввод суммы
amount = st.number_input(
    f"Сумма в {from_currency}({pars.list[from_currency][1]})",
    min_value=0.0,
    value=100.0,
    step=10.0,
    format="%.2f"
)

# Расчёт
if from_currency == to_currency:
    converted = amount
else:
    rate = get_exchange_rate(from_currency, to_currency)
    converted = amount * rate

# Отображение результата
st.markdown("---")
st.subheader("Результат")
st.markdown(
    f"""
    <div style="
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    ">
        {amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}
    </div>
    """,
    unsafe_allow_html=True
)

# Дополнительно: показать курс
if from_currency != to_currency:
    st.caption(f"Курс: 1 {pars.list[from_currency][1]} = {rate:.4f} {pars.list[to_currency][1]}")
