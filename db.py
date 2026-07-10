import sqlite3

db = 'contracts.db'

def database_setup():
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS contracts (
                   ocid TEXT PRIMARY KEY,
                   publish_date TEXT,
                   title TEXT,
                   status TEXT,
                   value_amount REAL,
                   value_currency TEXT,
                   buyer_name TEXT,
                   supplier_name TEXT,
                   raw_json TEXT,
                   hash TEXT)
                     ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            config_key TEXT PRIMARY KEY,
            config_value TEXT
        )
    ''')
    connect.commit()
    connect.close()
    print('Database established successfully.')

if __name__ == "__main__":
    database_setup()

def insert_contract(ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, hash):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute('''
                   INSERT OR REPLACE INTO contracts (ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, hash))
    connect.commit()
    connect.close()

