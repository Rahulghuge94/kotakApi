import requests
import datetime
import os
import pandas as pd
from pytz import timezone

tze=timezone('Asia/Kolkata')

class Instrument:
    def __init__(self):
        self.df=self.get_df()
        
    def get_file(self):
        today=datetime.datetime.now(tze).date().strftime("%d_%m_%Y")
        print(today)
        file=requests.get(f"https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_{today}.txt")
        open("Instruments.txt","wb").write(file.content)
        return file

    def get_df(self):
        if not os.path.isfile("Instruments.txt"):
           self.get_file()
        df = pd.read_table("Instruments.txt",delimiter='|')
        return df
    
    def get(self,symbol,strike,expiry,option_type):
        tmp=self.df[(self.df["instrumentName"]==symbol) & (self.df["expiry"]==expiry) & (self.df["strike"]==strike) & (self.df["optionType"]==option_type)]
        return tmp
