# espera até .ycd anterior ser apagado da pasta

# baixa novo ycd (file_number + 1)
	# baixa como .ycd.part
	# quando terminar, renomear para .ycd

# convert ycd into txt
# delete ycd
# searcher (filename, start idx, last digits) 

# repete


from distutils.cmd import Command
import urllib.request
import subprocess
import time


def urls(a, b):
    links = []
    final = [i for i in range(a, b)]
    for idx in final:
        link = f'https://storage.googleapis.com/pi100t/Pi%20-%20Dec%20-%20Chudnovsky/Pi%20-%20Dec%20-%20Chudnovsky%20-%20{idx}.ycd'
        links.append(link)
    return links


def download(url):
    urllib.request.urlretrieve(url, "file.ycd")


def bash(inicio, fim):
    Command = ['digitviewer-convert', 'file.ycd',
        str(inicio), str(fim), 'file.txt']
    subprocess.run(Command)


def main(a, b):
    start = time.time()
    u = urls(a, b)
    for i in range(len(u)):
        url = u[i]
        inicio = (i+a)*100*10**9+1
        fim = inicio + 100*10**9-1
        print("Iniciando o download", i+a)
        download(url)
        print("Iniciando o descompactamento", i+a)
        bash(inicio, fim)
        # FUNÇÃO_PATRICK()
        #print("Removendo o arquivo", i+a)
        #subprocess.run(['rm', 'file.txt'])
        #subprocess.run(['rm', 'file.ycd'])
        print("Arquivo Processado Nº", i+a)
        finish = time.time()
        delta = finish - start
        print("Tempo de Processamento", delta)

main(0, 1)