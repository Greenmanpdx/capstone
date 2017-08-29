BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'f#t=e5l@_1n_)q)3e0(2*)%n7efyp=h1be261x)o_li^b$29$b'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}





MEDIA_ROOT =  os.path.join(BASE_DIR,  "media")