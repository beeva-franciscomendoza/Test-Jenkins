# Funcionality of Test Result Jenkins 
import urllib2, base64
import json
import os
from termcolor import colored, cprint

def url_api_json(simple_url):
    url_to_add = "api/json"
    url_to_add_bar = "/api/json"
    finalUrl = ""
    if simple_url[len(simple_url)-1] == "/":
      finalUrl = simple_url + url_to_add
    else:
      finalUrl = simple_url + url_to_add_bar
    return finalUrl

def add_bar_url(simple_url):
    finalUrl = ""
    if simple_url[len(simple_url)-1] == "/":
      finalUrl = simple_url
    else: 
      finalUrl = simple_url + "/"
    return finalUrl

def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]

def create_headers(username, api_token):
    return {'Authorization': auth_headers(username,api_token)}

def jobs_info_of_master(server, username, password):
    headers = create_headers(username, password)
    server = add_bar_url(server)
    server = url_api_json(server)
    request = urllib2.Request(server,None, headers)
    jobs_master = None

    try:
        response = urllib2.urlopen(request)
        d = json.load(response)
        jobs_master = d["jobs"]

        for i, val in enumerate(jobs_master):

            k = str(val["_class"]).rfind(".")
            if (str(val["_class"][k+1:]) == "ExternalJob" or str(val["_class"][k+1:]) == "WorkflowJob" or str(val["_class"][k+1:]) == "FreeStyleProject"):
                info_job = "   " + val["name"] + "  " + str(val["_class"][k+1:]) + " -- "
                if  str(val["color"]) == "red":
                    info_job = info_job + str(colored('lastbuild', 'red'))
                else:
                    if str(val["color"]) == "blue":
                        info_job = info_job + str(colored('lastbuild', 'green'))
                    else:
                        info_job = info_job + str(colored('lastbuild', 'yellow'))
                print info_job
            else:
                print val["name"]
                jobs_info_of_master(val["url"], username, password)

    except urllib2.HTTPError, e:
        return e.code
    except urllib2.URLError, e:
        print(e.args)
    except Exception as e:
        print "Jenkins returned an error in get the jobs of jenkins master (info): " + str(e)
    return jobs_master

testResults = jobs_info_of_master(server, username , password)