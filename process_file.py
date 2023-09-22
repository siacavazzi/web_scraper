from lib.GPT_structuring import extract_contents
import json
import csv
import os

def read_file(name):
    path = f"raw_html/{name}"
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def process_file():
    path = "processed_events/test_data.csv"
    
    data = read_file("httpswwwnyccomevents.html")
    if not data:
        return  # Exit if there's no data

    f_names = extract_contents(data[0]).keys()
  
    # write headers
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            print(f_names)
            writer = csv.DictWriter(f, fieldnames=f_names)
            writer.writeheader()
    
    # append data
    with open(path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=f_names)
        for element in data:
            event = extract_contents(element)
            if event:
                writer.writerow(event)
                f.flush() # this forces python to write to file in real time

process_file()
