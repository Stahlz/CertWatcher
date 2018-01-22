#!/bin/bash

`pgrep -f 'python $1/agent.py' | grep -v 'grep'`