from flask import Flask, render_template, jsonify
import pandas as pd
import os
import sqlite3
from aggregation import *
import json

app=Flask(__name__)

# conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
# cursor = conn.cursor()

# pd.to_datetime(df['last_trade_timestamp'] / 1000, unit='s')

def getTokensDf():
    conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
    cursor = conn.cursor()
    query="SELECT * FROM tokens"
    df=pd.read_sql(query, conn)
    conn.close()
    return df

def getTokensData(address):
    conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
    cursor = conn.cursor()
    # address='2J3uWcDQ1AcWH4bUaiuiBfsc782RkPPDQ4RhLLbdpump'
    # cursor.execute(f'SELECT * FROM transactions WHERE mint = "{address}"')
    # cursor.fetchall()
    query=f'SELECT * FROM transactions WHERE mint = "{address}"'
    df=pd.read_sql(query, conn)
    conn.close()
    return df

def getSingleTokenData(address):
    conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
    cursor = conn.cursor()
    query=f'SELECT * FROM tokens WHERE token_address = "{address}"'
    df=pd.read_sql(query, conn)
    conn.close()
    return df


def getTokensTransactions(address):
    conn = sqlite3.connect("pump_fun.db")  # Creates a file called pump_fun.db
    cursor = conn.cursor()
    # address='2J3uWcDQ1AcWH4bUaiuiBfsc782RkPPDQ4RhLLbdpump'
    # cursor.execute(f'SELECT * FROM transactions WHERE mint = "{address}"')
    # cursor.fetchall()
    query=f'SELECT * FROM transactions WHERE mint = "{address}"'
    df=pd.read_sql(query, conn)
    conn.close()
    return df

@app.route('/')
def home():
    df=getTokensDf()
    data = df.to_dict(orient='records')[:5]
    return render_template('index.html', tokenData=data)

@app.route('/tokens')
def tokens():
    df=getTokensDf()
    data = df.to_dict(orient='records')[:50]
    return jsonify(data)

@app.route('/token_transactions/<token_address>')
def token_transactions(token_address):

    # return render_template('token_details.html')
    tf = getTokensData(token_address) 
    data = tf.to_dict(orient='records')
    if data:
        return jsonify(data)
    else:
        return "Token not found", 404
    
@app.route('/token_details/<token_address>')
def token_details(token_address):
    print(f'THIS IS THE TOKEN ADDRESS!!! {token_address}')
    # return render_template('token_details.html')
    tf = getTokensTransactions(token_address) 
    transactionData = tf.to_dict(orient='records')
    gf=aggregateTransactions(tf)
    traderData=gf.to_dict(orient='records')
    df = getSingleTokenData(token_address)
    tokenData = df.to_dict(orient='records')

    summaryData=getTransactionSummary(gf, tf, df)
    data = {'token': tokenData, 'transactions': transactionData, 'aggregation': traderData, 'summaryData':summaryData}
    # data={'test':1, 'test2':2}
    # with open('test.txt', 'w') as f:
    #     f.write(json.dumps(data))
    if data:
        return jsonify(data)
    else:
        return "Token not found", 404
    
if __name__=='__main__':
    app.run(debug=True)