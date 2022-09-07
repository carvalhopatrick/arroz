import time
import math
from multiprocessing import Process
from concurrent import futures

SIZE = 9
BUFSIZE = 1024*500
MAX_WORKERS = 12
MAX_PROCS = 48
START_IDX = 0
END_IDX = 1024*1024*1024*47

def is_prime(list):
	n = int(''.join(list))
	for i in range(2, int(math.sqrt(n))+1):
		if (n % i) == 0:
			return False
	return True

def is_palindrome(list):
	reversed = list[::-1]
	if (list == reversed):
		return True
	else:
		return False

def search(buf, f_idx):
	n = len(buf)
	window = [*buf[0:SIZE]]

	for i in range(n-SIZE):
		if (is_palindrome(window)):
			print('palindrome found at i = ' + str(i+f_idx))

			if (is_prime(window)):
				print('!!! PRIME FOUND AT i = ' + str(i+f_idx))
				print('!!! PRIME = ' + str(window))
				return window

		window.pop(0)
		window.insert(SIZE-1, buf[i+SIZE])
		# last window will be checked in the next search call
		# TODO: test if it really is the case
	return False

def main():
	# open local file with pi digits
	f = open("./input/pi_dec_1t_01.txt", 'r')
	
	# initial read offset (default = 2 to ignore "3.")
	f_idx = START_IDX if (START_IDX) else 2
	f.seek(f_idx)

	procs = []
	pool = futures.ProcessPoolExecutor(max_workers=MAX_WORKERS)
	buf = f.read(BUFSIZE)

	while (buf != '' and f_idx <= END_IDX): 
		# prevents more processes being submitted after limit is reached
		while (len(procs) <= MAX_PROCS):
			if not (f_idx % 1000*1000*10):
				print(f'creating // f_idx = {f_idx} // procs = {len(procs)}')
			p = pool.submit(search, buf, f_idx)
			procs.append(p)
			f_idx += BUFSIZE
			f.seek(f_idx - SIZE)		# rewinds read pointer to not miss combinations in the next search
			f_idx -= SIZE
			buf = f.read(BUFSIZE)
		

		# check for completed processes
		for completed in futures.as_completed(procs):
			result = completed.result()
			if (result == False):
				procs.remove(completed)
				if not (len(procs) % 1000):
					print(f'terminating // procs = {len(procs)}')
			else:
				pool.shutdown()
				print(result)
				print("PRIME FOUND: " + ''.join(result))
				print("terminating workers...")
				return

	# nothing has been found
	print("No palindromic primes found :(")
	pool.shutdown()
	return


if __name__ == '__main__':
	start_time = time.time()
	main()
	print(f"searched {END_IDX-START_IDX} digits in {(time.time()-start_time):.2f} seconds")
	