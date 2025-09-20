from tablas import Tablas
from parametricas_apareadas import IMCMujeresAdultas
import logging
import sys
from analisis_up import AlimentosUltraprocesados
from calorias import ConsumoCaloriasNiños2a5
from herramientas.configuracion import Configuracion
from imc import IMC

def configuracion():
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def analisis():
    configuracion = Configuracion("./config/config.json")
    tablas = Tablas("./data/ENNyS2_encuesta.csv", 
                    "./data/Base_Alimentos_Bebidas_Suplementos.csv",
                    "./data/Base_Nutrientes.csv", 
                    configuracion)
    
    encuesta = tablas.tabla_encuesta()
    # alimentos = tablas.tabla_alimentos()
    # nutrientes = tablas.tabla_nutrientes()
    
    # up = AlimentosUltraprocesados(configuracion)
    # up.analisis(alimentos)
    
    # ma = IMCMujeresAdultas(configuracion, encuesta)
    # ma.analisis()
    
    # c = ConsumoCaloriasNiños2a5(nutrientes, configuracion)
    # c.analisis()
    # c.graficos()
    imc = IMC(encuesta)   
    imc.analisis() 
    imc.graficos()
    
if __name__ == "__main__":
    configuracion()
    analisis()