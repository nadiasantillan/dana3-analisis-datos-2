import json

class Configuracion:
    def __init__(self, archivo_configuracion):
        with open(archivo_configuracion, "rt") as f:
            self.configuracion = json.load(f)
            
    def as_dict(self):
        return self.configuracion