from rich.console import Console
from rich.table import Table
from rich import box
from database import get_db

console = Console()
db = get_db()

def mostrar_productos():
    tabla = Table(title="📦 Lista de Productos", box=box.ROUNDED)
    tabla.add_column("ID", style="cyan")
    tabla.add_column("Nombre", style="white")
    tabla.add_column("Marca", style="yellow")
    tabla.add_column("Precio", style="green")
    tabla.add_column("Cantidad", style="red")

    productos = db.productos.find().limit(50)
    for p in productos:
        tabla.add_row(
            str(p.get("id", "")),
            str(p.get("nombre", "")),
            str(p.get("marca", "")),
            f"${p.get('precio', 0)}",
            str(p.get("cantidad", 0))
        )
    console.print(tabla)

def menu():
    while True:
        console.print("\n[bold cyan]===== MENÚ =====[/bold cyan]")
        console.print("[1]  Ver productos")
        console.print("[0] Salir")

        opcion = input("\nElige: ")
        if opcion == "1":
            mostrar_productos()
        elif opcion == "0":
            break

if __name__ == "__main__":
    menu()