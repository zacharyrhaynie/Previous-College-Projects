"""I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy."""

from concurrent.futures import ThreadPoolExecutor
from cia_a import get_flag
import time

"""Well, it worked! I did this in cia_b, which calls cia_a. Feels awesome to see things work! Also, the speed is insane haha. It
feels so weird not to have a main tbh. Also this one ran in 2.833 seconds on my machine. That's insane."""

if __name__ == "__main__":
    start = time.perf_counter()
    size = 0
    nations = []

    with open("flags.txt", "r") as f:
        for line in f:
            nation = line.strip()
            nations.append(nation)
    
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_flag, nations)
    size = sum(results)

    end = time.perf_counter()
    print(f"Elapsed time: {end - start} seconds")
    print(f"{size} bytes downloaded")