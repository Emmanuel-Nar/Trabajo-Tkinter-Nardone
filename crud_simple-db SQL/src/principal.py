import tkinter as tk
from tkinter import ttk
from vistas.crud_clientes import CRUDClientes
from vistas.crud_proveedores import CRUDProveedores
from controladores.gestor_datos import GestorDatos

class Aplicacion:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestion")
        self.ventana.geometry("600x350")
        self.ventana.resizable(False, False)
        
        self.color_fondo = "#d9d9d9"
        self.color_boton = "#1a1a1a"
        self.color_boton_texto = "#ffffff"
        self.color_texto = "#111111"
        
        self.ventana.configure(bg=self.color_fondo)
        self.gestor_datos = GestorDatos()
        
        self.configurar_estilos()
        self.construir_menu()
    
    def configurar_estilos(self):
        estilo = ttk.Style(self.ventana)
        estilo.theme_use('clam')
        
        estilo.configure("TFrame", background=self.color_fondo)
        estilo.configure("TLabel", background=self.color_fondo,
                          foreground=self.color_texto)
        
        estilo.configure("TButton", background=self.color_boton,
                          foreground=self.color_boton_texto, borderwidth=0,
                          focuscolor=self.color_boton)
        estilo.map("TButton",
                   background=[("active", "#333333")],
                   foreground=[("active", self.color_boton_texto)])
    
    def construir_menu(self):
        titulo = ttk.Label(self.ventana, text="Sistema de Gestion", 
                          font=("Arial", 18, "bold"))
        titulo.pack(pady=30)
        
        subtitulo = ttk.Label(self.ventana, text="Seleccione una opción:", 
                             font=("Arial", 12))
        subtitulo.pack(pady=10)
        
        frame_botones = ttk.Frame(self.ventana)
        frame_botones.pack(pady=20)
        
        btn_clientes = ttk.Button(frame_botones, text="👥 Clientes", 
                                 command=self.abrir_clientes, 
                                 width=25, padding=8)
        btn_clientes.pack(pady=8)
        
        btn_proveedores = ttk.Button(frame_botones, text="🏢 Proveedores", 
                                    command=self.abrir_proveedores, 
                                    width=25, padding=8)
        btn_proveedores.pack(pady=8)
        
        btn_salir = ttk.Button(frame_botones, text="❌ Salir", 
                              command=self.ventana.quit, 
                              width=25, padding=8)
        btn_salir.pack(pady=8)
      
    
    def abrir_clientes(self):
        CRUDClientes(self.ventana, self.gestor_datos)
    
    def abrir_proveedores(self):
        CRUDProveedores(self.ventana, self.gestor_datos)
    
    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()
