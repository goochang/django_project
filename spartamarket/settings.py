"""
Django settings for spartamarket project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-kdf&p(t)37nia9ju$(jl=jzy560afqby&sup5$%^ttl(74wqa("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "accounts",
    "products",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spartamarket.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spartamarket.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pokeshopdb",
        "USER": "cck",
        "PASSWORD": "lsy9003",  # 설정한 비밀번호로 적어주면 된다.
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # 디폴트 : True, 장고의 디폴트 로그 설정을 대체. / False : 장고의 디폴트 로그 설정의 전부 또는 일부를 다시 정의
    "formatters": {  # message 출력 포맷 형식
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "file_name.log",  # message가 저장될 파일명(파일명 변경 가능)
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],  # 'file' : handler의 이름
            "propagate": True,
            "level": "DEBUG",  # DEBUG 및 그 이상의 메시지를 file 핸들러에게 보내줍니다.
        },
        "app_name": {  # Project에서 생성한 app의 이름
            "handlers": ["file"],  # 다른 app을 생성 후 해당 app에서도
            "level": "DEBUG",  # 사용하고자 할 경우 해당 app 이름으로
        },  # 좌측 코드를 추가 작성해서 사용
    },
}
AUTH_USER_MODEL = "accounts.Account"
AUTHENTICATION_BACKENDS = ["accounts.backends.AuthBackend"]

POKETYPE = {
    "bug": "벌레",
    "dark": "악",
    "dragon": "용",
    "eletric": "전기",
    "fairy": "페어리",
    "fighting": "격투",
    "fire": "불",
    "flying": "비행",
    "ghost": "고스트",
    "grass": "풀",
    "ground": "땅",
    "ice": "얼음",
    "normal": "노말",
    "poison": "독",
    "psychic": "에스퍼",
    "rock": "바위",
    "steel": "강철",
    "water": "물",
}
