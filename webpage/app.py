#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 18:19:29 2020

@author: yensai
"""

import streamlit as st
import altair as alt

import pandas as pd
import numpy as np
import os
import joblib
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

fase01_info ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p>El dataset utilizado para entrenar los modelos esta formado por datos propios del IBEX 35 y métricas genéricas (deuda_publica, ipc, tasa_paro y pib); no todas se utilizan en todos los modelos. Además los datos utilizados son desde el 12-02-2015; se filtra por esta fecha porque viene marcado por el dataset AENA que sólo tiene datos desde esa fecha y las varibles predictoras / exógenas que utilizamos no tienen datos desde el año 1991.</p>
	</div>
	"""
    
fase02_info ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p>El dataset utilizado para entrenar los modelos esta formado por datos propios del IBEX 35, métricas genéricas (deuda_publica, ipc, tasa_paro y pib) y los 10 componentes más importantes que pertenecen a este índice (AENA, AMS, BBVA, CABK, FER, IBE, ITX, REP, SAN, TEF). Además los datos utilizados son desde el 12-02-2015; se filtra por esta fecha porque viene marcado por el dataset AENA que sólo tiene datos desde esa fecha y las varibles predictoras / exógenas que utilizamos no tienen datos desde el año 1991.</p>
	</div>
	"""
    
fase01_info_lr ="""
	<div class="box">
    	<p>Los predictores que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
                <li>tasa_paro, mide el nivel de desocupación en relación con la población activa</li>
                <li>pib, suma de todos los bienes y servicios finales que produce un país o una economía, elaborados dentro del territorio nacional tanto por empresas nacionales como extranjeras, y que se registran en un periodo determinado</li>
            </ul>
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""
    
fase02_info_lr ="""
	<div class="box">
    	<p>Los predictores que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
                <li>tasa_paro, mide el nivel de desocupación en relación con la población activa</li>
                <li>pib, suma de todos los bienes y servicios finales que produce un país o una economía, elaborados dentro del territorio nacional tanto por empresas nacionales como extranjeras, y que se registran en un periodo determinado</li>
                <li>COMPONENTE_ultimo, valor de cierre del componente expresado en puntos para ese día (unidad puntos)<li>
                <li>COMPONENTE_per, relación precio-beneficio para ese componente</li>
                <li>COMPONENTE_bpa, beneficio por acción para ese componente</li>
                <li>COMPONENTE_rentabilidad_por_dividendo, para ese componente</li>
                <li>COMPONENTE_precio_valor_contable, para ese componente</li>
                <li>COMPONENTE_ebitda, para ese componente</li>
            </ul>
            Donde COMPONENTE se corresponde a los componentes más importantes que conforman el índice IBEX 35 (AENA, AMS, BBVA, CABK, FER, IBE, ITX, REP, SAN, TEF).
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""

fase01_info_arima ="""
	<div class="box">
    	<p>Las variables exógenas que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
                <li>tasa_paro, mide el nivel de desocupación en relación con la población activa</li>
                <li>pib, suma de todos los bienes y servicios finales que produce un país o una economía, elaborados dentro del territorio nacional tanto por empresas nacionales como extranjeras, y que se registran en un periodo determinado</li>
            </ul>
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""
    
fase01_info_sarima ="""
	<div class="box">
    	<p>Las variables exógenas que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
                <li>tasa_paro, mide el nivel de desocupación en relación con la población activa</li>
                <li>pib, suma de todos los bienes y servicios finales que produce un país o una economía, elaborados dentro del territorio nacional tanto por empresas nacionales como extranjeras, y que se registran en un periodo determinado</li>
            </ul>
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""
    
fase01_info_svr ="""
	<div class="box">
    	<p>Los predictores que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
            </ul>
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""

fase02_info_svr ="""
	<div class="box">
    	<p>Los predictores que se han utilizado en el modelo son:
            <ul>
                <li>deuda_publica, conjunto de deudas que mantiene el Estado español frente a los particulares que pueden ser españoles o de otro país</li>
                <li>ipc, indicador que mide la variación de los precios de una cesta de bienes y servicios en un lugar concreto durante un determinado periodo de tiempo</li>
                <li>tasa_paro, mide el nivel de desocupación en relación con la población activa</li>
                <li>pib, suma de todos los bienes y servicios finales que produce un país o una economía, elaborados dentro del territorio nacional tanto por empresas nacionales como extranjeras, y que se registran en un periodo determinado</li>
                <li>COMPONENTE_ultimo, valor de cierre del componente expresado en puntos para ese día (unidad puntos)<li>
                <li>COMPONENTE_per, relación precio-beneficio para ese componente</li>
                <li>COMPONENTE_bpa, beneficio por acción para ese componente</li>
                <li>COMPONENTE_rentabilidad_por_dividendo, para ese componente</li>
                <li>COMPONENTE_precio_valor_contable, para ese componente</li>
                <li>COMPONENTE_ebitda, para ese componente</li>
            </ul>
            Donde COMPONENTE se corresponde a los componentes más importantes que conforman el índice IBEX 35 (AENA, AMS, BBVA, CABK, FER, IBE, ITX, REP, SAN, TEF).
            <br/>
            La variable a predecir:
            <ul>
                <li>último, valor de cierre del índice expresado en puntos para ese día (unidad puntos)</li>
            </ul>
        </p>
	</div>
	<hr />
	"""
    
def convert_period(item):
    transform = {'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12}
    try:
        return transform[item]
    except TypeError:
        return item

#@st.cache
def get_variables_data(max_predict_days):
    # Los modelos ARIMA y SARIMA han sido entrenados hasta el 2020-08-07 necesitamos obtener toda la información desde esa fecha
    old_dates_predict = pd.date_range(start = '2020-08-10', end =  datetime.date.today().strftime('%Y-%m-%d'), freq = "B")
    new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = max_predict_days, freq = "B")
    dates_predict = old_dates_predict.union(new_dates_predict)
    raw_data = {'fecha': dates_predict}
    data_test_predict = pd.DataFrame(raw_data)
    data_test_predict['trimestre_anio'] = data_test_predict['fecha'].dt.quarter.map(str) + "_" + data_test_predict['fecha'].dt.year.map(str)
    data_test_predict['mes_anio'] = data_test_predict['fecha'].dt.month.map(str) + "_" + data_test_predict['fecha'].dt.year.map(str)
    
    data_test_predict_with_dp = add_deuda_publica(data_test_predict)
    data_test_predict_with_ipc = add_ipc(data_test_predict_with_dp)
    data_test_predict_with_tasa_paro = add_tasa_paro(data_test_predict_with_ipc)
    data_test_predict_with_pib = add_pib(data_test_predict_with_tasa_paro)
    
    # Eliminamos las columnas "trimestre_anio" y "mes_anio"
    columns_drop = ["trimestre_anio", "mes_anio"]
    final_variables_data_with_pib = data_test_predict_with_pib.drop(columns_drop, axis=1)
    # Cambiamos el formato de miles y decimales de todas las columnas
    final_variables_data_with_pib = final_variables_data_with_pib.replace(r'[.]','', regex=True)
    final_variables_data_with_pib = final_variables_data_with_pib.replace(r'[,]','.', regex=True)
    return final_variables_data_with_pib

#@st.cache
def get_variables_data_with_components(max_predict_days):
    # Los modelos ARIMA y SARIMA han sido entrenados hasta el 2020-08-03 necesitamos obtener toda la información desde esa fecha
    old_dates_predict = pd.date_range(start = '2020-08-04', end =  datetime.date.today().strftime('%Y-%m-%d'), freq = "B")
    new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = max_predict_days, freq = "B")
    dates_predict = old_dates_predict.union(new_dates_predict)
    raw_data = {'fecha': dates_predict}
    data_test_predict = pd.DataFrame(raw_data)
    data_test_predict['trimestre_anio'] = data_test_predict['fecha'].dt.quarter.map(str) + "_" + data_test_predict['fecha'].dt.year.map(str)
    data_test_predict['mes_anio'] = data_test_predict['fecha'].dt.month.map(str) + "_" + data_test_predict['fecha'].dt.year.map(str)
    
    data_test_predict_with_dp = add_deuda_publica(data_test_predict)
    data_test_predict_with_ipc = add_ipc(data_test_predict_with_dp)
    data_test_predict_with_tasa_paro = add_tasa_paro(data_test_predict_with_ipc)
    data_test_predict_with_pib = add_pib(data_test_predict_with_tasa_paro)
    
    # Debemos de cargar la información de los 10 componentes más importantes y sus métricas
    today = datetime.date.today().strftime('%Y%m')
    year = datetime.date.today().strftime('%Y')
    componentes = ['AENA','AMS','BBVA','CABK','FER','IBE','ITX','REP','SAN','TEF']
    for item in componentes:
        # Cargamos la métrica por defecto para este año
        default_metrics_filename = './dataset/' + item + '/default_metrics_' + item + '_'+year+'.csv'
        if os.path.exists(default_metrics_filename):
            default_metrics = pd.read_csv(default_metrics_filename, index_col=None, header=0)
        # Cargamos el fichero con el ultimo valor para este componente
        ultimo_filename = './dataset/'+item+'/'+item+'_'+today+'.csv'
        if os.path.exists(ultimo_filename):
            count=len(open(ultimo_filename).readlines())
            ultimo = pd.read_csv(ultimo_filename, skiprows=range(1,count-1), index_col=None, sep=",")
            ultimo.columns=['fecha',item+'_ultimo',item+'_apertura',item+'_maximo',item+'_minimo',item+'_vol',item+'_variacion']
            data_test_predict_with_pib[item+'_ultimo']=ultimo[item+'_ultimo']
            data_test_predict_with_pib[item+'_ultimo'].fillna(method='ffill', inplace=True)
        # Cargamos el fichero con las últimas métricas para este componente
        metrics_filename = './dataset/'+item+'/metrics_'+item+'_'+today+'.csv'
        if os.path.exists(metrics_filename):
            count=len(open(metrics_filename).readlines())
            test = pd.read_csv(metrics_filename, skiprows=range(1,count-1), index_col=None, sep=",")
            test.columns=['fecha',item+'_per',item+'_bpa',item+'_rentabilidad_por_dividendo',item+'_precio_div_cash_flow',item+'_precio_valor_contable',item+'_ebitda',item+'_b_neto']
            if(test[item+'_per'].empty):
                data_test_predict_with_pib[item+'_per']=default_metrics['per']
            else:
                data_test_predict_with_pib[item+'_per']=test[item+'_per']
            if(test[item+'_bpa'].empty):
                data_test_predict_with_pib[item+'_bpa']=default_metrics['bpa']
            else:
                data_test_predict_with_pib[item+'_bpa']=test[item+'_bpa']
            if(test[item+'_rentabilidad_por_dividendo'].empty):
                data_test_predict_with_pib[item+'_rentabilidad_por_dividendo']=default_metrics['rentabilidad_por_dividendo']
            else:
                data_test_predict_with_pib[item+'_rentabilidad_por_dividendo']=test[item+'_rentabilidad_por_dividendo']
            if(test[item+'_precio_valor_contable'].empty):
                data_test_predict_with_pib[item+'_precio_valor_contable']=default_metrics['precio_valor_contable']
            else:
                data_test_predict_with_pib[item+'_precio_valor_contable']=test[item+'_precio_valor_contable']
            if(test[item+'_ebitda'].empty):
                data_test_predict_with_pib[item+'_ebitda']=default_metrics['ebitda']
            else:
                data_test_predict_with_pib[item+'_ebitda']=test[item+'_ebitda']
            data_test_predict_with_pib[item+'_per'].fillna(method='ffill', inplace=True)
            data_test_predict_with_pib[item+'_bpa'].fillna(method='ffill', inplace=True)
            data_test_predict_with_pib[item+'_rentabilidad_por_dividendo'].fillna(method='ffill', inplace=True)
            data_test_predict_with_pib[item+'_precio_valor_contable'].fillna(method='ffill', inplace=True)
            data_test_predict_with_pib[item+'_ebitda'].fillna(method='ffill', inplace=True)

    # Eliminamos las columnas "trimestre_anio" y "mes_anio"
    columns_drop = ["trimestre_anio", "mes_anio"]
    final_variables_data_with_pib = data_test_predict_with_pib.drop(columns_drop, axis=1)
    # Cambiamos el formato de miles y decimales de todas las columnas
    final_variables_data_with_pib = final_variables_data_with_pib.replace(r'[.]','', regex=True)
    final_variables_data_with_pib = final_variables_data_with_pib.replace(r'[,]','.', regex=True)
    final_variables_data_with_pib = final_variables_data_with_pib.replace('- ','-', regex=True)
    return final_variables_data_with_pib

def add_deuda_publica(final_variables_data):
    file = './dataset/COMMON_METRICS/evolucion_de_la_deuda_publica.csv'
    count=len(open(file).readlines()) 

    deuda_publica = pd.read_csv(file, skiprows=range(1,count-6), index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    deuda_publica.columns = ["anio", "periodo", "deuda_publica"]
    # Añadimos la columna month y obtenemos la columna calculada mes_anio
    deuda_publica['month'] = deuda_publica['periodo'].map(lambda x: convert_period(x) if (pd.notnull(x)) else x)
    deuda_publica['mes_anio'] = deuda_publica['month'].map(str) + "_" + deuda_publica['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    deuda_publica = deuda_publica.drop(['anio', 'periodo', 'month'], axis=1)

    deuda_publica_df = pd.DataFrame(deuda_publica, columns=["deuda_publica", "mes_anio"])
    final_variables_data_with_dp = final_variables_data.merge(deuda_publica_df, on="mes_anio", how="left")
    return final_variables_data_with_dp

def add_ipc(final_variables_data):
    file = './dataset/COMMON_METRICS/variacion_interanual_del_ipc.csv'
    count=len(open(file).readlines())
    
    ipc = pd.read_csv(file, skiprows=range(1,count-6), index_col=None, sep=";")
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
    final_variables_data_with_ipc = final_variables_data.merge(ipc_df, on="mes_anio", how="left")
    return final_variables_data_with_ipc

def add_tasa_paro(final_variables_data):
    file = './dataset/COMMON_METRICS/evolucion_de_la_tasa_de_paro.csv'
    count=len(open(file).readlines())
    
    tasa_paro = pd.read_csv(file, skiprows=range(1,count-6), index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    tasa_paro.columns = ["anio", "periodo", "tasa_paro"]
    # Añadimos la columna month y obtenemos la columna calculada trimestre_anio
    tasa_paro['trimestre_anio'] = tasa_paro['periodo'].str.replace('Trimestre ', '', regex=False) + "_" + tasa_paro['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    tasa_paro = tasa_paro.drop(['anio', 'periodo'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna tasa_paro
    tasa_paro_df = pd.DataFrame(tasa_paro, columns=["tasa_paro", "trimestre_anio"])
    final_variables_data_with_tasa_paro = final_variables_data.merge(tasa_paro_df, on="trimestre_anio", how="left")
    return final_variables_data_with_tasa_paro

def add_pib(final_variables_data):
    file = './dataset/COMMON_METRICS/evolucion_trimestral_del_PIB.csv'
    count=len(open(file).readlines())
    
    pib = pd.read_csv(file, skiprows=range(1,count-6), index_col=None, sep=";")
    # Aplicamos las transformaciones que nos hacen falta
    # Cambiamos los nombres de columnas
    pib.columns = ["anio", "periodo", "pib"]
    # Añadimos la columna calculada trimestre_anio
    pib['trimestre_anio'] = pib['periodo'].str.replace('Trimestre ', '', regex=False) + "_" + pib['anio'].map(str)
    # Eliminamos las columnas que no nos hacen falta
    pib = pib.drop(['anio', 'periodo'], axis=1)
    # Añadimos al dataframe final_historic_data la nueva columna pib
    pib_df = pd.DataFrame(pib, columns=["pib", "trimestre_anio"])
    final_variables_data_with_pib = final_variables_data.merge(pib_df, on="trimestre_anio", how="left")
    return final_variables_data_with_pib

def transform_data(final_variables_data, name_model, days_predict):
    if(name_model == 'LR'):
        if(days_predict == 10):
            final_variables_data = final_variables_data[-10:]
        else:
            final = days_predict - 10
            final_variables_data = final_variables_data[-10:final]
        # Quitamos la columna fecha
        final_variables_data = final_variables_data.drop(['fecha'], axis=1)
        # Convertimos las columnas a float
        final_variables_data = final_variables_data.astype({"deuda_publica": float, "ipc": float, "tasa_paro": float, "pib": float})
    elif(name_model=='LR_C'):
        if(days_predict == 10):
            final_variables_data = final_variables_data[-10:]
        else:
            final = days_predict - 10
            final_variables_data = final_variables_data[-10:final]
        # Quitamos la columna fecha
        final_variables_data = final_variables_data.drop(['fecha'], axis=1)
        # Convertimos los NaN a 0
        final_variables_data = final_variables_data.fillna(0)
        # Convertimos las columnas a float
        
    elif(name_model=='ST'):
        # Utilizamos la función fillna() con el método "forward fill" de forma que los valores no nulos se copien hacia
        # adelante siempre que se encuentren valores nulos en las columnas: deuda_publica, ipc, tasa_paro y pib
        if 'deuda_publica' in final_variables_data.columns:
            final_variables_data['deuda_publica'].fillna(method='ffill', inplace=True)
        if 'ipc' in final_variables_data.columns:
            final_variables_data['ipc'].fillna(method='ffill', inplace=True)
        if 'tasa_paro' in final_variables_data.columns:
            final_variables_data['tasa_paro'].fillna(method='ffill', inplace=True)
        if 'pib' in final_variables_data.columns:
            final_variables_data['pib'].fillna(method='ffill', inplace=True)
        # Convertimos los NaN a 0
        final_variables_data = final_variables_data.fillna(0)
        # Convertimos las columnas a los formatos indicados en el parámetro columns_type
        final_variables_data = final_variables_data.astype({"deuda_publica": float, "ipc": float, "tasa_paro": float, "pib": float})
        # Ordenamos el dataset por fecha en orden ascendente
        final_variables_data = final_variables_data.sort_values(by=["fecha"])
        # Ponemos la columna date como índice
        final_variables_data.set_index("fecha", inplace=True)
        # Ordenamos los índices
        final_variables_data.sort_index(inplace=True)
    elif(name_model=='ST_C'):
        # Utilizamos la función fillna() con el método "forward fill" de forma que los valores no nulos se copien hacia
        # adelante siempre que se encuentren valores nulos en las columnas: deuda_publica, ipc, tasa_paro y pib
        if 'deuda_publica' in final_variables_data.columns:
            final_variables_data['deuda_publica'].fillna(method='ffill', inplace=True)
        if 'ipc' in final_variables_data.columns:
            final_variables_data['ipc'].fillna(method='ffill', inplace=True)
        if 'tasa_paro' in final_variables_data.columns:
            final_variables_data['tasa_paro'].fillna(method='ffill', inplace=True)
        if 'pib' in final_variables_data.columns:
            final_variables_data['pib'].fillna(method='ffill', inplace=True)
        # Convertimos los NaN a 0
        final_variables_data = final_variables_data.fillna(0)
        # Convertimos las columnas a los formatos indicados en el parámetro columns_type
        final_variables_data = final_variables_data.astype({"deuda_publica": float, "ipc": float, "tasa_paro": float, "pib": float,"AENA_ultimo":float, "AENA_per": float, "AENA_bpa": float, "AENA_rentabilidad_por_dividendo": float,"AENA_precio_valor_contable": float, "AENA_ebitda": float,"AMS_ultimo":float, "AMS_per": float, "AMS_bpa": float, "AMS_rentabilidad_por_dividendo": float,"AMS_precio_valor_contable": float, "AMS_ebitda": float,"BBVA_ultimo":float, "BBVA_per": float, "BBVA_bpa": float, "BBVA_rentabilidad_por_dividendo": float,"BBVA_precio_valor_contable": float,"CABK_ultimo":float, "CABK_per": float, "CABK_bpa": float, "CABK_rentabilidad_por_dividendo": float,"CABK_precio_valor_contable": float,"FER_ultimo":float, "FER_per": float, "FER_bpa": float, "FER_rentabilidad_por_dividendo": float,"FER_precio_valor_contable": float, "FER_ebitda": float,"IBE_ultimo":float, "IBE_per": float, "IBE_bpa": float, "IBE_rentabilidad_por_dividendo": float,"IBE_precio_valor_contable": float, "IBE_ebitda": float,"ITX_ultimo":float, "ITX_per": float, "ITX_bpa": float, "ITX_rentabilidad_por_dividendo": float,"ITX_precio_valor_contable": float, "ITX_ebitda": float,"REP_ultimo":float, "REP_per": float, "REP_bpa": float, "REP_rentabilidad_por_dividendo": float,"REP_precio_valor_contable": float, "REP_ebitda": float,"SAN_ultimo":float, "SAN_per": float, "SAN_bpa": float, "SAN_rentabilidad_por_dividendo": float,"SAN_precio_valor_contable": float,"TEF_ultimo":float, "TEF_per": float, "TEF_bpa": float, "TEF_rentabilidad_por_dividendo": float,"TEF_precio_valor_contable": float, "TEF_ebitda": float})
        # Ordenamos el dataset por fecha en orden ascendente
        final_variables_data = final_variables_data.sort_values(by=["fecha"])
        # Ponemos la columna date como índice
        final_variables_data.set_index("fecha", inplace=True)
        # Ordenamos los índices
        final_variables_data.sort_index(inplace=True)
        # Obtain las 55 rows required for this model
        final_variables_data=final_variables_data[-55:]
        
    elif(name_model == 'SVR'):
        if(days_predict == 10):
            final_variables_data = final_variables_data[-10:]
        else:
            final = days_predict - 10
            final_variables_data = final_variables_data[-10:final]
        # Quitamos la columna fecha
        final_variables_data = final_variables_data.drop(['fecha','tasa_paro','pib'], axis=1)
        # Convertimos las columnas a float
        final_variables_data = final_variables_data.astype({"deuda_publica": float, "ipc": float})
    elif(name_model == 'SVR_C'):
        if(days_predict == 10):
            final_variables_data = final_variables_data[-10:]
        else:
            final = days_predict - 10
            final_variables_data = final_variables_data[-10:final]
        # Quitamos la columna fecha
        final_variables_data = final_variables_data.drop(['fecha'], axis=1)
        # Convertimos los NaN a 0
        final_variables_data = final_variables_data.fillna(0)
        # Convertimos las columnas a float
        #final_variables_data = final_variables_data.astype({"deuda_publica": float, "ipc": float})
    return final_variables_data

      
def load_model(path_model):
    model = joblib.load(open(os.path.join(path_model), "rb"))
    return model

def main():
    max_predict_days = 10
    # Block sidebar
    st.sidebar.title("Predicción del valor de las acciones en el índice IBEX 35")
    menu = ["Fase 01","Fase 02"]
    sub_menu_fase01 = ["-","Regresión Lineal Múltiple","Serie temporal - ARIMA","Serie temporal - SARIMA","SVR"]
    sub_menu_fase02 = ["-","Regresión Lineal Múltiple","Serie temporal - ARIMA","Serie temporal - SARIMA","SVR"]
    choice = st.sidebar.selectbox("Fases implementadas",menu)
    if choice == "Fase 01":
        df_test_data = get_variables_data(max_predict_days)
        #st.dataframe(df_test_data)
        st.subheader("Fase 01")
        st.markdown(fase01_info,unsafe_allow_html=True)
        model_select = st.sidebar.selectbox("Elige el modelo a analizar:",sub_menu_fase01)
        if model_select=="Regresión Lineal Múltiple":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Regresión Lineal Múltiple")
            st.markdown(fase01_info_lr,unsafe_allow_html=True)
            loaded_model = load_model("models/lm_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib_python.pkl")
            
            data_test_transform = transform_data(df_test_data, 'LR', days_predict)
            prediction = loaded_model.predict(data_test_transform)
            st.write("La predicción para los próximos " + str(days_predict) + " días:" , prediction)
            
            new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = days_predict, freq = "B")
            test = pd.DataFrame({'fecha': new_dates_predict})
            test['value'] = prediction

            #Mostramos la gráfica con los resultados de las predicciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="Serie temporal - ARIMA":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Serie temporal - ARIMA")
            st.markdown(fase01_info_arima,unsafe_allow_html=True)
            loaded_model = load_model("models/arima313_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib_python.pkl")
            
            data_test_transform = transform_data(df_test_data, 'ST', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(n_periods=days_predict, 
                                                             start=data_test_transform.index.min(), 
                                                             end=data_test_transform.index.max(),
                                                             exog=data_test_transform.iloc[:,-4:],
                                                             dynamic=False)
            final_prediction = prediction[-10:]
            st.write("La predicción para los próximos " + str(days_predict) + " días:", final_prediction[:days_predict])
            
            test = pd.DataFrame({'fecha': final_prediction[:days_predict].index, 'value': final_prediction[:days_predict].values})
            #st.write(test)
            
            # Mostramos la gráfica con los resultados de las prediciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="Serie temporal - SARIMA":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Serie temporal - SARIMA")
            st.markdown(fase01_info_sarima,unsafe_allow_html=True)
            loaded_model = load_model("models/sarima313011_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib_python.pkl")
            
            data_test_transform = transform_data(df_test_data, 'ST', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(n_periods=days_predict, 
                                                             start=data_test_transform.index.min(), 
                                                             end=data_test_transform.index.max(),
                                                             exog=data_test_transform.iloc[:,-4:],
                                                             dynamic=False)
            final_prediction = prediction[-10:]
            st.write("La predicción para los próximos " + str(days_predict) + " días:", final_prediction[:days_predict])
            
            test = pd.DataFrame({'fecha': final_prediction[:days_predict].index, 'value': final_prediction[:days_predict].values})
            #st.write(test)
            
            # Mostramos la gráfica con los resultados de las prediciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="SVR":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Support Vector Regression")
            st.markdown(fase01_info_svr,unsafe_allow_html=True)
            loaded_model = load_model("models/svr_fit_ultimo_filter_data_deuda_publica+ipc_python.pkl")
            
            data_test_transform = transform_data(df_test_data, 'SVR', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(data_test_transform)
            st.write("La predicción para los próximos " + str(days_predict) + " días:", prediction)
            
            new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = days_predict, freq = "B")
            test = pd.DataFrame({'fecha': new_dates_predict})
            test['value'] = prediction

            #Mostramos la gráfica con los resultados de las predicciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
            
    elif choice == "Fase 02":
        df_test_data = get_variables_data_with_components(max_predict_days)
        #st.dataframe(df_test_data)
        st.subheader("Fase 02")
        st.markdown(fase02_info,unsafe_allow_html=True)
        model_select = st.sidebar.selectbox("Elige el modelo a analizar:",sub_menu_fase02)
        if model_select=="Regresión Lineal Múltiple":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Regresión Lineal Múltiple")
            st.markdown(fase02_info_lr,unsafe_allow_html=True)
            loaded_model = load_model("models/lm_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib+other_components_python.pkl")
            
            data_test_transform = transform_data(df_test_data, 'LR_C', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(data_test_transform)
            st.write("La predicción para los próximos " + str(days_predict) + " días:" , prediction)
            
            new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = days_predict, freq = "B")
            test = pd.DataFrame({'fecha': new_dates_predict})
            test['value'] = prediction

            #Mostramos la gráfica con los resultados de las predicciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="Serie temporal - ARIMA":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Serie temporal - ARIMA")
            st.markdown(fase01_info_arima,unsafe_allow_html=True)
            loaded_model = load_model("models/arima110_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib+other_components.pkl")
            
            data_test_transform = transform_data(df_test_data, 'ST_C', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(n_periods=days_predict, 
                                                             start=data_test_transform.index.min(), 
                                                             end=data_test_transform.index.max(),
                                                             exog=data_test_transform.iloc[:,-61:],
                                                             dynamic=False)
            final_prediction = prediction[-10:]
            st.write("La predicción para los próximos " + str(days_predict) + " días:", final_prediction[:days_predict])
            
            test = pd.DataFrame({'fecha': final_prediction[:days_predict].index, 'value': final_prediction[:days_predict].values})
            #st.write(test)
            
            # Mostramos la gráfica con los resultados de las prediciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="Serie temporal - SARIMA":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Serie temporal - SARIMA")
            st.markdown(fase01_info_sarima,unsafe_allow_html=True)
            loaded_model = load_model("models/sarima110011_fit_ultimo_filter_data_deuda_publica+ipc+tasa_paro+pib+other_components.pkl")
            
            data_test_transform = transform_data(df_test_data, 'ST_C', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(n_periods=days_predict, 
                                                             start=data_test_transform.index.min(), 
                                                             end=data_test_transform.index.max(),
                                                             exog=data_test_transform.iloc[:,-61:],
                                                             dynamic=False)
            final_prediction = prediction[-10:]
            st.write("La predicción para los próximos " + str(days_predict) + " días:", final_prediction[:days_predict])
            
            test = pd.DataFrame({'fecha': final_prediction[:days_predict].index, 'value': final_prediction[:days_predict].values})
            #st.write(test)
            
            # Mostramos la gráfica con los resultados de las prediciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
        if model_select=="SVR":
            days_predict = st.sidebar.slider("Número de días a predecir:", 0, 10, 5, 1)
            st.subheader("Support Vector Regression")
            st.markdown(fase02_info_svr,unsafe_allow_html=True)
            loaded_model = load_model("models/svr_fit_ultimo_filter_data_deuda_publica+ipc+other_components.pkl")
            
            data_test_transform = transform_data(df_test_data, 'SVR_C', days_predict)
            #st.dataframe(data_test_transform)
            prediction = loaded_model.predict(data_test_transform)
            st.write("La predicción para los próximos " + str(days_predict) + " días:", prediction)
            
            new_dates_predict = pd.date_range(start = datetime.date.today().strftime('%Y-%m-%d'), periods = days_predict, freq = "B")
            test = pd.DataFrame({'fecha': new_dates_predict})
            test['value'] = prediction

            #Mostramos la gráfica con los resultados de las predicciones
            plt.rcParams.update({'font.size': 6})
            plt.plot(test['fecha'], test['value'], marker='o', label='ARIMA')
            plt.legend()
            plt.title('Gráfica con los resultados')
            plt.xlabel('Fecha')
            plt.ylabel('Predicción')
            st.pyplot()
    

if __name__ == '__main__':
	main()