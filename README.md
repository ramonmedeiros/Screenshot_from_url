# Taking screenshots from URL

Microservice that take screenshot from url (one or a list)

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

It uses Flask as web framework, ImageHash to generate the hash of the images and don't store duplicated files and GCP (Both Google Kubernetes Engine and Google Cloud Storage). 
