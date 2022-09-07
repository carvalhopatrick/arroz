from asyncio.windows_utils import BUFSIZE
import math
import time
import requests
import threading

SIZE = 21
DIGITS = 1000
BUFSIZE

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

def fetch_digits(api_idx):
	res = requests.get(f'https://api.pi.delivery/v1/pi?start={api_idx}&numberOfDigits={DIGITS}&radix=10')
	j = json.loads(res.text)
	return j['content']

def main():
	i = 0
	pal=0
	buf = f.read(SIZE+2)
	window = [*buf]

	# # discards the '3.'
	# window.pop(0)
	# window.pop(0)

	for i in range(1000000000-SIZE):
		if (is_palindrome(window) == True):
			pal += 1
			print(i)

			if (is_prime(window) == True):
				print('!!! pal = ' + str(pal) + ' / i = ' + str(i))
				print('found: ' + ''.join(window))
				return

		window.pop(0)
		window.insert(SIZE-1,f.read(1))

	print('!!! pal = ' + str(pal) + ' / i = ' + str(i))

start_time = time.time()
main()
print("finished with %.2f seconds" % (time.time() - start_time))