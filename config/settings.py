from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-b=5-s*x-4_7i%$m081hs5edyw(dp5rgx_^hvn@4x6g^(9y0_&x'

DEBUG = True

ALLOWED_HOSTS = []

if DEBUG:
    ALLOWED_HOSTS.append('*')

AUTH_USER_MODEL = 'main.User'

JAZZMIN_SETTINGS = {
    # Заголовок окна
    'site_title': 'Админка сайта',

    # Заголовок на брендированной панели и экране входа (макс. 19 символов)
    'site_header': 'Админка сайта',

    # Логотип для вашего сайта, должен быть в статических файлах, используется для бренда в левом верхнем углу
    # 'site_logo': 'your_app/logo.png',

    # Приветственный текст на экране входа
    'welcome_sign': 'Добро пожаловать в админку',

    # Авторское право в нижнем колонтитуле
    'copyright': 'Ваша Компания',

    # Модель для поиска из строки поиска, строка поиска не будет видна, если исключена
    'search_model': 'auth.User',

    # Имя поля в модели пользователя, содержащее аватар
    # 'user_avatar': 'avatar',
}



INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'main.apps.MainConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2'
        ,
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment': 'my_jinja2.environment',
        },
    },

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# # Разрешить все домены (не рекомендуется для продакшена)
# CORS_ALLOW_ALL_ORIGINS = True
#
# CSRF_TRUSTED_ORIGINS = [
#     # 'https://ldent.online', 'http://localhost'
# ]
#
# CORS_ALLOWED_ORIGINS = [
#     # 'http://ldent.online',
#     # 'https://ldent.online',
#     'http://localhost'
# ]


# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_COOKIE_AGE = 1209600
# SESSION_SAVE_EVERY_REQUEST = True
#
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')