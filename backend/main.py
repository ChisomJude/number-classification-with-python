from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import requests
import logging
import math
import os
from fastapi.staticfiles import StaticFiles
from mangum import Mangum




logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

#just a test 
@app.get("/test")
def test_route():
    return {"message": "Hello, World!"}

# call to the frontend
app.mount("/static", StaticFiles(directory="frontend", html=True), name="frontend")

# URL for Numbers API
url = "http://numbersapi.com/{}/math"

#defining functions for each input checks
def is_armstrong(n:int):
    #Check if a number is an Armstrong number.
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

def even(n:int):
    #Check if a number is an even number.
    return n % 2 == 0

def properties (n:int):
    props = []
    if is_armstrong(n):
        props.append("armstrong")
    if even(n):
        props.append("even")
    else:
        props.append("odd")
    return props


def digit_sum(n:int):
    #Calculate the sum of the digits of a number.
    return sum(int(digit) for digit in str(abs(n)))

def perfect_number(n:int):
    #Check if a number is a perfect .
    if n < 0:
        return False
    sum_divisor = 1
    for i in range (2, int(n**0.5)+1):
        if n % i ==0:
            sum_divisor+=i
            if i != n//i:
                sum_divisor+=n//i
    return  sum_divisor==n


def is_prime(n: int):
    #check if number is a prime number
    if n < 2:
        return False
    if n in (2,3):
        return True
    if n % 2 == 0 or n % 3==0:
        return False
    i = 5
    while i *i <= n:
        if n % i ==0 or n %(i + 2)==0:
            return False
        i +=6 
    return True
    
  #set the classify api endpoint  
@app.get ("/api/classify-number")
def num_check(number: Optional[ str]=None):
    if number is None:
        return JSONResponse(content={"error": True}, status_code=400)
    try:
        number_int = int(number)
    except ValueError:
        return JSONResponse(content={"number": number, "error": True},status_code=400)

    # Fetch fun fact about the number from Numbers API
    try:
        response = requests.get(url.format(number_int))
        if response.status_code == 200:
            return {
                "number": number_int,
                "is_prime": is_prime(number_int),
                "is_perfect": perfect_number(number_int),
                "properties": properties(number_int),
                "digit_sum": digit_sum(number_int),
                "fun_fact": response.text
            }
        else:
            return JSONResponse({"error":True},status_code=400)
    except requests.exceptions.RequestException:
            return JSONResponse(content={"error": True},status_code=400 )
    
# Create the Lambda handler
handler = Mangum(app)