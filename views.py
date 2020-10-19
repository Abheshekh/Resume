"""
Routes and views for the flask application.
"""


from datetime import datetime
from flask import render_template
from Resume import app
import pyodbc
import pandas as pd
#---------------------------- Global Variables --------------------------------------------------------------
database = "resume_aa"
username = "releasenotes"
password = "releasenotes"
server = "DESKTOP-KEFPP9Q\SQLEXPRESS"
driver = "{ODBC Driver 17 for SQL Server}"

#---------------------------- Connecting to DB, Fetching menu_table and View_tables ----------------------

try:
    connection = pyodbc.connect(DRIVER=driver,SERVER=server,DATABASE=database,UID=username,PWD=password)
    menuitems_table = pd.read_sql("SELECT * FROM menu ORDER BY oderID",connection)
    print(menuitems_table)

except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))


#------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    #test()
    return render_template(
        'profile.html',
        #nav_options = nav_options(),
        brand = 'Home',
        hide = "hide",
        body = ' class= "home"  ',
        list = home_pg_list(),
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        brand = 'About',
        nav_list = nav_list(menuID),
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/tables/<int:menuID>')
def tables(menuID):
    try:
        pg_name = menuitems_table.loc[menuitems_table['oderID'] == menuID]['title']
        pg_name = list(pg_name)[0]
        return render_template(
            'tables.html',
            brand = pg_name,
            nav_list = nav_list(pg_name),
            data=data(menuID),
            year=datetime.now().year,
            message='Your contact page.'
        )
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_tables_route: ",e,str(exc_tb.tb_lineno))

@app.route('/certificates')
def certificates():
    """Renders the about page."""
    return render_template(
        'tables.html',
        brand = 'Certificates',
        data = '<h1> Page Under Constuction!!! </h1> <i class="fa fa-chain-broken" style="font-size:48px;color:red"></i>',
        nav_list = nav_list('Certificates'),
        year=datetime.now().year,
        message='Your application description page.'
    )
#--------------------------------------------------------------------------Def Home -----------------------------------------------------------------------------------

def home_pg_list():
    tags = ""
    for title,id,func in zip(menuitems_table['title'],menuitems_table['oderID'],menuitems_table['func_name']):
        if(title.lower() == "home"):
            continue
        tags += '<li class="borders"> <a href="/'
        tags += func +'/' + str(id) if func.lower() == 'tables' else func 
        tags += '"> <h3> '+title.title()+' </h3> </a> </li>\n'
    return tags

def nav_list(pg_name):
    try:
        nav_items = ""
        for title,id,func in zip(menuitems_table['title'],menuitems_table['oderID'],menuitems_table['func_name']):          
            if(title == pg_name):
                continue
            nav_items += '<li class="nav-item">\n\t'
            nav_items += '<a class="nav-link" href="/'
            nav_items += func +'/' + str(id) if func.lower() == 'tables' else func 
            nav_items += '"> <h5> '+title.title()+' </h5> </a> </li>\n'
            nav_items += '</li>'
        return nav_items
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))

def data(id):
    try:
        title = list(menuitems_table.loc[menuitems_table['oderID'] == id]['title'])[0]
        table_name = list(menuitems_table.loc[menuitems_table['oderID'] == id]['table_name'])[0]
        #data_tags = '<div class="'+title.lower()+'">'
        add_start = ""
        add_end = ""
        if(title.lower() == 'about me'):
            add_start, add_end = abt()
        data_tags = '<h1>'+ title +'</h1>\n'
        table_data = pd.read_sql("SELECT * FROM "+table_name,connection)
        if('oderID' in list(table_data.columns)):
            table_data = pd.read_sql("SELECT * FROM "+table_name+'ODER BY oderID',connection)
        data_tags += '<div class="container">'
        data_tags += add_start
        data_tags += '<table>'
        data_tags += '<thead>'
        for i in list(table_data.columns):
            data_tags += '<th>'+i.title()+'</th>'
        data_tags += '</thead>'
        for td in range(0,len(table_data)):
            data_tags += '<tr>'
            for d in range(0,len(list(table_data.iloc[td]))):
                print('-'*20,'data1','-'*20)
                print(list(table_data.columns)[d])
                print('-'*20,'data1','-'*20)
                if('link' in list(table_data.columns)[d].lower()):
                    data_tags += '<td> <a href="'+str(table_data.iloc[td][d])+'">'+list(table_data.columns)[d].upper()+'</a> </td>'
                else:
                    data_tags += '<td>'+str(table_data.iloc[td][d])+'</td>'
            data_tags += '</tr>'
        data_tags += '</table>'
        data_tags += '</div>'
        #data_tags += '</div>'
        return data_tags+add_end
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_data : ",e,str(exc_tb.tb_lineno))

def abt():
    abt_tag_s = '<div class = "row justify-content-center">'
    abt_tag_e = '</div>'
    abt_tag_e += '<div class = "row justify-content-center">'
    abt_tag_e += '<div class = "col-xs-6 mc">'
    abt_tag_e += '<a href="#"><i class="fa fa-linkedin-square fa-2x" aria-hidden="true"></i></a>'
    abt_tag_e += '</div>'
    abt_tag_e += '<div class = "col-xs-6 mc">'
    abt_tag_e += '<a href="#"><i class="fa fa-github-square fa-2x" aria-hidden="true"></i></a>'
    abt_tag_e += '</div>'
    abt_tag_e += '<div class = "col-xs-6 mc">'
    abt_tag_e += '<a href="#"><i class="fa fa-map-marker fa-2x" aria-hidden="true"></i></i></a>'
    abt_tag_e += '</div>'
    abt_tag_e += '</div>'
    return abt_tag_s,abt_tag_e