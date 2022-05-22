import configparser
import time
from iqoptionapi.stable_api import IQ_Option

config= configparser.ConfigParser()
config.read('config.ini')
email = config["GERAL"]["email"]
senha = config["GERAL"]["senha"]
tipodeconta = config["GERAL"]["tipodeconta"]
timeframe = int(config["GERAL"]["timeframe"]) 
entrada = float(config["GERAL"]["entrada"]) 
stopwin = float(config["GERAL"]["stopwin"]) 
stoploss = float(config["GERAL"]["stoploss"]) 
martingales= config["GERAL"]["martingales"]  

API = IQ_Option(email, senha)
API.connect()

status = False
agora = None
lucro = 0

contadorcall = 0
contadorput = 0 

vela = API.get_candles("EURUSD",(60*timeframe),1,time.time())
print("Aguardando encerramento da vela vigente.")
while agora != vela[0]['to']:
    agora = int(time.time())
print("Vela vigente encerrada.\n")

while True:
    if contadorcall == 2 and contadorput == 2:
        contadorcall, contadorput = 0,0
    if contadorcall == 2:
        contadorput+=1
        print("Compra direção PUT")
        check, id= API.buy (entrada, "EURUSD", "PUT",timeframe)
        status, lucro_ = API.check_win_v4(id)
        if status == "win":
            lucro += lucro_
            resultado = "Win"
        elif status == "loose":
            lucro += lucro_
            resultado = "Loss"
        else:
            lucro += 0
            resultado = "Doji"
        print(f"Resultado Operação: {resultado}\nLucro: R${lucro:.2f}\n")
    else: 
        contadorcall +=1 
        print("Compra direção CALL")
        check, id= API.buy (entrada, "EURUSD", "CALL", timeframe)
        status, lucro_ = API.check_win_v4(id)
        if status == "win":
            lucro += lucro_
            resultado = "Win"
        elif status == "loose":
            lucro += lucro_
            resultado = "Loss"
        else:
            lucro += 0
            resultado = "Doji"
        print(f"Resultado Operação: {resultado}\nLucro: R${lucro:.2f}\n")
