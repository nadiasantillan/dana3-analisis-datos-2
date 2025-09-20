import matplotlib.pyplot as plt
from seaborn import histplot
import logging
from prettytable import PrettyTable

class ContinuousVariable:
    def __init__(self, configuracion_dict, name, series):
        self.configuracion_dict = configuracion_dict
        self.name = name
        self.series = series
        
    def analisis(self):
        logging.warning("NaNs: %d", self.series.isna().sum())
        logging.warning("Faltantes: %d", self.series.isnull().sum())     
        
        tabla = PrettyTable()
        tabla.field_names = ["Min", "Max", "Media", "Mediana", "Desvío", "Q1", "Q3", "IQR", "Q1 - 1.5 IQR", "Q3 + 1.5 IQR"]
        q1, q3 = self.series.quantile([.25, .75])
        iqr = q3 - q1
        mino = q1 - 1.5 * iqr
        maxo = q3 + 1.5 * iqr
        tabla.add_row((
            self.series.min(), 
            self.series.max(), 
            self.series.mean(), 
            self.series.median(), 
            self.series.std(), 
            q1, 
            q3,
            iqr, 
            mino,
            maxo))

        logging.info("Variable %s: %s", self.name, tabla)   
        
    def graficos(self):
        self._histograma()
        
    def _histograma(self):
        histplot(self.series, kde=True)
        plt.xlabel(self.name)
        plt.ylabel("Frecuencia")