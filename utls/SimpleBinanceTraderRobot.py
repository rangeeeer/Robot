from binance.websockets import BinanceSocketManager
from clint.textui import colored, puts
from binance.client import Client
from utls.algorythm import *
from binance.enums import *

import pandas as pd

import time
import os


class simpleBinanceTraderRobot:

    def __init__(self, api_key="api-key",
                api_secret="api-secret",
                test=True, interval=KLINE_INTERVAL_30MINUTE,coin_list=None):

        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client("api-key", "api-secret")
        self.__interval=interval
        self.msinterval = self.__interval_to_miliseconds()
        self.dict_dataframes = dict()
        self.__conkey=None
        self.CoinList=coin_list 
        self.__ping=0.0
        self.__MAX_DF_DATA_SIZE=self.msinterval
        __t=self.msinterval*round(time.time()*1000/self.msinterval)
        for i in self.CoinList:
            #histo=self.client.get_historical_klines(i, '1d', str(__t), str(__t+self.msinterval*50))
            self.dict_dataframes[i]=pd.DataFrame(data={   'time':[float(__t)],
                                                          'open':[float()],
                                                          'low':[float()],
                                                          'high':[float()],
                                                          'close':[float()],
                                                          'signal':['nan'],
            }) 
            pd.set_option('mode.chained_assignment', None)
                          
    def __main(self):
        
        for i in self.CoinList:
            df=self.dict_dataframes[i]
            sign=emacros(self.dict_dataframes[i])
            df.at[-1,'signal']=sign
            self.dict_dataframes[i]=df    
    def run(self):
        def ticker_process(msg):
            #os.system('cls')
            t = time.time()
            sym =self.__msg_parser(msg)
            self.__symdf_update(sym)
            self.__main()
            os.system('cls')
            self.__visulise()
            print("ping  = ",round((time.time()-self.__ping)*1000),'ms')
            self.__ping=time.time()
            print("ptime = ",round((time.time()-t)*1000),'ms')    
        bm = BinanceSocketManager(self.client)
        self.__conkey = bm.start_ticker_socket(ticker_process)
        bm.run()
    def __symdf_update(self,msg):
        for coindic in msg:
            df=self.dict_dataframes[coindic['s']]
            msgftime=self.msinterval*round(coindic['E']/self.msinterval)
            maxtime=float(float(df.iloc[-1]['time'])+self.msinterval)
            msgmtime=float(coindic['E'])
            if msgmtime<maxtime:
                if  float(df.at[df.index[-1],'low'])>float(coindic['c']):
                    df.at[df.index[-1],'low']=coindic['c']
                if  float(df.at[df.index[-1],'high'])<float(coindic['c']):
                    df.at[df.index[-1],'high']=coindic['c']
                df.at[df.index[-1],'clsoe']=coindic['c'] 
            else:
                df=df.append({
                            'time':msgftime,
                            'open':coindic['c'],
                            'low':coindic['c'],
                            'high':coindic['c'],
                            'close':coindic['c'],
                            'signal':'nan',
                            },ignore_index=True)
            self.dict_dataframes[coindic['s']]=df
            self.dict_dataframes[coindic['s']]=self.dict_dataframes[coindic['s']].tail(50) 
    def __visulise(self):
        os.system('mode con: cols=22 lines={}'.format(3+len(self.CoinList)))
        for coindic in self.dict_dataframes:
            if self.dict_dataframes[coindic].shape[0]>2:
                signal=self.dict_dataframes[coindic].iloc[-1]['signal']
                if signal=='buy':
                    print(colored.blue(coindic+"----buy"))
                if signal=='sell':
                    print(colored.red(coindic+"----sell"))
                if signal=='nan':
                    print(colored.yellow(coindic+"----nan"))
    def __msg_parser(self,msg):
        ret=list()
        for dic in msg:
            if(dic['s'] in self.CoinList):
                ret.append(dic)
        return ret                          
    def __interval_to_miliseconds(self):
        s = None
        seconds_per_unit = {
            "s": 1,
            "m": 60,
            "h": 60 * 60,
            "d": 24 * 60 * 60,
            "w": 7 * 24 * 60 * 60
        }
        i=self.__interval
        unit = i[-1]
        if unit in seconds_per_unit:
            try:
                s = int(i[:-1]) * seconds_per_unit[unit]*1000
            except ValueError:
                pass
        return s