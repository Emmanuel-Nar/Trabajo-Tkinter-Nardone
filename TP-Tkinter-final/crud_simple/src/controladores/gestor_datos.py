class GestorDatos:
    
    def __init__(self):
        self.datos = {
            "cliente": [],
            "proveedor": []
        }
        self.contadores = {
            "cliente": 0,
            "proveedor": 0
        }
    
    def crear(self, entidad, datos):
        self.contadores[entidad] += 1
        registro = {"id": self.contadores[entidad], **datos}
        self.datos[entidad].append(registro)
        return registro
    
    def obtener_todos(self, entidad):
        return self.datos.get(entidad, [])
    
    def actualizar(self, entidad, id_registro, datos):
        for i, reg in enumerate(self.datos[entidad]):
            if reg["id"] == id_registro:
                self.datos[entidad][i] = {"id": id_registro, **datos}
                return True
        return False
    
    def eliminar(self, entidad, id_registro):
        for i, reg in enumerate(self.datos[entidad]):
            if reg["id"] == id_registro:
                del self.datos[entidad][i]
                return True
        return False
