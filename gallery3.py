# -*- coding: utf-8 -*-

import urllib,urllib2,re,os,pickle
try:
    import json
except:
    import simplejson as json

regex_itemId = re.compile("\\d+$");
regex_thumbId = re.compile("/(\\d+)\\?");
regex_number = re.compile("\\d+");

class GalleryAlbum:
  def __init__(self,itemId,title,thumbnail, childCount = 0):
    self.itemId = itemId;
    self.title = title;
    self.thumbnail = thumbnail;
    self.childCount = childCount;
    self.isBrowsable = True;
    
class GalleryImage:
  def __init__(self,itemId,title,thumbnail, imageLink):
    self.itemId = itemId;
    self.title = title;
    self.thumbnail = thumbnail;
    self.imageLink = imageLink;
    self.isBrowsable = False;

class Gallery3(object):
  def __init__(self,rootUrl,apiKey,gui, imageCache, thumbCache):
    self.restLink = rootUrl + "index.php/rest/item/%s"
    self.apiKey = apiKey;
    self.imageCache = imageCache;
    self.thumbCache = thumbCache;
    self.gui = gui
    
    
  def getHTTPSocket(self, link):
    request = urllib2.Request(link)
    request.add_header('X-Gallery-Request-Key', self.apiKey)
    return urllib2.urlopen(request);
    
  def doJSONRequest(self, link):
    
    sock = self.getHTTPSocket(link);
    jsonResponse = json.loads(sock.read().decode('utf-8'))

    sock.close();
    return jsonResponse;
    
  def displayChildItems(self,itemId):
    jsonResponse = self.doJSONRequest(self.restLink%(itemId));
    children = [];
    updateDate = jsonResponse['entity']['updated'];
    membersCount = len(jsonResponse["members"]);
    archiveFile = os.path.join(self.imageCache,"%s.bin"%itemId);
    counter = 0;
    #if not os.path.exists(archiveFile) or os.stat(archiveFile)[8] < int(updateDate):
    for item in jsonResponse["members"]:
      try:
        itemId = regex_itemId.search(item).group();
        galleryChild = self.getGalleryItem(itemId);
        self.display(galleryChild, membersCount)
        children.append(galleryChild);
        if(counter > 10):
          break;
        counter = counter + 1
      except:
        pass;
      #output = open(archiveFile, 'wb')
      #pickle.dump(children, output);
      #output.close();
    #else:
    #  input = open(archiveFile, 'rb')
    #  children = pickle.load(input);
    #  input.close();
    #  childCount = len(children);
    #  for child in children:
    #    self.display(child, childCount);
        
  def display(self, item, totalItemCount):
    if(item.isBrowsable):
      self.gui.addDir(item, totalItemCount);
    else:
      self.gui.addImage(item, totalItemCount);
      
  def downloadThumbnail(self, link):
    thumbId = regex_thumbId.search(link).group();
    thumbId = regex_number.search(thumbId).group();
    targetLink = os.path.join(self.thumbCache,"%s.jpeg"%thumbId);
    if not os.path.exists(targetLink):
      sock = self.getHTTPSocket(link);
      
      thumbFile = open(targetLink,'w');
      thumbFile.write(sock.read());
      thumbFile.close();
      sock.close();
    
    return targetLink;
  
  def downloadImage(self, link, updateDate):
    imageId = regex_thumbId.search(link).group();
    imageId = regex_number.search(imageId).group();
    targetLink = os.path.join(self.imageCache,"%s.jpeg"%imageId);
      
    if not os.path.exists(targetLink) or os.stat(targetLink)[8] < int(updateDate):
      sock = self.getHTTPSocket(link);
      imageFile = open(targetLink,'w');
      imageFile.write(sock.read());
      imageFile.close();
      sock.close();
    
    return targetLink;
      
  def getGalleryItem(self,itemId):
    response = self.doJSONRequest(self.restLink%(itemId));
    
    entity = response['entity'];
    
    itemId = entity['id'];
    title = entity['title'];
    itemType = entity['type'];
    
    thumbLink = "%s|X-Gallery-Request-Key=%s&X-Gallery-Request-Method=get"%(entity['thumb_url'],self.apiKey)
    #thumbLink = self.downloadThumbnail(thumbLink);
    print thumbLink
    
    if(itemType == "album"):
      childCount = len(response['members'])
      return GalleryAlbum(itemId,title,thumbLink,childCount);
    if(itemType == "photo"):
      
      imageLink = "%s|X-Gallery-Request-Key=%s&X-Gallery-Request-Method=get"%(entity['file_url'],self.apiKey);
      changeDate = entity['updated'];
      #imageLink = self.downloadImage(imageLink,changeDate);
      print imageLink
      return GalleryImage(itemId, title, thumbLink, thumbLink);
      