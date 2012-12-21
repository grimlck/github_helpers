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
        sys.exit("Cannot list repositories, please specify a GitHub user")
    else:
        request = urllib2.Request("https://api.github.com/users/"+str(github_user)+"/repos")
        request.get_method = lambda: 'GET'
        try:
            repositories = urllib2.urlopen(request)
            repositories = json.loads("\n".join(repositories.readlines()))
            
            return repositories
        
        except urllib2.HTTPError as e:
            print "Repository not found:", e
            sys.exit()

def main():
    for repository in get_repositories(""):
        print "Repository: %s" % repository['name']
        print "Description: %s" % repository['description']
        print "URL: %s" % repository['html_url']
        print "Created at: %s" % repository['created_at']
        print "Updated at: %s" % repository['updated_at']
        print "Open issues: %s" % repository['open_issues']
        print "Clone URL: %s" % repository['clone_url']
        print "\n"


if __name__ == "__main__":
    main()

