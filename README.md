# Python Template
## Extra Django Setup
After creating your project, some additional configuration is required to allow the project to run in Gitpod and make 


### Enabling CORS in Django
Since Django is a web framework, it’s very simple to enable CORS. So, here are the steps you must take to do so.

Install the CORS module:
`pip install django-cors-headers`

Once that’s done, enable the module in Django. This is done in the installed apps section. Oh, and don’t forget the trailing comma; otherwise, you’ll get an error.

```python
INSTALLED_APPS = [
  ...
  'corsheaders',
  ...
]
```

Next, add the middleware classes to listen in on server responses. Middleware classes hook on Django’s request/response processing. You can think of it as a plugin system to modify Django’s input or output. Make sure to put the corsheaders middleware BEFORE the already present django.CommonMiddleware.

```python
MIDDLEWARE = [
  ...,
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  ...,
]
```

Finally, set up the allowed origins.
```python
CSRF_TRUSTED_ORIGINS = ['https://*.gitpod.io']
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.gitpod\.io$",
]
```
