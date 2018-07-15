#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import os

if (not os path.exists("/data/in/tables")): os.makedirs("/data/in/tables")


print("\n".join(os.listdir("/data/in/tables")))
