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
    
    def get(self,symbol:str,strike:int,expiry:str,option_type:str):
        tmp=self.df[(self.df["instrumentName"]==symbol) & (self.df["expiry"]==expiry) & (self.df["strike"]==strike) & (self.df["optionType"]==option_type)]
        return tmp.to_dict("records")[0]
    
    def get_future(self,symbol:str,expiry:str):
        tmp=self.df[(self.df["instrumentName"]==symbol) & (self.df["expiry"]==expiry) & (self.df["optionType"]=="XX")]
        return tmp.to_dict("records")[0]

    def get_all_instrument_by_expiry(self,symbol:str,expiry:str):
        tmp=self.df[(self.df["instrumentName"]==symbol) & (self.df["expiry"]==expiry)]
        return tmp.to_dict("records")


        
#i=Instrument()
