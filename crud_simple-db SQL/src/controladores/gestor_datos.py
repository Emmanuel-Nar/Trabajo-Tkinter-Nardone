import sqlite3


class GestorDatos:

    def __init__(self, ruta_bd="datos.db"):
        self.conexion = sqlite3.connect(ruta_bd)
        self.conexion.row_factory = sqlite3.Row
        self.cursor = self.conexion.cursor()

    def _tabla_existe(self, entidad):
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (entidad,)
        )
        return self.cursor.fetchone() is not None

    def _crear_tabla(self, entidad, datos):
        columnas = ", ".join(f'"{clave}" TEXT' for clave in datos.keys())
        sql = f'CREATE TABLE "{entidad}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columnas})'
        self.cursor.execute(sql)
        self.conexion.commit()

    def crear(self, entidad, datos):
        if not self._tabla_existe(entidad):
            self._crear_tabla(entidad, datos)

        columnas = ", ".join(f'"{clave}"' for clave in datos.keys())
        marcadores = ", ".join("?" for _ in datos)
        valores = list(datos.values())

        sql = f'INSERT INTO "{entidad}" ({columnas}) VALUES ({marcadores})'
        self.cursor.execute(sql, valores)
        self.conexion.commit()

        nuevo_id = self.cursor.lastrowid
        return {"id": nuevo_id, **datos}

    def obtener_todos(self, entidad):
        if not self._tabla_existe(entidad):
            return []

        self.cursor.execute(f'SELECT * FROM "{entidad}"')
        filas = self.cursor.fetchall()
        return [dict(fila) for fila in filas]

    def actualizar(self, entidad, id_registro, datos):
        if not self._tabla_existe(entidad):
            return False

        asignaciones = ", ".join(f'"{clave}" = ?' for clave in datos.keys())
        valores = list(datos.values()) + [id_registro]

        sql = f'UPDATE "{entidad}" SET {asignaciones} WHERE id = ?'
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, entidad, id_registro):
        if not self._tabla_existe(entidad):
            return False

        sql = f'DELETE FROM "{entidad}" WHERE id = ?'
        self.cursor.execute(sql, (id_registro,))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def cerrar(self):
        self.conexion.close()
