__author__ = 'nisha_000'

import endpoints
import datetime
import time
import geohash
import threading
from protorpc import messages
from protorpc import message_types
from google.appengine.ext import db
from google.appengine.api import users
from protorpc import remote
from google.appengine.api import files
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


class DropletImage(db.Model):
    imageID = db.StringProperty(required=True, indexed=True)
    userID = db.StringProperty(required=True, indexed=True)
    geoHash = db.StringProperty(required=True, indexed=True)
    blobKey = blobstore.BlobReferenceProperty(required=True)
    like = db.IntegerProperty()
    timeStamp = db.DateTimeProperty(auto_now_add=True)
    flag=db.IntegerProperty()

#commentID needs to be required
class dsImageComments(db.Model):
    imageID = db.StringProperty(required=True, indexed=True)
    commentID=db.StringProperty(indexed=True)
    comment = db.StringProperty()
    likes = db.IntegerProperty()
    flag= db.IntegerProperty()
    userID=db.StringProperty()
    timeStamp=db.DateTimeProperty(auto_now_add=True)



