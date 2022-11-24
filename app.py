from flask import Flask, request, app, jsonify, url_for, render_template 
import pandas as pd 

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")  
def about():
    return render_template('about.html')


@app.route('/schedule',methods=['GET', 'POST'])
def schedule():
    
    df=[]
    tea1 = request.form.get("Tea1")
    df.append(tea1)
    tea2 = request.form.get("Tea2")
    df.append(tea2)
    tea3 = request.form.get("Tea3")
    df.append(tea3)
    df = pd.DataFrame()

    
   
   
    
    
    return render_template('home.html', schedule_text = "The schedule may start from  {}" .format(df))

if __name__ == '__main__':
    app.run(debug=True)