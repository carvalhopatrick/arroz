
Code to solve [SigmaGeek's challenge](https://sigmageek.com/challenge_results/1656603146901x235034290182684670) to find large palindromic prime numbers within pi's decimal expansion.

## The approach

The initial goal was to find the largest number that was both a palindrome and a prime number, contained in the pi decimal digits.

For this, I've used Google Cloud's record breaking [100 trillion digits of pi dataset](https://storage.googleapis.com/pi100t/index.html), calculated using y-cruncher and published in 2022.

The code in /cloud/controller.py is designed to autonomously:

1. Download the digits in .ycd (y-cruncher output), provided by Google Cloud. Each file is 39GB and contains 100 billion digits.
2. Convert it to a txt. I've forked [Mysticial/DigitViewer](https://github.com/Mysticial/DigitViewer) to accept automated CLI calling with custom digit ranges (fork at [carvalhopatrick/DigitViewer](https://github.com/carvalhopatrick/DigitViewer))
3. Search the digits, looking for large palindromes that have an odd number of digits (as only those can be prime), and saving what's found in a output txt. This is done while downloading/converting the next file. The primality test was removed, because the largest palindromes were so rare that it was more efficient to check manually afterwards.
4. Delete the files already used to not waste storage. 250GB is needed to work as parallel as possible.

Much of the process generate logs so I could check if something went wrong while I left the PC crushing the digits.

The searcher (cloud/searcher.py) code is multithreaded, but, being written in python, it's not the most optimized. It scans around 16 million digits per second with an i7-9750H CPU. During the challenge, I was planning on rewriting it in C++, but the biggest bottleneck was actually my internet speed (to download the digits), so it wasn't needed.

In the end, me and a friend ([tbochniak](https://github.com/tbochniak)) got together to use our free student credits in Google Cloud and rent some VMs to finish the search on time. The download speeds were much quicker on those.

## The result

- The largest number found that was both a palindrome and a prime was **9609457639843489367549069**, with 25 digits. It starts the decimal digit #**33044988112960**. ([Verify it on pi.delivery](https://api.pi.delivery/v1/pi?start=33135773126758&numberOfDigits=25&radix=10))

- Another 25 digit prime palindrome is within the dataset, but it has a smaller magnitude. The number is **7331530558321238550351337** and it starts in digit #**33044988112960**. ([Verify it](https://api.pi.delivery/v1/pi?start=33044988112960&numberOfDigits=25&radix=10))

- The biggest non-prime palindromes had 29 digits. 4 of them were found, one of them being **70421912916317671361921912407** at #**80830942786239**. ([Verify it](https://api.pi.delivery/v1/pi?start=80830942786239&numberOfDigits=29&radix=10))

Having found the largest prime palindrome, I was one of the 26 people who got to the final stage, which had a different challenge. Unfortunately, I was not quick enough to be one of the 3 winners in that one.
Having found the largest prime palindrome, I was one of the 26 people who got to the final stage, which had a different challenge. Unfortunately, I was not quick enough to be one of the 3 winners in that one.
