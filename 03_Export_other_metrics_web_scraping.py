#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 18:59:48 2020

@author: yensai

Desde la página web https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html > Ratios se van a extraer
los siguientes datos:
    - PER (Price earning ratio o relación precio-beneficio). Mide la relación entre el precio en bolsa de una acción y los beneficios que obtiene año tras año.
    - BPA (Beneficio por acción)
    - Rentabilidad por dividendo (últimos 12 meses)
    - Precio /Cash Flow
    - Precio valor contable
    - EBITDA
    - Beneficio neto (millones)
Este script se ejecutará de L-V para obtener los ratios del día actual
"""
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from datetime import datetime, timedelta
import time
from logging.handlers import TimedRotatingFileHandler
import yaml
import sys

# Función que configura los logs para que roten cada medianoche
def set_timed_rotating_log(path):
    logger = logging.getLogger("Export ratios data")
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
    filename = './dataset/'+stock_market+'/metrics_'+stock_market+'_'+year_month+'.csv'
    if not os.path.isfile(filename):
        df.to_csv(filename, header=cols, index=False)
    else: # else it exists so append without writing the header
        df.to_csv(filename, mode='a', header=False, index=False)

def main():
    logger = set_timed_rotating_log('logs/ratios.log')
    cfg = get_yaml_configs('conf/config_ratios.yml')
    day = datetime.now().day
    this_year_month = datetime.today().strftime('%Y%m')
    last_year_month = (datetime.today() - timedelta(days=day)).strftime('%Y%m')
    

    logger.info('Inicio web scraping')
    url = cfg['RATIOS']['url']
    logger.info('-- url:' + url)
    # Obtener el chromeDriver necesario https://chromedriver.chromium.org/downloads
    browser = webdriver.Chrome('./driver/chromedriver85')
    browser.get(url)
    time.sleep(2)
    browser.find_element_by_xpath("//ul[@id='pestanas_modulo_valores_analisis_superior']/li[text()='Ratios']").click()
    time.sleep(2)
    browser.find_elements_by_xpath("//table[@id='ratios']")[0]
    
    page_soup =  BeautifulSoup(browser.page_source)
    # Obtenemos los valores de las distintas métricas
    table_metrics = page_soup.find('table', id='ratios')
    
    if table_metrics:
        # Creamos una lista vacia para ir añadiendo los datos de los registros
        data_row=[]
        for tr in table_metrics.find_all('tr'):
            td = tr.find_all('td')
            row = [data_tr.text.strip('\n') for data_tr in td if tr.text.strip('\n')]
            if row:
                data_row.append(row)
                logger.info(' --- row: ' + str(row))
    # Obtenemos la fecha del día que se esta obteniendo dicha información
    table_date = page_soup.find("table", id="ficha_indice4")
    date_table_metrics = table_date.tbody.find_all("tr")[0].select('td')[0].text
    logger.info(' --- fecha:' + date_table_metrics)
    
    # Convertimos la información en un dataframe
    df = pd.DataFrame(data_row, columns=cfg['RATIOS']['columns_scraping']) 
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los valores vacio a NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    # Añadimos la columna fecha
    df.insert(1, 'fecha', date_table_metrics)
    # Convertimos el formato de fecha
    df['fecha'] =  pd.to_datetime(df['fecha'], format = "%d/%m/%Y", errors ='coerce')
    df['year_month'] = df['fecha'].map(lambda x: x.strftime('%Y%m'))
    
    valores = cfg['VALORES'].items()
    for key, stock_market in valores:
        logger.info('-' + stock_market + ':')
        # Filtramos los datos del dataframe por el componente deseado
        df_filter_by_key = df[df['componente']==key]
        logger.info(' - shape: ' + str(df_filter_by_key.shape))
        # Guardamos la información
        this_year_month = df_filter_by_key.iloc[0]['year_month']
        save_data_in_csv(df_filter_by_key[cfg['RATIOS']['columns']], cfg['RATIOS']['columns'], stock_market, this_year_month)

    #browser.quit()

if __name__ == "__main__":
    main()