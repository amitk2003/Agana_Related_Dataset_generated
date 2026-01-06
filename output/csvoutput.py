import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("asana_Totaldataset.sqlite")

df = pd.read_sql("SELECT * FROM workspaces", conn)

output_path = os.path.abspath("./FinalCSV/workspaces_sample_full.csv")
df.to_csv(output_path, index=False)

print("CSV saved at:", output_path)

conn.close()
