[![Build Status](https://travis-ci.org/ramonmedeiros/Screenshot_from_url.svg?branch=master)](https://travis-ci.org/ramonmedeiros/Screenshot_from_url)

# Taking screenshots from URL 

Microservice that take screenshot from url (one or a list)

## Look at / for swagger 

This microservice uses swagger. Use it :)

## How the microservice works

Using Flask framework, it has a endpoint /screenshot that receives:
```
curl -X POST -d {"url": "http://site.se"}

{"screenshot":"https://storage.googleapis.com/file"}

```

OR

```
curl -X POST {"urls": "http://site.se;http://othersite.se"}

{"screenshots":[{"http://site.se":"https://storage.googleapis.com/file1"},                                                                     {"http://othersite.se":"https://storage.googleapis.com/file2"}
               ]
  }

```

## Tech stack

* Flask as web framework and Flask Rest+ for Swagger documentation
* GCP (Both Google Kubernetes Engine and Google Cloud Storage). 
* Selenium for screenshot

## Deployment and scaling issues

The microservice running Flask is deployed on GKE with 6 replicas. The microservice listens on port 8080. Kubernetes expose the service with a LoadBalancer, that listen at port 80.

Unfortunately, Kubernetes only offer autoscaling based on cpu consumption. You can also write your own metrics, but it's a little bit trick. In this case, to solve the scalability issue, I put a lock to avoid the microservice accept parallel requests, which takes more time, since each request is answered at a time, but avoid problems with evicted containers.

Other possiblity was to scale vertically the containers, which requires more testing and also, I'm not sure if selenium is designed to vertically scalling.

