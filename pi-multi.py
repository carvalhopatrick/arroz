import time
import math
from concurrent import futures
import sys

SIZE = 21							# size of the palindromic prime to be searched
BUFSIZE = 1024*500					# size (number of digits) of each worker buffer
MAX_WORKERS = 11					# max number of concurrent workers
MAX_PROCS = 200						# max number of processes at once in the worker pool
START_IDX = 0						# min Pi digit index to search
END_IDX = sys.maxsize				# max Pi digit index to search
INPUT_FILE = './input/pi-1b.txt'		# path to input file with pi digits
HAS_INTEGER = True						# True if input file has integer part ('3.')

# checks if number is prime (slow method, but adequate for this use case)
def is_prime(list):
	n = int(''.join(list))
	for i in range(2, int(math.sqrt(n))+1):
		if (n % i) == 0:
			return False
	return True

# checks if number is palindrome
def is_palindrome(list):
	reversed = list[::-1]
	if (list == reversed):
		return True
	else:
		return False

# searches for palindromes and primes in a string full of pi digits
def search(buf, f_idx):
	n = len(buf)
	window = [*buf[0:SIZE]]

	for i in range(n-SIZE):
		if (is_palindrome(window)):
			print('palindrome found at i = ' + str(i+f_idx))

			if (is_prime(window)):
				print('!!! PRIME FOUND AT i = ' + str(i+f_idx))
				print('!!! PRIME = ' + str(window))
				return (i+f_idx, window)

		window.pop(0)
		window.insert(SIZE-1, buf[i+SIZE])
		# last window will be checked in the next search call
		# TODO: test if it really is the case
	return False

def main():
	# open local file with pi digits
	with open(INPUT_FILE, 'r') as f:
		# initial read offset (default = 2 to ignore "3.")
		if (HAS_INTEGER):
			f_idx = START_IDX if (START_IDX) else 2
		else:
			f_idx = START_IDX
		f.seek(f_idx)

		procs = []
		primes = {}
		pool = futures.ProcessPoolExecutor(max_workers=MAX_WORKERS)
		buf = f.read(BUFSIZE)
		progress_counter = 0

		while (buf != '' and f_idx <= END_IDX): 
			# add processes to pool until MAX_PROCS limit
			while (len(procs) <= MAX_PROCS and buf != '' and f_idx <= END_IDX):
				if (progress_counter >= 100*1000*1000): # prints every 100M digits, just to check progress
					print(f'creating // f_idx = {f_idx} // procs = {len(procs)}')
					progress_counter = 0
				p = pool.submit(search, buf, f_idx)
				procs.append(p)
				progress_counter -= f_idx
				f_idx += BUFSIZE
				f.seek(f_idx - SIZE)		# rewinds read pointer to not miss combinations in the next search
				f_idx -= SIZE
				buf = f.read(BUFSIZE)
				progress_counter += f_idx
			
			# check for completed processes
			for completed in futures.as_completed(procs):
				result = completed.result()
				
				if (result == False):	# no prime found
					procs.remove(completed)

				else:	# prime found
					primes[result[0]] = result[1]
					print("prime added (idx, result): " + str(result))
			
			if (len(primes) > 0):
				# one or more primes has been found, use the one with the smallest index
				pool.shutdown()
				print('terminating pool...')
				first_idx = min(primes)
				first_prime = ''.join(primes[first_idx])
				print(f'FINAL RESULT: i = {first_idx} // prime = {first_prime}')
				return f_idx

	# nothing has been found
	print("No palindromic primes found :(")
	pool.shutdown()
	return f_idx

if __name__ == '__main__':
	assert BUFSIZE > SIZE
	assert END_IDX > START_IDX

	start_time = time.time()
	last_idx = main()
	print(f'searched {last_idx-START_IDX} digits in {(time.time()-start_time):.2f} seconds')
	print(f'last safe index: {last_idx-BUFSIZE-SIZE-1}')
	