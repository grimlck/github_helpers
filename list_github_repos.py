#!/usr/bin/env python

import sys
import base64
import urllib2
import json
import sys

def get_repositories(github_user):
    """get the GitHub repositories for the given GitHub account.
    The return value is a list of dictionaries which contain the repository data.
    Available keys can be found here:
    http://developer.github.com/v3/repos/"""
    
    if not github_user:
        return [1, {"message": "GitHub username missing"}]
    else:
        request = urllib2.Request("https://api.github.com/users/"+str(github_user)+"/repos")
        request.get_method = lambda: 'GET'
        try:
            repositories = urllib2.urlopen(request)
            repositories = json.loads("\n".join(repositories.readlines()))
            
            return [0, repositories]
        
        except urllib2.HTTPError as e:
            return [1, str(e)+": "+json.loads('\n',join(e.readlines))]

def main():
    repositories = get_repositories("")
    if repositories[0] == 0:
        for repository in repositories[1]:
            print "Repository: %s" % repository['name']
            print "Description: %s" % repository['description']
            print "URL: %s" % repository['html_url']
            print "Created at: %s" % repository['created_at']
            print "Updated at: %s" % repository['updated_at']
            print "Open issues: %s" % repository['open_issues']
            print "Clone URL: %s" % repository['clone_url']
            print "\n"
    else:
        print repositories[1]['message']


if __name__ == "__main__":
    main()

