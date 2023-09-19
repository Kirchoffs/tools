import json

json_input_file = input("Enter the name of the JSON file: ")

with open(json_input_file, "r") as fin:
    json_text = fin.read()
    json_text_string = json.dumps(json_text, ensure_ascii = False).replace('\n', r'\n')
    print(json_text_string)