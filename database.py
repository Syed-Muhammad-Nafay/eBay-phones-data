import psycopg2

DB_config = {
    'dbname': 'Flag_ship',
    'user': 'postgres',
    'password': 'sql',
    'host': 'localhost'
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_config)
        return conn
    except Exception as e:
        print("Connection failed:", e)

def initiat_schema(table_name='product'):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS WEB_SCRAPPER_DATA_FOR_{table_name} (
                    ID BIGSERIAL PRIMARY KEY,
                    PRODUCT_NAME VARCHAR(255) NOT NULL,
                    CONDITIONS VARCHAR(50) NOT NULL,
                    PRICE VARCHAR(255) NOT NULL,
                    DELIVERY_CHARGES VARCHAR(255) NOT NULL,
                    LOCATION_OF_ORIGIN VARCHAR(255) NOT NULL,
                    CATEGORY VARCHAR(255) NOT NULL
                );
            """)
            conn.commit()
            print(f"Table WEB_SCRAPPER_DATA_FOR_{table_name} created or already exists.")
    except Exception as e:
        print("Error during schema creation:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_table(table_name='product'):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(f"""DROP TABLE IF EXISTS WEB_SCRAPPER_DATA_FOR_{table_name}""")
            conn.commit()
            print(f"Table WEB_SCRAPPER_DATA_FOR_{table_name} deleted successfully (if it existed).")
    except Exception as e:
        print("Error deleting table:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_a_record(product_name, condition, price, location, delivery_charges, category, table_name='product'):
    conn = None
    cur = None
    try:
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO WEB_SCRAPPER_DATA_FOR_{table_name} 
                (PRODUCT_NAME, CONDITIONS, PRICE, DELIVERY_CHARGES, LOCATION_OF_ORIGIN, CATEGORY)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (product_name, condition, price, delivery_charges, location, category))
            conn.commit()
            print("Record added successfully.")
    except Exception as e:
        print("Error adding record:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
