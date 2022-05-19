#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from appJar import gui
from pathlib import Path
from App_Processes import ReadMeasCsvFile, ReadStudyZoneGeomFile, ReadObstaclesGeomsFile, SortData, gen_points_labels_grid, write_points_labels_grid_to_csv
from Plot_Tools import SetGeom, ScatterNoiseData, InterpolateData, ContourData, PlotPointsGridWithDataLabels
import webbrowser


def validate_input_geom_file(geom_file):
    errors = False
    if len(Path(geom_file).name) == 0:
        box_message = u'Aucun fichier de géométrie renseigné. Choisir le fichier exemple?'
        if app.yesNoBox("exemple", box_message, parent=None) == True:
            geom_file = r"fichiers_de_mesure/fichier_geometrie_zone_etude(exemple).csv"
        else:
            errors = True
            app.errorBox("no_geom_file", u"Aucun fichier de géométrie sélectionné. L'application déterminera l'enveloppe convexe des points des mesure.")
    else:
        if Path(geom_file).suffix.lower() != ".csv":
            errors = True
            app.errorBox("not_csv_file", u"Sélectionner un fichier d'entrée de type *.csv.")
    return geom_file, errors


def validate_input_obst_geoms_file(obst_geoms_file):
    errors = False
    if len(Path(obst_geoms_file).name) == 0:
        box_message = u'Aucun fichier de géométries d\'obstacles renseigné. Choisir le fichier exemple?'
        if app.yesNoBox("exemple", box_message, parent=None) == True:
            obst_geoms_file = r"fichiers_de_mesure/fichier_geometries_obstacles(exemple).csv"
        else:
            app.errorBox("no_geom_file", u"Aucun fichier de géométries d\'obstacles sélectionné.")
    else:
        if Path(obst_geoms_file).suffix.lower() != ".csv":
            errors = True
            app.errorBox("not_csv_file", u"Sélectionner un fichier d'entrée de type *.csv.")
    return obst_geoms_file, errors


def validate_input_grid_step(grid_step):
    errors = False
    # Make sure the grid step has been given
    try:
        grid_step = float(app.getEntry("Distance entre les points de mesure"))
    except ValueError:
        if app.yesNoBox("grid_step_ungiven", u"Distance entre les points de mesure non renseignée. Choisir une distance de 1m ?", parent=None) == True:
            errors = False
            grid_step = 1.0
        else:
            errors = True
            app.errorBox("no_grid_step", u"Renseigner une distance entre les points de mesure.")
    return grid_step, errors


def validate_output_repository(output_dir):
    errors = False
    if len(output_dir)==0:
        if app.yesNoBox("mkdir", u"Aucun dossier de sauvegarde sélectionné. Choisir le dossier \'resultats\' ?", parent=None) == True:
            output_dir = "resultats/"
        else:
            errors = True
            app.errorBox("no_output_dir", u"Sélectionner un répertoire de sortie.")
    # Check for a valid directory
    if not(Path(output_dir)).exists():
        if app.yesNoBox("mkdir", u"Le dossier n'existe pas. Créer le dossier ?", parent=None) == True:
            os.mkdir(output_dir)
            errors = False
        else:
            errors = True
            app.errorBox("wrong_output_dir", u"Sélectionner un répertoire de sortie valide ou existant.")
    return output_dir, errors


def validate_input_filename(output_dir, file_name, suffixes):
    errors = False
    # Check files names
    list_files_to_check = [os.path.join(output_dir, file_name) + suffix for suffix in suffixes]
    if len(file_name) < 1:
        errors = True
        app.errorBox("no_input_filename", u"Entrer un préfixe pour le nom de fichier.")
    if any([os.path.exists(fic) for fic in list_files_to_check]):
        errors = True
        box_message = u"Des fichiers avec ce préfixe existent déjà. Remplacer les fichiers ?"
        if app.yesNoBox("file_already_exists", box_message, parent=None) == True:
            errors = False
        else:
            errors = True
            app.errorBox("no_input_filename", u"Entrer un préfixe pour le nom de fichier.")
    return file_name, errors


def validate_input_meas_file(meas_file):
    errors = False
    # Make sure a csv is given or is selected
    if len(meas_file)==0:
        if app.yesNoBox("no_measfile", u"Aucun fichier de mesure sélectionné. Choisir le fichier exemple ?", parent=None) == True:
            meas_file = r"fichiers_de_mesure/fichier_de_mesures(exemple).csv"
        else:
            errors = True
            app.errorBox("no_input_measfile", u"Sélectionner un fichier de mesure.")
    elif Path(meas_file).suffix.lower() != ".csv":
        errors = True
        app.errorBox("not_csv_file", u"Sélectionner un fichier d'entrée de type *.csv.")
    return meas_file, errors


def run_generate_grid_points():
    study_zone_geom_file = app.getEntry("menu_generate_study_zone_file_btn")
    geom_file, errors = validate_input_geom_file(study_zone_geom_file)
    if errors:
        app.selectFrame("FRAME STACK", 1)
        return
    spatial_step = app.getEntry("Distance entre les points de mesure")
    grid_step, errors = validate_input_grid_step(spatial_step)
    if errors:
        app.selectFrame("FRAME STACK", 1)
        app.setEntry("menu_generate_study_zone_file_btn", geom_file)
        return
    dest_dir = app.getEntry("menu_generate_outrep_btn")
    dest_dir, errors = validate_output_repository(dest_dir)
    if errors:
        app.selectFrame("FRAME STACK", 1)
        app.setEntry("menu_generate_study_zone_file_btn", geom_file)
        app.setEntry("Distance entre les points de mesure", grid_step)
        return
    suffixes = ["-grille_points_de_mesure.html", ]
    outfile = app.getEntry("menu_generate_outfile_btn")
    outfile, errors = validate_input_filename(dest_dir, outfile, suffixes)
    if errors:
        app.selectFrame("FRAME STACK", 1)
        app.setEntry("menu_generate_study_zone_file_btn", geom_file)
        app.setEntry("Distance entre les points de mesure", grid_step)
        app.setEntry("menu_generate_outrep_btn", dest_dir)
        return
    app.setMeterFill("progress_generation", "green")
    geom = ReadStudyZoneGeomFile(geom_file)
    app.setMeter("progress_generation", 10)
    pts_coords_labels = gen_points_labels_grid(geom, grid_step, grid_step)
    app.setMeter("progress_generation", 30)
    csv_file = os.path.join(dest_dir, outfile+"-grille_points_de_mesure.csv")
    write_points_labels_grid_to_csv(csv_file, pts_coords_labels)
    app.setMeter("progress_generation", 50)
    gridlabels_file_path = os.path.join(dest_dir, outfile+"-grille_points_de_mesure")
    fig_grid_points_labels = PlotPointsGridWithDataLabels(geom, pts_coords_labels, gridlabels_file_path)
    app.setMeter("progress_generation", 100)
    if app.yesNoBox("Process_ended", u"Le tableau et l'image de la grille de mesure sont générés. Ouvrir l'image ?",
                    parent=None) == True:
        webbrowser.open(gridlabels_file_path + ".html", new=2)
    if app.yesNoBox("Process_ended", u"Quitter l'application ?", parent=None) == True:
        app.stop()
    return

def run_measurement_treatment():
    meas_file = app.getEntry("menu_treatment_meas_file_btn")
    meas_file, errors = validate_input_meas_file(meas_file)
    if errors:
        app.selectFrame("FRAME STACK", 2)
        return
    study_zone_geom_file = app.getEntry("menu_treatment_geom_file_btn")
    study_zone_geom_file, errors = validate_input_geom_file(study_zone_geom_file)
    if errors:
        app.selectFrame("FRAME STACK", 2)
        app.setEntry("menu_treatment_meas_file_btn", meas_file)
        return
    obst_geoms_file = app.getEntry("menu_treatment_obst_file_btn")
    obst_geoms_file, errors = validate_input_obst_geoms_file(obst_geoms_file)
    if errors:
        app.selectFrame("FRAME STACK", 2)
        app.setEntry("menu_treatment_meas_file_btn", meas_file)
        app.setEntry("menu_treatment_geom_file_btn", study_zone_geom_file)
        return
    dest_dir = app.getEntry("menu_treatment_outrep_btn")
    dest_dir, errors = validate_output_repository(dest_dir)
    if errors:
        app.selectFrame("FRAME STACK", 2)
        app.setEntry("menu_treatment_meas_file_btn", meas_file)
        app.setEntry("menu_treatment_geom_file_btn", study_zone_geom_file)
        app.setEntry("menu_treatment_obst_file_btn", obst_geoms_file)
        return
    out_file = app.getEntry("menu_treatment_outfile_btn")
    suffixes = ["-1_points_mesures.html", "-2_interpolation.html", "-3_isocontours.html"]
    out_file, errors = validate_input_filename(dest_dir, out_file, suffixes)
    if errors:
        app.selectFrame("FRAME STACK", 2)
        app.setEntry("menu_treatment_meas_file_btn", meas_file)
        app.setEntry("menu_treatment_geom_file_btn", study_zone_geom_file)
        app.setEntry("menu_treatment_obst_file_btn", obst_geoms_file)
        app.setEntry("menu_treatment_outrep_btn", dest_dir)
        return
    app.setMeterFill("progress_treatment", "blue")
    # Read and merge data
    print(u"Lecture du fichier %s" % (meas_file))
    content_tmp = ReadMeasCsvFile(meas_file)
    app.setMeter("progress_treatment", 10)
    # Sort data
    print(u"Ordonnancement des mesures")
    content = SortData(content_tmp)  # pts_labels, x, y, dB
    app.setMeter("progress_treatment", 20)
    # Read the study_zone geometry file
    if len(study_zone_geom_file) > 0:
        print(u"Lecture du fichier %s" % (study_zone_geom_file))
        geom = ReadStudyZoneGeomFile(study_zone_geom_file)
    else:
        # Retrieve the geometry
        print(u"Calcul de l'enveloppe convexe des points de mesure")
        rec_pos_x, rec_pos_y = zip(*content)[1:3]
        rec_pos = np.array(zip(rec_pos_x, rec_pos_y))
        hull, geom = SetGeom(rec_pos)
    app.setMeter("progress_treatment", 40)
    # Read the obstacles geometries file
    if len(obst_geoms_file) > 0:
        print(u"Lecture du fichier %s" % (obst_geoms_file))
        obst_geoms = ReadObstaclesGeomsFile(obst_geoms_file)
    else:
        obst_geoms = None
    app.setMeter("progress_treatment", 50)
    # Display noise levels dataset
    print(u"Affichage de la zone d'etude et des points de mesure")
    points_file_path = os.path.join(dest_dir, out_file + "-1_points_mesures")
    fig_scatter = ScatterNoiseData(content, geom, points_file_path, obst_geoms)
    app.setMeter("progress_treatment", 60)
    # Interpolate data
    print(u"Interpolation des mesures")
    interpol_file_path = os.path.join(dest_dir, out_file + "-2_interpolation")
    fig_interp = InterpolateData(content, geom, interpol_file_path, obst_geoms)
    app.setMeter("progress_treatment", 80)
    # Interpolated data with contours
    print(u"Affichage des isocontours")
    contours_file_path = os.path.join(dest_dir, out_file + "-3_isocontours")
    fig_contour = ContourData(content, geom, contours_file_path, obst_geoms)
    app.setMeter("progress_treatment", 100)
    if app.yesNoBox("Process_ended", u"Le traitement des mesures est terminé. Ouvrir les fichiers résultats ?",
                    parent=None) == True:
        webbrowser.open(points_file_path+".html", new=2)
        webbrowser.open(interpol_file_path+".html", new=2)
        webbrowser.open(contours_file_path+".html", new=2)
    if app.yesNoBox("Process_ended", u"Quitter l'application ?", parent=None) == True:
        app.stop()
    return

def press(button):
    if button == u"Générer":
        run_generate_grid_points()
    elif button == u"Traiter":
        run_measurement_treatment()
    elif button == u"Quitter":
        app.stop()
    elif button == u"À propos":
        app.infoBox(u"À propos", u"Auteur : Gwenaël GUILLAUME\n Contact : gwenael.guillaume@cerema.fr\n Version 1.0")
    else:
        app.stop()

def press_menu(button):
    if button == u"Menu principal":
        app.firstFrame("FRAME STACK")
    elif button == "Preparation":
        app.nextFrame("FRAME STACK")
    elif button == "Traitement":
        app.lastFrame("FRAME STACK")
    elif button == u"Quitter":
        app.stop()
    elif button == u"À propos":
        app.infoBox(u"À propos",
                    u"Auteur : Gwenaël GUILLAUME\n Contact : gwenael.guillaume@cerema.fr\n Version 1.0")
    else:
        app.stop()

## FOR DEBUGING
debug = False    # True for testing scripts with the Python editor

# Add Images
dirpath = os.path.dirname(os.path.realpath('__file__'))

if debug:
    if sys.platform == "win32":
        images_path = os.path.join(dirpath, "images")
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        images_path = os.path.join(os.getcwd(), "images")
else:
    if sys.platform == "win32":
        images_path = os.path.join(dirpath, "icones")
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        images_path = os.path.join(os.getcwd(), "icones")

# Create the GUI Window
app = gui(u"Cartographie des niveaux sonores", useTtk=True)
app.setTtkTheme("classic")
if sys.platform == "win32":
    app.setSize(1000, 800)
elif sys.platform == "linux2":
    app.setSize(800, 600)
app.setBg(colour='LightYellow')
app.addImage("menu_princ_header_img", os.path.join(images_path, "bandeau.gif"), row=0, column=0, colspan=3)
app.set_Resizable(canResize=True)
app.startFrameStack("FRAME STACK", start=0)

##
# FRAME 0 : MENU PRINCIPAL
app.startFrame(u"Menu principal")
# app.addLabel(" ", row=0, column=0)
app.addImageButton("Preparation", press_menu, imgFile=os.path.join(images_path, "menu_princ_generate_img.gif"),
                   row=0, column=0, colspan=1, align=None)
app.addLabel(u"\tGénérer le tableau et l'image de la grille de points de mesures", row=0, column=2)
app.addImage("menu_princ_generate_img_output", os.path.join(images_path, "menu_princ_generate_run_img.gif"), row=0, column=3)
app.addImageButton("Traitement", press_menu, imgFile=os.path.join(images_path, "menu_princ_treat_img.gif"),
                   row=1, column=0, colspan=1, align=None)
app.addLabel(u"\tProduire la cartographie sonore à partir des mesures", row=1, column=2)
app.addImage("menu_princ_treat_img_output", os.path.join(images_path, "menu_princ_treat_run_img.gif"), row=1, column=3)
app.stopFrame()

##
# FRAME 1 : GÉNÉRATION  DE LA GRILLE DE POINTS DE MESURE
app.startFrame(u"Preparation")
app.addImage("texte_preparation", os.path.join(images_path, "texte_preparation.gif"), row=0, column=0, colspan=3)
app.addImage("menu_generate_study_zone_img", os.path.join(images_path, "study_zone_geom_file.gif"), row=1, column=0)
app.addFileEntry("menu_generate_study_zone_file_btn", row=1, column=1, colspan=2).theButton.config(text=u"Géométrie de la zone d'étude")
# app.setEntryDefault("menu_generate_study_zone_file_btn", os.path.join()
app.addImage("menu_generate_dist_pts_img", os.path.join(images_path, "distance_pts_mesure.gif"), row=2, column=0)
app.setEntryDefault("menu_generate_study_zone_file_btn", u"Sélection du fichier de la géométrie de la zone d'étude")
app.addLabelEntry("Distance entre les points de mesure", row=2, column=1)
app.setEntryDefault("Distance entre les points de mesure", u"1.0")
app.addLabel(u"m", row=2, column=2)
app.addImage("menu_generate_outrep_img", os.path.join(images_path, "repository.gif"), row=3, column=0)
app.addDirectoryEntry("menu_generate_outrep_btn", row=3, column=1, colspan=2).theButton.config(text=u"Dossier de résultats")
app.setEntryDefault("menu_generate_outrep_btn", u"Dossier de résultats")
app.addEntry("menu_generate_outfile_btn", row=4, column=1)
app.setEntryDefault("menu_generate_outfile_btn", u"Préfixe des fichiers csv et html de résultats (...-grille_points_de_mesure.csv)")
#
app.addImage("texte_generate_run_img", os.path.join(images_path, "texte_generate_run_img.gif"), row=0, column=4, colspan=3)
app.addImageButton(u"Générer", press, imgFile=os.path.join(images_path, "menu_generate_run_img.gif"),
                   row=2, column=4, rowspan=2, colspan=2, align=None)
app.addMeter("progress_generation", row=5, column=4, colspan=2)
app.stopFrame()

##
# FRAME 2 : TRAITEMENT DES MESURES
app.startFrame(u"Traitement")
app.addImage("texte_treatment_input", os.path.join(images_path, "texte_treatment_input.gif"), row=0, column=0, colspan=3)
app.addImage("menu_treatment_meas_file_img", os.path.join(images_path, "insert_file.gif"), row=1, column=0)
app.addFileEntry("menu_treatment_meas_file_btn", row=1, column=1, colspan=2).theButton.config(text=u"Mesures")
app.setEntryDefault("menu_treatment_meas_file_btn", u"Fichier de mesures")
app.addImage("menu_treatment_geom_file_img", os.path.join(images_path, "study_zone_geom_file.gif"), row=2, column=0)
app.addFileEntry("menu_treatment_geom_file_btn", row=2, column=1, colspan=2).theButton.config(text=u"Géométrie de la zone d'étude")
app.setEntryDefault("menu_treatment_geom_file_btn", u"--- OPTIONNEL --- Fichier de la géométrie de la zone d'étude")
app.addImage("menu_treatment_obst_file_img", os.path.join(images_path, "obstacles_geoms_file.gif"), row=3, column=0)
app.addFileEntry("menu_treatment_obst_file_btn", row=3, column=1, colspan=2).theButton.config(text=u"Géométries des obstacles")
app.setEntryDefault("menu_treatment_obst_file_btn", u"--- OPTIONNEL --- Fichier des géométries des obstacles")
app.addImage("menu_treatment_outrep_img", os.path.join(images_path, "repository.gif"), row=4, column=0)
app.addDirectoryEntry("menu_treatment_outrep_btn", row=4, column=1, colspan=2).theButton.config(text=u"Dossier de résultats")
app.setEntryDefault("menu_treatment_outrep_btn", u"Dossier de résultats")
app.addImage("menu_treatment_outfile_img", os.path.join(images_path, "treatement_outfile_img.gif"), row=5, column=0)
app.addEntry("menu_treatment_outfile_btn", row=5, column=1)
app.setEntryDefault("menu_treatment_outfile_btn", u"Préfixe des fichiers html de résultats (...-1_points_mesures.html/-2_interpolation.html/-3_isocontours.html)")
#
app.addImage("texte_treat_run_img", os.path.join(images_path, "texte_treat_run_img.gif"), row=0, column=4, colspan=3)
app.addImageButton(u"Traiter", press, imgFile=os.path.join(images_path, "menu_treat_run_img.gif"),
                   row=2, column=4, rowspan=2, colspan=2, align=None)
app.addMeter("progress_treatment", row=5, column=4, colspan=2)
app.stopFrame()

app.stopFrameStack()

app.addButtons([u"Menu principal", u"À propos", u"Quitter"], press_menu)

# Start the GUI
app.go()
