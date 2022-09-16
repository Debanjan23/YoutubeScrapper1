import os.path
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request
from flask_cors import cross_origin
import json
import requests
import re
import pandas as ps
import Data
#from Schema import Load_Data as ld

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/load',methods=['POST','GET'])
@cross_origin()
def main():
    if request.method=='POST':
        try:
            URL = request.form['content'].replace(" ","")
            soup = bs(requests.get(URL).content, "html.parser")
            data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify)).group(1)
            json_data = json.loads(data)
            channel_id = json_data['header']['c4TabbedHeaderRenderer']['channelId']
            Data_obj = Data.Data()
            p = Data_obj.get_video_stats(channel_id)
            df = ps.DataFrame(p)
            html = df.to_html()
            if os.path.exists('templates/result_data.html'):
                os.remove('templates/result_data.html')
                text_file=open('templates/result_data.html','w', encoding='utf-8')
                text_file.write(html)
                text_file.close()
            else:
                text_file = open('templates/result_data.html', 'w', encoding='utf-8')
                text_file.write(html)
                text_file.close()
            #filename = df['Youtuber_name'][0].replace(' ','_') + '.csv'
            #df.to_csv(filename, encoding='utf-8', index=False)
            #if filename!='':
              #os.system("csvsql --db mysql://root:Skhan87!@localhost:3306/test --insert --overwrite "+filename)

            #msg = ld.Load_Data.load_mongo(p)
            #if msg == 1:
            #return render_template('load_data.html')
            return render_template('result_data.html')
            #else:
            #return 'Data not loaded'
        except Exception as e:
          print(e)

if __name__=='__main__':
    #app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)
