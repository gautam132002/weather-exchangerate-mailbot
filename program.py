import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re

# wzogippwniqeglid

OPENWEATHERMAP_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

OPENWEATHERMAP_API_KEY = "4b0a9096534179f10a0ac5255a8d218b"


GMAIL_ADDRESS = "demoscript2002@gmail.com"
GMAIL_PASSWORD = "wzogippwniqeglid"

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_api(api):
    return api.lower() == "openweathermap" or api.lower() == "finage"

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius,2)


def get_weather_data(CITY):
    try:
        response = requests.get(OPENWEATHERMAP_ENDPOINT, params={"q": CITY, "appid": OPENWEATHERMAP_API_KEY})
        response.raise_for_status()
        data = response.json()

        return f"Current weather in your city: {data['weather'][0]['description']}. Temperature: {str(kelvin_to_celsius(float(data['main']['temp'])))}°C"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def get_financial_data(BASE):
    try:


        url = f"https://api.apilayer.com/exchangerates_data/latest?base={BASE}"

        payload = {}
        headers= {
        "apikey": "APILAYER_API_KEY"
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        status_code = response.status_code
        result = response.json()
        bs = result["base"]
        data = result["rates"]
        txt = ""

        for i in data:
            txt += f"The latest exchange rate of {base.upper()}/{i} => {data[i]}\n"

        return txt

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate data : {e}")
        return None


def send_email(subject, message, to_email, from_email, password, attachment=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    body = MIMEText(message, _subtype='plain')
    msg.attach(body)

    if attachment:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read(), Name=attachment)
            part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()
    print(f'Sent email to {to_email} successfully!')

if __name__ == "__main__":
    print("init")
    if len(sys.argv) != 3:
        print("Usage: python program.py email_address api_name")
        sys.exit(1)

    email_address = sys.argv[1]
    api_name = sys.argv[2]

    print(f"email - > {email_address}")
    print(f"api - > {api_name}")


    if not is_valid_email(email_address):
        print("Invalid email address")
        sys.exit(1)

    if not is_valid_api(api_name):
        print("Invalid API name")
        sys.exit(1)

    if api_name.lower() == "openweathermap":
        city = input("enter the name of your city : ")
        data = get_weather_data(city)
        print(data)
    elif api_name.lower() == "finage":
        base = input("enter the symbol for base : ")
        data = get_financial_data(base)
        print(data)

    if data is not None:
        message = data
        subject = f"Here is your data from {api_name}."

        send_email(subject, message, email_address, GMAIL_ADDRESS, GMAIL_PASSWORD)
