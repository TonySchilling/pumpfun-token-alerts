import pandas as pd
import sqlite3
import os



# Step 1: Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
cursor = conn.cursor()

#Token Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_address TEXT UNIQUE NOT NULL,
    name TEXT,
    symbol TEXT,
    description TEXT,
    image_url TEXT,
    metadata_uri TEXT,
    twitter TEXT,
    telegram TEXT,
    bonding_curve TEXT,
    associated_bonding_curve TEXT,
    creator TEXT,
    created_timestamp TIMESTAMP,
    last_trade_timestamp TIMESTAMP,
    raydium_pool TEXT,
    virtual_sol_reserves TEXT,
    virtual_token_reserves TEXT,
    total_supply INT,
    website TEXT,
    usd_market_cap REAL

)
""")

def updateTokens():
    p=r'D:\crypto\scanner\data\pumpFun\site\pfSummary_20250127_113707.csv'
    pf=pd.read_csv(p)
    #Insert token data
    for index, row in pf.iterrows():
        cursor.execute("""
    INSERT INTO tokens (token_address, name, symbol, description, image_url, metadata_uri, twitter, telegram, bonding_curve, associated_bonding_curve, creator, created_timestamp, last_trade_timestamp, raydium_pool, virtual_sol_reserves, virtual_token_reserves, total_supply, website, usd_market_cap)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (row['mint'],row['name'],row['symbol'],row['description'],row['image_uri'],row['metadata_uri'],row['twitter'],row['telegram'],row['bonding_curve'],row['associated_bonding_curve'],row['creator'],row['created_timestamp'],row['last_trade_timestamp'],row['raydium_pool'],row['virtual_sol_reserves'],row['virtual_token_reserves'],row['total_supply'],row['website'],row['usd_market_cap']))




# query="SELECT * FROM tokens"
# df=pd.read_sql(query, conn)




cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    owner TEXT,
    tradeType TEXT,
    sol REAL,
    tokenAmount REAL,
    mint TEXT,
    hash TEXT,
    FOREIGN KEY (mint) REFERENCES tokens (id)
)
""")


def updateTransactionsTable(path):

    tf=pd.read_csv(path)

    for index, row in tf.iterrows():
        cursor.execute("""
        INSERT INTO transactions (date, owner, tradeType, sol, tokenAmount, mint, hash)
                        VALUES (?,?,?,?,?,?,?)""",
                        (row['blockTime'],row['owner'],row['tradeType'],row['sol'],row['amountFormatted'],row['mint'],row['hash']))

def addAllTransactions():
    p=r'D:\crypto\scanner\data\pumpFun\site\transactions'
    files=[os.path.join(p, f) for f in os.listdir(p) if '.csv' in f]

    for path in files:
        updateTransactionsTable(path)
# Commit the changes
# conn.commit()

print("Database and tables created successfully!")

# cursor.execute('DROP TABLE IF EXISTS pf_transactions')

# conn.close()