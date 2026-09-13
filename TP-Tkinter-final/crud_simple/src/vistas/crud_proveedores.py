from vistas.crud import CRUD

class CRUDProveedores(CRUD):
    
    def obtener_titulo(self):
        return "Gestión de Proveedores"
    
    def obtener_campos(self):
        return {
            "razon_social": "Razón Social",
            "cuit": "CUIT",
            "direccion": "Dirección",
            "telefono": "Teléfono",
            "email": "Correo Electrónico"
        }
    
    def obtener_entidad(self):
        return "proveedor"
    
    def validar_especifico(self, datos):
        if not datos['cuit'].isdigit():
            return False, "El CUIT debe contener solo números"
        
        if len(datos['cuit']) != 11:
            return False, "El CUIT debe tener exactamente 11 dígitos"
        
        if not datos['telefono'].isdigit():
            return False, "El teléfono debe contener solo números"
        
        if '@' not in datos['email']:
            return False, "El correo electrónico debe tener un formato válido"
        
        return True, ""
