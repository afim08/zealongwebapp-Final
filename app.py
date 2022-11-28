from flask import Flask, request, app, jsonify, url_for, render_template, request, session 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError 
from flask_wtf.file import FileField, FileAllowed
import pandas as pd 
import pickle 
import os
from werkzeug.utils import secure_filename

app=Flask(__name__, static_folder='static')
# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join('static', 'uploads')
 
# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {'csv'}


# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'







#schedulefunction = pickle.load(open('schedule.pkl','rb'))
df_show = pd.read_csv('Automate.csv')


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")  
def about():
    return render_template('about.html')

@app.route("/sub3")  
def subb1():
    return render_template('sub.html')

@app.route('/show_data',  methods=("POST", "GET"))
def showData():
    #df_show = pd.read_csv('Automate.csv')
    # Convert pandas dataframe to html table flask
    #df_html = df_show.to_html()
    
    df_1 =df_show.TEA
    df_2 =df_show.COUNT
    l =len(df_1)
    
    return render_template('show_csv_data.html', data_var=df_1, data_var2 = l, data_var3 = df_2)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploadFile',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']
        uploaded_df.filename ='abc.csv'
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
 
        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
 
        return render_template('upload2.html')





@app.route('/data',  methods=("POST", "GET"))
def Data():
    #df_show = pd.read_csv('Automate.csv')
    # Convert pandas dataframe to html table flask
    #df_html = df_show.to_html()
    df_show = pd.DataFrame()
    df_show = pd.read_csv('./static/uploads/abc.csv')
    df_html = df_show.to_html(classes='table table-stripped')
    #df_1 =df_show.TEA
    #df_2 =df_show.COUNT
    
    
    #return render_template('show_csv_data.html', data_var=df_1, data_var2 = l, data_var3 = df_2)
    return render_template('data.html', data_var4=df_html)


@app.route('/schedule',methods=['GET', 'POST'])
def schedule():
    
    df_tea=[]
    df_qty=[]
    tea1 = request.form.get("Tea1")
    df_tea.append(tea1)
    tea2 = request.form.get("Tea2")
    df_tea.append(tea2)
    tea3 = request.form.get("Tea3")
    df_tea.append(tea3)

    teaqty1 = request.form.get("Teacount1")
    df_qty.append(teaqty1)
    teaqty2 = request.form.get("Teacount2")
    df_qty.append(teaqty2)
    teaqty3 = request.form.get("Teacount3")
    df_qty.append(teaqty3)
    
    #schedulefunction(df_tea,df_qty)
    
    return render_template('home.html', schedule_text = "The best production schedule order is   {} and {}" .format(df1_1,df2))

if __name__ == '__main__':
    app.run(debug=True)