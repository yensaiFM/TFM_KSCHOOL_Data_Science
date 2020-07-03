#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:26:20 2020

@author: yensai

Los datos se han obtenido de la página https://es.investing.com/indices/spain-35-historical-data mediante la 
utilidad "Información histórica"
"""

import numpy as np
import pandas as pd
import glob
import datetime
import logging
import time
import os
from logging.handlers import TimedRotatingFileHandler

# Función que configura los logs para que roten cada medianoche
def set_timed_rotating_log(path):
    logger = logging.getLogger("Historic data Log")
    logger.setLevel(logging.DEBUG)
    
    handler = TimedRotatingFileHandler(path, when='midnight', interval=1, backupCount=5, encoding='UTF-8')
    formatter = '%(asctime)s %(name)-2s %(levelname)-2s %(message)s'
    handler.setFormatter(logging.Formatter(formatter, '%Y-%m-%d %H:%M:%S'))
    handler.suffix = '%Y_%m_%d.log'
    logger.addHandler(handler)
    return logger

def main():
    logger = set_timed_rotating_log('logs/historic_data.log')
    components = ['IBEX35','AENA','AMS','BBVA','CABK','FER','IBE','ITX','REP','SAN','TEF']

    logger.info('Inicio generate historic data')
    for item in components:
        logger.info('-- component:' + item)
        all_historic_data = []
        files = glob.glob(r'./dataset/' + item + '/historic_data_*.csv')
        if(len(files)>0):
            for file in files:
                historic_data_item = pd.read_csv(file, index_col=None, header=0)
                logger.info('--- file:' + file)
                all_historic_data.append(historic_data_item)
            # Juntamos los distintos ficheros
            final_historic_data = pd.concat(all_historic_data, axis=0, ignore_index=True)
            
            # Aplicamos las transformaciones que nos hacen falta
            # Cambiamos los nombres de columnas
            final_historic_data.columns = ["fecha","ultimo","apertura","maximo","minimo","vol","variacion"]
            # Cambiamos el valor "-" de la columna vol a NaN
            final_historic_data["vol"] = final_historic_data["vol"].replace("-", np.NaN)
            # Necesitamos convertir la columna Fecha a Date
            final_historic_data['fecha'] =  pd.to_datetime(final_historic_data['fecha'], format = "%d.%m.%Y", errors ='coerce')
            # Filtramos los datos para quedarnos con aquellos a partir del 12/02/2015 
            # Esto viene marcado por el dataset de AENA que sólo tiene datos a partir de esa fecha
            final_historic_data = final_historic_data[final_historic_data["fecha"]>='2015-02-12']
            final_historic_data.sort_values(by=('fecha'),ascending=True)
            
            df = pd.DataFrame(final_historic_data, columns=["fecha","ultimo","apertura","maximo","minimo","vol","variacion"])
        
            # Validamos si existe el directorio y si no existe lo creamos
            dir_filename = './dataset/'+item
            if not os.path.exists(dir_filename):
                os.makedirs(dir_filename)
            filename = './dataset/' + item + '/final_historic_data_' + item + '.csv'
            if not os.path.isfile(filename):
                df.to_csv(filename, header=["fecha","ultimo","apertura","maximo","minimo","vol","variacion"], index=False)
                logger.info('-- final file:' + filename)
            else: # else it exists so append without writing the header
                df.to_csv(filename, mode='w', index=False)
                logger.info('-- final file:' + filename)
            
            


if __name__ == "__main__":
    main()