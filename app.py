from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime
import secrets

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cafecart.db"
app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key-before-deployment"

PRODUCTS = [
    {"id": 1, "name": "Classic Cappuccino", "category": "Hot Coffee", "price": 120, "description": "Espresso with steamed milk and a soft foam top.", "symbol": "☕", "tag": "Bestseller"},
    {"id": 2, "name": "Caramel Latte", "category": "Hot Coffee", "price": 145, "description": "Smooth coffee with a gentle caramel sweetness.", "symbol": "🥤", "tag": "Popular"},
    {"id": 3, "name": "Dark Mocha", "category": "Hot Coffee", "price": 155, "description": "A rich coffee blended with chocolate.", "symbol": "🍫", "tag": ""},
    {"id": 4, "name": "Masala Chai", "category": "Tea", "price": 55, "description": "Indian tea brewed with warming spices.", "symbol": "🫖", "tag": "Classic"},
    {"id": 5, "name": "Iced Coffee", "category": "Cold Drinks", "price": 130, "description": "Chilled coffee served over ice.", "symbol": "🧋", "tag": "Chilled"},
    {"id": 6, "name": "Cold Cocoa", "category": "Cold Drinks", "price": 125, "description": "Creamy cocoa with a chocolate finish.", "symbol": "🥛", "tag": ""},
    {"id": 7, "name": "Strawberry Milkshake", "category": "Cold Drinks", "price": 140, "description": "A cool, fruity milkshake.", "symbol": "🍓", "tag": ""},
    {"id": 8, "name": "Chocolate Brownie", "category": "Cakes & Desserts", "price": 95, "description": "A soft brownie with a deep cocoa flavour.", "symbol": "🍰", "tag": "Sweet pick"},
    {"id": 9, "name": "Vanilla Cupcake", "category": "Cakes & Desserts", "price": 75, "description": "A little vanilla cake topped with creamy frosting.", "symbol": "🧁", "tag": ""},
    {"id": 10, "name": "Blueberry Cheesecake", "category": "Cakes & Desserts", "price": 165, "description": "Creamy cheesecake with a berry topping.", "symbol": "🫐", "tag": ""},
    {"id": 11, "name": "Veggie Club Sandwich", "category": "Sandwiches", "price": 135, "description": "Toasted bread with fresh vegetables and a light spread.", "symbol": "🥪", "tag": "Filling"},
    {"id": 12, "name": "Paneer Tikka Sandwich", "category": "Sandwiches", "price": 155, "description": "Spiced paneer and vegetables in toasted bread.", "symbol": "🥙", "tag": ""},
    {"id": 13, "name": "Cheese Garlic Toast", "category": "Snacks", "price": 90, "description": "Toasted bread with garlic and melted cheese.", "symbol": "🍞", "tag": ""},
    {"id": 14, "name": "Peri Peri Fries", "category": "Snacks", "price": 105, "description": "Crispy fries tossed in a mild peri-peri seasoning.", "symbol": "🍟", "tag": "Popular"},
    {"id": 15, "name": "Corn Cheese Bites", "category": "Snacks", "price": 115, "description": "Golden bites filled with sweet corn and cheese.", "symbol": "🌽", "tag": ""},
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                items_json TEXT NOT NULL,
                total REAL NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Received',
                created_at TEXT NOT NULL
            )
        """)

@app.template_filter("inr")
def inr(value):
    return "₹{:,.0f}".format(value)

@app.route("/")
def home():
    return render_template("index.html", featured=PRODUCTS[:4])

@app.route("/menu")
def menu():
    return render_template("menu.html", products=PRODUCTS, categories=sorted(set(p["category"] for p in PRODUCTS)))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please complete every field.", "error")
        elif len(name) > 100 or len(email) > 150 or len(message) > 1500:
            flash("One or more fields are too long.", "error")
        else:
            flash("Thank you! Your message has been received in this demo.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        return render_template("checkout.html")
    name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    payment = request.form.get("payment_method", "Cash on Delivery")
    items_raw = request.form.get("cart_json", "")
    if not name or not phone or not address or not items_raw:
        flash("Please enter your details and add items to your cart.", "error")
        return redirect(url_for("checkout"))
    if len(name) > 100 or len(phone) > 20 or len(address) > 500:
        flash("Please check the length of your details.", "error")
        return redirect(url_for("checkout"))
    try:
        import json
        submitted = json.loads(items_raw)
        if not isinstance(submitted, list) or not submitted:
            raise ValueError()
        clean_items, total = [], 0
        product_by_id = {p["id"]: p for p in PRODUCTS}
        for item in submitted:
            pid = int(item.get("id", 0))
            qty = int(item.get("qty", 0))
            if pid not in product_by_id or qty < 1 or qty > 20:
                raise ValueError()
            product = product_by_id[pid]
            line_total = product["price"] * qty
            total += line_total
            clean_items.append({"id": pid, "name": product["name"], "price": product["price"], "qty": qty, "line_total": line_total})
    except (ValueError, TypeError, AttributeError):
        flash("Your cart could not be verified. Please review it and try again.", "error")
        return redirect(url_for("checkout"))
    if payment not in ("Cash on Delivery", "Pay at Café"):
        payment = "Cash on Delivery"
    order_code = "CC" + datetime.now().strftime("%y%m%d") + secrets.token_hex(2).upper()
    with get_db() as conn:
        conn.execute("""
            INSERT INTO orders (order_code, customer_name, phone, address, items_json, total, payment_method, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_code, name, phone, address, json.dumps(clean_items), total, payment, "Received", datetime.now().strftime("%d %b %Y, %I:%M %p")))
    return render_template("confirmation.html", order_code=order_code, name=name, total=total)

@app.route("/api/products")
def api_products():
    return jsonify(PRODUCTS)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

init_db()

if __name__ == "__main__":
    app.run(debug=True)
