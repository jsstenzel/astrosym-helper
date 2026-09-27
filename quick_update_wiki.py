import sys

sys.path.append('..')
import config
from src.wikidotapi import *
from wiki.wiki_image_reformat import *
from wiki.wiki_imagedump import *
from wiki.wiki_imagesync import *
#import wiki.wiki_listscraper import *
from wiki.wiki_navigate_fix import *
from wiki.wiki_tagmommy import *

###First, enforce the normal state of affairs
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/jovian/","planets:jupiter")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/saturnian/","planets:saturn")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/uranian/","planets:uranus")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/planets-moons/neptunian/","planets:neptune")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/exoplanets/","exoplanets")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/fictional/","fictional")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/proposals/","proposed")
dump_imagesdir_to_wikipage(config.NSS_location+"handdrawn/other/osiris-rex-proposals/","101955contest")
sync_imagenum_to_pagenum(config.NSS_location+"handdrawn/")
sync_imagenum_to_pagenum(config.NSS_location+"autosymbols/")
fix_tag_needsimage()

###Things that probably mostly won't need to be run:
#fix_astropage_sequencing()
#fix_image_formats()

#TODO I need to figure out some fix for why a majority of pages aren't rendering with the image, despite it being linked? size=thumbnail is causing the problem in some cases?