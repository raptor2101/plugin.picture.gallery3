# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# 
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
import xbmc, xbmcgui, xbmcplugin,xbmcaddon, sys, urllib, urllib2, os,re
__plugin__ = "Gallery3"

class SimpleXbmcGui(object):    
  def log(self, msg):
    if type(msg) not in (str, unicode):
      xbmc.output("[%s]: %s" % (__plugin__, type(msg)))
    else:
      xbmc.output("[%s]: %s" % (__plugin__, msg.encode('utf8')))
    
  def addImage(self,galleryItem, itemCount):
    print "Thumb:"+galleryItem.thumbnail;
    print "Image:"+galleryItem.imageLink;
    listItem=xbmcgui.ListItem(galleryItem.title, iconImage="DefaultImage.png", thumbnailImage=galleryItem.thumbnail)
    listItem.setInfo(type="image", infoLabels={ "Title": galleryItem.title } )
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=galleryItem.imageLink,listitem=listItem,isFolder=False,totalItems = itemCount)
    

  def addDir(self,galleryItem, itemCount):
    print galleryItem.thumbnail;
    listItem=xbmcgui.ListItem(galleryItem.title, iconImage="DefaultFolder.png", thumbnailImage=galleryItem.thumbnail)
      
    link = "%s?itemId=%s" % (sys.argv[0], galleryItem.itemId)
    print galleryItem.childCount;
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=link,listitem=listItem,isFolder=True,totalItems = itemCount)
  
  def openMenuContext(self):
    self.dialogProgress = xbmcgui.DialogProgress();
  
  def closeMenuContext(self):
    xbmcplugin.endOfDirectory(int(sys.argv[1]));
        
  def refresh(self):
    xbmc.executebuiltin("Container.Refresh");
  
  def errorOK(self,title="", msg=""):
    e = str( sys.exc_info()[ 1 ] )
    self.log(e)
    if not title:
      title = __plugin__
    if not msg:
      msg = "ERROR!"
    if(e == None):
      xbmcgui.Dialog().ok( title, msg, e )  
    else:
      xbmcgui.Dialog().ok( title, msg)  
