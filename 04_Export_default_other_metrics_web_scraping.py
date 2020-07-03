#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:46:40 2020

@author: yensai

Desde las páginas de los distintos componentes del IBEX35 > Análisis. Fund se van a extraer los siguientes ratios fundamentales:
    - PER (Price earning ratio o relación precio-beneficio). Mide la relación entre el precio en bolsa de una acción y los beneficios que obtiene año tras año.
    - Precio /Cash Flow
    - Precio valor contable
    - ROE
    - Dividendo neto por acción
    - BPA (Beneficio por acción)
    - Rentabilidad por dividendo (últimos 12 meses)
    - Beneficio neto (millones)
    - EBITDA
    - BPA
Este script se ejecutará una vez a la semana para obtener los valores por defecto
"""
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import logging
from datetime import datetime, timedelta
import time
from logging.handlers import TimedRotatingFileHandler
import yaml
import sys

# Función que configura los logs para que roten cada medianoche
def set_timed_rotating_log(path):
    logger = logging.getLogger("Export default ratios")
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

def save_data_in_csv(df, cols, stock_market, year ):
    # Validamos si existe el directorio y si no existe lo creamos
    dir_filename = './dataset/'+stock_market
    if not os.path.exists(dir_filename):
        os.makedirs(dir_filename)
    filename = './dataset/'+stock_market+'/default_metrics_'+stock_market+'_'+year+'.csv'
    df.to_csv(filename, mode='w', header=cols, index=False)

def main():
    logger = set_timed_rotating_log('logs/default_ratios.log')
    cfg = get_yaml_configs('conf/config_default_ratios.yml')

    logger.info('Inicio web scraping')
    for stock_market in cfg:
        logger.info('-' + stock_market + ':')
        # Establecemos la variable 
        init_time = time.time()
        logger.info('-- url:' + cfg[stock_market]['url'])
        response = Request(cfg[stock_market]['url'], headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urlopen(response).read()
            #webpage = html.decode('utf-8')
            webpage = html
        except HTTPError as e:
            logger.error('The server couldn\'t fulfill the request.' + cfg[stock_market]['url'])
            logger.error('Error code: ', e.code)
        except URLError as e:
            logger.error('We failed to reach a server' + cfg[stock_market]['url'])
            logger.error('Reason: ', e.reason)
            
    
        page_soup =  BeautifulSoup(webpage)
        section = page_soup.find("section", id="analisis")
        table = section.find("table")
    
        if table:
            # Obtenemos los nombres de las columnas (son dinámicos)
            tr = table.find_all('th')
            head = [tr.text.strip() for tr in tr if tr.text.strip('\n')]
            # Creamos una lista vacia para ir añadiendo los datos de los registros
            data_row=[]
            for tr in table.find_all('tr'):
                td = tr.find_all('td')
                row = [data_tr.text for data_tr in td]
                if row:
                    data_row.append(row)
        
        # Convertimos la información en un dataframe
        df = pd.DataFrame(data_row, columns=head)    
        # Aplicamos las transformaciones que nos hacen falta
        # Cambiamos los valores vacios a NaN
        df = df.replace(r'^\s*$', np.nan, regex=True)
        # Eliminamos de los nombres de columna el caracter especial *
        df.columns = df.columns.str.replace(r"[*]", "")
        # Para hacer la transpuesta del dataframe necesitamos primero establecer el index del dataframe a la columna 'Ratio'
        # De esta forma cada registro tendrá toda la información de un año. Nos será más cómodo a la hora de guardarlo
        df = df.set_index('Ratio')
        df.T
        # Cambiamos el nombre de las columnas
        #for column in cfg[stock_market]['url']
        
        # Guardamos cada año en ficheros separados
        for year, row in df.items():
            i=0
            info = []
            while True:
                info.append(row[i])
                i += 1
                if(i>=df.shape[0]):
                    break
            row_data = pd.DataFrame([info], columns=cfg[stock_market]['columns'])
            save_data_in_csv(row_data, cfg[stock_market]['columns'],stock_market, year)
        

        total_time = time.time() - init_time
        time.sleep(10*total_time)

if __name__ == "__main__":
    main()