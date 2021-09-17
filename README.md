## Voctiv Test Task 
A Flask application to estimate linear distances from any given address to the centroid point of a Moscow Ring Road.

## Table of Contents
*[Definition of Done](#definition-of-done)
*[Tech & Tools](#tech-&-tools)
*[Setup](#setup)
*[Running](#running)
*[Using](#using)
*[Final Considerations](#final-considerations)

## Definition of Done
[x] Estimate distance between coordinates, to do so was suggested the use of yandex geocoder API (optional).

[x] If the given coordinate is within the Moscow Ring Road, the distance doesnt need to be estimated.

[x] Functions and Algorithms provided with informative comments.

[x] Create docker container with the application (optional).

[x] Documenting the code and application readme.md.

[x] PEP8 compliance and type annotations.

[x] Python version greater or equal 3.8.

[x] Unittest and corner cases checks.

[x] Publish source code.

[x] Directly Blueprint.

[x] Log results.


## Tech & Tools
In order to use the server correctly, the user must have:

* Python 3.9.2
* Flask 2.0.1
* Shapely 1.7.1
* Requests 2.26.0

## Setup
To install all dependencies, run the command below:
```
$ pip3 install -r requirements.txt
```
## Running
To turn the server on you must run:
```
$ python3 app.py
```

## Using
To use the API you must get a access key by creating an account on https://positionstack.com/

After that, set a enviroment variable called API_KEY with value given by positionstack, to do so run:
```
$ export API_KEY=givenvaluefrompositionstack
```

then make a POST on the server address. ex: 

JSON:
```
{"address":"Eiffel Tower, Paris, France"}
```

Curl:
```
$ curl --header "Content-Type: application/json" -d "{\"address\":\"Moscow Planetarium, Moscow, Russia\"}" http://localhost:5000/
```

## Final Considerations
1.Tried to create an account on yandex but had issues, then used positionstack.

2.Harvesine distances assumes earth as a sphere (constant radius), which is not completely true, so there is room for error if there is a considerable vertical distance between the given coordinates. (ex: top of Everest and its antipode point.)

3.The centroid point used as reference was estimated based on the elements of list MKAD_KM, if more elements were given the centroid probably would change its coordinates too.

4.Cyrillic alphabet may cause trouble during encode/decode and api consumption, and because of that this app is using utf-8, also please, write the addresses in english.
