import requests
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime


def currency_data(code, data_frame):
    curr_page = f"http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/last/{topCount}/?format=json"
    data = requests.get(curr_page).json()["rates"]
    new_df = pd.DataFrame(data)
    data_name = f"{code.upper()}\PLN"
    new_df.rename(columns={"effectiveDate": "Date", "mid": data_name}, inplace=True)
    new_df = new_df.loc[:, ["Date", data_name]]

    try:
        data_frame = data_frame.merge(new_df)
    except pd.errors.MergeError:
        data_frame = new_df

    return data_frame


def show_plot(df):
    plt.style.use("seaborn-whitegrid")
    figure, ax = plt.subplots(constrained_layout=True)
    ax.plot(corona["Active"].sum(), color='r')
    ax.legend(["Active cases"], loc='upper left')
    ax.set_yscale('log')
    ax2 = ax.twinx()
    ax2.plot(df["Date"], df.drop(columns=["Date"]))
    print(df)
    ax2.legend(df.columns[1:], loc='upper right')
    plt.show()


print("Getting data about coronavirus")
api = "https://api.covid19api.com/all"
corona = requests.get(api).json()
corona = pd.DataFrame(corona)
print("Cleaning data")
corona = corona.loc[:, ['Country', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Date']]
corona["Date"] = pd.to_datetime(corona["Date"])
latest_date = datetime.strptime(corona["Date"].min().strftime("%Y-%m-%d"), "%Y-%m-%d")
corona = corona.groupby(["Country", "Date"]).sum()
corona = corona.groupby(["Date"])

today = datetime.now()
# topCount = 100
topCount = (today - latest_date).days

print("Getting currency data")
currency = pd.DataFrame()
table = "a"
currency = currency_data('usd', currency)
currency = currency_data('eur', currency)
currency["Date"] = pd.to_datetime(currency["Date"])
print(currency)

print("Plot with coronavirus and currency rate")
show_plot(currency)

print("Getting gold prices")
gold_page = f"http://api.nbp.pl/api/cenyzlota/last/{topCount}"
gold = requests.get(gold_page).json()
gold_df = pd.DataFrame(gold)
gold_df.rename(columns={"data": "Date", "cena": "Gold price"}, inplace=True)
gold_df["Date"] = pd.to_datetime(gold_df["Date"])

print("Plot with coronavirus and gold prices")
show_plot(gold_df)
