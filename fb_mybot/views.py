#from django.shortcuts import render
# ,ybot/fb_,ybot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

PAGE_ACCESS_TOKEN = "EAAIm7i2gCoMBAEAgjTmizIXLHGt7Yb7CeE1tmexdQe72ZCXr5ulyYln8gfLcKLiavR4S37j1OBg03wa3Nw8Aod4kqPfGDa9YEWhHHiX0thapu2SWHNggIBX89voC2PsXEBIutcmUN8wOZBs9bCMZArBAkDfiuKfe9B4viTxxAZDZD"
# Create your views here.
class MyBotView(generic.View):
    def get(self, request, *args, **kwargs): 
     if self.request.GET['hub.verify_token'] == '2318934571': 
      return HttpResponse(self.request.GET['hub.challenge'])
     else: 
      return HttpResponse('Error, invalid token')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

        
def post_facebook_message(fbid, recevied_message):           
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	#post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=<page-access-token>' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
    