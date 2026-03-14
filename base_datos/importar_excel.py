import pandas as pd
from crud import crear_tablas, agregar_producto

def importar_desde_excel(archivo):
    print("Leyendo Excel...")
    df = pd.read_excel(archivo, sheet_name="DATA")
    
    crear_tablas()
    
    total = 0
    errores = 0
    
    for index, fila in df.iterrows():
        try:
            nombre = str(fila["Nombre"]).strip()
            marca = str(fila["Marca"]).strip()
            precio = float(fila["Precio"]) if pd.notna(fila["Precio"]) else 0.0
            sku = str(fila["Sku"]).strip()
            
            agregar_producto(nombre, marca, precio, sku, cantidad=0)
            total += 1
            
            if total % 500 == 0:
                print(f"{total} productos importados...")
                
        except Exception as e:
            errores += 1
            continue
    
    print(f"Importacion completa: {total} productos, {errores} errores")

if __name__ == "__main__":
    importar_desde_excel("C:\\Users\\fabri\\SCV\\base_datos\\productos.xls")