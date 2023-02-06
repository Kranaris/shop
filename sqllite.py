import sqlite3
import sqlite3 as sq


async def db_connect() -> None:
    global db, cur

    db = sq.connect('products.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS products(product_id INTEGER PRIMARY KEY, photo TEXT, title TEXT, description TEXT, price INTEGER)")

    db.commit()


async def get_all_products_bd() -> list:
    products = cur.execute("SELECT * FROM products").fetchall()
    return products


async def create_new_product(state) -> sqlite3.Cursor:
    async with state.proxy() as data:
        new_product = cur.execute("INSERT INTO products (photo, title, description, price) VALUES (?, ?, ?, ?)",
                                  (data['photo'],
                                   data['title'],
                                   data['description'],
                                   data['price']))
        db.commit()
    return new_product


async def delete_product(product_id: int) -> None:
    cur.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    db.commit()


async def edit_some(product_id: int, column: str, text: str) -> None:
    cur.execute(f"UPDATE products SET {column} = ? WHERE product_id = ?", (text, product_id,))
    db.commit()
