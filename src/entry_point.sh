#!/bin/bash

Xvfb $DISPLAY &
flask run --host=0.0.0.0 --port=8080
