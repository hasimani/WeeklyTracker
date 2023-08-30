from flask import Flask, request, render_template,redirect
import sqlite3
import pandas as pd

app = Flask(__name__)

Goals = ['Research', 'Shallows', 'Career_Path', 'Couplish', 'Others', 'Mental', 'Physical']

week_number = 0
date = ""
df = pd.DataFrame(columns=['goal','task', 'score', 'date', 'week_num'])
User = ""
df_remarks = pd.DataFrame(columns=['remarks', 'week_num'])

@app.route('/', methods=['GET', 'POST'])
def setup():
    global week_number, date, User 

    if request.method == 'POST':
        # Get the number from the form
        week_number = int(request.form['week_number'])
        date = request.form['date']
        User = request.form['user']
        print(User)
        return redirect('/0')
        
    return render_template('setup.html', global_variable=week_number)


@app.route('/<int:IDX>', methods=['GET', 'POST'])
def add_task(IDX):
    global week_number, date, df, User

    if IDX == len(Goals):
        return redirect('/done')
    goal = Goals[IDX]
    if request.method == 'POST':
        
        tasks = request.form.getlist('tasks[]')
        scores = request.form.getlist('scores[]')
        goals = [goal for score in scores]
        dates = [pd.to_datetime(date) for score in scores]
        week_nums = [week_number for score in scores]
        # print(tasks,scores,goals,goal)
        # Process the data and store it in a Pandas DataFrame
        data = {'goal': goals,'task': tasks, 'score': scores, 'date': dates, 'week_num': week_nums}
        df_temp = pd.DataFrame()
        for key, value in data.items():
            df_temp[key] = value
        df = pd.concat([df, df_temp], ignore_index=True)

        return redirect(f'/{IDX + 1}')  
    return render_template('index.html',GOAL = goal, Week_num= week_number, index = IDX, Date = date, user= User)

@app.route('/done', methods=['GET', 'POST'])
def done():
    global week_number,df_remarks,User,df

    if request.method == 'POST':
        remarks = request.form.get('paragraph')
        df_temp = pd.DataFrame.from_dict({'remarks':[remarks], 'week_num':[week_number]})
        df_remarks = pd.concat([df_remarks, df_temp], ignore_index=True)
                
        conn = sqlite3.connect('mydatabase.db')

        df.to_sql(f'{User}_scores', conn, if_exists='append', index=False)
        df_remarks.to_sql(f'{User}_remarks', conn, if_exists='append', index=False)

        conn.close()

        return 'Done!'
    return render_template('done.html',Week_num= week_number,user=User)

if __name__ == '__main__':
    app.run(debug=True)