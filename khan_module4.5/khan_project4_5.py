# -*- coding: utf-8 -*-
"""
Data 608, Fall 2018
author: Mehdi Khan
"""

import pandas as pd
from sodapy import Socrata
from flask import Flask, render_template, make_response, jsonify
 

app = Flask(__name__)

# Shows the main page
@app.route("/")
def show_main_page():
    return render_template('main.html', msg = "!! WELCOME !!")

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

client = Socrata("data.cityofnewyork.us", None)
results = client.get("5rq2-4hqu", limit=5000)
results_df = pd.DataFrame.from_records(results)
#results_df.columns
data = results_df #pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json')

@app.route('/boroname/<string:borough_name>', methods=['GET'])
def show_data(borough_name):
     #datasubset = data[data.boroname==borough_name,['spc_common','health','steward']]
     borough_name = borough_name.title()
     tree= ['American hornbeam',' American linden ','Callery pear','London planetree','Norway maple','Siberian elm','Sophora','ginkgo','honeylocust','pin oak']
     
     try:             
         datasubset = data.loc[(data.boroname==borough_name) & (data.spc_common.isin(tree)) ,['boroname','spc_common','health','steward']]
         df =  pd.DataFrame( datasubset.groupby(['health','spc_common']).size())
         df1 = df.unstack(level=0).reset_index()
         df1.columns=df1.columns.droplevel()
         df1.columns = ['Tree Species', 'Fair', 'Good', 'Poor']
         df1=df1.fillna(0)
         df1 = df1.astype({'Fair': int, 'Good': int,'Poor':int})
         message = 'The number of ten tree species in fair, good and poor health status in your selected borough:'
     except ValueError:
         message = 'ERROR: You must select one of the above listed brough names!!!  you selected:'
     return render_template('main.html', tbl =df1.to_html(index=False, classes="statTable") , boro=borough_name, msg=message)


if __name__ == '__main__':
     app.run(debug=True)
     