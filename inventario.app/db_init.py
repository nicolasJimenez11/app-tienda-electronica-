from app import create_app
from models import db, Producto, Cliente

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    # Datos de ejemplo:
    db.session.add_all([
        Producto(id=1, nombre="Mouse Gamer", cantidad=15, precio=19.99),
        Producto(id=2, nombre="Teclado Mecánico", cantidad=8, precio=49.90),
    ])
    db.session.add_all([
        Cliente(id=1, nombre="Cliente Demo", email="demo@tienda.com"),
    ])
    db.session.commit()
    print("DB inicializada.")
