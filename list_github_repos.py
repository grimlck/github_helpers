#!/usr/bin/env python

import sys
import urllib2
import json
import sys
import argparse

def get_repositories(github_user):
    """get the GitHub repositories for the given GitHub account.
    The return value is a list of dictionaries which contain the repository data.
    Available keys can be found here:
    http://developer.github.com/v3/repos/"""
    
    if not github_user:
        return [1, {"message": "GitHub username missing"}]
    else:

        # build Request object
        request = urllib2.Request("https://api.github.com/users/"+str(github_user)+"/repos")
        request.get_method = lambda: 'GET'
        try:
            # try to send the request to the GitHub API and create Python dictionary from JSON response

            repositories = urllib2.urlopen(request)
            repositories = json.loads("\n".join(repositories.readlines()))
            
            return [0, repositories]
        
        except urllib2.HTTPError as e:

            # return HTTP error and the message from the API  
            return [1, {"message": str(e)+": "+json.loads('\n'.join(e.readlines()))['message']}]

def main():

    # build argument parser, takes two arguments: GitHub username and number of repositories to show 
    ap = argparse.ArgumentParser(description="List GitHub repositories by user")
    ap.add_argument("username", type=str, help="GitHub username")
    ap.add_argument("-n", dest="show_only", metavar="number", type=int, help="Show only first n repositories", default=-1)
    args = ap.parse_args()

    repositories = get_repositories(args.username)

    if repositories[0] == 0:

        if args.show_only == -1 or args.show_only > len(repositories[1]):
            show_range = range(0, len(repositories[1]))
        else:
            show_range = range(0, args.show_only)

        # show only repositories in range
        for x in show_range:
            print "Repository: %s" % repositories[1][x]['name']
            print "Description: %s" % repositories[1][x]['description']
            print "URL: %s" % repositories[1][x]['html_url']
            print "Created at: %s" % repositories[1][x]['created_at']
            print "Updated at: %s" % repositories[1][x]['updated_at']
            print "Open issues: %s" % repositories[1][x]['open_issues']
            print "Clone URL: %s" % repositories[1][x]['clone_url']
            print "\n"
    else:
        print repositories[1]['message']
        


if __name__ == "__main__":
    main()

