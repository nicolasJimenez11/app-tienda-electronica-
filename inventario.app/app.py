from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Producto, Cliente

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventario.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

app = create_app()

# ---- Vistas HTML ----
@app.get("/")
def home():
    return redirect(url_for("inventario"))

@app.get("/inventario")
def inventario():
    productos = Producto.query.order_by(Producto.id).all()
    return render_template("inventario.html", productos=productos)

@app.get("/pc2-form")
def pc2_form():
    # formulario simple para PC2 (también puede abrirlo cualquiera)
    return render_template("form_pc2.html")

# ---- API v1 (básica) ----
@app.post("/v1/productos")
def crear_producto_v1():
    # admite form-urlencoded o JSON
    data = request.get_json(silent=True) or request.form
    try:
        pid = int(data.get("id"))
        nombre = data.get("nombre") or data.get("producto")  # por compatibilidad con tu campo "Producto"
        cantidad = int(data.get("cantidad"))
        precio = float(data.get("precio"))
        if not nombre:
            return jsonify({"error": "nombre requerido"}), 400

        # upsert sencillo: si existe, actualiza
        prod = Producto.query.get(pid)
        if prod:
            prod.nombre = nombre
            prod.cantidad = cantidad
            prod.precio = precio
        else:
            prod = Producto(id=pid, nombre=nombre, cantidad=cantidad, precio=precio)
            db.session.add(prod)
        db.session.commit()
        return jsonify({"ok": True, "id": prod.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ---- API v2 (ejemplo de versión: endpoint y esquema podrían variar) ----
@app.post("/v2/productos")
def crear_producto_v2():
    # v2 podría exigir JSON estrictamente y validar más
    data = request.get_json(force=True)
    pid = int(data["id"])
    nombre = data["nombre"]
    cantidad = int(data["cantidad"])
    precio = float(data["precio"])

    prod = Producto.query.get(pid)
    if prod:
        prod.nombre = nombre
        prod.cantidad = cantidad
        prod.precio = precio
    else:
        prod = Producto(id=pid, nombre=nombre, cantidad=cantidad, precio=precio)
        db.session.add(prod)
    db.session.commit()
    return jsonify({"ok": True, "version": "v2", "id": prod.id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

