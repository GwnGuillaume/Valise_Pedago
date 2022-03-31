#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title           : setup.py
# description     : This script enables to build executables for Windows operating systems.
# author          : Gwenaël GUILLAUME
# date            : 07/11/2019
# version         : 1.0
# usage           : python setup.py build
# notes           :
# python_version  : 3.9


import sys
import os
import encodings
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata
from cx_Freeze import setup, Executable
if sys.platform == "win32":
    import tkinter
    root = tkinter.Tk()
elif sys.platform == 'linux' or sys.platform == 'linux2':
    import tkinter
    root = tkinter.Tk()

"""
    Préparation des options
"""

# Chemins pour le module tkinter
if sys.platform == "win32":
    os.environ["TCL_LIBRARY"] = os.path.normpath(root.tk.exprstring('$tcl_library'))
    os.environ["TK_LIBRARY"] = os.path.normpath(root.tk.exprstring('$tk_library'))
    PYTHON_INSTALL_DIR = r"C:\Users\gwenael.guillaume\PycharmProjects\Valise_pedago\venv"  # r"C:\Python38"
    # PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
elif sys.platform == 'linux' or sys.platform == 'linux2':
    os.environ['TCL_LIBRARY'] = root.tk.exprstring('$tcl_library')
    os.environ['TK_LIBRARY'] = root.tk.exprstring('$tk_library')
    # PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
    # os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
    # os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Options des chemins vers les répertoires
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path
if sys.platform == "win32":
    images_path = os.path.join(sys.path[0], "images")  # Dossier des images qui seront copiees dans le dossier icones
    path.append(images_path)
elif sys.platform == 'linux' or sys.platform == 'linux2':
    images_path = os.path.join(os.getcwd(), "images")  # Dossier des images qui seront copiees dans le dossier icones
    path.append(images_path)

# Options d'inclusion/exclusion de modules
if sys.platform == "win32":
    includes = ['tkinter', 'encodings']  # 'numpy.core._methods', 'numpy.lib.format'
    packages = ['appJar', 'chart_studio', 'csv',  'cx_Freeze', 'encodings', 'imgkit', 'io', 'numpy', 'pandas', 'pathlib', 'plotly', 'psutil', 'scipy',
                'shapely', 'string', 'sys', 'threading', 'tkinter', 'time']
elif sys.platform == 'linux' or sys.platform == 'linux2':
    includes = ['numpy.core._methods']  # nommer les modules non trouves par cx_freeze
    packages = ['appJar', 'csv', 'cx_Freeze', 'imgkit', 'numpy', 'pathlib', 'pdfkit', 'plotly', 'psutil', 'scipy',
                'shapely.geometry', 'sys', 'threading', 'tkinter', 'time']
else:
    pass
excludes = []
if sys.platform == "win32":
    excludes = ['email', 'matplotlib', 'mpl_toolkits', 'pip', 'PyPDF2', 'setuptools', 'sqlite3']
elif sys.platform == 'linux' or sys.platform == 'linux2':
    excludes = ['Cython', 'email', 'future', 'matplotlib', 'mpl_toolkits', 'pip', 'PyPDF2', 'PyQt4',    # 'pandas'
                'setuptools', 'sqlite3', 'xlsxwriter']
else:
    pass

# Copier les fichiers non-Python et/ou repertoires et leur contenu:
if sys.platform == "win32":
    includefiles = [
#                     (r'C:\projects\deps\geos-3.6.4-msvc2019-x86\bin\geos.dll', os.path.join('lib', 'geos.dll')),
#                     (r'C:\projects\deps\geos-3.6.4-msvc2019-x86\bin\geos_c.dll', os.path.join('lib', 'geos_c.dll')),
##                     (os.path.join(os.path.dirname(PYTHON_INSTALL_DIR), 'lib', 'site-packages', 'shapely', 'DLLs', 'geos.dll'), os.path.join('lib', 'geos.dll')),
##                     (os.path.join(os.path.dirname(PYTHON_INSTALL_DIR), 'lib', 'site-packages', 'shapely', 'DLLs', 'geos_c.dll'), os.path.join('lib', 'geos_c.dll')),
#                    (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
#                    (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
#                     (os.path.join(os.path.dirname(PYTHON_INSTALL_DIR), 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
#                     (os.path.join(os.path.dirname(PYTHON_INSTALL_DIR), 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
                    (os.path.join(sys.path[0], 'DLLs', 'SQLite3.dll'), os.path.join('lib', 'sqlite3.dll')),
#                     (os.path.join(os.path.dirname(PYTHON_INSTALL_DIR), 'DLLs', 'sqlite3.dll'), os.path.join('lib', 'sqlite3.dll')),
                    # (os.path.join(PYTHON_INSTALL_DIR, 'Lib', 'site-packages'), 'lib'),
                    # (os.path.join(r'C:\Python27\Lib\site-packages\scipy'), 'lib\scipy'),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_de_mesures(exemple).csv"),
                     (os.path.join("fichiers_de_mesure", "fichier_de_mesures(exemple).csv"))),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_geometrie_zone_etude(exemple).csv"),
                     (os.path.join("fichiers_de_mesure", "fichier_geometrie_zone_etude(exemple).csv"))),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_geometries_obstacles(exemple).csv"),
                     (os.path.join("fichiers_de_mesure", "fichier_geometries_obstacles(exemple).csv"))),
                    ## Images
                    (os.path.join(images_path, "distance_pts_mesure.gif"),
                     os.path.join("icones", "distance_pts_mesure.gif")),
                    (os.path.join(images_path, "bandeau.gif"), os.path.join("icones", "bandeau.gif")),
                    (os.path.join(images_path, "icone.gif"), os.path.join("icones", "icone.gif")),
                    (os.path.join(images_path, "insert_file.gif"), os.path.join("icones", "insert_file.gif")),
                    (os.path.join(images_path, "menu_generate_run_img.gif"),
                     os.path.join("icones", "menu_generate_run_img.gif")),
                    (os.path.join(images_path, "menu_princ_generate_img.gif"),
                     os.path.join("icones", "menu_princ_generate_img.gif")),
                    (os.path.join(images_path, "menu_princ_generate_run_img.gif"),
                     os.path.join("icones", "menu_princ_generate_run_img.gif")),
                    (os.path.join(images_path, "menu_princ_treat_img.gif"),
                     os.path.join("icones", "menu_princ_treat_img.gif")),
                    (os.path.join(images_path, "menu_princ_treat_run_img.gif"),
                     os.path.join("icones", "menu_princ_treat_run_img.gif")),
                    (os.path.join(images_path, "menu_treat_run_img.gif"),
                     os.path.join("icones", "menu_treat_run_img.gif")),
                    (os.path.join(images_path, "obstacles_geoms_file.gif"),
                     os.path.join("icones", "obstacles_geoms_file.gif")),
                    (os.path.join(images_path, "repository.gif"), os.path.join("icones", "repository.gif")),
                    (os.path.join(images_path, "study_zone_geom_file.gif"),
                     os.path.join("icones", "study_zone_geom_file.gif")),
                    (os.path.join(images_path, "texte_generate_run_img.gif"),
                     os.path.join("icones", "texte_generate_run_img.gif")),
                    (os.path.join(images_path, "texte_preparation.gif"),
                     os.path.join("icones", "texte_preparation.gif")),
                    (os.path.join(images_path, "texte_treatment_input.gif"),
                     os.path.join("icones", "texte_treatment_input.gif")),
                    (os.path.join(images_path, "texte_treat_run_img.gif"),
                     os.path.join("icones", "texte_treat_run_img.gif")),
                    (os.path.join(images_path, "treatement_outfile_img.gif"),
                     os.path.join("icones", "treatement_outfile_img.gif")),
                    ## Output examples
                    (os.path.join(sys.path[0], "resultats/exemple-1_points_mesures.html"), "resultats/exemple-1_points_mesures.html"),
                    (os.path.join(sys.path[0], "resultats/exemple-2_interpolation.html"), "resultats/exemple-2_interpolation.html"),
                    (os.path.join(sys.path[0], "resultats/exemple-3_isocontours.html"), "resultats/exemple-3_isocontours.html")]
    pass
elif sys.platform == 'linux' or sys.platform == 'linux2':
    includefiles = [(r"/usr/share/tcltk/tcl8.6/tm.tcl", "lib/tm.tcl"),
                    (r"/usr/share/tcltk/tk8.6/tk.tcl", "lib/tk.tcl"),
                    (r"/usr/include/zlib.h", "lib/zlib.h"),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_de_mesures(exemple).csv"),
                     os.path.join("fichiers_de_mesure", "fichier_de_mesures(exemple).csv")),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_geometrie_zone_etude(exemple).csv"),
                     os.path.join("fichiers_de_mesure", "fichier_geometrie_zone_etude(exemple).csv")),
                    (os.path.join(sys.path[0], "fichiers_de_mesure", "fichier_geometries_obstacles(exemple).csv"),
                     os.path.join("fichiers_de_mesure", "fichier_geometries_obstacles(exemple).csv")),
                    ## Images
                    (os.path.join(images_path, "distance_pts_mesure.gif"), os.path.join("icones", "distance_pts_mesure.gif")),
                    (os.path.join(images_path, "bandeau.gif"), os.path.join("icones", "bandeau.gif")),
                    (os.path.join(images_path, "icone.gif"), os.path.join("icones", "icone.gif")),
                    (os.path.join(images_path, "insert_file.gif"), os.path.join("icones", "insert_file.gif")),
                    (os.path.join(images_path, "menu_generate_run_img.gif"), os.path.join("icones", "menu_generate_run_img.gif")),
                    (os.path.join(images_path, "menu_princ_generate_img.gif"), os.path.join("icones", "menu_princ_generate_img.gif")),
                    (os.path.join(images_path, "menu_princ_generate_run_img.gif"), os.path.join("icones", "menu_princ_generate_run_img.gif")),
                    (os.path.join(images_path, "menu_princ_treat_img.gif"), os.path.join("icones", "menu_princ_treat_img.gif")),
                    (os.path.join(images_path, "menu_princ_treat_run_img.gif"), os.path.join("icones", "menu_princ_treat_run_img.gif")),
                    (os.path.join(images_path, "menu_treat_run_img.gif"), os.path.join("icones", "menu_treat_run_img.gif")),
                    (os.path.join(images_path, "obstacles_geoms_file.gif"), os.path.join("icones", "obstacles_geoms_file.gif")),
                    (os.path.join(images_path, "repository.gif"), os.path.join("icones", "repository.gif")),
                    (os.path.join(images_path, "study_zone_geom_file.gif"), os.path.join("icones", "study_zone_geom_file.gif")),
                    (os.path.join(images_path, "texte_generate_run_img.gif"), os.path.join("icones", "texte_generate_run_img.gif")),
                    (os.path.join(images_path, "texte_preparation.gif"), os.path.join("icones", "texte_preparation.gif")),
                    (os.path.join(images_path, "texte_treatment_input.gif"), os.path.join("icones", "texte_treatment_input.gif")),
                    (os.path.join(images_path, "texte_treat_run_img.gif"), os.path.join("icones", "texte_treat_run_img.gif")),
                    (os.path.join(images_path, "treatement_outfile_img.gif"), os.path.join("icones", "treatement_outfile_img.gif")),
                    ## Output examples
                    (os.path.join(sys.path[0], "resultats", "exemple-1_points_mesures.html"), os.path.join("resultats", "exemple-1_points_mesures.html")),
                    (os.path.join(sys.path[0], "resultats", "exemple-2_interpolation.html"), os.path.join("resultats", "exemple-2_interpolation.html")),
                    (os.path.join(sys.path[0], "resultats", "exemple-3_isocontours.html"), os.path.join("resultats", "exemple-3_isocontours.html"))]
    pass
else:
    pass

# Pour que les bibliotheques binaires de /usr/lib soient recopiees
binpathincludes = []
if sys.platform == 'linux' or sys.platform == 'linux2':
    binpathincludes += ["/usr/lib", "/usr/share"]
# if sys.platform == 'linux' or sys.platform == 'linux2':
#     binpathincludes += ["/usr/local/lib/python2.7/dist-packages/matplotlib/"]     # += ["/usr/lib", "/usr/share"]

# Pour que les bibliotheques binaires de /usr/lib ne soient pas recopiees
binpathexcludes = []
if sys.platform == 'linux' or sys.platform == 'linux2':
    binpathexcludes += ["/usr/zone_etude/lib/python2.7/dist-packages/",
                        "/usr/share/tcltk/"]

# Niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# Si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = False

# Construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "bin_path_excludes": binpathexcludes,
           "optimize": optimize,
           "silent": silent
           # "zip_include_packages": "*"
           # "zip_exclude_packages": ""
           }

# Pour inclure sous Windows les dll system necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

"""
    Préparation de la cible
"""

# Application graphique ou console
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows

# Icone de l'application
icone = None
targetRootName = "carto_acoustique_interieure"
if sys.platform == "win32":
    icone = os.path.join(images_path, "icone.gif")
    targetName = targetRootName + ".exe"
elif sys.platform == 'linux' or sys.platform == 'linux2':
    icone = "images/icone.gif"
    targetName = targetRootName

# Cible de l'exécutable
if sys.platform == 'win32':
    script = os.path.join(sys.path[0], "carto.py")
elif sys.platform == 'linux' or sys.platform == 'linux2':
    script = "carto.py"
cible = Executable(script=script,
                   base=base,   #icon=icone,
                   targetName=targetName)

#############################################################################
# creation du setup
setup(
      name=u"Cartographie_aoustique_en_espace_clos",
      description=u"Cartographie aoustique en espace clos sur la base de mesures ponctuelles géoréférencées",
      author=u"Gwenaël GUILLAUME",
      version="1.0",
      options={"build_exe": options},
      executables=[cible]
)