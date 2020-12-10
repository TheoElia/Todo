from accounts.models import CustomUser
from .models import Todo
import time
from django.shortcuts import render,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict


class ExtendedEncoderAllFields(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            try:
                mypath = o.path
            except:
                return ''
            else:
                return mypath
        # this will either recusively return all atrributes of the object or return just the id
        elif isinstance(o, Model):
            return model_to_dict(o)
            # return o.id
        return super().default(o)

# Create your views here.

def index(request):
    template = "todoapp/index.html"
    args = {}
    users = CustomUser.objects.all()
    tasks = [i for i in Todo.objects.all()][::-1]
    print(users)
    args['users']=users
    args['tasks']=tasks
    return render(request,template,args)


def onboarding(request):
    template = "todoapp/onboarding.html"
    args = {}
    return render(request,template,args)


def checkKey(key):
    if key == "araba":
        return True
    return False

@csrf_exempt
def create_task(request):
    user =  CustomUser.objects.get(username="TheoElia")
    objects = {}
    response = {}
    headers = {}
    head_json = request.META
    for key,val in head_json.items():
        if key.startswith('HTTP_'):
            headers[key]=val
    # print(headers)
    try:
        api_key = headers['HTTP_API_KEY']
    except Exception as e:
        response['success']=False
        response['message']= "Please provide an api key"
        dump = json.dumps(response,cls=ExtendedEncoderAllFields)
        return HttpResponse(dump, content_type='application/json')
    if checkKey(api_key):
        # Getting data posted by user
        json_data = json.loads(str(request.body, encoding='utf-8'))
        # putting data posted by user into our own dictionary
        for key,val in json_data.items():
            objects[key]=val
        
        # create a new task
        # time.sleep(10)
        # Trying to make sure api caller provided all fields
        try:
            task = Todo()
            task.title = objects['title']
            task.description = objects['description']
            task.due_date = objects['due_date']
        except KeyError as e:
            # if a field is missin, ask api caller for it
            response['success']=False
            response['message']= "Please provide "+str(e)
        except Exception as e:
            # if there's an unknown error, tell api caller
            response['success']=False
            response['message']=str(e)
        else:
            # if everything is fine, let's save
            task.save()
            response['success']=True
            response['message']="Task created"
            response['user']=user
    else:
        response['success']=False
        response['message']= "Wrong api key provided"
    # converting response dictionary to json
    dump = json.dumps(response,cls=ExtendedEncoderAllFields)
    return HttpResponse(dump, content_type='application/json')
