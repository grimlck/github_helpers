#!/usr/bin/env python
import urllib2
import json
import base64
import sys

user_setting = {"username": "",
                "password": ""
               }

auth_settings = {"scopes":'["public_repo"]'}

def request_token(username, password, scope="", note=""):
    """request a token from GitHub to access your repository
    scope variable can have following values:
    public, public_repo, repo, repo:status, delete_repo, notifications, gist
    see http://developer.github.com/v3/oauth/#scopes for explanations"""
    
    if username and password:
        # GitHub expects username:password to be base64 encoded
        base64string = base64.encodestring(str(username)+":"+str(password)).replace('\n','')

        # build the Request object
        request = urllib2.Request("https://api.github.com/authorizations")
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
            result = urllib2.urlopen(request, '{"note":'+str(note)+'", "scopes":'+str(scope)+'}')
            
            # as the response comes in JSON format, we need to deserialize it to a Python object
            result = json.loads('\n'.join(result.readlines()))
            
            if result['token'] and type(result) == dict:
                return result['token']
        
        except urllib2.HTTPError as e:
            sys.exit()

    else:
        sys.exit("Cannot request token, username or password not specified")

def repository_exists(username, repository_name):
    """
    Checks if the repository already exists.
    """
    request = urllib2.Request("https://api.github.com/repos/"+str(username)+"/"+str(repository_name))

    try:
        if urllib2.urlopen(request).getcode() == 200:
            return True
        else:
            return False

    except urllib2.HTTPError as e:
        result = json.loads("\n".join(e.readlines()))
        if result['message'] == "Not Found":
            return False
        else:
            sys.exit("Cannot determine if the repository exists.")
