##Author: 
##Date Started:
##Notes:

# here's my prior code
from sqlite_utils import Database
import sqlite_utils
import json
from pprint import pprint as pp

def add_columns(db_path, table_name, columns_to_add):
    """
    Adds specified columns to a table in a SQLite database.

    Args:
        db_path: Path to the SQLite database file.
        table_name: Name of the table to add columns to.
        columns_to_add: A dictionary where keys are column names and values
                       are SQLite data types (e.g., {'clean_transcript': 'TEXT', '5m_chunks': 'TEXT', 'summary': 'TEXT'}).
    """

    db = sqlite_utils.Database(db_path)

    if table_name not in db.table_names():
        print(f"Table '{table_name}' does not exist.  Please create the table first.")
        return  # Or raise an exception if you prefer

    table = db[table_name]

    for column_name, column_type in columns_to_add.items():
        if column_name not in table.columns_dict:
            try:
                db.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                print(f"Column '{column_name}' added to table '{table_name}' with type '{column_type}'.")
            except Exception as e:
                print(f"Error adding column '{column_name}': {e}")
        else:
            print(f"Column '{column_name}' already exists in table '{table_name}'.")

db_path = 'transcriptions.db'
filename_column="filename"
table_name = "transcriptions"

db = Database(db_path)
table = db[table_name]
print(table.count)
print(table.pks)
# sql_query = f"SELECT {filename_column}, COUNT(*) FROM {table_name} GROUP BY {filename_column} HAVING COUNT(*) > 1"
# duplicates = list(db.query(sql_query))

columns_to_add = {
    'clean_transcript': 'TEXT',
    'five_m_chunks': 'TEXT',
    'summary': 'TEXT'
}

add_columns(db_path, table_name, columns_to_add)

column_names = table.columns

#check to see if we have a clean_transcript
for row in table.rows:
    if row['clean_transcript'] == None:
        print(row['filename'])
        segments = json.loads(row['transcription'])['segments']
        print(len(segments))
        out = ""
        for s in segments:
            out += f"{s['start']/60:.2f} => {s['end']/60:.2f} | {s['text']}\n"
        #print(out)
        table.update(row['filename'], {"clean_transcript": out})
        print("done!")
