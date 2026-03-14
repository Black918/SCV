import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("almacen.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            precio REAL,
            sku TEXT,
            cantidad INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            tipo TEXT,
            fecha TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de datos ready")

def agregar_producto(nombre, marca, precio, sku, cantidad=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, marca, precio, sku, cantidad)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, marca, precio, sku, cantidad))
    conn.commit()
    conn.close()
    print(f"Producto '{nombre}' agregado")

def consultar_producto(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM productos WHERE nombre LIKE ?
    ''', (f'%{nombre}%',))
    productos = cursor.fetchall()
    conn.close()
    return productos

def actualizar_cantidad(nombre, cantidad, tipo):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, cantidad FROM productos WHERE nombre LIKE ?', (f'%{nombre}%',))
    producto = cursor.fetchone()
    
    if producto:
        if tipo == "entrada":
            nueva_cantidad = producto[1] + cantidad
        else:
            nueva_cantidad = producto[1] - cantidad
            
        cursor.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, producto[0]))
        
        cursor.execute('''
            INSERT INTO movimientos (producto_id, cantidad, tipo, fecha)
            VALUES (?, ?, ?, ?)
        ''', (producto[0], cantidad, tipo, datetime.now().strftime("%d/%m/%Y %H:%M")))
        
        conn.commit()
        print(f"Stock actualizado: {nombre} ahora tiene {nueva_cantidad}")
    else:
        print(f"Producto '{nombre}' no encontrado")
    
    conn.close()

def eliminar_producto(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE nombre LIKE ?', (f'%{nombre}%',))
    conn.commit()
    conn.close()
    print(f"Producto '{nombre}' eliminado")

if __name__ == "__main__":
    crear_tablas()