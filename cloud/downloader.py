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
	file_number = str(file_number)
	try:
		url = f'https://storage.googleapis.com/pi100t/Pi%20-%20Dec%20-%20Chudnovsky/Pi%20-%20Dec%20-%20Chudnovsky%20-%20{file_number}.ycd'
		r = request.urlretrieve(url, f'./input/pi{file_number}.ycd.part')
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
		# rename file to .pitxt so that controller can start the search in it
		os.rename(f'{txt_name}', f'{txt_name.replace(".txt", ".pitxt")}')
		return True
	except:
		log("ERROR: extract_ycd", filename)
		return False

def main():
	file_number = 0
	next_download = 0

	download_data = utils.json_read(utils.DOWNLOAD_DATA)
	next_download = int(download_data['next_download']) 
	next_extract = int(download_data['next_extract'])
	next_download_bak = next_download
	next_extract_bak = next_extract 

	# TODO: ao iniciar downloader, apagar possiveis arquivos .ycd.part e .txt
	part = glob.glob('./input/*.txt')
	part += glob.glob('./input/*.part')
	for i in part:
		os.remove(i)

	while(int(next_download) <= 1000):
		try:
			data = utils.json_read(utils.DATAFILE)
			file_number = int(data['file_number'])

			download_data = utils.json_read(utils.DOWNLOAD_DATA)
			next_download = int(download_data['next_download'])
			next_extract = int(download_data['next_extract'])
			next_download_bak = next_download
			next_extract_bak = next_extract 

			txt_list = glob.glob('./input/*.txt')
			pitxt_list = glob.glob('./input/*.pitxt')
			ycd_list = glob.glob('./input/*.ycd')

			# no there's a txt that wasn't fully extracted
			if (len(txt_list) > 0):
				for file in txt_list:
					os.remove(file)

			# download and extract a maximum of one file ahead of controller 
			if (next_download - file_number <= 1):
				# no ycd, download a new one
				if (len(ycd_list) == 0):
					log(f"Starting download\t{datetime.now()}", next_download)
					start_time = time.time()
					r = download_ycd(next_download)
					
					if (r): # file finished downloading
						log(f"Downloaded in {time.time() - start_time}s", file_number)
						next_download += 1
						download_data['next_download'] = next_download
						utils.json_write(download_data, utils.DOWNLOAD_DATA)
					else:
						part_ycd = glob.glob('./input/*.ycd.part')
						for i in part_ycd:
							os.remove(i)
						raise Exception("ERROR: download_ycd")

			# ycd downloaded, no pending txt, extract it
			if (len(ycd_list) > 0 and len(pitxt_list) <= 1):
				filename = ycd_list[0]
				log(f"Starting extraction of {filename}\t{datetime.now()}")
				start_time = time.time()
				r = extract_ycd(f"{filename}", next_extract)

				if (r):
					log(f"Extracted in {time.time() - start_time}s", file_number)
					next_extract += 1
					download_data['next_extract'] = next_extract
					utils.json_write(download_data, utils.DOWNLOAD_DATA)
					os.remove(f'{filename}') # remove ycd
				else:
					part_txt = glob.glob('./input/*.txt')
					for i in part_txt:
						os.remove(i)
					raise Exception("ERROR: extract_ycd")

			time.sleep(2)
		except:
			data['next_download'] = int(next_download_bak)
			data['next_extract'] = int(next_extract_bak)
			log('ERROR: downloader loop!', file_number)
			time.sleep(2)
			continue


if __name__ == '__main__':
	main()
