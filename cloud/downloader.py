from urllib import request
import os, subprocess
import time
import utils
import glob
from datetime import datetime

LOGFILE = "./logs/download.log"

def log(string, file_number=''):
	file_number = str(file_number)
	with open(LOGFILE, 'a+') as lf:
		print(f"{file_number}\t{string}", flush=True)
		lf.write(f"{file_number}\t{string}\n")

def download_ycd(file_number):
	try:
		url = f'https://storage.googleapis.com/pi100t/Pi%20-%20Dec%20-%20Chudnovsky/Pi%20-%20Dec%20-%20Chudnovsky%20-%20{file_number}.ycd'
		r = request.urlretrieve(url, f'./input/pi{file_number}.ycd.part')
		print(r)
		if (r):
			os.rename(f'./input/pi{file_number}.ycd.part', f'./input/pi{file_number}.ycd')
		return True
	except:
		log("ERROR: download_ycd", file_number)
		return False

def extract_ycd(filename, file_number):
	try:
		start = int(file_number) * (100*10**9) + 1
		end = (start - 1) + 100*10**9
		txt_name = filename.replace('.ycd', '.txt')

		cmd = ['digitviewer-convert', filename,
					str(start), str(end), txt_name]
		p = subprocess.run(cmd)
		return True
	except:
		log("ERROR: extract_ycd", file_number)
		return False

def main():
	file_number = 0

	while(int(file_number) <= 1000):
		try:
			data = utils.json_read(utils.DATAFILE)
			file_number = str(data['file_number'])

			txt_list = glob.glob('./input/*.txt')
			ycd_list = glob.glob('./input/*.ycd')

			# no ycd, download a new one
			if (len(ycd_list) == 0):
				log(f"Starting download\t{datetime.now()}", file_number)
				start_time = time.time()
				r = download_ycd(file_number)
				
				if (r):
					log(f"Downloaded in {time.time() - start_time}s", file_number)
				else:
					raise Exception("ERROR: download_ycd")

			# ycd downloaded, no pending txt, extract it
			if (len(ycd_list) > 0 and len(txt_list) == 0):
				filename = ycd_list[0]
				log(f"Starting extraction of {filename}\t{datetime.now()}", file_number)
				start_time = time.time()
				r = extract_ycd(f"./input/{filename}", file_number)

				if (r):
					log(f"Extracted in {time.time() - start_time}s", file_number)
					# os.remove(f'./input/{filename}') ### TODO: reabilitar
				else:
					raise Exception("ERROR: extract_ycd")

			time.sleep(2)
		except:
			log('ERROR: downloader loop!', file_number)
			time.sleep(2)
			continue



if __name__ == '__main__':
	main()