import sys, datetime, logging, traceback, json
from flask import *
from service import app, logTime
from service.constants import *
from service.models.GmToken import *
from service.controllers.BaseController import *
from service.controllers.RecognitionController import *
from functools import wraps

bp = Blueprint('mail_service', __name__, template_folder='templates')

response = {
    'VERSION': app.config['RESPONSE_VERSION']
}

#decorator (middleware)
def authRequired(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        token  = request.headers.get('Token')
        exists = GmToken.query.filter(GmToken.TOKEN==token).first()
        if not exists:
            response.update({
                'STATUS' : 1,
                'MESSAGE' : 'invalid token'
            })
            return response
        else:
            email           = exists.EMAIL
            kwargs['email'] = email
            return f(*args, **kwargs)
    return decoratedFunction

@bp.route('/image-recognition', methods=["POST"])
@authRequired
def imageRecognitionRoute(email):
    return imageRecognition(response, request, email);