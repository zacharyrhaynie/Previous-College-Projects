"""I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy."""

import requests
import time

def get_flag(nation):
    """This gets the flag from the CIA website. I decided to write it as a function with the hopes that I could import it into the other
    CIA files and save time from having to write the same code. Hopefully I can map it onto the dataset that I'll be grabbing from the
    flags.txt. Takes the letters from flags.txt and uses them to find, then save the flag."""
    endpoint_prefix = "https://www.cia.gov/library/publications/resources/the-world-factbook/graphics/flags/large/"
    file_name = endpoint_prefix + f"{nation}-lgflag.gif"
    flag = requests.get(file_name).content
    flag_name = nation + ".gif"
    with open(flag_name, "wb") as f:
        f.write(flag)
    return len(flag)

def main():
    """Main to this program. Gets the info out of flags.txt and uses it to run get_flag. Also tracks the time it requires to do all of this."""
    start = time.perf_counter()
    nations =[]
    size = 0

    with open("flags.txt", "r") as file:
        for line in file:
            nation = line.strip()
            nations.append(nation)
    
    for nation in nations:
        file_size = get_flag(nation)
        size += file_size
    
    end = time.perf_counter()

    print(f"Elapsed time: {end - start} seconds")
    print(f"{size} bytes downloaded")

if __name__ == "__main__":
    main()
    
