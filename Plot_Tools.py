#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import os
from scipy.spatial import ConvexHull
from scipy.interpolate import griddata
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import plotly.graph_objs as go
from plotly.offline import plot
from math import ceil, floor
# from plotly.io import write_image

# Round up a number to specified digits
def roundup(a, digits=0):
    n = 10**-digits
    return round(ceil(a / n) * n, digits)

# Round down a number to specified digits
def rounddown(a, digits=0):
    n = 10**-digits
    return round(floor(a / n) * n, digits)

##
# \~english
# \fn myfloor(x, base=5)
# \brief Round down to nearest integer
# \return The rounded value.
def myfloor(x, base=5):
    mf = base * np.floor(float(x) / base)
    if (mf == x) or (abs(mf)-abs(x) <= base):
        if mf > 0:
            mf += base
        else:
            mf -= base
    return mf

##
# \~english
# \fn myceil(x, base=5)
# \brief Round up to nearest integer
# \return The rounded value.
def myceil(x, base=5):
    mc = base * np.ceil(float(x) / base)
    if mc == x or (abs(mc) - abs(x) <= base):
        if mc > 0:
            mc += base
        else:
            mc -= base
    return mc

##
# \~english
# \fn get_geom_bounds(vertices, grid_steps)
# \brief Get x-axis and y-axis rounded bounds of the geometry
# @param vertices The vertices of the geometry;
# @param grid_steps The spatial steps of the grid in the x-axis and y-axis directions (xstep, ystep).
# \return The x-axis and y-axis bounds rounded to nearest interger according to the grid steps in the form of 2 tuples (xmin, xmax) and (ymin, ymax).
def get_geom_bounds(vertices, grid_steps):
    sortxIndices = np.argsort(vertices[:,0])
    sortyIndices = np.argsort(vertices[:,1])
    xmin = vertices[sortxIndices[0],:][0]
    xmin_rnd = myfloor(xmin, grid_steps[0])
    xmax = vertices[sortxIndices[-1],:][0]
    xmax_rnd = myceil(xmax, grid_steps[0])
    ymin = vertices[sortyIndices[0],:][1]
    ymin_rnd = myfloor(ymin, grid_steps[1])
    ymax = vertices[sortyIndices[-1],:][1]
    ymax_rnd = myceil(ymax, grid_steps[1])
    xbnds = (xmin_rnd, xmax_rnd)
    ybnds = (ymin_rnd, ymax_rnd)
    return xbnds, ybnds

# Room geometry
def SetGeom(rec_pos):   # rec_pos = array with x and y locations of the measurements
    hull = ConvexHull(rec_pos)
    geom = dict()
    # Geometry (corners)
    geom['vertices'] = np.zeros((hull.nsimplex+1, 2))
    for idvert, vertice in enumerate(hull._vertices):
        geom['vertices'][idvert, :] = rec_pos[vertice, :]
    geom['vertices'][-1] = np.array([geom['vertices'][0]])      # Add a copy of the first point
    geom['polygon'] = Polygon(geom['vertices'])
    return hull, geom


# Bounds
def SetAxisBounds(points):
    xmin = np.min([p[0] for p in points]) - 1.0
    xmax = np.max([p[0] for p in points]) + 1.0
    ymin = np.min([p[1] for p in points]) - 1.0
    ymax = np.max([p[1] for p in points]) + 1.0
    return (xmin, xmax), (ymin, ymax)


# Standard colors for noise maps (see http://www.carreteros.org/explotacion/2012/6.pdf)
def noise_maps_standard_colors():
    colorscale = [[0., "rgb(255, 255, 255)"],       # <35dB : white
                  [.1, "rgb(35, 132, 67)"],         # 35-40dB : HEX code #238443 Moderate sea green
                  [.2, "rgb(120, 198, 121)"],       # 40-45dB : HEX code #78C679 Greyish green
                  [.3, "rgb(194, 230, 153)"],       # 45-50dB : HEX code #C2E699 Light greyish chartreuse green
                  [.4, "rgb(255, 255, 178)"],       # 50-55dB : HEX code #FFFFB2 Pale yellow
                  [.5, "rgb(254, 204, 92)"],        # 55-60dB : HEX code #FECC5C Light brilliant amber
                  [.6, "rgb(252, 141, 60)"],        # 60-65dB : HEX code #FD8D3C Brilliant tangelo
                  [.7, "rgb(255, 9, 9)"],           # 65-70dB : HEX code #FF0909 Light brilliant red
                  [.8, "rgb(179, 6, 34)"],          # 70-75dB : HEX code #B30622 Moderate amaranth
                  [.9, "rgb(103, 3, 59)"],          # 75-80dB : HEX code #67033B Dark rose
                  [1., "rgb(28, 0, 84)"]]           # >80dB: HEX code #1C0054 Deep blue violet
    # colorscale = [[0., None],
    return colorscale


# Bounds
def SetAxisBounds(points):
    xmin = min([p[0] for p in points]) - 1.0
    xmax = max([p[0] for p in points]) + 1.0
    ymin = min([p[1] for p in points]) - 1.0
    ymax = max([p[1] for p in points]) + 1.0
    return (xmin, xmax), (ymin, ymax)


# Plot room geometry
def PlotGeometry(geom):
    x_vert = [vertex[0] for vertex in geom["vertices"]]
    y_vert = [vertex[1] for vertex in geom["vertices"]]
    trace = go.Scatter(x=x_vert, y=y_vert, mode='lines',
                       name="Géométrie du local",
                       line={'color': '#7f7f7f', 'width': 5})
    return trace


# Plot machines geometries
def PlotMachinesGeometries(mach_geoms):
    mach_names = mach_geoms.keys()
    traces = []
    mach_names = mach_geoms.keys()
    traces = []
    for mach_name in mach_names:
        mach_geom = mach_geoms[mach_name]
        x_vert = [vertex[0] for vertex in mach_geom["vertices"]]
        y_vert = [vertex[1] for vertex in mach_geom["vertices"]]
        name_of_machine = mach_name
        vars()[name_of_machine] = go.Scatter(x=x_vert, y=y_vert, mode='lines+text', fill='toself', fillcolor='gray',
                                             opacity=0.7, name=name_of_machine, showlegend=False,
                                             line={'color': '#7f7f7f', 'width': 1})
        traces.append(vars()[name_of_machine])
    centroids = list(zip(*[mach_geoms[mach_name]['polygon'].centroid.coords[0] for mach_name in mach_names])) # Python 3
    # centroids = zip(*[mach_geoms[mach_name]['polygon'].centroid.coords[0] for mach_name in mach_names]) # Python 2
    mach_names_str = ["<b>%s</b>" % (mach_name) for mach_name in mach_names]
    for ind_name_str, mach_name_str in enumerate(mach_names_str):
        ind_space = mach_name_str.find(' ')
        if ind_space != -1:
            mach_names_str[ind_name_str] = mach_name_str[:ind_space] + '<br />' + mach_name_str[ind_space:]
    trace_mach_name = go.Scatter(x=centroids[0], y=centroids[1], mode="text", text=mach_names_str, showlegend=False,
                                 textfont={'family': "sans serif", 'size': 14, 'color': "white"}, name="machine")
    traces.append(trace_mach_name)
    return traces


# Plot machines geometries
def PlotPointsGridWithDataLabels(geom, pts_coords_labels, image_path):
    local = PlotGeometry(geom)
    (xmin, xmax), (ymin, ymax) = SetAxisBounds(geom['vertices'])
    # Measurement points
    pts_labels_str = ["<b>%s</b>" % (pt_label) for pt_label in pts_coords_labels[0]]
    pts_x = pts_coords_labels[1]
    pts_y = pts_coords_labels[2]
    # Display measurement points
    trace2 = go.Scatter(x=pts_x, y=pts_y, mode='markers+text', name="Points de mesure", text=pts_labels_str,
                        marker=dict(size=28, color='white', line=dict(width=1., color='black')),
                        )
    layout = go.Layout(title=go.layout.Title(text="Points de mesure", font=dict(size=28)),
                       xaxis=dict(range=[xmin - 1, xmax + 1],
                                  title=go.layout.xaxis.Title(text="x [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f"))),
                       yaxis=dict(range=[ymin - 1, ymax + 1],
                                  title=go.layout.yaxis.Title(text="y [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f"))),
                       legend=dict(x=0.8, y=-0.15),
                       width=1024 * 1.5, height=800 * 1.5
                       )
    trace_data = [local, trace2]
    fig = go.Figure(data=trace_data, layout=layout)
    plot(fig, filename=image_path+".html", auto_open=False)
    return fig


# Scatter plot
def ScatterNoiseData(data, geom, image_path, mach_geoms):
    # Display room geometry
    local = PlotGeometry(geom)
    (xmin, xmax), (ymin, ymax) = SetAxisBounds(geom['vertices'])
    # Measurement points
    pts_x = [d[1] for d in data]
    pts_y = [d[2] for d in data]
    pts_dB = [d[3] for d in data]
    colorscale = noise_maps_standard_colors()
    # Display measurement points
    trace2 = go.Scatter(x=pts_x, y=pts_y, mode='markers', name="Points de mesure",
                        marker=dict(cmin=50, cmax=90, color=pts_dB, size=12, colorscale=colorscale, showscale=True, colorbar=dict(title='dB(A)')) #, cmin=35., cmax=80.
                        )
    layout = go.Layout(title=go.layout.Title(text="Points de mesure et enveloppe convexe", font=dict(size=28)),
                       xaxis=dict(range=[xmin - 1, xmax + 1],
                                  title=go.layout.xaxis.Title(text="x [m]",
                                                              font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))),
                       yaxis=dict(range=[ymin - 1, ymax + 1],
                                  title=go.layout.yaxis.Title(text="y [m]",
                                                              font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))),
                       legend=dict(x=0.8, y=-0.15),
                       width=1024, height=800
                       )
    trace_data = [local, trace2]
    if not mach_geoms is None:
        trace3 = PlotMachinesGeometries(mach_geoms)
        for i in range(len(trace3)):
            trace_data.append(trace3[i])
    fig = go.Figure(data=trace_data, layout=layout)
    plot(fig, filename=image_path+".html", auto_open=False)
    return fig

# Interpolation plot
def InterpolateData(data, geom, image_path, mach_geoms):
    # Display room geometry
    local = PlotGeometry(geom)
    (xmin, xmax), (ymin, ymax) = SetAxisBounds(geom['vertices'])
    # Measurement points
    dataset = np.array([d[1:] for d in data])

    Xi = np.arange(roundup(xmin), rounddown(xmax), 1.)
    Yi = np.arange(roundup(ymin), rounddown(ymax), 1.)
    xi, yi = np.meshgrid(Xi, Yi)
    zi = griddata((dataset[:, 0], dataset[:, 1]), dataset[:, 2], (xi, yi), method='cubic')
    for idx, x in enumerate(Xi):
        for idy, y in enumerate(Yi):
            point = Point(x, y)
            if not geom['polygon'].contains(point):
                zi[idy, idx] = np.nan
    colorscale = noise_maps_standard_colors()
    trace2 = go.Heatmap(x=Xi, y=Yi, z=zi, zmin=50, zmax=90, colorscale=colorscale, colorbar=dict(title='dB(A)'), name="Interpolation des points de mesure")    # , zmin=35., zmax=80.
    trace_data = [local, trace2]
    layout = go.Layout(title=go.layout.Title(text="Interpolation des points de mesure", font=dict(size=28)),
                       xaxis=dict(range=[xmin - 1, xmax + 1],
                                  title=go.layout.xaxis.Title(text="x [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f")
                                                              )),
                       yaxis=dict(range=[ymin - 1, ymax + 1],
                                  title=go.layout.yaxis.Title(text="y [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f")
                                                              )),
                       legend=dict(x=0.8, y=-0.15), showlegend=True,      # showlegend=False
                       width=1024, height=800
                       )
    if not mach_geoms is None:
        trace3 = PlotMachinesGeometries(mach_geoms)
        for i in range(len(trace3)):
            trace_data.append(trace3[i])
    fig = go.Figure(data=trace_data, layout=layout)
    plot(fig, filename=image_path+".html", auto_open=False)
    return fig


# Contour plot
def ContourData(data, geom, image_path, mach_geoms):
    # Display room geometry
    local = PlotGeometry(geom)
    (xmin, xmax), (ymin, ymax) = SetAxisBounds(geom['vertices'])
    # Measurement points
    dataset = np.array([d[1:] for d in data])
    Xi = np.arange(xmin, xmax, 1.)
    Yi = np.arange(ymin, ymax, 1.)
    xi, yi = np.meshgrid(Xi, Yi)
    zi = griddata((dataset[:, 0], dataset[:, 1]), dataset[:, 2], (xi, yi), method='cubic')
    for idx, x in enumerate(Xi):
        for idy, y in enumerate(Yi):
            point = Point(x, y)
            if not geom['polygon'].contains(point):
                zi[idy, idx] = np.nan
    colorscale = noise_maps_standard_colors()
    trace2 = go.Contour(x=Xi, y=Yi, z=zi, zmin=50., zmax=90.1, colorscale=colorscale, colorbar=dict(title='dB(A)'), line_smoothing=0.85,
                        name="Isocontours des niveaux sonores")
    trace_data = [local, trace2]
    layout = go.Layout(title=go.layout.Title(text="Isocontours des niveaux sonores", font=dict(size=28)),
                       xaxis=dict(range=[xmin - 1, xmax + 1],
                                  title=go.layout.xaxis.Title(text="x [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f")
                                                              )),
                       yaxis=dict(range=[ymin - 1, ymax + 1],
                                  title=go.layout.yaxis.Title(text="y [m]",
                                                              font=dict(family="Courier New, monospace", size=18,
                                                                        color="#7f7f7f")
                                                              )),
                       legend=dict(x=0.8, y=-0.15), showlegend=True,      # showlegend=False
                       width=1024, height=800
                       )
    if not mach_geoms is None:
        trace3 = PlotMachinesGeometries(mach_geoms)
        for i in range(len(trace3)):
            trace_data.append(trace3[i])
    fig = go.Figure(data=trace_data, layout=layout)
    plot(fig, filename=image_path+".html", auto_open=False)
    return fig
