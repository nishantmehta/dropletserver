__author__ = 'nisha_000'

from cStringIO import StringIO
import cgi
import urllib
from google.appengine.ext import webapp
import logging
from PIL import Image
import datetime
from google.appengine.api import images
import cloudstorage as gcs
from google.appengine.ext.webapp.util import run_wsgi_app
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
from dsModel import *


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            requestURL=str(self.request.uri)
            logging.info("URl handle : "+requestURL)
            arr = requestURL.split('/')
            cuserID=arr[-1]
            geohash=arr[-2]
            cimageID=str(int(time.time()))
            logging.info("storing object with userID "+cuserID+" location "+ geohash+ " imageID "+cimageID)
            upload = self.get_uploads()[0]
            blob_key=upload.key()

            logging.info("imageID "+cimageID+" blobKey "+str(blob_key))

            imageObject= DropletImage(imageID=cimageID,
                                      userID=cuserID,
                                      geoHash=geohash,
                                      like=0,
                                      blobKey=blob_key)
            imageObject.put()
            logging.info("image saved with blobkey "+str(blob_key))
            self.response.write("image saved with blobkey "+str(blob_key))
        except Exception as e:
            print e
            self.response.write("there was some error, please try again" + str(type(e)))


app = webapp.WSGIApplication([('/upload/.*',PhotoUploadHandler)
                                     ], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()