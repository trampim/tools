ativos_ibov = [
    "RRRP3.SA", "TTEN3.SA", "ABCB4.SA", "AESB3.SA", "ALOS3.SA", "ALPA4.SA", "ALUP11.SA",
    "ABEV3.SA", "AMBP3.SA", "ANIM3.SA", "ARZZ3.SA", "ARML3.SA", "ASAI3.SA", "AURE3.SA",
    "AZEV4.SA", "AZUL4.SA", "B3SA3.SA", "BPAN4.SA", "BRSR6.SA", "BBSE3.SA", "BMOB3.SA",
    "BLAU3.SA", "BBDC3.SA", "BBDC4.SA", "BRAP4.SA", "BBAS3.SA", "AGRO3.SA", "BRKM5.SA",
    "BRFS3.SA", "BPAC11.SA", "CXSE3.SA", "CAML3.SA", "CRFB3.SA", "CBAV3.SA", "CCRO3.SA",
    "CEAB3.SA", "CMIG3.SA", "CMIG4.SA", "CIEL3.SA", "CLSA3.SA", "COGN3.SA", "CSMG3.SA",
    "CPLE3.SA", "CPLE6.SA", "CSAN3.SA", "CPFE3.SA", "CMIN3.SA", "CURY3.SA", "CVCB3.SA",
    "CYRE3.SA", "DASA3.SA", "DXCO3.SA", "PNVL3.SA", "DIRR3.SA", "ECOR3.SA", "ELET3.SA",
    "ELET6.SA", "EMBR3.SA", "ENAT3.SA", "ENGI11.SA", "ENEV3.SA", "EGIE3.SA", "EQTL3.SA",
    "EVEN3.SA", "EZTC3.SA", "FESA4.SA", "FLRY3.SA", "FRAS3.SA", "GFSA3.SA", "GGBR4.SA",
    "GOAU4.SA", "GGPS3.SA", "GRND3.SA", "GMAT3.SA", "NTCO3.SA", "SBFG3.SA", "SOMA3.SA",
    "GUAR3.SA", "HAPV3.SA", "HBSA3.SA", "HYPE3.SA", "IGTI11.SA", "IFCM3.SA", "INTB3.SA",
    "MYPK3.SA", "RANI3.SA", "IRBR3.SA", "ITSA4.SA", "ITUB3.SA", "ITUB4.SA", "JALL3.SA",
    "JBSS3.SA", "JHSF3.SA", "JSLG3.SA", "KEPL3.SA", "KLBN11.SA", "LAVV3.SA", "RENT3.SA",
    "LOGG3.SA", "LREN3.SA", "LWSA3.SA", "MDIA3.SA", "MGLU3.SA", "POMO4.SA", "MRFG3.SA",
    "MATD3.SA", "CASH3.SA", "LEVE3.SA", "MILS3.SA", "BEEF3.SA", "MTRE3.SA", "MBLY3.SA",
    "MDNE3.SA", "MOVI3.SA", "MRVE3.SA", "MLAS3.SA", "MULT3.SA", "NEOE3.SA", "ODPV3.SA",
    "ONCO3.SA", "ORVR3.SA", "PCAR3.SA", "PGMN3.SA", "PETR3.SA", "PETR4.SA", "RECV3.SA",
    "PRIO3.SA", "PETZ3.SA", "PLPL3.SA", "PSSA3.SA", "PTBL3.SA", "POSI3.SA", "QUAL3.SA",
    "LJQQ3.SA", "RADL3.SA", "RAIZ4.SA", "RAPT4.SA", "RCSL3.SA", "RDOR3.SA", "ROMI3.SA",
    "RAIL3.SA", "SBSP3.SA", "SAPR11.SA", "SANB11.SA", "STBP3.SA", "SMTO3.SA", "SEER3.SA",
    "SRNA3.SA", "CSNA3.SA", "SIMH3.SA", "SLCE3.SA", "SMFT3.SA", "SUZB3.SA", "TAEE11.SA",
    "TASA4.SA", "TGMA3.SA", "VIVT3.SA", "TEND3.SA", "TIMS3.SA", "TOTS3.SA", "TRPL4.SA",
    "TRIS3.SA", "TUPY3.SA", "UGPA3.SA", "UNIP6.SA", "USIM3.SA", "USIM5.SA", "VALE3.SA",
    "VLID3.SA", "VAMO3.SA", "VBBR3.SA", "VIVA3.SA", "VVEO3.SA", "VULC3.SA", "WEGE3.SA",
    "PORT3.SA", "WIZC3.SA", "YDUQ3.SA", "ZAMP3.SA"
]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import yfinance as yf

data = {}
for i in ativos_ibov:
  data['df_' + str(i)] = yf.download(i, start='2022-08-21', end='2025-03-18')
  #data['df_' + str(i)] = yf.download(i, start='2022-09-11', end='2023-07-13')
 
tick = 0.01
for df_name, df_data in data.items():
    df = df_data.copy()  # Make a copy of the DataFrame to avoid modifying the original data
    df["buy_price"] = np.where(1==1, np.where(df["Open"] > df["High"].shift(1), df["Open"], df["High"].shift(1) + tick),np.nan)
    max_high = df["High"].rolling(4).max()
    min_low = df["Low"].rolling(4).min()
    amplitude = (max_high.shift(1) - min_low.shift(1))*1.62
    entry = df["High"].shift(1)
    df["target"] =  amplitude + entry
    df["stop"] = df["Low"].shift(2) - tick
    # Update the DataFrame in the data_frames dictionary with the modified one
    janela = 10
    resultados = []
    b, a = signal.butter(2, 0.0025)
    x = df["Close"].values.flatten()
    if len(x) > 200:
        padlen = min(150, len(x) - 1)
        try:
            padlen = 150
            df["filt"] = signal.filtfilt(b, a, x, padlen=padlen)
        except ValueError as e:
            print("Erro no filtfilt:", e)
            print("Tamanho do vetor:", len(x))
            print("Padlen utilizado:", padlen)
        
        #df["filt"] = signal.filtfilt(b, a, df["Close"].values, padlen=padlen)
        # Iterando sobre cada linha do dataframe
        std_dev = np.std(df['Close'].tail(200).values - df["filt"].tail(200).values)
        #df['std_dev_moving'] = (df['Close'] - df['filt']).rolling(window=150).std()
        df['upper_bands'] = df['filt'] + std_dev
        df['lower_bands'] = df['filt'] - std_dev
        #if df["Close"].tail(1).values[0] > df['upper_bands'].tail(1).values[0] or df["Close"].tail(1).values[0] < df['lower_bands'].tail(1).values[0]:
        plt.figure(figsize=(12, 6))
        plt.title(f'Análise do Filtro para {df_name}')
        plt.plot(df['Close'], label='Valores Originais')
        plt.plot(df['filt'], label='Valores Filtrados')
        plt.plot(df['upper_bands'], label='Banda Superior', linestyle='--')
        plt.plot(df['lower_bands'], label='Banda Inferior', linestyle='--')
        plt.legend()
        plt.show()
