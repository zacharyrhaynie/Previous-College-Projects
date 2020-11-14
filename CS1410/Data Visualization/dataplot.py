"""I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy."""

import matplotlib.pyplot as plt
import numpy as np
import glob

def analyze(file_name):
    """Main workhorse of this project. Takes a filename from the main() and starts up all the work."""
    raw = np.loadtxt(file_name, dtype="i4")
    smooth = raw.copy()
    outfile = file_name[:-4]

    i = 4 #we start on the 4th datapoint, and as the next line shows, we end on the 4th form the end
    endpoint = len(smooth) - 4 #sets this endpoint so that I can know when I'm on the 3rd from the last data point (as we don't touch the first 3 or last 3)
    while True:
        smooth[i] = ((raw[i-3]) + (raw[i-2] * 2) + (raw[i - 1] * 3) + (raw[i] * 3) + (raw[i + 1] * 3) + (raw[i + 2] * 2) + (raw[i + 3])) // 15
        #Line before is my attempt at the smoothing. Changes the entry of smooth to the average of the surronding numbers from raw
        i += 1
        #iterates until the next number would be the 3rd from the last entry
        if i == endpoint: 
            break
    
    _, axs = plt.subplots(2)
    axs[0].plot(raw, linewidth=0.5)
    axs[0].set(title=file_name, ylabel="Raw")
    axs[1].plot(smooth, linewidth=0.5)
    axs[1].set(ylabel="Smooth")

    plt.savefig(f"{outfile}.pdf")

    pulses = find_pulse_start(smooth)
    find_pulse_area(file_name, outfile, pulses, raw)

    return f"Done with {file_name}"

def find_pulse_start(smooth_entry):
    """Finds the pulse by checking whether there is an increase between 3 consecutive entries on the array passed in. If the difference
    between the first and third entries (that are rising) is over 100 it has found a pulse that begins at the first index. Then looks past
    the third entry (via find_pulse_end) to find where it starts to decline and finds the next pulse (if any). """
    pulses = []

    i=0
    endpoint = len(smooth_entry) - 3
    while True:
        if smooth_entry[i] < smooth_entry[i+1]:
            if smooth_entry[i+1] < smooth_entry[i+2]:
                if smooth_entry[i+2] - smooth_entry[i] >= 100:
                    pulse_end = find_pulse_end(smooth_entry, i)
                    pulses.append(i)
                    i = pulse_end
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1
        if i == endpoint:
            break
    return pulses

def find_pulse_end(smooth_entry, entry):
    """Simple function to return the endpoint of a pulse. Takes the smoothed list and the index to start on. Returns the index of the end of
    pulse"""
    i = entry
    while True:
        if smooth_entry[i] < smooth_entry[i+1]:
            i+=1
        else:
            return i

def find_pulse_area(file_name, outfile, pulses, raw):
    """Finds the pulse area by summing up the next 50 y values, or up to but not including the next pulse start. Prints to the output file
    the results."""
    outfile_name = outfile + ".out"
    
    i=0
    endpoint = len(pulses) - 1
    results = []
    for _ in pulses: #checks if it's the last pulse, then if it's within 50 of the next index, or if it's not within 50 and calculates area
        if pulses[i] == pulses[endpoint]:
            result = sum((raw[pulses[i]:(pulses[i]+ 50)]))#takes the next 50 y values and sums them if it's the last pulse
            results.append((pulses[i], result))
        elif pulses[i+1] <= pulses[i] + 50:
            result = sum((raw[pulses[i]:pulses[i+1]]))
            results.append((pulses[i], result))
            i += 1
        else:
            result = sum((raw[pulses[i]:pulses[i+50]]))
            results.append((pulses[i], result))
            i += 1
    with open(outfile_name, 'w') as output:
        print(file_name, file=output)
        x = 1
        for _ in results:
            list_index = results[x-1][0] + 1
            result = results[x-1][1]
            print(f"Pulse {x}: {list_index} ({result})", file=output)
            x += 1


def main():
    """Main file provided by the documentation for the program. Uses glob to find all files with a suffix of .dat in the folder that my
    dataplot.py resides in and then calls analyze on them to do all the work."""
    for fname in glob.glob('*.dat'):
        print(analyze(fname))

if __name__ == "__main__":
    main()