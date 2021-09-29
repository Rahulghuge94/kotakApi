#kotak securities api.
import requests
from retry import retry
import datetime,time
import json
import sys,os

#path to store session token. it saves token where module is installed.
m_path=__file__
m_name=__file__.split("\\")[-1]
m_path=m_path.replace("\\"+m_name,"")

routes={"login":"/session/1.0/session/login/userid","2fa":"/session/1.0/session/2FA/oneTimeToken","orderbook":"","order":"",
        "orderbook":"/reports/1.0/orders","position":"/positions/1.0/positions","fund":"/margin/1.0/margin","tradebook":"/reports/1.0/trades",
        "ltp":"","no":"/orders/1.0/order/normal","miso":"/orders/1.0/order/mis","mtfo":"/orders/1.0/order/mtf","soro":"/orders/1.0/order/sor",
        "qtdepth":"/depth/instruments/{instrumentTokens","qtohlc":"/ohlc/instruments/{instrumentTokens","qtltp":"/ltp/instruments/{instrumentTokens",
        "qtful":"/instruments/{instrumentTokens"}

class kotak_client(object):
    
    def __init__(self,userid:str=None,password:str=None,access_token:str=None,consumer_key:str=None,access_code:str=None,app_id:str=None,ip:str= "127.0.0.1"):
        self.session=requests.session()
        self.userid=userid
        self.password=password
        self.access_token=access_token
        self.consumer_key=consumer_key
        self.app_id=app_id
        self.ip=ip
        self.url="https://tradeapi.kotaksecurities.com/apim"
        self.ott=None
        self.access_code=access_code
        self.sessiontoken=self.get_session()
        
    def login(self):
        data=json.dumps({"userid":str(self.userid),"password":str(self.password)})
        headers = { "Accept": "application/json","consumerKey": self.consumer_key,"ip": "1.1.1.1", "appId": "KotakAPI","Content-Type": "application/json", "Authorization": "Bearer "+self.access_token,}
        res=self.session.post("https://tradeapi.kotaksecurities.com/apim/session/1.0/session/login/userid",headers=headers,data=data)
        if res.status_code==200:
           self.ott=res.json()["Success"]["oneTimeToken"]
        self.session_2fa()

    def session_2fa(self):
        headers = { "accept": "application/json","oneTimeToken": self.ott,"consumerKey": self.consumer_key,"ip": "1.1.1.1", "appId": "KotakAPI","Content-Type": "application/json", "Authorization": "Bearer "+self.access_token,}
        data=None
        if not self.access_code:
           data=json.dumps({"userid":str(self.userid),"accessCode":str(self.access_code)})
        else:
           data=json.dumps({"userid":str(self.userid)})
        res=self.session.post("https://tradeapi.kotaksecurities.com/apim/session/1.0/session/2FA/oneTimeToken", headers=headers, data=data)
        if res.status_code==200:
           sessiontoken=res.json()["success"]["sessionToken"]
           self.write_session(sessiontoken)
        print("Logged In")

    def write_session(self,sessiontoken):
        file=open(f"{m_path}\\session_.json","w")
        json.dump({"sessiontoken":sessiontoken},file)
        
    def api_headers(self):
        headers = { "accept": "application/json","Content-Type": "application/json","consumerKey": self.consumer_key,"sessionToken":self.get_session(),"Authorization": "Bearer "+self.access_token,}
        return headers

    @retry(delay=3,tries=3)
    def api_helper(self,method:str,route:str,data:dict=None,str_param:str=None):
        if str_param==None:
           str_param=""
        print(str_param)
        if method=="POST":
           headers=self.api_headers()
           resp=self.session.post(self.url+routes[route],headers=headers,data=data)
           if resp.status_code==403:
              self.login()
              resp=self.session.post(self.url+routes[route],headers=headers,data=data)
           return resp
        elif method=="GET":
           headers=self.api_headers()
           print(self.url+routes[route]+str_param)
           resp=self.session.get(self.url+routes[route]+str_param,headers=headers)
           if resp.status_code==403:
              self.login()
              resp=self.session.get(self.url+routes[route]+str_param,headers=headers)
           return resp
        elif method=="PUT":
           headers=self.api_headers()
           resp=self.session.put(self.url+routes[route],headers=headers,data=data)
           if resp.status_code==403:
              self.login()
              resp=self.session.put(self.url+routes[route],headers=headers,data=data)
           return resp
        elif method=="DELETE":
           headers=self.api_headers()
           resp=self.session.delete(self.url+routes[route]+str_param,headers=headers)
           if resp.status_code==403:
              self.login()
              resp=self.session.delete(self.url+routes[route]+str_param,headers=headers)
           return resp
        else:
           return "Unknown Http method."
           
    def get_session(self):
        if not os.path.isfile(f"{m_path}\\session_.json"):
           print("Not found session token. Generate session token.")
           return None
        if os.path.isfile(f"{m_path}\\session_.json"):
           try:
               file=open(f"{m_path}\\session_.json","r")
               dic=json.load(file)
               return dic["sessiontoken"]
           except:
              print("error while accessing file 'session_.json'. please delete file.")

    def fund(self,str_param=None):
        return self.api_helper("GET",route="fund")

    def position(self,str_param=None):
        return self.api_helper("GET",route="position",str_param=str_param)
    
    def orderbook(self,str_param=None):
        return self.api_helper("GET",route="orderbook")
    
    def tradebook(self,str_param=None):
        return self.api_helper("GET",route="tradebook")

    def order(self,price:float,qty:int,bs:str,scripcode:int,,triggerprc:float=0,ordertype:str="N",variety:str="REGULAR",validity:str="GFD"):
        route=""
        if ordertype=="N":
           route="no"
        elif ordertype=="MIS":
           route="miso"
        elif ordertype=="MTF":
           route="mtfo"
        elif ordertype=="SOR":
           route="soro"
        trsnstp={"B":"BUY","S":"SELL"}
        data=json({"instrumentToken":scripcode,"transactionType":trsnstp[bs],"quantity":qty,"price":price,"validity":validity,"variety":variety,"disclosedQuantity":0,"triggerPrice":trggerprc,"tag":"string"})
        return self.api_helper("POST",route=route,data=data)
    
    def modify_order(self,orderid:str,price:float,qty:int,triggerprc:float=0,ordertype:str="N",validity:str="GFD"):
        route=""
        if ordertype=="N":
           route="no"
        elif ordertype=="MIS":
           route="miso"
        elif ordertype=="MTF":
           route="mtfo"
        elif ordertype=="SOR":
           route="soro"
        data=json({"orderId":orderid,"quantity":qty,"price":price,"validity":validity,"disclosedQuantity":0,"triggerPrice":trggerprc})
        return self.api_helper("PUT",route=route,data=data)
    
    def cancel_order(self,orderid:str):
        route=""
        if ordertype=="N":
           route="no"
        elif ordertype=="MIS":
           route="miso"
        elif ordertype=="MTF":
           route="mtfo"
        elif ordertype=="SOR":
           route="soro"
        return self.api_helper("DELETE",route=route,str_param=str(orderid))
    
    def quote(self,scripcode:str,quote_type="LTP"):
        route=''
        if quote_type=="LTP":
           route="qtltp"
        elif quote_type=="FULL":
           route="qtful"
        elif quote_type=="DEPTH":
           route="qtdepth"
        elif quote_type=="OHLC":
           route="qtohlc"
        else:
           return "provide correct quote type."
        return self.api_helper("DELETE",route=route,str_param=str(scripcode))
