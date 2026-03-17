from database import get_db

db = get_db()
db.test.insert_one({"mensaje": "Conexión exitosa!"})
print("✅ MongoDB conectado correctamente")