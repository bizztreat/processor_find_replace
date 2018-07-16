#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import os
import csv
import json


#print("Just forcing diff with this line")
#if (not os.path.exists("/data/out/tables")): os.makedirs("/data/out/tables")
#if (not os.path.exists("in/tables")): os.makedirs("in/tables")

print("Starting processor Find & Replace")
print("Will process following tables:")
print("\n".join(os.listdir("/in/tables")))


if not os.path.exists("/data/config.json"):
	#Interactive mode
	interactive_mode = True
	print("/data/config.json not found, running in interactive debug mode")
	config_find = input("Find string [\"\"\"]: ")
	config_replacement = input("Replace with [\"\"]: ")
	config_encoding = input("Input tables encoding [utf-8]: ")
	if config_find=="": config_find = "\"\"\""
	if config_replacement=="": config_replacement = "\"\""
	if config_encoding=="": config_encoding = "utf-8"
	debug_mode = 1
else:
	with open("/data/config.json","r") as fid:
		config = json.load(fid)
	interactive_mode = False
	config_find = config["parameters"]["find"]
	config_replacement = config["parameters"]["replacement"]
	config_encoding = config["parameters"]["encoding"]
	debug_mode = int(config["parameters"]["debug"])

for table_name in os.listdir("/in/tables"):
	table_path = os.path.join("/in/tables",table_name)
	output_path = os.path.join("/out/tables",table_name)
	print("Processing file %s..."%table_path)
	with open(table_path,"rt",encoding=config_encoding) as infile, open(output_path,"wt",encoding=config_encoding) as outfile:
		for inline in infile:
			outfile.write(inline.replace(config_find,config_replacement))
		