import os
import re
import requests
import json

def prepare(s):
    return re.sub("^export ", "", s).replace('"', "").split("=")

def read_params(fn):
    with open(fn, "rt") as f:
        return dict(map(prepare, f.read().split("\n")))

def get_repos(token, org, page, per_page):
    url = "https://api.github.com/orgs/%s/repos?page=%s&per_page=%s" % (
        org, page, per_page
    )
    auth = "token %s" % token
    return requests.get(url, headers={"Authorization": auth}).json()

def get_all_repos_info(token, org):
   res = []
   page = 1
   per_page = 100
   while True:
      repos = get_repos(token, org, page, per_page)
      if not repos:
         return res
      res.extend(repos)
      page += 1

params = read_params(os.path.expanduser("~/.github"))
token = params["GITHUB_TOKEN"]
org = params["ORG"]
clone_dst = params["CLONE_DST"]

repos = get_all_repos_info(token, org)

fn = os.path.join(clone_dst, "repos.json")
with open(fn, "wt") as f:
    f.write(json.dumps(repos, indent=2))
