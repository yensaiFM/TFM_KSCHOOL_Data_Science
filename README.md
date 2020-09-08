# TFM_KSCHOOL_Data_Science
El objetivo del presente trabajo es desarrollar y obtener el mejor algoritmo que permita predecir a corto plazo el comportamiento del IBEX 35 utilizando técnicas de aprendizaje supervisado. Para ello se ha utilizado el histórico del IBEX 35, los históricos de los 10 principales componentes que conforman el IBEX 35 (AENA, AMS, BBVA, CABK, FER, IBE, ITX, REP, SAN, TEF), además de otras métricas genéricas como son la deuda pública, IPC, tasa de paro y PIB. 


El proyecto está formado por los siguientes ficheros:
1. ETLs
- 01_Generate_historic_data.py
Este script se encarga de unificar los datos históricos con las métricas del índice IBEX 35 y los distintos componentes.

2. Recopilación de la información
- 02_Export_historical_data_web_scraping.py
Utilizando la técnica de web scraping obtenemos los valores de cierre del índice IBEX 35 y los distintos componentes. Los datos se obtienen de la página web ‘https://es.investing.com/’.
- 03_Export_other_metrics_web_scraping.py
Utilizando las técnicas de web scraping y selenium se obtiene información de las métricas PER, BPA, Rentabilidad por dividendo, Precio/Cash flow, Precio/Valor contable, ebitda y beneficio neto del índice IBEX 35 y los distintos componentes. Los datos se obtienen de la página web 'https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html'
- 04_Export_default_other_metrics_web_scraping.py
Utilizando la técnica de web scraping se obtiene información de las métricas por defecto PER, Precio/Cash flow, Precio/Valor contable, ROE, dividendo neto por acción, BPA, Rentabilidad por dividendo, beneficio neto y ebitda de los diez componentes más importantes del IBEX 35. Los datos se obtienen de la siguiente página web ‘https://www.expansion.com’.

3. Análisis de los modelos
- FASE 0
  - 06_Multiple_lineal_regression_data_filterby_20150212_apertura+vol.ipynb
Análisis desarrollado en python utilizando un modelo de regresión lineal múltiple utilizando únicamente los predictores apertura y volúmen del IBEX 35.
  - 06_Multiple_lineal_regression_data_filterby_20150212_apertura+vol.Rmd
Análisis desarrollado en R utilizando un modelo de regresión lineal múltiple utilizando únicamente los predictores apertura y volúmen del IBEX 35.
  - 07_Series_temporales_all_data_apertura+vol.ipynb
Análisis desarrollado en python utilizando los modelos ARIMA(p,d,q) sin variables exógenas y utilizando como variables exógenas apertura y volumen.
- FASE 1
  - 06_01_Multiple_lineal_regression_all_data_deuda_publica+ipc+tasa_paro+pib.ipynb
Análisis desarrollado en python utilizando un modelo de regresión lineal múltiple utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset completo con los datos desde el 09-09-1991.
  - 06_01_Multiple_lineal_regression_all_data_deuda_publica+ipc+tasa_paro+pib.Rmd
Análisis desarrollado en R utilizando un modelo de regresión lineal múltiple utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset completo con los datos desde el 09-09-1991.
  - 06_01_Multiple_lineal_regression_data_filterby_20150212_deuda_publica+ipc+tasa_paro+pib.ipynb
Análisis desarrollado en python utilizando un modelo de regresión lineal múltiple utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset filtrado desde el 12-02-2015.
  - 06_01_Multiple_lineal_regression_data_filterby_20150212_deuda_publica+ipc+tasa_paro+pib.Rmd
Análisis desarrollado en R utilizando un modelo de regresión lineal múltiple utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset filtrado desde el 12-02-2015.
  - 07_01_Series_temporales_all_data_deuda_publica+ipc+tasa+paro+pib.ipynb
Análisis desarrollado en python utilizando los modelos ARIMA(p,d,q) sin variables exógenas y utilizando como variables exógenas deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset completo con los datos desde el 09-09-1991.
  - 07_01_Series_temporales_data_filterby_20150212_deuda_publica+ipc+tasa+paro+pib.ipynb
Análisis desarrollado en python utilizando los modelos ARIMA(p,d,q) y SARIMA(p,d,q)x(P,D,Q)s sin variables exógenas y utilizando como variables exógenas deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset filtrado desde el 12-02-2015.
  - 08_01_Support_vector_regression_all_data_deuda_publica+ipc+tasa+paro+pib.ipynb
Análisis desarrollado en python utilizando el modelo support vector regression utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset completo con los datos desde el 09-09-1991.
  - 08_01_Support_vector_regression_data_filtery_20150212_deuda_publica+ipc+tasa+paro+pib.ipynb
Análisis desarrollado en python utilizando el modelo support vector regression utilizando los predictores deuda pública, IPC, tasa de paro y PIB únicamente para el índice IBEX 35. Se ha utilizado el dataset filtrado desde el 12-02-2015.
- FASE 2
  - 06_02_Multiple_lineal_regression_data_filterby_20150212_deuda_publica+ipc+tasa_paro+pib+other_components.ipynb
Análisis desarrollado en python utilizando un modelo de regresión lineal múltiple utilizando como predictores deuda pública, IPC, tasa de paro, PIB y los diez componentes más importantes que pertenecen a ese índice. Se ha utilizado el dataset filtrado desde el 12-02-2015.
  - 07_02_Series_temporales_data_filterby_20150212_deuda_publica+ipc+tasa+paro+pib+other_components.ipynb
Análisis desarrollado en python utilizando los modelos ARIMA(p,d,q) y SARIMA(p,d,q)x(P,D,Q)s utilizando como variables exógenas deuda pública, IPC, tasa de paro y PIB y los diez componentes más importantes que pertenecen a ese índice. Se ha utilizado el dataset filtrado desde el 12-02-2015.
  - 08_02_Support_vector_regression_data_filtery_20150212_deuda_publica+ipc+tasa+paro+pib+other_components.ipynb
Análisis desarrollado en python utilizando el modelo support vector regression utilizando los predictores deuda pública, IPC, tasa de paro, PIB y los diez componentes más importantes que pertenecen a ese índice.  Se ha utilizado el dataset filtrado desde el 12-02-2015.

4. Visualización
- Todo lo correspondiente al directorio webpage.
Desde este website el usuario podrá obtener las predicciones para los próximos días de los modelos con mejor MSE obtenido en las distintas fases.
