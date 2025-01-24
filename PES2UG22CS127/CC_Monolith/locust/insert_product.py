import sqlite3
import requests
import random

def initialize_auth_db():
    connection = sqlite3.connect("auth.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

def initialize_products_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

def get_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    
    connection.close()
    return products

def insert_cart_products(cookies, products):
    random.seed(42)
    for i in range(100):
        p = random.choice(products)
        print("http://localhost:5000/cart/{}".format(p[0]))
        r = requests.post("http://localhost:5000/cart/{}".format(p[0]), cookies=cookies)
        
        if r.status_code == 200:
            print(r)
            print("Inserted product")
        else:
            print("Failed to insert")

def insert_user(username, password):
    connection = sqlite3.connect("auth.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()

def login(username, password):
    session = requests.Session()
    payload = {
        "username": username,
        "password": password
    }
    r = session.post("http://localhost:5000/login", data=payload)
    if r.status_code == 200:
        print("Logged in successfully")
        return session.cookies
    else:
        print("Login failed")
        exit()

def main():
    username = "test123"
    password = "test123"
    
    # Initialize databases
    initialize_auth_db()
    initialize_products_db()
    
    insert_user(username, password)
    cookies = login(username, password)
    products = get_products()
    insert_cart_products(cookies, products)

if __name__ == "__main__":
    main()
