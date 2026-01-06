import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("asana_newdataset.sqlite")

df = pd.read_sql("SELECT * FROM tasks", conn)

output_path = os.path.abspath("tasks_sample_full.csv")
df.to_csv(output_path, index=False)

print("CSV saved at:", output_path)

conn.close()
