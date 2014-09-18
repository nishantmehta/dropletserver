

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

'''
Image upload API messages
'''


class dsImageUploadRequest(messages.Message):
    latitude = messages.FloatField(1)
    longitude = messages.FloatField(2)
    userID = messages.StringField(3)


class dsImageUploadURLResponse(messages.Message):
    URL = messages.StringField(1)


'''
Image request API
'''


class imageRequestMessage(messages.Message):
    latitude = messages.FloatField(1)
    longitude = messages.FloatField(2)
    radius = messages.IntegerField(3)
    flag = messages.StringField(4)


class imageData(messages.Message):
    url = messages.StringField(1)
    imageID = messages.StringField(2)
    flag = messages.StringField(3)
    like = messages.IntegerField(4)
    score = messages.IntegerField(5)
    latitude = messages.StringField(6)
    longitude = messages.StringField(7)



class responseMessage(messages.Message):
    images = messages.MessageField(imageData, 1, repeated=True)

'''
Like & flag image API
'''


class incrementLikeRequest(messages.Message):
    imageID = messages.StringField(1)


class incrementLikeResponse(messages.Message):
    imageID = messages.StringField(1)
    likes = messages.IntegerField(2)

class incrementFlagRequest(messages.Message):
    imageID = messages.StringField(1)


class incrementFlagResponse(messages.Message):
    imageID = messages.StringField(1)
    flags = messages.IntegerField(2)

'''
Comment API
'''

class comment(messages.Message):
    userID=messages.StringField(1)
    likes=messages.IntegerField(2)
    flag=messages.IntegerField(3)
    commentString=messages.StringField(4)
    timeStamp=messages.StringField(5)
    commentID=messages.StringField(6)

class getCommentsRequest(messages.Message):
    imageID = messages.StringField(1)

class getCommentResponse(messages.Message):
    imageID = messages.StringField(1)
    comments = messages.MessageField(comment, 2, repeated=True)

class addCommentRequest(messages.Message):
    imageID = messages.StringField(1)
    commentString = messages.StringField(2)
    userID=messages.StringField(3)

class likeCommentRequest(messages.Message):
    commentID = messages.StringField(1)

class likeCommentResponse(messages.Message):
    commentID = messages.StringField(1)
    likes = messages.IntegerField(2)

class flagCommentRequest(messages.Message):
    commentID = messages.StringField(1)

class flagCommentResponse(messages.Message):
    commentID = messages.StringField(1)
    flags = messages.IntegerField(2)


'''
class imageRequestMessage(messages.Message):
    latitude=messages.FloatField(1)
    longitude=messages.FloatField(2)
    radius=messages.IntegerField(3)
    flag=messages.StringField(4)

class imageData(messages.Message):
    url=messages.StringField(1)
    comments=messages.StringField(2)
    flag=messages.StringField(3)
    like=messages.IntegerField(4)


class stringData(messages.Message):
    url=messages.StringField(1)

class responseMessage(messages.Message):
    images=messages.MessageField(imageData,1,repeated=True)
    '''