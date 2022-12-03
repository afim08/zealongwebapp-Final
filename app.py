from flask import Flask, request, app, jsonify, url_for, render_template, request, session ,flash
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

@app.route('/operations')
def operations():
    return render_template('operations.html')


@app.route('/add', methods=['POST'])
def add():
    import numpy as np
    data= [x for x in request.form.values()]
    d=np.array(data)
    daily_operation = pd.read_csv('./static/uploads/dailyoperation.csv')
    daily_operation.loc[len(daily_operation)] =d
    daily_operation= daily_operation.sort_index(ascending=False)
    


    #daily_operation.insert(0,data)
    
    daily_operation.to_csv('./static/uploads/dailyoperation.csv', index=False)
    flash('The operation has been added. ', 'success')
    
    
    daily_operation_display = daily_operation.to_html(classes='table table-stripped')
    return render_template('operations.html',data_var7= daily_operation_display)
    
@app.route('/operations_chart')
def operationsChart():

    
    operations = pd.read_csv('./static/uploads/dailyoperation.csv')
    
    operations = operations.to_html(classes='table table-stripped')
    return render_template('operationschart.html', data_var8 =operations)
    
    


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


@app.route("/packaging")  
def packaging():
    return render_template('packaging.html')

@app.route("/ingredients")  
def ingredients():

    ginger = 20 
    return render_template('ingredients.html', a = ginger)


@app.route("/blends")  
def blends():
    pass

@app.route("/origins")  
def origins():
    pass



@app.route("/inventory")  
def inventory():
    return render_template('inventory.html')


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
        import pandas as pd
        import math

        #defining all different teas and their classifications 
        origins = ['Oolong','Green','Black'] 
        black_blend = ['Black','ZBT','FI','Chai','SA','Grey','CHM','ChinaGrey']
        green_blend = ['Green','LG','IB']
        oolong_blend= ['Oolong','GH']
        no_tea =['RG','CHCF']
        huami =['Jasmine','HuamiOolong','HuamiBlack','HuamiGreen']
        tea_2g = ['sCHCF','sOolong','sGreen','sBlack','sZBT','sChai','sSA','sGrey','sLG','sIB','sGH']
        sachets= ['CHCF','Oolong','Green','Black','ZBT','Chai','SA','Grey','LG','IB','GH']
        non_woven=['SA','Chai','ZBT','RG','sZBT','sChai','sSA']
        on_csk = ['Oolong','Green','Black','FI','Grey','CHM','ChinaGrey','LG'
                ,'IB','GH','RG','CHCF','sCHCF','sOolong','sGreen','sBlack','sGrey','sLG','sIB','sGH']
        on_csz = ['Jasmine','HuamiOolong','HuamiBlack','HuamiGreen','SA','Chai','ZBT','RG']

        all_tea_dict = {"black_blend": ["Black",'ZBT','FI','Chai','SA','Grey','CHM','ChinaGrey','sBlack','sGrey'],
                        "green_blend" : ["Green",'LG','IB','sGreen','sLG','sIB'],"oolong_blend": ["Oolong",'GH','sOolong','sGH'],"no_tea" :['RG','CHCF','sCHCF'],
                        "huami" :['Jasmine','HuamiOolong','HuamiBlack','HuamiGreen']}


        #defining class for classification of tea based on machine and filter
        class TeaType:
            def __init__(self,name):
                self.name=name
                TeaType.tea_origin(self.name)
                TeaType.tea_filter(self.name)

            @classmethod
            def tea_origin(self,inp):

                for x,y in all_tea_dict.items():
                    for t in y:
                        if inp==t:
                            return x

            @classmethod
            def tea_filter(self,inp):

                if inp in non_woven:
                    return False
                else:
                    return True

            @classmethod
            def tea_machine(self,inp):
                if inp in on_csk:
                    return 'csk'
                else:
                    return "csz"


        # csv file taken as dataframe and 
        # sorted on the basis of machine 
        df = pd.DataFrame(columns=["TEA","COUNT"])
        df = pd.read_csv('./static/uploads/abc.csv')
        machine_csz=[]
        machine_csz_count=[]
        machine_csk=[]
        machine_csk_count=[]
        for i in range(len(df.TEA)):
            c=TeaType.tea_machine(df.TEA[i])
            if c=='csz':
                machine_csz.append(df.TEA[i])
                machine_csz_count.append(df.COUNT[i])
            else:
                machine_csk.append(df.TEA[i])
                machine_csk_count.append(df.COUNT[i])

        # Teas from the sheet is fetched and sorted on the basis of CS-Z and CS-K 

        # we will try to sort the Tea order now 
        #first consider the csk teas
        df1 =pd.DataFrame()
        df1["CSK"] =pd.Series(machine_csk)
        df1["COUNT"]=pd.Series(machine_csk_count)

        #sorting cs-z
        df2 =pd.DataFrame()
        df2["CSZ"] =pd.Series(machine_csz)
        df2["COUNT"]=pd.Series(machine_csz_count)
        new2=[]
        for i in range(len(df2.CSZ)):
            b=TeaType.tea_origin(df2.CSZ[i])
            new2.append(b)
        df2["Origin"] =new2

        #adding the origin of each tea as a column 

        new=[]
        for i in range(len(df1.CSK)):
            a=TeaType.tea_origin(df1.CSK[i])
            new.append(a)
        df1["Origin"] =new


        df1_1 =pd.DataFrame(columns=df1.columns)# make a new df with same headings

        m=len(df1.index)
        index_lst=[]
        for i in range(m):
            index_lst.append(df1.index[i])

        l = 5 if len(df1.index) > 5 else len(df1.index)

        comp_list=[]
        for i in index_lst:
            comp_list.append(df1.loc[i][2])

        total_num= len(df1.index)


        a=df1.loc[index_lst[0]]
        df1_1= df1_1.append(a)
        df1.drop(index_lst[0],axis="index",inplace=True)


        while len(df1_1.index)<total_num:


            m=len(df1.index)
            index_lst=[]
            for i in range(m):
                index_lst.append(df1.index[i])



            l = 5 if len(df1.index) > 5 else len(df1.index)




            comp_list=[]
            for i in index_lst:
                comp_list.append(df1.loc[i][2])




            n=len(df1_1.index)
            index_lst_temp=[]
            for i in range(n):
                index_lst_temp.append(df1_1.index[i])

            b=index_lst_temp[-1]

            for i in index_lst[0:l]:
                if df1_1.loc[b][2]== df1.loc[i][2]:
                    t= df1.loc[i]
                    df1_1= df1_1.append(t)
                    df1.drop(i,axis="index",inplace=True)
                else:
                    pass 


            if df1_1.index[-1]==b:

                df1_1=df1_1.append(df1.loc[index_lst[0]])
                try:
                    df1_1=df1_1.append(df1.loc[index_lst[1]])
                except:
                    pass
                try:
                    df1.drop(index_lst[0],axis="index",inplace=True)
                except:
                    pass
                try:
                    df1.drop(index_lst[1],axis="index",inplace=True)
                except:
                    pass




    
        

        df1_1display = df1_1.to_html(classes='table table-stripped')
        df1_display = df2.to_html(classes='table table-stripped')

    
        return render_template('schedule.html', data_var5=df1_1display, data_var6 = df1_display)
 



 
if __name__ == '__main__':
    app.run(debug=True)