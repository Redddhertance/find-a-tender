import sqlite3
from db import insert_contract, db
import hashlib
from datetime import datetime, timedelta

def contract_hash(title,status,value,end_date,supplier=None):
    #prevents crashes
    safe_title = str(title) if title else ""
    safe_status = str(status) if status else ""
    safe_value = str(value) if value else ""
    safe_end_date = str(end_date) if end_date else ""
    safe_supplier = str(supplier) if supplier else ""

    raw_string = '{}|{}|{}|{}|{}'.format(safe_title, safe_status, safe_value, safe_end_date, safe_supplier)
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

def process_contract(ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, contract_hash):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()

    #does contract exist
    cursor.execute('SELECT hash FROM contracts WHERE ocid = ?', (ocid,))
    result = cursor.fetchone()

    if result is None:
        #new, insert
        cursor.execute('''
                       INSERT INTO contracts (ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, hash)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                          ''',
        (ocid, publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, contract_hash))
        action = 'NEW'
    else:
        existing_hash = result[0]
        if existing_hash != contract_hash:
            #updated, update record
            cursor.execute('''
                           UPDATE contracts
                           SET publish_date = ?, title = ?, status = ?, value_amount = ?, value_currency = ?, buyer_name = ?, supplier_name = ?, raw_json = ?, hash = ?
                           WHERE ocid = ?
                           ''',
            (publish_date, title, status, value_amount, value_currency, buyer_name, supplier_name, raw_json, contract_hash, ocid))
            action = 'UPDATED'
        else:
            #no change
            action = 'UNCHANGED'
    connect.commit()
    connect.close()

    return action

def get_sync_time():
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    
    cursor.execute("SELECT config_value FROM system_config WHERE config_key = 'last_sync_time'")
    result = cursor.fetchone()
    connect.close()

    if result:
       #identified timestamp
        return result[0]
    else:
        #default to an hour ago
        one_hour_ago = datetime.now() - timedelta(hours=1)
        #formats to iso 8601
        return one_hour_ago.strftime('%Y-%m-%dT%H:%M:%S')
    
def update_sync_time(timestamp_string):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO system_config (config_key, config_value) 
        VALUES ('last_sync_time', ?)
    ''', (timestamp_string,))
    connect.commit()
    connect.close()