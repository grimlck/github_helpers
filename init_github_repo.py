#!/usr/bin/env python
import urllib2
import json
import base64
import sys
import argparse
from getpass import getpass

def request_token(username, password, scopes=[""], note=""):
    """request a token from GitHub to access your repository
    scope variable can have following values:
    public, public_repo, repo, repo:status, delete_repo, notifications, gist
    see http://developer.github.com/v3/oauth/#scopes for explanations"""

    valid_scopes = ["", "public_repo", "repo", "user", "repo:status", "delete_repo", "notifications", "gist"]

    # Check if the scope is in the list of valid scopes
    for scope in scopes:
        if not scope in valid_scopes:
            error = 1
            break
        else:
            error = 0

    if username and password and error == 0:
        # GitHub expects username:password to be base64 encoded
        base64string = base64.encodestring(str(username)+":"+str(password)).replace('\n','')

        # build the Request object
        request = urllib2.Request("https://api.github.com/authorizations")
        request.add_header("Authorization", "Basic %s" % base64string)

        if scope and type(scope) == list:
            scope = json.dumps(scope)

        try:
            result = urllib2.urlopen(request, '{"note": "'+str(note)+'", "scopes": '+scopes+'}')
            
            # as the response comes in JSON format, we need to deserialize it to a Python object
            result = json.loads('\n'.join(result.readlines()))
            
            if result['token'] and type(result) == dict:
                return [0, result['token']]
        
        except urllib2.HTTPError as e:
            return [1, {"message": str(e)+": "+json.loads("\n".join(e.readlines()))['message']}]

    else:
        return [1, {"message": "Wrong scopes or username/password not specified"}]

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
            return True

def create_repository(token, repository_name, description="", auto_init=True, gitignore_template=""):
    if token and repository_name:
        create_options = '{"name": "'+str(repository_name)+'"'

        if description:
            create_options += ', "description": "'+str(description)+'"'

        if auto_init == True:
            create_options += ', "auto_init": true'
            if gitignore_template:
                create_options += ', "gitignore_template": "'+str(gitignore_template)+'"'

        create_options += '}'

        request = urllib2.Request("https://api.github.com/user/repos")
        request.add_header("Authorization", "token %s" % token)

        try:
            response = urllib2.urlopen(request,create_options)
            response_data=json.loads('\n'.join(response.readlines()))
            if response.getcode() == 201:
                return [0, response_data]
            else:
                return [1, response_data]

        except urllib2.HTTPError as e:
            return [1, {"message": str(e)+": "+json.loads("\n".join(e.readlines()))['message']}]

    else:
        return [1, {"message": "Authorization failed"}]

def main():
    ap = argparse.ArgumentParser(description="Inititalize a Github repository")
    ap.add_argument('-u', dest='username', metavar='Username', type=str, required=True, help='GitHub account name')
    ap.add_argument('-p', dest='password', metavar='Password', type=str, required=False, help='GitHub account password')
    ap.add_argument('-n', dest='repo_name', metavar='Repository name', type=str, required=True, help='Name of the new GitHub repository')
    ap.add_argument('-d', dest='desc', metavar='Description', type=str, required=False, help='Description for the new repository')
    ap.add_argument('-a', action='store_true', help='Initialize repository with empty README.md')
    ap.add_argument('-g', dest='lang', metavar='Language or Platform', type=str, required=False, help='Initialize repository with .gitignore for the specified language (e.g.: Python)')
    args = ap.parse_args()

    if not args.password:
        args.password = getpass("Password: ")

    if repository_exists(args.username, args.repo_name) == False:
        print "Requesting token..."
        token = request_token(args.username, args.password, ['repost'])
        if token[0] == 0:
            print "Creating repository..."
            result = create_repository(token[1], args.repo_name, args.desc, args.a, args.lang)
            if result[0] == 0:
                print "Repository created successfully.\n"
                print "Name: %s" % result[1]['name']
                print "Description: %s" % result[1]['description']
                print "URL: %s" % result[1]['html_url']
                print "Clone URL: %s" % result[1]['clone_url']
                print "\n"
            else:
                print "An error occured."
                print result['message']
        else:
            print "Cannot get valid token."
            print token[1]['message']
 

    else:
        print "Repository %s/%s already exists." % (args.username, args.repo_name)
        print "URL: https://github.com/%s/%s" % (args.username, args.repo_name)

if __name__ == "__main__":
    main()


