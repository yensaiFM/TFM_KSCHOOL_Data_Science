#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:22:57 2020

@author: yensai

Este script se ejecutará de L-V para obtener los datos históricos del mes actual
"""
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import time
from logging.handlers import TimedRotatingFileHandler
import yaml
import sys

# Función que configura los logs para que roten cada medianoche
def set_timed_rotating_log(path):
    logger = logging.getLogger("Export historical data")
    logger.setLevel(logging.DEBUG)
    
    handler = TimedRotatingFileHandler(path, when='midnight', interval=1, backupCount=5, encoding='UTF-8')
    formatter = '%(asctime)s %(name)-2s %(levelname)-2s %(message)s'
    handler.setFormatter(logging.Formatter(formatter, '%Y-%m-%d %H:%M:%S'))
    handler.suffix = '%Y_%m_%d.log'
    logger.addHandler(handler)
    return logger

# Función que lee distintas configuraciones en formato YAML
def get_yaml_configs(path):
    # Cargamos todas las configuraciones
    with open(path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

def save_data_in_csv(df, cols, stock_market, year_month ):
    # Validamos si existe el directorio y si no existe lo creamos
    dir_filename = './dataset/'+stock_market
    if not os.path.exists(dir_filename):
        os.makedirs(dir_filename)
    filename = './dataset/'+stock_market+'/'+stock_market+'_'+year_month+'.csv'
    df.to_csv(filename, mode='w', header=cols, index=False)


def main():
    logger = set_timed_rotating_log('logs/historical_data.log')
    cfg = get_yaml_configs('conf/config_historical_data.yml')
    day = datetime.now().day
    this_year_month = datetime.today().strftime('%Y%m')
    last_year_month = (datetime.today() - timedelta(days=day)).strftime('%Y%m')
    

    logger.info('Inicio web scraping')
    for stock_market in cfg:
        logger.info('-' + stock_market + ':')
        # Establecemos la variable 
        init_time = time.time()
        logger.info('-- url:' + cfg[stock_market]['url'])
        response = Request(cfg[stock_market]['url'], headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urlopen(response).read()
            webpage = html.decode('utf-8')
            #webpage = html
        except HTTPError as e:
            logger.error('The server couldn\'t fulfill the request.' + cfg[stock_market]['url'])
            logger.error('Error code: ', e.code)
        except URLError as e:
            logger.error('We failed to reach a server' + cfg[stock_market]['url'])
            logger.error('Reason: ', e.reason)
            
    
        page_soup =  BeautifulSoup(webpage)
        table = page_soup.find('table', id='curr_table')
    
        if table:
            # Creamos una lista vacia para ir añadiendo los datos de los registros
            data_row=[]
            for tr in table.find_all('tr'):
                td = tr.find_all('td')
                row = [data_tr.text.strip('\n') for data_tr in td if tr.text.strip('\n')]
                if row:
                    data_row.append(row)
        
        # Convertimos la información en un dataframe
        df = pd.DataFrame(data_row, columns=cfg[stock_market]['columns'])    
        # Aplicamos las transformaciones que nos hacen falta
        # Cambiamos el valor "-" de la columna vol a NaN
        df["vol"] = df["vol"].replace("-", np.NaN)
        # Necesitamos convertir la columna Fecha a Date
        df['fecha'] =  pd.to_datetime(df['fecha'], format = "%d.%m.%Y", errors ='coerce')
        df['year_month'] = df['fecha'].map(lambda x: x.strftime('%Y%m'))
        # Guardamos la información del mes actual
        data_row_this_month = df[df["year_month"]==this_year_month]
        save_data_in_csv(data_row_this_month[cfg[stock_market]['columns']], cfg[stock_market]['columns'], stock_market, this_year_month)
        if(day<3):
            # Guardamos la información del mes pasado
            data_row_last_month = df[df["year_month"]==last_year_month]
            save_data_in_csv(data_row_last_month[cfg[stock_market]['columns']], cfg[stock_market]['columns'], stock_market, last_year_month)
                    
        total_time = time.time() - init_time
        time.sleep(10*total_time)
    

if __name__ == "__main__":
    main()