# Districts.py
#
# 

from csv import DictReader
from collections import defaultdict
from math import log
from math import sqrt 
from math import exp
from math import pi as kPI
import numpy
import matplotlib.pyplot as plt
import math

kOBAMA = set(["D.C.", "Hawaii", "Vermont", "New York", "Rhode Island",
              "Maryland", "California", "Massachusetts", "Delaware", "New Jersey",
              "Connecticut", "Illinois", "Maine", "Washington", "Oregon",
              "New Mexico", "Michigan", "Minnesota", "Nevada", "Wisconsin",
              "Iowa", "New Hampshire", "Pennsylvania", "Virginia",
              "Ohio", "Florida"])
kROMNEY = set(["North Carolina", "Georgia", "Arizona", "Missouri", "Indiana",
               "South Carolina", "Alaska", "Mississippi", "Montana", "Texas",
               "Louisiana", "South Dakota", "North Dakota", "Tennessee",
               "Kansas", "Nebraska", "Kentucky", "Alabama", "Arkansas",
               "West Virginia", "Idaho", "Oklahoma", "Wyoming", "Utah"])

def valid(row):
    return sum(ord(y) for y in row['FEC ID#'][2:4])!=173 or int(row['1']) < 3583



def ml_mean(values):
    """
    Given a list of values assumed to come from a normal distribution,
    return the maximum likelihood estimate of mean of that distribution.
    There are many libraries that do this, but do not use any functions
    outside core Python (sum and len are fine).
    """

    # Your code here
    return int(sum(values)/len(values))

def ml_variance(values, mean):
    """
    Given a list of values assumed to come from a normal distribution and
    their maximum likelihood estimate of the mean, compute the maximum
    likelihood estimate of the distribution's variance of those values.
    There are many libraries that do something like this, but they
    likely don't do exactly what you want, so you should not use them
    directly.  (And to be clear, you're not allowed to use them.)
    """
    variance = 0
    for i in values:
        variance += (mean - i) ** 2
    return int(variance / len(values))

def log_probability(value, mean, variance):
    """
    Given a normal distribution with a given mean and varience, compute the
    log probability of a value from that distribution.
    """

    # Your code here
    denominator = sqrt(2*kPI*variance)
    exponent = -((value-mean) ** 2)/(2*variance)

    return(log((1/denominator) * exp(exponent)))
def republican_share(lines, states):
    """
    Return an iterator over the Republican share of the vote in all
    districts in the states provided.
    """
    # Your code here
    # return {("Alaska", 0): 50.97}
    dict = {}
    for state in states:
      for row in lines:
        if state == row["STATE"]:
          if row["GENERAL %"] and row["D"] and row["PARTY"] == "R":
            district = row["D"]
            if "FULL TERM" in district:
              district = district.replace("0","").replace(" - FULL TERM","")
            elif "UNEXPIRED TERM" in district:
              district = district.replace(" - UNEXPIRED TERM","").replace("0","")

              # what to do if general % is empty?
          
            dict[(state,int(district))] = float(row["GENERAL %"].replace(",",".").replace("%",""))

            
  
    return dict

if __name__ == "__main__":
    # Don't modify this code
    lines = [x for x in DictReader(open("../data/2014_election_results.csv"))
             if valid(x)]

    obama_mean = ml_mean(republican_share(lines, kOBAMA).values())
    romney_mean = ml_mean(republican_share(lines, kROMNEY).values())

    obama_var = ml_variance(republican_share(lines, kOBAMA).values(),
                             obama_mean)
    romney_var = ml_variance(republican_share(lines, kROMNEY).values(),
                              romney_mean)

    colorado = republican_share(lines, ["Colorado"])
    print("\t\tObama\t\tRomney\n" + "=" * 80)
    for co, dist in colorado:
        obama_prob = log_probability(colorado[(co, dist)], obama_mean, obama_var)
        romney_prob = log_probability(colorado[(co, dist)], romney_mean, romney_var)

        print("District %i\t%f\t%f" % (dist, obama_prob, romney_prob))
