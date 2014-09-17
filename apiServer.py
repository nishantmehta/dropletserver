

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
from google.appengine.api import images
from PIL import Image
from dsMessage import *
from dsModel import *
import logging
'''
Improvements:
1. use config file for bucket name
'''

@endpoints.api(name='dsAPI', version='v1',
               description="has all api calls need to communicate with the server")
class dsAPI(remote.Service):

    #upload Image API
    @endpoints.method(dsImageUploadRequest, dsImageUploadURLResponse, name="upload_image_request")
    def uploadImage(self, request):
        geoHash = geohash.encode(request.latitude, request.longitude)
        #db.delete(DropletImage.all(keys_only=True))
        userID=request.userID
        callbackURLString="/upload/"+str(geoHash)+"/"+userID
        logging.info("call back URL is " + callbackURLString)
        upload_url = blobstore.create_upload_url(callbackURLString, gs_bucket_name='dropletserver.appspot.com/publicimages/')
        logging.info("upload url is "+ upload_url)
        return dsImageUploadURLResponse(URL=str(upload_url))

    #image request API
    @endpoints.method(imageRequestMessage,responseMessage,name="request_images")
    def getImages(self,request):
        imageSet=db.GqlQuery("SELECT * FROM DropletImage")
        logging.info("Image count from database"+str(imageSet.count()))
        list=[]
        for e in imageSet:
            a=imageData(imageID=e.imageID, url=images.get_serving_url(e.blobKey), flag="na", like=e.like,score=1)
            list.append(a)
        logging.info("Image count for response"+str(len(list)))
        return responseMessage(images=list)

    #image like API
    @endpoints.method(incrementLikeRequest,incrementLikeResponse,name="update_like_counter")
    def updateLike(self,request):
        imageID=request.imageID
        imageInfo=db.GqlQuery("SELECT * from DropletImage WHERE imageID = :1",imageID)
        #imageInfo=db.GqlQuery("SELECT * from DropletImage")
        likeCounter=0
        for data in imageInfo.run(limit=1):
            logging.info(data.userID)
            data.like=data.like+1
            likeCounter=data.like
            data.put()
            print data.userID
        return incrementLikeResponse(imageID=imageID,likes=likeCounter )

    @endpoints.method(getCommentsRequest,getCommentResponse,name="get_all_comments")
    def getComments(self,request):
        imageID=request.imageID
        imageComments=db.GqlQuery("SELECT * from dsImageComments WHERE imageID = :1",imageID)
        logging.info("Number of comments for imageID: "+imageID+" is "+str(imageComments.count()))
        list=[]
        for data in imageComments:
            commentData=comment(userID=data.userID,likes=data.likes,flag=data.flag,commentString=data.comment,timeStamp=str(data.timeStamp),commentID=data.commentID)
            list.append(commentData)
        return getCommentResponse(imageID=imageID,comments=list)

    @endpoints.method(addCommentRequest,getCommentResponse,name="add_comment_to_a_image")
    def addComment(self,request):
        #db.delete(dsImageComments.all(keys_only=True))
        newComment=dsImageComments(userID=request.userID,
                                   comment=request.commentString,
                                   imageID=request.imageID,
                                   commentID="cc"+str(int(time.time()))
                                   )
        newComment.put()

        imageID=request.imageID
        imageComments=db.GqlQuery("SELECT * from dsImageComments WHERE imageID = :1",imageID)
        logging.info("Number of comments for imageID: "+imageID+" is "+str(imageComments.count()))
        list=[]
        for data in imageComments:
            commentData=comment(userID=data.userID,likes=data.likes,flag=data.flag,commentString=data.comment,timeStamp=str(data.timeStamp),commentID=data.commentID)
            list.append(commentData)
        if len(list)>0:
            return getCommentResponse(imageID=imageID,comments=list)
        else:
            return getCommentResponse(imageID=imageID)

APPLICATION = endpoints.api_server([dsAPI])
