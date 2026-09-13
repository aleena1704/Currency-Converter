from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json
from datetime import date, timedelta

app = Flask(__name__)


# ============================================================
# COUNTRY + CURRENCY DATA
# ============================================================

COUNTRIES = [
    ("Afghanistan", "AFN", "Afghan Afghani", "؋"),
    ("Albania", "ALL", "Albanian Lek", "Lek"),
    ("Algeria", "DZD", "Algerian Dinar", "دج"),
    ("Andorra", "EUR", "Euro", "€"),
    ("Angola", "AOA", "Angolan Kwanza", "Kz"),
    ("Antigua and Barbuda", "XCD", "East Caribbean Dollar", "$"),
    ("Argentina", "ARS", "Argentine Peso", "$"),
    ("Armenia", "AMD", "Armenian Dram", "֏"),
    ("Australia", "AUD", "Australian Dollar", "$"),
    ("Austria", "EUR", "Euro", "€"),
    ("Azerbaijan", "AZN", "Azerbaijani Manat", "₼"),
    ("Bahamas", "BSD", "Bahamian Dollar", "$"),
    ("Bahrain", "BHD", "Bahraini Dinar", "د.ب"),
    ("Bangladesh", "BDT", "Bangladeshi Taka", "৳"),
    ("Barbados", "BBD", "Barbadian Dollar", "$"),
    ("Belarus", "BYN", "Belarusian Ruble", "Br"),
    ("Belgium", "EUR", "Euro", "€"),
    ("Belize", "BZD", "Belize Dollar", "$"),
    ("Benin", "XOF", "West African CFA Franc", "CFA"),
    ("Bhutan", "BTN", "Bhutanese Ngultrum", "Nu."),
    ("Bolivia", "BOB", "Bolivian Boliviano", "Bs."),
    ("Bosnia and Herzegovina", "BAM", "Convertible Mark", "KM"),
    ("Botswana", "BWP", "Botswana Pula", "P"),
    ("Brazil", "BRL", "Brazilian Real", "R$"),
    ("Brunei", "BND", "Brunei Dollar", "$"),
    ("Bulgaria", "EUR", "Euro", "€"),
    ("Burkina Faso", "XOF", "West African CFA Franc", "CFA"),
    ("Burundi", "BIF", "Burundian Franc", "FBu"),
    ("Cambodia", "KHR", "Cambodian Riel", "៛"),
    ("Cameroon", "XAF", "Central African CFA Franc", "CFA"),
    ("Canada", "CAD", "Canadian Dollar", "$"),
    ("Chad", "XAF", "Central African CFA Franc", "CFA"),
    ("Chile", "CLP", "Chilean Peso", "$"),
    ("China", "CNY", "Chinese Yuan", "¥"),
    ("Colombia", "COP", "Colombian Peso", "$"),
    ("Comoros", "KMF", "Comorian Franc", "CF"),
    ("Costa Rica", "CRC", "Costa Rican Colón", "₡"),
    ("Croatia", "EUR", "Euro", "€"),
    ("Cyprus", "EUR", "Euro", "€"),
    ("Czech Republic", "CZK", "Czech Koruna", "Kč"),
    ("Denmark", "DKK", "Danish Krone", "kr"),
    ("Djibouti", "DJF", "Djiboutian Franc", "Fdj"),
    ("Dominica", "XCD", "East Caribbean Dollar", "$"),
    ("Dominican Republic", "DOP", "Dominican Peso", "RD$"),
    ("Ecuador", "USD", "US Dollar", "$"),
    ("Egypt", "EGP", "Egyptian Pound", "£"),
    ("El Salvador", "USD", "US Dollar", "$"),
    ("Estonia", "EUR", "Euro", "€"),
    ("Eswatini", "SZL", "Swazi Lilangeni", "E"),
    ("Ethiopia", "ETB", "Ethiopian Birr", "Br"),
    ("Fiji", "FJD", "Fijian Dollar", "$"),
    ("Finland", "EUR", "Euro", "€"),
    ("France", "EUR", "Euro", "€"),
    ("Gabon", "XAF", "Central African CFA Franc", "CFA"),
    ("Gambia", "GMD", "Gambian Dalasi", "D"),
    ("Georgia", "GEL", "Georgian Lari", "₾"),
    ("Germany", "EUR", "Euro", "€"),
    ("Ghana", "GHS", "Ghanaian Cedi", "₵"),
    ("Greece", "EUR", "Euro", "€"),
    ("Grenada", "XCD", "East Caribbean Dollar", "$"),
    ("Guatemala", "GTQ", "Guatemalan Quetzal", "Q"),
    ("Guinea", "GNF", "Guinean Franc", "FG"),
    ("Guyana", "GYD", "Guyanese Dollar", "$"),
    ("Haiti", "HTG", "Haitian Gourde", "G"),
    ("Honduras", "HNL", "Honduran Lempira", "L"),
    ("Hungary", "HUF", "Hungarian Forint", "Ft"),
    ("Iceland", "ISK", "Icelandic Króna", "kr"),
    ("India", "INR", "Indian Rupee", "₹"),
    ("Indonesia", "IDR", "Indonesian Rupiah", "Rp"),
    ("Iraq", "IQD", "Iraqi Dinar", "ع.د"),
    ("Ireland", "EUR", "Euro", "€"),
    ("Israel", "ILS", "Israeli New Shekel", "₪"),
    ("Italy", "EUR", "Euro", "€"),
    ("Jamaica", "JMD", "Jamaican Dollar", "$"),
    ("Japan", "JPY", "Japanese Yen", "¥"),
    ("Jordan", "JOD", "Jordanian Dinar", "د.ا"),
    ("Kazakhstan", "KZT", "Kazakhstani Tenge", "₸"),
    ("Kenya", "KES", "Kenyan Shilling", "KSh"),
    ("Kiribati", "AUD", "Australian Dollar", "$"),
    ("Kuwait", "KWD", "Kuwaiti Dinar", "د.ك"),
    ("Kyrgyzstan", "KGS", "Kyrgyzstani Som", "с"),
    ("Laos", "LAK", "Lao Kip", "₭"),
    ("Latvia", "EUR", "Euro", "€"),
    ("Lebanon", "LBP", "Lebanese Pound", "ل.ل"),
    ("Lesotho", "LSL", "Lesotho Loti", "L"),
    ("Liberia", "LRD", "Liberian Dollar", "$"),
    ("Libya", "LYD", "Libyan Dinar", "ل.د"),
    ("Liechtenstein", "CHF", "Swiss Franc", "CHF"),
    ("Lithuania", "EUR", "Euro", "€"),
    ("Luxembourg", "EUR", "Euro", "€"),
    ("Madagascar", "MGA", "Malagasy Ariary", "Ar"),
    ("Malawi", "MWK", "Malawian Kwacha", "MK"),
    ("Malaysia", "MYR", "Malaysian Ringgit", "RM"),
    ("Maldives", "MVR", "Maldivian Rufiyaa", "Rf"),
    ("Malta", "EUR", "Euro", "€"),
    ("Mauritius", "MUR", "Mauritian Rupee", "₨"),
    ("Mexico", "MXN", "Mexican Peso", "$"),
    ("Moldova", "MDL", "Moldovan Leu", "L"),
    ("Monaco", "EUR", "Euro", "€"),
    ("Mongolia", "MNT", "Mongolian Tögrög", "₮"),
    ("Montenegro", "EUR", "Euro", "€"),
    ("Morocco", "MAD", "Moroccan Dirham", "د.م."),
    ("Mozambique", "MZN", "Mozambican Metical", "MT"),
    ("Myanmar", "MMK", "Myanmar Kyat", "K"),
    ("Namibia", "NAD", "Namibian Dollar", "$"),
    ("Nepal", "NPR", "Nepalese Rupee", "₨"),
    ("Netherlands", "EUR", "Euro", "€"),
    ("New Zealand", "NZD", "New Zealand Dollar", "$"),
    ("Nicaragua", "NIO", "Nicaraguan Córdoba", "C$"),
    ("Nigeria", "NGN", "Nigerian Naira", "₦"),
    ("North Macedonia", "MKD", "Macedonian Denar", "ден"),
    ("Norway", "NOK", "Norwegian Krone", "kr"),
    ("Oman", "OMR", "Omani Rial", "ر.ع."),
    ("Pakistan", "PKR", "Pakistani Rupee", "₨"),
    ("Palau", "USD", "US Dollar", "$"),
    ("Panama", "PAB", "Panamanian Balboa", "B/."),
    ("Papua New Guinea", "PGK", "Papua New Guinean Kina", "K"),
    ("Paraguay", "PYG", "Paraguayan Guaraní", "₲"),
    ("Peru", "PEN", "Peruvian Sol", "S/"),
    ("Philippines", "PHP", "Philippine Peso", "₱"),
    ("Poland", "PLN", "Polish Złoty", "zł"),
    ("Portugal", "EUR", "Euro", "€"),
    ("Qatar", "QAR", "Qatari Riyal", "ر.ق"),
    ("Romania", "RON", "Romanian Leu", "lei"),
    ("Russia", "RUB", "Russian Ruble", "₽"),
    ("Rwanda", "RWF", "Rwandan Franc", "FRw"),
    ("Samoa", "WST", "Samoan Tala", "T"),
    ("San Marino", "EUR", "Euro", "€"),
    ("Saudi Arabia", "SAR", "Saudi Riyal", "ر.س"),
    ("Senegal", "XOF", "West African CFA Franc", "CFA"),
    ("Serbia", "RSD", "Serbian Dinar", "дин"),
    ("Seychelles", "SCR", "Seychellois Rupee", "₨"),
    ("Sierra Leone", "SLE", "Sierra Leonean Leone", "Le"),
    ("Singapore", "SGD", "Singapore Dollar", "$"),
    ("Slovakia", "EUR", "Euro", "€"),
    ("Slovenia", "EUR", "Euro", "€"),
    ("Solomon Islands", "SBD", "Solomon Islands Dollar", "$"),
    ("Somalia", "SOS", "Somali Shilling", "Sh"),
    ("South Africa", "ZAR", "South African Rand", "R"),
    ("South Korea", "KRW", "South Korean Won", "₩"),
    ("Spain", "EUR", "Euro", "€"),
    ("Sri Lanka", "LKR", "Sri Lankan Rupee", "₨"),
    ("Sudan", "SDG", "Sudanese Pound", "ج.س."),
    ("Suriname", "SRD", "Surinamese Dollar", "$"),
    ("Sweden", "SEK", "Swedish Krona", "kr"),
    ("Switzerland", "CHF", "Swiss Franc", "CHF"),
    ("Taiwan", "TWD", "New Taiwan Dollar", "NT$"),
    ("Tajikistan", "TJS", "Tajikistani Somoni", "ЅМ"),
    ("Tanzania", "TZS", "Tanzanian Shilling", "Sh"),
    ("Thailand", "THB", "Thai Baht", "฿"),
    ("Tonga", "TOP", "Tongan Paʻanga", "T$"),
    ("Trinidad and Tobago", "TTD", "Trinidad and Tobago Dollar", "$"),
    ("Tunisia", "TND", "Tunisian Dinar", "د.ت"),
    ("Turkey", "TRY", "Turkish Lira", "₺"),
    ("Turkmenistan", "TMT", "Turkmenistani Manat", "m"),
    ("Tuvalu", "AUD", "Australian Dollar", "$"),
    ("Uganda", "UGX", "Ugandan Shilling", "USh"),
    ("Ukraine", "UAH", "Ukrainian Hryvnia", "₴"),
    ("United Arab Emirates", "AED", "UAE Dirham", "د.إ"),
    ("United Kingdom", "GBP", "British Pound", "£"),
    ("United States", "USD", "US Dollar", "$"),
    ("Uruguay", "UYU", "Uruguayan Peso", "$"),
    ("Uzbekistan", "UZS", "Uzbekistani Som", "so'm"),
    ("Vanuatu", "VUV", "Vanuatu Vatu", "VT"),
    ("Vatican City", "EUR", "Euro", "€"),
    ("Venezuela", "VES", "Venezuelan Bolívar", "Bs."),
    ("Vietnam", "VND", "Vietnamese Đồng", "₫"),
    ("Yemen", "YER", "Yemeni Rial", "﷼"),
    ("Zambia", "ZMW", "Zambian Kwacha", "ZK"),
    ("Zimbabwe", "ZWG", "Zimbabwe Gold", "ZiG")
]


def get_country_data():
    return [
        {
            "name": country[0],
            "currency": country[1],
            "currency_name": country[2],
            "symbol": country[3]
        }
        for country in COUNTRIES
    ]


# ============================================================
# HELPER: GET JSON FROM API
# ============================================================

def get_json(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CurrencyConverter/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    countries = get_country_data()

    return render_template(
        "index.html",
        countries=countries
    )


# ============================================================
# CONVERT
# ============================================================

@app.route("/convert", methods=["POST"])
def convert():

    try:

        data = request.get_json()

        amount = float(data.get("amount", 0))

        from_currency = str(
            data.get("from_currency", "")
        ).upper()

        to_currency = str(
            data.get("to_currency", "")
        ).upper()


        if amount <= 0:

            return jsonify({
                "success": False,
                "message": "Please enter an amount greater than 0."
            })


        if not from_currency or not to_currency:

            return jsonify({
                "success": False,
                "message": "Please select both currencies."
            })


        # Same currency

        if from_currency == to_currency:

            return jsonify({
                "success": True,
                "result": round(amount, 2),
                "rate": 1,
                "from": from_currency,
                "to": to_currency
            })


        # Frankfurter v2 single-rate endpoint

        url = (
            "https://api.frankfurter.dev/v2/rate/"
            + urllib.parse.quote(from_currency)
            + "/"
            + urllib.parse.quote(to_currency)
        )


        result = get_json(url)


        rate = result.get("rate")


        if rate is None:

            return jsonify({
                "success": False,
                "message":
                    f"Exchange rate for "
                    f"{from_currency} to "
                    f"{to_currency} is not available."
            })


        rate = float(rate)

        converted_amount = amount * rate


        return jsonify({

            "success": True,

            "result": round(
                converted_amount,
                2
            ),

            "rate": rate,

            "from": from_currency,

            "to": to_currency

        })


    except urllib.error.HTTPError as e:

        if e.code == 404 or e.code == 422:

            return jsonify({
                "success": False,
                "message":
                    "This currency pair is not supported by the exchange-rate service."
            })


        return jsonify({
            "success": False,
            "message":
                "Exchange-rate service returned an error."
        })


    except Exception as e:

        print("CONVERSION ERROR:", e)

        return jsonify({
            "success": False,
            "message":
                "Unable to get the exchange rate right now. "
                "Please try again."
        })


# ============================================================
# CHART
# ============================================================

@app.route("/chart", methods=["POST"])
def chart():

    try:

        data = request.get_json()

        from_currency = str(
            data.get("from_currency", "")
        ).upper()

        to_currency = str(
            data.get("to_currency", "")
        ).upper()


        if not from_currency or not to_currency:

            return jsonify({
                "success": False,
                "message":
                    "Please select both currencies."
            })


        if from_currency == to_currency:

            return jsonify({
                "success": False,
                "message":
                    "Please select two different currencies."
            })


        # ----------------------------------------------------
        # Get approximately the last 30 days
        # ----------------------------------------------------

        today = date.today()

        start_date = today - timedelta(days=30)


        url = (
            "https://api.frankfurter.dev/v2/rates?"
            + urllib.parse.urlencode({

                "base": from_currency,

                "quotes": to_currency,

                "from": start_date.isoformat(),

                "to": today.isoformat()

            })
        )


        print("CHART URL:", url)


        rows = get_json(url)


        if not isinstance(rows, list):

            return jsonify({
                "success": False,
                "message":
                    "The exchange-rate service returned invalid chart data."
            })


        labels = []

        values = []


        for row in rows:

            if (
                row.get("date")
                and row.get("rate") is not None
            ):

                labels.append(
                    row["date"]
                )

                values.append(
                    float(row["rate"])
                )


        if len(labels) == 0:

            return jsonify({
                "success": False,
                "message":
                    "No historical exchange-rate data is available for this currency pair."
            })


        return jsonify({

            "success": True,

            "labels": labels,

            "values": values,

            "from": from_currency,

            "to": to_currency

        })


    except urllib.error.HTTPError as e:

        print(
            "CHART HTTP ERROR:",
            e.code
        )


        return jsonify({

            "success": False,

            "message":
                "Historical chart data is not available for this currency pair."

        })


    except Exception as e:

        print(
            "CHART ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to load chart data right now."

        })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )