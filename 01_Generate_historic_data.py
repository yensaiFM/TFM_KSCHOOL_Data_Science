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

def convert_period(item):
    transform = {'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12}
    try:
        return transform[item]
    except TypeError:
        return item

def get_historic_data(component, filter_year, logger):
    logger.info('-- get_historic_data > component:' + component)
    all_historic_data = []
    files = glob.glob(r'./dataset/' + component + '/historic_data_*.csv')
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
        # Añadimos 2 nuevas columnas: 
        # - trimestre_anio
        # - mes_anio
        final_historic_data['trimestre_anio'] = final_historic_data['fecha'].dt.quarter.map(str) + "_" + final_historic_data['fecha'].dt.year.map(str)
        final_historic_data['mes_anio'] = final_historic_data['fecha'].dt.month.map(str) + "_" + final_historic_data['fecha'].dt.year.map(str)
        
        # Filtramos los datos para quedarnos con aquellos a partir del 12/02/2015 
        # Esto viene marcado por el dataset de AENA que sólo tiene datos a partir de esa fecha
        if(filter_year == True):
            final_historic_data = final_historic_data[final_historic_data["fecha"]>='2015-02-12']
        final_historic_data = final_historic_data.sort_values(by=('fecha'),ascending=True)
        
        final_historic_data_df = pd.DataFrame(final_historic_data, columns=["fecha","ultimo","apertura","maximo","minimo","vol","variacion","trimestre_anio", "mes_anio"])
        return final_historic_data_df

def get_historic_data_script(component, logger):
    logger.info('-- get_script_historic_data > component:' + component)
    all_historic_data = []
    files = glob.glob(r'./dataset/' + component + '/' + component + '_*.csv')
    if(len(files)>0):
        for file in files:
            historic_data_item = pd.read_csv(file, index_col=None, header=0)
            logger.info('--- file:' + file)
            all_historic_data.append(historic_data_item)
        
        # Juntamos los distintos ficheros
        final_historic_data_script = pd.concat(all_historic_data, axis=0, ignore_index=True)
        
        # Aplicamos las transformaciones que nos hacen falta
        # Cambiamos el valor "-" de la columna vol a NaN
        final_historic_data_script["vol"] = final_historic_data_script["vol"].replace("-", np.NaN)
        # Necesitamos convertir la columna Fecha a Date
        final_historic_data_script['fecha'] =  pd.to_datetime(final_historic_data_script['fecha'], format = "%Y-%m-%d", errors ='coerce')
        # Añadimos 2 nuevas columnas: 
        # - trimestre_anio
        # - mes_anio
        final_historic_data_script['trimestre_anio'] = final_historic_data_script['fecha'].dt.quarter.map(str) + "_" + final_historic_data_script['fecha'].dt.year.map(str)
        final_historic_data_script['mes_anio'] = final_historic_data_script['fecha'].dt.month.map(str) + "_" + final_historic_data_script['fecha'].dt.year.map(str)
        final_historic_data_script = final_historic_data_script.sort_values(by=('fecha'),ascending=True)
        
        final_historic_data_script_df = pd.DataFrame(final_historic_data_script, columns=["fecha","ultimo","apertura","maximo","minimo","vol","variacion","trimestre_anio", "mes_anio"])
        return final_historic_data_script_df
    
    
def add_deuda_publica(component, final_historic_data, logger):
    logger.info('-- add_deuda_publica > component:' + component)
    file = './dataset/COMMON_METRICS/evolucion_de_la_deuda_publica.csv'
    deuda_publica = pd.read_csv(file, index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    deuda_publica.columns = ["anio", "periodo", "deuda_publica"]
    # Añadimos la columna month y obtenemos la columna calculada mes_anio
    deuda_publica['month'] = deuda_publica['periodo'].map(lambda x: convert_period(x) if (pd.notnull(x)) else x)
    deuda_publica['mes_anio'] = deuda_publica['month'].map(str) + "_" + deuda_publica['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    deuda_publica = deuda_publica.drop(['anio', 'periodo', 'month'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna deuda_publica
    deuda_publica_df = pd.DataFrame(deuda_publica, columns=["deuda_publica", "mes_anio"])
    final_historic_data_with_dp = final_historic_data.merge(deuda_publica_df, on="mes_anio", how="left")
    return final_historic_data_with_dp

def add_ipc(component, final_historic_data, logger):
    logger.info('-- add_ipc > component:' + component)
    file = './dataset/COMMON_METRICS/variacion_interanual_del_ipc.csv'
    ipc = pd.read_csv(file, index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    ipc.columns = ["anio", "periodo", "ipc"]
    # Añadimos la columna month y obtenemos la columna calculada mes_anio
    ipc['month'] = ipc['periodo'].map(lambda x: convert_period(x) if (pd.notnull(x)) else x)
    ipc['mes_anio'] = ipc['month'].map(str) + "_" + ipc['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    ipc = ipc.drop(['anio', 'periodo', 'month'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna ipc
    ipc_df = pd.DataFrame(ipc, columns=["ipc", "mes_anio"])
    final_historic_data_with_ipc = final_historic_data.merge(ipc_df, on="mes_anio", how="left")
    return final_historic_data_with_ipc

def add_tasa_paro(component, final_historic_data, logger):
    logger.info('-- add_tasa_paro > component:' + component)
    file = './dataset/COMMON_METRICS/evolucion_de_la_tasa_de_paro.csv'
    tasa_paro = pd.read_csv(file, index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    tasa_paro.columns = ["anio", "periodo", "tasa_paro"]
    # Añadimos la columna month y obtenemos la columna calculada trimestre_anio
    tasa_paro['trimestre_anio'] = tasa_paro['periodo'].str.replace('Trimestre ', '', regex=False) + "_" + tasa_paro['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    tasa_paro = tasa_paro.drop(['anio', 'periodo'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna tasa_paro
    tasa_paro_df = pd.DataFrame(tasa_paro, columns=["tasa_paro", "trimestre_anio"])
    final_historic_data_with_tasa_paro = final_historic_data.merge(tasa_paro_df, on="trimestre_anio", how="left")
    return final_historic_data_with_tasa_paro

def add_pib(component, final_historic_data, logger):
    logger.info('-- add_pib > component:' + component)
    file = './dataset/COMMON_METRICS/evolucion_trimestral_del_PIB.csv'
    pib = pd.read_csv(file, index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    pib.columns = ["anio", "periodo", "pib"]
    # Añadimos la columna calculada trimestre_anio
    pib['trimestre_anio'] = pib['periodo'].str.replace('Trimestre ', '', regex=False) + "_" + pib['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    pib = pib.drop(['anio', 'periodo'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna pib
    pib_df = pd.DataFrame(pib, columns=["pib", "trimestre_anio"])
    final_historic_data_with_pib = final_historic_data.merge(pib_df, on="trimestre_anio", how="left")
    return final_historic_data_with_pib
    
    
def save_historic_data(component, columns, final_historic_data, filter_year, logger):
    logger.info('-- save_historic_data > component::' + component)
        
    # Validamos si existe el directorio y si no existe lo creamos
    dir_filename = './dataset/'+component
    if not os.path.exists(dir_filename):
        os.makedirs(dir_filename)
    if(filter_year==False):
        filename = './dataset/' + component + '/final_historic_data_with_metrics_' + component + '_all.csv'
    else:
        filename = './dataset/' + component + '/final_historic_data_with_metrics_' + component + '_filter_by_20150212.csv'
    if not os.path.isfile(filename):
        final_historic_data.to_csv(filename, header=columns, index=False)
        logger.info('-- final file:' + filename)
    else: # else it exists so append without writing the header
        final_historic_data.to_csv(filename, mode='w', index=False)
        logger.info('-- final file:' + filename)

def main():
    logger = set_timed_rotating_log('logs/historic_data.log')
    components = ['IBEX35','AENA','AMS','BBVA','CABK','FER','IBE','ITX','REP','SAN','TEF']
    filter_year = False

    logger.info('Inicio generate historic data')
    for item in components:
        final_historic_data = get_historic_data(item, filter_year, logger)
        final_historic_data_script = get_historic_data_script(item, logger)
        # Juntamos los dos dataframes
        final_historic_data_concat = pd.concat([final_historic_data, final_historic_data_script], axis=0, ignore_index=True)
       
        final_historic_data_with_dp = add_deuda_publica(item, final_historic_data_concat, logger)
        final_historic_data_with_ipc = add_ipc(item, final_historic_data_with_dp, logger)
        final_historic_data_with_tasa_paro = add_tasa_paro(item, final_historic_data_with_ipc, logger)
        final_historic_data_with_pib = add_pib(item, final_historic_data_with_tasa_paro, logger)
        
        # Eliminamos los valores duplicados
        final_historic_data_with_pib.drop_duplicates(subset="fecha", keep="last", inplace=True)
        # Eliminamos las columnas "trimestre_anio" y "mes_anio"
        columns_drop = ["trimestre_anio", "mes_anio"]
        final_historic_data_with_pib = final_historic_data_with_pib.drop(columns_drop, axis=1)
        
        columns_historic_data = ["fecha","ultimo","apertura","maximo","minimo","vol","variacion","deuda_publica","ipc","tasa_paro","pib"]
        save_historic_data(item, columns_historic_data, final_historic_data_with_pib, filter_year, logger)
        

if __name__ == "__main__":
    main()