##Author: 
##Date Started:
##Notes:

from glob import glob
import os
from subprocess import getoutput as go
import whisper
import sys
import sqlite3
import sqlite_utils
from pprint import pprint as pp
import mutagen

recs = glob("/Users/****/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.m4a")

# transdir = "/Users/****/transcripts"

# go(f"mkdir -p {transdir}")

# Connect to SQLite database (or create it if it doesn't exist)
db = sqlite3.connect("transcriptions.db")
db_utils = sqlite_utils.Database(db)

# Create a table for transcriptions if it doesn't exist
if "transcriptions" not in db_utils.table_names():
    db_utils["transcriptions"].create({"filename": str, "transcription": str})

# Check for complementary text files in /Users/Dan/trans
print(f"Processing {len(recs)} recordings")
for rec in recs[:]:
    fna = rec.split("/")[-1]
    fnt = f'{transdir}/{fna.replace("m4a","txt")}'

    try:
        audio_file = mutagen.File(rec)
        foo = dict(audio_file.items())
        note = foo['©nam'][0]
    except: note = "recording"
    rtime = os.path.getctime(rec)
    
    if os.path.isfile(fnt):
        None
        #print("File exists.")
    else:
        audio_file = rec
        output_file = fnt

        # Load the Whisper model
        model = whisper.load_model("base")

        # Transcribe the audio file using Whisper
        result = model.transcribe(audio_file)

        # Write the transcription to the output text file
        with open(output_file, "w") as f:
            f.write(result['text'])

        # Store results in the SQLite database
        db_utils["transcriptions"].upsert({
            "filename": fna,
            "transcription": result,
            "time":rtime,
            "note":note
        },pk="filename",alter=True)

# Commit and close the database connection
db.commit()
db.close()

