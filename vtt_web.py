##Author: 
##Date Started:
##Notes:

from flask import Flask, request, redirect, url_for
import sqlite_utils
import markdown
from datetime import datetime

app = Flask(__name__)
DATABASE = "transcriptions.db"

idx_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Table</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <style>
    body{font-family:'Helvetica'}
    a{text-decoration:none;color:grey}
    a:hover{text-decoration:none;color:red}
    </style>
    <script>
        $(document).ready(function () {
            $('#myTable').DataTable(
                {
                    "order": [[ 1, "desc" ]],
                    aLengthMenu: [
                            [25, 50, 100, 200, -1],
                            [25, 50, 100, 200, "All"]
                    ],
                     iDisplayLength: 100
                    
                });
            });
    </script>
</head>
<body>
##TABLEGOESHERE##
</body>
</html>
"""


# Define your database model (adjust to match your table structure)
def get_db():
    db = sqlite_utils.Database(DATABASE)
    return db

def linker(s,ol):
    return f'<a href="/detail/{s}">{ol}</a>'

def make_table(rows):
    out = "<table id='myTable'>\r"
    out+= f"<thead><tr><th>meeting</th><th>time</th></tr></thead>\r"

    for row in rows:
        fn = row['filename']
        dt = row['filename'][0:15]
        ol = row['oneline']
        dt = f'{dt[0:4]}-{dt[4:6]}-{dt[6:8]} {dt[9:11]}:{dt[11:13]}:{dt[13:15]}'
        out+= f"<tr><td>{linker(fn,ol)}</td><td>{dt}</td></tr>\r"
    out+="</table>"
    return out

def make_det(data):
    md = f"""

# {data['oneline']}
##Summary/Actions
{data['summary']}

##Distilled Transcript
{data['five_m_chunks']}

##Clean Transcript
{data['clean_transcript'].replace(chr(10),"<br>")}

"""

    style = """
        body{font-family:'Helvetica'}
"""

    out = f"""
    <html>
    <head>
        <style>
        {style}
        </style>
    </head>
    <body>
    {markdown.markdown(md)}
    </body>
    </html>
    """ 
    return out

@app.route('/')
def index():
    with app.app_context():
        db = get_db()
        data = []
        for row in db["transcriptions"].rows_where(select="filename,time,oneline"):
            data.append(row)

        strang = idx_str.replace("##TABLEGOESHERE##",make_table(data))

        return strang


@app.route('/detail/<str>')
def detail(str):
    db = get_db()
    item = db["transcriptions"].get(str)
    if item:
        dd = {}
        dd['oneline'] = item['oneline']
        dd['clean_transcript'] = item['clean_transcript']
        dd['five_m_chunks'] = item['five_m_chunks']
        dd['summary'] = item['summary']
        return make_det(dd)
    else:
        return "Item not found", 404


if __name__ == '__main__':
    db = sqlite_utils.Database(DATABASE)
    table = db['transcriptions']
    print(table.count)

    app.run(debug=True,host="0.0.0.0",port=1235)