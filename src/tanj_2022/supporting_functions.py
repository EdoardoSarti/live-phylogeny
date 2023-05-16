# Fundamentals
import os
import sys
import random
import argparse
import numpy as np

# Trees
from skbio import DistanceMatrix
from skbio import tree
from ete3 import Tree
from cmath import inf

def SI(a,b):
    """returns SI value over non-gapped pairs"""
    matches = 0
    norm = 0
    for i in range(len(a)):
        if a[i] != '-' and b[i] != '-':
            norm += 1
            if a[i] == b[i]:
                 matches+=1
    if norm == 0:
        return 0.
    return matches/norm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
