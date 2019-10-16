#!/usr/bin/env python3

# Author: Andrei Voronin
# Year: 2019
# License: MIT

import sys


class Common:
    def __init__(self):
        self.table = {}

    def parse(self, line):
        parsed = {}
        for k, v in self.table.items():
            parsed[k] = line[v[0] - 1:v[1]]
        return parsed

    def format(self, parsed):
        result = ""
        for k, v in parsed.items():
            size = self.table[k][1] - self.table[k][0] + 1
            result += v[0:size].rjust(size)
        return result


class RSstandard(Common):
    def __init__(self):
        super().__init__()
        self.table["Record id"] = (1, 1)
        self.table["Line name"] = (2, 17)
        self.table["Point number"] = (18, 25)
        self.table["Point index"] = (26, 26)
        self.table["Point code"] = (27, 28)
        self.table["Static correction"] = (29, 32)
        self.table["Point depth"] = (33, 36)
        self.table["Seismic datum"] = (37, 40)
        self.table["Uphole time"] = (41, 42)
        self.table["Water depth"] = (43, 46)
        self.table["Easting"] = (47, 55)
        self.table["Northing"] = (56, 65)
        self.table["Elevation"] = (66, 71)
        self.table["Day of year"] = (72, 74)
        self.table["Time"] = (75, 80)


class Xstandard(Common):
    def __init__(self):
        super().__init__()
        self.table["recordId"] = (1, 1)
        self.table["ffid"] = (2, 7)
        self.table["ffidInc"] = (12, 12)
        self.table["istrCode"] = (13, 13)
        self.table["lineName"] = (14, 29)
        self.table["pointNum"] = (30, 37)
        self.table["pointIndex"] = (38, 38)
        self.table["fromChan"] = (39, 42)
        self.table["toChan"] = (43, 46)
        self.table["chanInc"] = (47, 47)
        self.table["lineName"] = (48, 63)
        self.table["fromRec"] = (64, 71)
        self.table["toRec"] = (72, 79)
        self.table["recIndex"] = (80, 80)


class OverrideRS(RSstandard):
    def override(self, name, tup):
        if name in self.table:
            self.table[name] = tup
        else:
            print("Name not found in RS table: {}".format(name))
            exit()


class OverrideX(Xstandard):
    def override(self, name, tup):
        if name in self.table:
            self.table[name] = tup
        else:
            print("Name not found in X table: {}".format(name))
            exit()


RS = RSstandard()
X = Xstandard()

myRS = OverrideRS()
myRS.override("Static correction", (29, 33))
myRS.override("Point depth", (34, 37))
myRS.override("Seismic datum", (38, 40))

myX = OverrideX()

with open(sys.argv[1]) as file:
    for line in file:
        if line.startswith("H"):
            print(line)
        elif line.startswith("R"):
            print(RS.format(myRS.parse(line)))
        elif line.startswith("S"):
            print(RS.format(myRS.parse(line)))
        elif line.startswith("X"):
            print(X.format(myX.parse(line)))
        else:
            print("Unknown format. String starts with: {}".format(line[0]))
            sys.exit()
