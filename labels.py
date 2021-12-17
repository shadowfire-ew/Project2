from os import sep
import pandas as pd
import shapely.geometry as geo
import json

table = pd.read_csv("us-state-boundaries.csv",sep=';')

def FindStateBoundaries(statename):
    querystr = "name == \"{a}\"".format(a=statename)
    entrytable = table.query(querystr)
    shapescol = entrytable["St Asgeojson"]
    shapstr = shapescol.iloc[0]
    shapeobj = json.loads(shapstr)
    return geo.shape(shapeobj)


if __name__ == "__main__":
    print(table.head())
    paentry = FindStateBoundaries("Pennsylvania")
    print(paentry.centroid)
    p1 = geo.Point(-77,41)
    print(p1.within(paentry))
    p2 = geo.Point(-77,55)
    print(p2.within(paentry))