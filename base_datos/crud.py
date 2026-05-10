import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from datetime import datetime

db = get_db()

def crear_tablas():
    # En MongoDB no se necesitan crear tablas
    print("Base de datos MongoDB lista ✅")

def agregar_producto(nombre, marca, precio, sku, cantidad=0):
    db.productos.insert_one({
        "nombre": nombre,
        "marca": marca,
        "precio": precio,
        "sku": sku,
        "cantidad": cantidad
    })
    print(f"Producto '{nombre}' agregado")

def consultar_producto(nombre):
    productos = list(db.productos.find(
        {"nombre": {"$regex": nombre, "$options": "i"}},
        {"_id": 0}
    ))
    return productos

def actualizar_cantidad(nombre, cantidad, tipo):
    producto = db.productos.find_one(
        {"nombre": {"$regex": nombre, "$options": "i"}}
    )
    if producto:
        if tipo == "entrada":
            nueva_cantidad = producto["cantidad"] + cantidad
        else:
            nueva_cantidad = producto["cantidad"] - cantidad

        db.productos.update_one(
            {"_id": producto["_id"]},
            {"$set": {"cantidad": nueva_cantidad}}
        )

        db.movimientos.insert_one({
            "producto_id": str(producto["_id"]),
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "tipo": tipo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        print(f"Stock actualizado: {nombre} ahora tiene {nueva_cantidad}")
    else:
        print(f"Producto '{nombre}' no encontrado")

def eliminar_producto(nombre):
    db.productos.delete_one(
        {"nombre": {"$regex": nombre, "$options": "i"}}
    )
    print(f"Producto '{nombre}' eliminado")

if __name__ == "__main__":
    crear_tablas()