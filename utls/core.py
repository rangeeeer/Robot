from utls.SimpleBinanceTraderRobot import simpleBinanceTraderRobot as SMTR

apikey = "2Aqb2zFfazi6krRSQL09M9tiFmRZ1NwdOV0cSrsDVk9s0Rk5DrK3kYHhIeplAJsJ"
apisecret = "ScDSqn4SHGztgMjCRrEboSlVyRmrpIzJ1W28fk34QrN7b4Xm5ZStltXkrt5fC0Lp"

def starter():
    file=open('COINS.txt','r')
    symbols=file.read().split('\n')
    file.close()
    smtr = SMTR(api_key=apikey, api_secret=apisecret,interval=symbols[-1],coin_list=symbols[:-1])
    smtr.run()
