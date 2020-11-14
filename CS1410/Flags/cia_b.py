"""I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy."""

from concurrent.futures import ProcessPoolExecutor
from cia_a import get_flag
import time

"""Now, I defined get_flag() in cia_a in the hopes of being able to import it, and then map the data onto the things that this pulls in.
This means there is legit next to no code in this file. I hope this works haha."""

if __name__ == "__main__":
    start = time.perf_counter()
    size = 0
    nations = []

    with open("flags.txt", "r") as f:
        for line in f:
            nation = line.strip()
            nations.append(nation)
    
    with ProcessPoolExecutor() as executor:
        results = executor.map(get_flag, nations)
    size = sum(results)

    end = time.perf_counter()
    print(f"Elapsed time: {end - start} seconds")
    print(f"{size} bytes downloaded")