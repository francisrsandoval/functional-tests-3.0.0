# OpenADR 3.0.0 functional tests

## Overview
This is a simple test agent for the OpenADR 3.0.0 REST platform. Each API endpoint is touched, with one or more 
predefined tokens.  

This program uses the request library to make http request against a VTN and evaluate responses.

## Requirements
Python 3.5.2+ (validated on 3.9.0)

## Usage
This program depends upon the REST server VTN to be running locally. 
See https://github.com/openadr-rest/OpenADR_3.0

To run the program, execute the following from the root directory:

```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 VTN_functional_tester.py
```