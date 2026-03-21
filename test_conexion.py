from database import get_db

try:
    db = get_db()
    db.command("ping")
    print("Conectado a MongoDB Atlas correctamente!")
except Exception as e:
    print(f" Error de conexión: {e}")