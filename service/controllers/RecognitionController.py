from flask import jsonify
from service import app, logTime
from service.controllers.BaseController import *
from service.models.Booking import *
from service.models.BookingVhcImage import *
from service.models.LogImageRecognition import *
from sqlalchemy import insert
from threading import Thread
import logging, traceback, boto3, time

def doImageRecognition(email, data):
    try:    
        logging.info("Do Image Recognition Thread Start: %s" % time.ctime())

        #init log automated, process start
        insertLog = LogImageRecognition(
            TOTAL_DATA    = 0,
            TOTAL_VALID   = 0,
            TOTAL_SKIPPED = 0,
            FINISHED      = 0,
            CREATED_BY    = email,
        )
        db.session.add(insertLog)
        db.session.flush()
        automationId = insertLog.AUTOMATION_ID
        db.session.commit()

        #get all related booking to scan
        bookingVhc = db.session.query(Booking, BookingVhcImage).join(Booking, BookingVhcImage.BOOKING_ID == Booking.BOOKING_ID)\
                                        .filter(Booking.WSP_DATE >= data['START_DATE'])\
                                        .filter(Booking.WSP_DATE <= data['END_DATE'])\
                                        .filter(BookingVhcImage.IMC_ID == 'IMC01')\
                                        .filter(Booking.VALIDATION == 'PENDING')\
                                        .filter(Booking.BOOKING_TYPE != 'WALKIN')\
                                        .filter(Booking.BATCH_SCAN == None)\
        
        if(data['WS_ID'] != ""):
            bookingVhc = bookingVhc.filter(Booking.WS_ID == data['WS_ID'])

        bookingVhc = bookingVhc.all()
                                    
        client = boto3.client('rekognition',
            aws_access_key_id     = app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key = app.config['AWS_SECRET_KEY'],
            region_name           = app.config['AWS_REGION']
        )

        #init total variable
        totalData    = 0
        totalValid   = 0
        totalSkipped = 0


        for row in bookingVhc:
            bookingId   = row.Booking.BOOKING_ID
            plateNumber = row.Booking.UV_LICENSE_PLATE
            imageName   = row.BookingVhcImage.VHC_IMAGE
            
            # call lib aws for image recognition
            awsRes = client.detect_text(
                Image={
                    'S3Object': {
                        'Bucket': app.config['AWS_BUCKET'],
                        'Name'  : imageName,
                    }
                }
            )

            #filter only type is LINE
            awsRes  = filter(lambda x: x['Type'] == 'LINE', awsRes['TextDetections'] )
            isValid = 0
            for key, sample in enumerate(awsRes):
                sample = sample['DetectedText']
                sample = sample.replace(' ', '')
                ratio  = compareString(plateNumber, sample)
                if(ratio >= 0.85):
                    isValid = 1
                    break
            
            if(isValid):
                Booking.query.filter(Booking.BOOKING_ID == bookingId).update({
                    'VALIDATION'     : 'VALID',
                    'IS_FINAL_STATUS': 1,
                    'BATCH_SCAN'     : automationId,
                    'UPDATED_BY'     : email
                })
                totalValid += 1
            else:
                Booking.query.filter(Booking.BOOKING_ID == bookingId).update({
                    'BATCH_SCAN' : automationId,
                    'UPDATED_BY' : email
                })    
                totalSkipped += 1
        
            totalData += 1

        #update log data and set finished
        LogImageRecognition.query.filter(LogImageRecognition.AUTOMATION_ID == automationId)\
                                .update({
                                    'TOTAL_DATA'   : totalData,
                                    'TOTAL_VALID'  : totalValid,
                                    'TOTAL_SKIPPED': totalSkipped,
                                    'FINISHED'     : 1,
                                })
        logging.info("Do Image Recognition Thread End: %s" % time.ctime())
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.exception(logTime+ " RecognitionController@doImageRecognition Error: "+traceback.format_exc())
        return 'failed'

def imageRecognition(response, request, email):
    try:
        data = request.json

        # create thread for image recognition
        imageRecognitionThread = Thread(target=doImageRecognition, args=[email, data])
        imageRecognitionThread.start();

        response.update({
            'STATUS' : '1',
            'MESSAGE' : 'image recognition success'
        })
    except Exception as e:
        db.session.rollback()
        logging.exception(logTime + "RecognitionController@imageRecognition error: "+traceback.format_exc())
        response.update({
            'STATUS' : '0',
            'MESSAGE' : 'catch error RecognitionController@imageRecognition: '+traceback.format_exc()
        })
    return response