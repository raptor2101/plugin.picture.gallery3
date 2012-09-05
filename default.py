# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.image.gallery3 - 
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
from gallery3 import Gallery3
from simplexbmc import SimpleXbmcGui

import os,xbmcaddon;
#data = 'user=Raptor 2101&password=Pyi2SZxdtvRV-mjYUeMD'

__settings__ = xbmcaddon.Addon(id='plugin.image.gallery3')

def get_params():
  """ extract params from argv[2] to make a dict (key=value) """
  paramDict = {}
  print "get_params() argv=", sys.argv
  if sys.argv[2]:
    paramPairs=sys.argv[2][1:].split( "&" )
    for paramsPair in paramPairs:
      paramSplits = paramsPair.split('=')
      if (len(paramSplits))==2:
        paramDict[paramSplits[0]] = paramSplits[1]
  return paramDict

params = get_params();
itemId = params.get("itemId","1");
DIR_HOME = xbmc.translatePath(__settings__.getAddonInfo("profile"))

if not os.path.exists(DIR_HOME):
  os.mkdir(DIR_HOME);

DIR_CACHE_ROOT = os.path.join(DIR_HOME, 'cache')
if not os.path.exists(DIR_CACHE_ROOT):
  os.mkdir(DIR_CACHE_ROOT);

DIR_CACHE_THUMPS = os.path.join(DIR_CACHE_ROOT, 'thumbs')
if not os.path.exists(DIR_CACHE_THUMPS):
  os.mkdir(DIR_CACHE_THUMPS);

gui = SimpleXbmcGui();
gallery = Gallery3("<your.host/path/to/gal3>","<an valid secure-token>",gui,DIR_CACHE_ROOT,DIR_CACHE_THUMPS);
gui.openMenuContext();



gallery.displayChildItems(itemId);

gui.closeMenuContext()
#imdbJson = json.loads(results.read().decode('utf-8'))
