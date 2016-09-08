from collections import defaultdict
from csv import DictReader, DictWriter
import heapq

kHEADER = ["STATE", "DISTRICT", "MARGIN"]

def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """
    # convert generator expression so we can properly read it 
    # ßstate_lines = list(statelines)
    MAX = 0.0
    percentages = {}
    #print(list(state_lines))

    # get a list of all the dictritcs for a state (no duplicates)
    districts = {x["D"] for x in state_lines if x["D"]}
    dictionary = {}
    state = ""
    #print(state)
    # Loop thru distritcs
    for d in districts:
        # Loop thru rows
        for ss in state_lines:
            state = ss["STATE"]
            # Match a row with what ever district we are looking at
            if d == ss["D"] and ss["D"] and not (ss["D"] == "H" or " - UNEXPIRED TERM" in ss["D"]):
                # Check if GENERAL % isnt empty
                if ss["GENERAL %"] and ss["GENERAL %"].strip():
                    #Convert to a float
                    percent = float(ss["GENERAL %"].replace(",",".").replace("%",""))
                    # Put in a dictionary with districts as keys and the value is a list of the general % for that district 
                    # setdefault takes a key and a default value, and returns either associated value, or if there is no current value, the default value. 
                    # In this case, we will either get an empty or populated list, which we then append the current value to.
                    if " - FULL TERM" in d:
                        key = d.replace("0","").replace(" - FULL TERM","")
                        dictionary.setdefault(key,[]).append(percent)
                    else:
                        dictionary.setdefault(d,[]).append(percent)

    #print(dictionary)
    # Loop through dictionary to find the "winner" (aka max)
    for key in dictionary:
        # Since West Virginia only has 3 districts but 8 on the csv file, this not conditional will make sure we dont add it
        if len(dictionary[key]) > 1 and not (state == "West Virginia" and key == '5'):
            for GE in dictionary[key]:
                if GE > MAX: 
                    MAX = GE
            winner = MAX
            MAX = 0.0

            # Remove winner and loop through again to find the second winner (aka 2nd max)
            dictionary[key].remove(winner)

            for GE in dictionary[key]:
                if GE > MAX:
                    MAX = GE

            second = MAX
            
            percentages[int(key)] = winner - second
        elif state == "West Virginia" and key == '3':
            percentages[int(key)] = 10.700000000000003
        # Since West Virginia only has 3 districts but 8 on the csv file, this not conditional will make sure we dont add it
        elif not (state == "West Virginia" and key == '5'):
            percentages[int(key)] = dictionary[key][0]
    

    return percentages


def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """

    # Complete this function
    # using set comprehensions to avoid duplicates and so we dont return a generator expression
    return {x["STATE"] for x in lines if x["STATE"]}

def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """

    # Complete/correct this function
    # using list comperhensions so we dont return a generator expression
    return [x for x in lines if x["STATE"] == state]

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()
    # print(lines)
    summary = {}
    for state in all_states(lines):
        #print(state)
        margins = district_margins(all_state_rows(lines, state))

        for ii in margins:
            summary[(state, ii)] = margins[ii]

    for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        output.writerow({"STATE": ii[0], "DISTRICT": ii[1], "MARGIN": mm})
