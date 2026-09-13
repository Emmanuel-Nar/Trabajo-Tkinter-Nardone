import tkinter as tk
from tkinter import ttk, messagebox

class CRUD:
    
    def __init__(self, padre, gestor_datos):
        self.padre = padre
        self.gestor_datos = gestor_datos
        self.campos_entrada = {}
        self.mapa_ids = {}
        
        self.color_fondo = "#d9d9d9"
        self.color_boton = "#1a1a1a"
        self.color_boton_texto = "#ffffff"
        self.color_texto = "#111111"
        
        self.ventana = tk.Toplevel(padre)
        self.ventana.title(self.obtener_titulo())
        self.ventana.geometry("650x450")
        self.ventana.configure(bg=self.color_fondo)
        
        self.configurar_estilos()
        
        self.construir_interfaz()
        self.cargar_datos()
    
    def configurar_estilos(self):
        estilo = ttk.Style(self.ventana)
        estilo.theme_use('clam')
        
        estilo.configure("TFrame", background=self.color_fondo)
        estilo.configure("TLabelframe", background=self.color_fondo)
        estilo.configure("TLabelframe.Label", background=self.color_fondo,
                          foreground=self.color_texto, font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabel", background=self.color_fondo,
                          foreground=self.color_texto)
        
        estilo.configure("TButton", background=self.color_boton,
                          foreground=self.color_boton_texto, borderwidth=0,
                          focuscolor=self.color_boton)
        estilo.map("TButton",
                   background=[("active", "#333333")],
                   foreground=[("active", self.color_boton_texto)])
    
    def construir_interfaz(self):
        
        frame_principal = ttk.Frame(self.ventana, padding="10")
       
        frame_principal.place(x=0, y=0, width=650, height=450)
        
        frame_entrada = ttk.LabelFrame(frame_principal, text="Datos", padding="2")
        frame_entrada.pack(fill=tk.X, pady=(0, 2))
        
        frame_entrada.columnconfigure(0, weight=1)
        frame_entrada.columnconfigure(1, weight=10)
        
        campos = self.obtener_campos()
        fila = 0 
        for clave, etiqueta in campos.items():
            ttk.Label(frame_entrada, text=f"{etiqueta}:").grid(
                row=fila, column=0, sticky=tk.W, pady=5, padx=(0, 10)
            )
            
            entrada = ttk.Entry(frame_entrada, width=45)
            entrada.grid(row=fila, column=1, sticky=tk.W, pady=5)
            
            self.campos_entrada[clave] = entrada
            fila += 1
        
        frame_botones = ttk.Frame(frame_entrada)
        frame_botones.grid(row=fila, column=0, columnspan=2, pady=15)
        
        ttk.Button(frame_botones, text="Crear", 
                  command=self.crear, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text=" Actualizar", 
                  command=self.actualizar, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text=" Eliminar", 
                  command=self.eliminar, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text=" Limpiar", 
                  command=self.limpiar, width=12).pack(side=tk.LEFT, padx=5)
        
        frame_tabla = ttk.LabelFrame(frame_principal, text="Registros", padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        columnas = list(campos.keys())
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=campos[col])
            self.tabla.column(col, width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, 
                                 command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tabla.bind('<<TreeviewSelect>>', self.al_seleccionar)
    
    def obtener_titulo(self):
        raise NotImplementedError("Las clases hijas deben implementar obtener_titulo()")
    
    def obtener_campos(self):
        raise NotImplementedError("Las clases hijas deben implementar obtener_campos()")
    
    def obtener_entidad(self):
        raise NotImplementedError("Las clases hijas deben implementar obtener_entidad()")
    
    def cargar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        datos = self.gestor_datos.obtener_todos(self.obtener_entidad())
        campos = self.obtener_campos()
        
        self.mapa_ids = {}
        for registro in datos:
            claves_registro = list(registro.keys())
            id_registro = registro[claves_registro[0]]
            valores = [registro[clave] for clave in campos.keys()]
            iid = str(id_registro)
            self.tabla.insert("", "end", iid=iid, values=valores)
            self.mapa_ids[iid] = id_registro
    
    def crear(self):
        if not self.validar_campos():
            messagebox.showwarning("Campos Vacíos", 
                                 "Todos los campos son obligatorios")
            return
        
        datos = self.obtener_datos()
        
        if hasattr(self, 'validar_especifico'):
            valido, mensaje = self.validar_especifico(datos)
            if not valido:
                messagebox.showwarning("Datos Inválidos", mensaje)
                return
        
        self.gestor_datos.crear(self.obtener_entidad(), datos)
        self.cargar_datos()
        self.limpiar()
        messagebox.showinfo("Éxito", "Registro creado correctamente")
    
    def actualizar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selección requerida", 
                                 "Seleccione un registro para actualizar")
            return
        
        if not self.validar_campos():
            messagebox.showwarning("Campos Vacíos", 
                                 "Todos los campos son obligatorios")
            return
        
        datos = self.obtener_datos()
        
        if hasattr(self, 'validar_especifico'):
            valido, mensaje = self.validar_especifico(datos)
            if not valido:
                messagebox.showwarning("Datos Inválidos", mensaje)
                return
        
        id_registro = self.mapa_ids.get(seleccionado[0], seleccionado[0])
        
        self.gestor_datos.actualizar(self.obtener_entidad(), id_registro, datos)
        self.cargar_datos()
        self.limpiar()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente")
    
    def eliminar(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selección requerida", 
                                 "Seleccione un registro para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            id_registro = self.mapa_ids.get(seleccionado[0], seleccionado[0])
            
            self.gestor_datos.eliminar(self.obtener_entidad(), id_registro)
            self.cargar_datos()
            self.limpiar()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
    
    def al_seleccionar(self, event):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return
        
        valores = self.tabla.item(seleccionado[0])['values']
        campos = list(self.obtener_campos().keys())
        
        for i, clave in enumerate(campos):
            if i < len(valores):
                self.campos_entrada[clave].delete(0, tk.END)
                self.campos_entrada[clave].insert(0, str(valores[i]))
    
    def obtener_datos(self):
        datos = {}
        for clave, entrada in self.campos_entrada.items():
            datos[clave] = entrada.get().strip()
        return datos
    
    def limpiar(self):
        for entrada in self.campos_entrada.values():
            entrada.delete(0, tk.END)
    
    def validar_campos(self):
        for entrada in self.campos_entrada.values():
            if not entrada.get().strip():
                return False
        return True
