from vistas.crud import CRUD

class CRUDClientes(CRUD):
    
    def obtener_titulo(self):
        return "Programa de gestión de Clientes"
    
    def obtener_campos(self):
        return {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "dni": "DNI",
            "telefono": "Teléfono",
            "email": "Correo Electrónico"
        }
    
    def obtener_entidad(self):
        return "cliente"
    
    def validar_especifico(self, datos):
        if not datos['dni'].isdigit():
            return False, "El DNI debe contener solo números"
        
        if not datos['telefono'].isdigit():
            return False, "El teléfono debe contener solo números"
        
        if '@' not in datos['email']:
            return False, "El correo electrónico debe tener un formato válido"
        
        return True, ""
