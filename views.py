"""
Routes and views for the flask application.
"""


from datetime import datetime
from flask import render_template
from Resume import app
import pyodbc
import pandas as pd
import psycopg2
from psycopg2 import Error
import matplotlib.pyplot as plt
import random
from Resume.linePlot import lineplot

#---------------------------- Global Variables --------------------------------------------------------------
#database = "resume_aa"
#username = "releasenotes"
#password = "releasenotes"
#server = "DESKTOP-KEFPP9Q\SQLEXPRESS"
#driver = "{ODBC Driver 17 for SQL Server}"

#---------------------------- Connecting to DB, Fetching menu_table and View_tables  MS SQL ----------------------

#try:
#    connection = pyodbc.connect(DRIVER=driver,SERVER=server,DATABASE=database,UID=username,PWD=password)
#    menuitems_table = pd.read_sql("SELECT * FROM menu ORDER BY menu_order",connection)
#    print(menuitems_table)

#except Exception as e:
#        import os
#        import sys
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))


#---------------------------- PG Connecting to DB, Fetching menu_table and View_tables ----------------------

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "11121121",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "resume")
    menuitems_table = pd.read_sql("SELECT * FROM menu ORDER BY menu_order",connection)
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
    try:
        print("--------------------------------------------------------------------------------------")
        return render_template(
            'index.html',
            #nav_options = nav_options(),
            brand = 'Home',
            hide = "hide",
            body = ' class= "home"  ',
            list = home_pg_list(),
            year=datetime.now().year,
        )
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))


@app.route('/tst2')
def tst2():
    try:
        names = ['one','two','three','four']
        x1 = [i for i in range(1,21)]
        x2 = [i+1 for i in x1]
        x3 = [i+2 for i in x1]
        x4 = [i+3 for i in x1] 
        d = {'one' : x1,'two' : x2,'three': x3,'four' : x4}
        df = pd.DataFrame(d)
        return render_template(
            'tst2.html',
            data = lineplot(df)
            )
    except Exception as e:
            import os
            import sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))

 
@app.route('/about')
def about():
    """Renders the about page."""
    try:
        return render_template(
            'about.html',
            brand = 'About Me',
            title = 'About Me',
            nav_list = nav_list('about me'),
            year=datetime.now().year,
            message='Your application description page.'
        )
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))

@app.route('/tables/<int:menuID>')
def tables(menuID):
    try:
        pg_name = menuitems_table.loc[menuitems_table['menu_order'] == menuID]['title']
        pg_name = list(pg_name)[0]
        return render_template(
            'tables.html',
            brand = pg_name.title(),
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

#@app.route('/certificates')
#def certificates():
#    try:
#        pg_name = menuitems_table.loc[menuitems_table['menu_order'] == menuID]['title']
#        pg_name = list(pg_name)[0]
#        return render_template(
#            'certi_page.html',
#            brand = pg_name,
#            nav_list = nav_list(pg_name),
#            data = home_pg_list("certi"),
#            year=datetime.now().year,
#            message='Your contact page.'
#        )
#    except Exception as e:
#        import os
#        import sys
#        exc_type, exc_obj, exc_tb = sys.exc_info()
#        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#        print("Error_tables_route: ",e,str(exc_tb.tb_lineno))

#--------------------------------------------------------------------------Def Home -----------------------------------------------------------------------------------

def home_pg_list():
    try:
        tags = ""
        for title,id,func in zip(menuitems_table['title'],menuitems_table['menu_order'],menuitems_table['func_name']):
            if(title.lower() == "menu" or title.lower() == "profile"):
                continue
            tags += '<li class="borders"> <a href="/'
            tags += func +'/' + str(id) if func.lower() == 'tables' else func 
            tags += '"> <h3> '+title.title()+' </h3> </a> </li>\n'
            print(tags)
        return tags
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))
        

def nav_list(pg_name):
    try:
        nav_items = ""
        for title,id,func in zip(menuitems_table['title'],menuitems_table['menu_order'],menuitems_table['func_name']):     
            #print("-"*50)
            #print(title)
            #print("-"*50)
            if(title.lower() == pg_name.lower()):
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
        title = list(menuitems_table.loc[menuitems_table['menu_order'] == id]['title'])[0]
        func_name = list(menuitems_table.loc[menuitems_table['menu_order'] == id]['func_name'])[0]
        #data_tags = '<div class="'+title.lower()+'">'
        #add_start = ""
        #add_end = ""
        #if(title.lower() == 'about me'):
        #    add_start, add_end = abt()
        data_tags = '<h1>'+ title +'</h1>\n'
        table_data = pd.read_sql("SELECT * FROM "+title,connection)
        if('menu_order' in list(table_data.columns)):
            table_data = pd.read_sql("SELECT * FROM "+title+'ODER BY menu_order',connection)
        data_tags += '<div class="container">'
        #data_tags += add_start
        data_tags += '<table>'
        data_tags += '<thead>'
        for i in list(table_data.columns):
            data_tags += '<th>'+i.title()+'</th>'
        data_tags += '</thead>'
        for td in range(0,len(table_data)):
            data_tags += '<tr>'
            for d in range(0,len(list(table_data.iloc[td]))):
                #print('-'*20,'data1','-'*20)
                #print(list(table_data.columns)[d])
                #print('-'*20,'data1','-'*20)
                if('link' in list(table_data.columns)[d].lower() and str(table_data.iloc[td][d]) != '-'):
                    #print("-"*50)
                    #print(str(table_data.iloc[td][d]))
                    #print("-"*50)
                    data_tags += '<td> <a href="'+str(table_data.iloc[td][d])+'">'+list(table_data.columns)[d].upper()+'</a> </td>'
                else:
                    data_tags += '<td>'+str(table_data.iloc[td][d])+'</td>'
            data_tags += '</tr>'
        data_tags += '</table>'
        data_tags += '</div>'
        #data_tags += '</div>'
        return data_tags #+add_end
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_data : ",e,str(exc_tb.tb_lineno))

def abt():
    try:
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
    except Exception as e:
        import os
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))