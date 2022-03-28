#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
from numpy import mean, argsort, array, arange, ceil, argwhere
from csv import reader as csvreader, writer
from shapely.geometry.polygon import Polygon
from threading import Thread
from time import sleep
from tkinter import Toplevel, Label
import string
from shapely.geometry import Point
from Plot_Tools import get_geom_bounds


# Waiting thread
def processingPleaseWait(text, function):
    window = Toplevel() # or tkinter.Tk()
    # code before computation starts
    label = Label(window, text=text)
    label.pack()
    done = []
    def call():
        result = function()
        done.append(result)
    thread = Thread(target = call)
    thread.start() # start parallel computation
    while thread.is_alive():
        # code while computing
        window.update()
        sleep(0.001)
    # code when computation is done
    label['text'] = str(done)


# Read measurements csv file and feed dictionnary
def ReadMeasCsvFile(csv_file):
    pts_labels, x, y, db = ([] for i in range(4))
    with open(csv_file, 'r') as csvfile:   # Python 2 : with open(csv_file, 'rb') as csvfile
        reader = csvreader(csvfile, delimiter=',')
        # Skip the first row of the CSV file
        next(reader)
        for row in reader:
            pt_label, xpos, ypos, dbcell = [r for r in row[:4]]
            # Treat only rows with reported noise data
            if len(dbcell) > 0:
                # Replace comma by point for decimal noise data
                if dbcell.find(',') != -1:
                    dbcell = dbcell.replace(',', '.')
                dbval = float(dbcell)
                # Test if another measurement already exists for this point
                if pt_label in pts_labels:
                    id_same_pt = pts_labels.index(pt_label)
                    dbval = mean([dbval, db[pts_labels.index(pt_label)]])  # Average two values for this point
                    db[id_same_pt] = dbval
                else:
                    if float(xpos) in x:
                        idxpos = x.index(float(xpos))
                        if float(ypos) == y[idxpos]:
                            raw_input("%s" % (pts_labels[idxpos]))
                    db.append(dbval)
                    pts_labels.append(pt_label)
                    x.append(float(xpos))
                    y.append(float(ypos))
    content = dict()
    content['db'] = db
    content['pts_labels'] = pts_labels
    content['x'] = x
    content['y'] = y
    return content


# Read room geometry file and feed dictionnary
def ReadStudyZoneGeomFile(csv_file):
    # num_angle, x, y = ([] for i in range(3))
    geom = dict()
    with open(csv_file, 'rt') as csvfile:       # 'rb' sous Linux
        reader = csvreader(csvfile, delimiter=',')
        # Skip the first row of the CSV file
        next(reader)
        corners_coords = []
        for row in reader:
            num_angle, x, y = [r for r in row[:3]]
            corners_coords.append((float(x), float(y)))
        corners_coords.append(corners_coords[0])    # Add a copy of the first point
        geom['vertices'] = array(corners_coords)
        geom['polygon'] = Polygon(geom['vertices'])
    return geom


# Read machines geometries file and feed dictionnary
def ReadObstaclesGeomsFile(csv_file):
    # mach_name, polyline = ([] for i in range(2))
    mach_geoms = dict()
    with open(csv_file, 'r') as csvfile:   # Python 2 : with open(csv_file, 'rb') as csvfile
        reader = csvreader(csvfile, delimiter=',')
        # Skip the first row of the CSV file
        next(reader)
        for row in reader:
            mach_name, corner_num, x, y = [r for r in row[:4]]
            if not mach_name in mach_geoms:
                mach_geoms[mach_name] = {}
                mach_geoms[mach_name]['vertices'] = [[float(x), float(y)]]
            else:
                mach_geoms[mach_name]['vertices'].append([float(x), float(y)])
        for mach_name in mach_geoms.keys():
            corners_coords = mach_geoms[mach_name]['vertices']
            corners_coords.append(corners_coords[0])    # Add a copy of the first point
            mach_geoms[mach_name]['vertices'] = array(corners_coords)    # Add a copy of the first point
            mach_geoms[mach_name]['polygon'] = Polygon(mach_geoms[mach_name]['vertices'])
    return mach_geoms


# Sort data
def SortData(data):
    pts_labels, x, y, db = data['pts_labels'], data['x'], data['y'], data['db']
    # Sort data
    pts_labels_len3, x_len3, y_len3, db_len3 = ([] for i in range(4))
    pts_labels_len4, x_len4, y_len4, db_len4 = ([] for i in range(4))
    for id_pt, pt_label in enumerate(pts_labels):
        if (len(pt_label) == 2 or len(pt_label) == 3):
            pts_labels_len3.append(pt_label)
            x_len3.append(x[id_pt])
            y_len3.append(y[id_pt])
            db_len3.append(db[id_pt])
        elif len(pt_label) == 4:
            pts_labels_len4.append(pt_label)
            x_len4.append(x[id_pt])
            y_len4.append(y[id_pt])
            db_len4.append(db[id_pt])
    # List of points labels starting with one letter only
    id_sorted_len3 = argsort(pts_labels_len3)
    pts_labels_sorted_len3 = [pts_labels_len3[id3] for id3 in id_sorted_len3]
    x_sorted_len3 = [x_len3[id3] for id3 in id_sorted_len3]
    y_sorted_len3 = [y_len3[id3] for id3 in id_sorted_len3]
    db_sorted_len3 = [db_len3[id3] for id3 in id_sorted_len3]
    # List of points labels starting with two letters
    id_sorted_len4 = argsort(pts_labels_len4)
    pts_labels_sorted_len4 = [pts_labels_len4[id4] for id4 in id_sorted_len4]
    x_sorted_len4 = [x_len4[id4] for id4 in id_sorted_len4]
    y_sorted_len4 = [y_len4[id4] for id4 in id_sorted_len4]
    db_sorted_len4 = [db_len4[id4] for id4 in id_sorted_len4]
    # Concatenate the sorted lists with one letter only first and two letters next
    pts_labels_sorted = pts_labels_sorted_len3 + pts_labels_sorted_len4
    x_sorted = x_sorted_len3 + x_sorted_len4
    y_sorted = y_sorted_len3 + y_sorted_len4
    db_sorted = db_sorted_len3 + db_sorted_len4
    # Output
    data_out = list(zip(pts_labels_sorted, x_sorted, y_sorted, db_sorted))
    return data_out


# Generate grid of points and related labels
def gen_points_labels_grid(geom, xgrid_step=1., ygrid_step=1.):
    # Bounds of the geometry
    xbnds, ybnds = get_geom_bounds(geom['vertices'], (xgrid_step, ygrid_step))
    # Regular grid axis
    xaxis_range = arange(xbnds[0], xbnds[1], xgrid_step)
    yaxis_range = arange(ybnds[0], ybnds[1], ygrid_step)

    # Size of regular grid
    ny, nx = len(xaxis_range), len(yaxis_range)

    # Alphabet
    alphabet = list(string.ascii_uppercase)
    nbAlphabet = int(ceil(nx / len(alphabet)))
    alphaList = alphabet
    alphaList.extend([alphaList[i] + letter for letter in alphaList for i in range(nbAlphabet)])
    numsList = range(1, 2 * int(ygrid_step) * ny, int(ygrid_step))

    # Regular grid axis
    xaxis_range = arange(xbnds[0], xbnds[1], xgrid_step)

    # Initialize data points
    x = []
    y = []
    pts_labels = []
    for idxi, xi in enumerate(xaxis_range):
        for idyi, yi in enumerate(yaxis_range):
            point = Point(xi, yi)
            if geom['polygon'].contains(point):
                x.append(xi)
                y.append(yi)
                idAlpha = argwhere(xi == xaxis_range)[0][0] - 2
                idNum = argwhere(yi == yaxis_range)[0][
                            0] - 2  # - (np.argmin([vertice[1] for vertice in true_vertices])+2)
                pts_labels.append(alphaList[idAlpha] + str(numsList[idNum]))
    return (pts_labels, x, y)


# Generate grid of points and related labels
def write_points_labels_grid_to_csv(csv_file, pts_coords_labels):
    with open(csv_file, 'w') as csvfile:   # Python 2 : with open(csv_file, 'wb') as csvfile
        csvwriter = writer(csvfile, delimiter=',')
        csvwriter.writerow(['Indice', 'x', 'y', 'dB'])
        for idrow in range(len(pts_coords_labels[0])):
            csvwriter.writerow([pts_coords_labels[0][idrow], pts_coords_labels[1][idrow], pts_coords_labels[2][idrow], ''])
    csvfile.close()
