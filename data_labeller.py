#!/usr/bin/env python3

import sys
import pickle
import json

f = open("badwords4.json")
badwords = json.load(f)
badwords

for line in sys.stdin: # read input from STDIN
  line = line.strip() # remove leading and trailing whitespace
  if line.find('"http://') == 0:
    line_string = line[line.find("{"):len(line)]
    if len(line_string) == 0:
      line_string == {}

  converted_object = json.loads(line_string)
  #print(type(converted_object))

  if "content-oneline" in converted_object:

      badlist = badwords.keys()

      # Slow initial solution
      #slurs = [value for value in badlist if value in siteinfo["content-tokens"]]
      
      # Way faster solution using sets
      slurs = list(set(badlist).intersection(set(converted_object["content-tokens"])))
      
      if len(slurs) > 0:
          siterating = badwords[slurs[0]]["severity_rating"]
          for slur in slurs:
              wordrating = badwords[slur]["severity_rating"]
              siterating = round((siterating + wordrating) / 2, 1)

          if siterating >= 2.5:
              label = "Severe"
          elif siterating >= 1.5:
              label = "Strong"
          elif siterating >= 0:
              label = "Mild"
          else:
              label = "Safe"

          converted_object["contains-slur"] = True
          converted_object["slurs"] = slurs
          converted_object["site-rating"] = siterating
          converted_object["site-label"] = label
      else:
          converted_object["contains-slur"] = False
          converted_object["slurs"] = None # or []
          converted_object["site-rating"] = 0
          converted_object["site-label"] = "Safe"
  print(json.dumps(converted_object))



