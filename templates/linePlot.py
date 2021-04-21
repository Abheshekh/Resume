def lineplot(stock_data_frame):
    colors = ["#A52A2A","#00FFFF","#FF7F50","#D2691E","#DC143C","#006400","#8B0000","#FF8C00","#B22222","#F08080","#FF00FF"]
    dates = []
    for date in stock_data_frame:
        dates.append('"'+str(date)+'"')
    chart_html = ""
    chart_html += '<canvas id="lineChart" width="900" height="400"></canvas>\n'
    chart_html += '<script>\n'
    chart_html += 'var cts = document.getElementById("lineChart").getContext("2d"); \nvar lineChart = new Chart(cts, {\n'
    chart_html += 'type: "line",\n'
    chart_html += 'data: {\n'
    chart_html += 'labels:'+" ["+",".join(dates)+'],\n'
    chart_html += 'datasets: [\n'
    color_num = 0
    for date in dates:
        chart_html += '{'
        chart_html += 'label:'+date+',\n'
        chart_html += 'data:' + " ["+",".join(list(map(str,stock_data_frame[date.replace('"','')])))+"],\n" #stock_data_frame[date]
        chart_html += 'fill: false,\nborderColor: "'+colors[color_num]+'",\nlineTension: 0.1},\n'
        color_num += 1
        if(color_num > len(colors)):
            color_num = 0
    chart_html += ']},\noptions: {\nresponsive: true\n}});\n</script>'
    print(chart_html)
    return chart_html






#Bellow code to be added in main py file

#@app.route('/tst2')  # --> Calling function
#def tst2(): # --> Same name as above line
#    try:                                                #--------------------
#        names = ['one','two','three','four']            #                   |
#        x1 = [i for i in range(1,21)]                   #                   |
#        x2 = [i+1 for i in x1]                          #                   |
#        x3 = [i+2 for i in x1]                          #                   | ---------> Sample dataFrame
#        x4 = [i+3 for i in x1]                          #                   |
#        d = {'one' : x1,'two' : x2,'three': x3,'four' : x4}     #           |
#        df = pd.DataFrame(d)                            #--------------------
#        return render_template(
#            'tst2.html', # --> HTML to render
#            data = lineplot(df)  # --> dataFrame to br ploted
#            )
#    except Exception as e:
#            import os
#            import sys
#            exc_type, exc_obj, exc_tb = sys.exc_info()
#            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#            print("Error_db_conncetion: ",e,str(exc_tb.tb_lineno))