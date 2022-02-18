# Name : Surya Narayanan Nadhamuni Suresh
# UTA ID : 1001877873

from flask import Flask, render_template, request,url_for,flash
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = 'random string'

#DB connection details
HOST='utacloud1.reclaimhosting.com'
USER = 'sxn7873_surya'
PASSWORD='Pn2E)^Gq&Dc]'
DATABASE='sxn7873_adb'

#A specific function to set up a db connection
def dbConnect():
    global conn # defining a global variable
    #connect to database
    conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
    return conn

# the main select query
mainQuery = "Select * from earthquake "

#Fuction to return the content of the whole table
def allData():
    dbConnect()
    cursor = conn.cursor()
    cursor.execute(mainQuery)
    res = cursor.fetchall()
    conn.close()
    return res

def largestN(fields):
    query=mainQuery
    dbConnect()
    cursor = conn.cursor()
    for key,value in fields.items():
        query+="order by mag desc LIMIT 0,"+value
        #query+="where mag > "+value+" order by mag desc"
    print(query)
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res

def dateRange(fields):
    query=mainQuery
    dbConnect()
    cursor = conn.cursor()
    query+=" where DATE(time)>='"+fields['From']+"' and Date(time)<='"+fields['To']+"' and mag>"+fields['Mag']
    print(query)
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res


def groupByMag(fields):
    query = "select t.new as 'mag_range', count(*) as 'number_of_occurences' from ( "
    query+="select case when mag>=1 and mag<2 then '1-2' "
    query+="when mag>=2 and mag<3 then '2-3' when mag>=3 and mag<4 then '3-4' "
    query+="when mag>=4 and mag<5 then '4-5' when mag>=5 and mag<6 then '5-6' "
    query+="when mag>=6 and mag<7 then '6-7' else 'other(negatives)' end as new "
    query+="from earthquake "
    query+="where date(time)>=date(curdate()-"
    query+=fields['days']+")"
    query+=" ) t group by t.new"
    dbConnect()
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    print(query)
    print(res)
    conn.close()
    return res

    
        




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        dic={}
        for key,value in request.form.items():
            if value!='':
                dic[key]=value
        
        print(dic)

        if dic:
            result=largestN(dic)
        else:
            result=[]
            flash('Please enter values in the field')
    
    else:
        result = allData()

    return render_template('index.html', data=result)

@app.route('/groupby',methods=['POST','GET'])
def groupBy():
    if request.method=='POST':
        dic={}
        for key,value in request.form.items():
            if value!='':
                dic[key]=value

        if dic:
            result=groupByMag(dic)
        else:
            result=[]
            flash('Please enter values in the field')

        
    return render_template('index.html',data2=result)

@app.route('/date', methods=['GET','POST'])
def date():
    if request.method=='POST':
        dic={}
        result=[]
        for key,value in request.form.items():
            if value!='':
                dic[key] = value
        
        #print(dic)
        if dic:
            result = dateRange(dic)
        else:
            flash('Please enter values in fields')
        
        if result==[]:
            flash ('No Such entries in table')
        
    
    return render_template('index.html', data=result)









if __name__=="__main__":
    app.run()