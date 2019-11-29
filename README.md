# ChatbotResources
[![Build Status](https://travis-ci.com/UAlberta-CMPUT401/ChatbotResources.svg?token=Z5vtfE1m9VBPow8TRogE&branch=master)](https://travis-ci.com/UAlberta-CMPUT401/ChatbotResources)

ChatBot Portal (name tbd) is a place where people with different backgrounds and experiences can share, discuss their resources and their experiences working with individuals suffering from disorders such as ADHD, Autism etc. The portal is used to collect resources that a chatbot can serve to chatters. 

ChatBot Portal allows users to upload a resource and give that resource a rating based on how accurate and helpful resource was for them.Users can add relevant tags to identify the resource, which can be later be used to advise other users. Users can also gain reputation points based on the number of approved resources they submit. They can also choose their own username, create/delete account whenever they want. Chatbot Portal also has reviewer and admin statuses which can approve resource submissions and manage users respectively.

Apart from all this, they can also browse through find a resource section where all the “approved” submitted resources are shown along with different tags as filters.

# How to run

#### Cybera Deployment URL

http://162.246.157.169:8000/chatbotportal/app = http://tinyurl.com/chatbotportal

#### Create mysql database
```
mysql -u root -p
SHOW DATABASES;
DROP DATABASE test_main_db;
DROP DATABASE main_db;
GRANT ALL PRIVILEGES ON . TO 'root'@'localhost';
CREATE DATABASE main_db;
```

#### Django backend (Go to ChatbotPortal)
```
pip install -r requirements.txt
python manage.py makemigrations 
python manage.py migrate && python manage.py migrate --run-syncdb
python manage.py createsuperuser
python manage.py runserver
```

OR 

```
python manage.py makemigrations auth
python manage.py migrate auth
python manage.py makemigrations authentication
python manage.py migrate authentication
python manage.py makemigrations admin
python manage.py migrate admin
python manage.py makemigrations
python manage.py migrate
python manage.py migrate –run-syncdb
```
If encounter 401 error, login to admin site

#### React frontend (Go to ChatbotPortal/frontend/react)
```
npm install
npm run-script build
```

#### Installing the chrome extension
- Chrome > settings > extensions
- Make sure developer mode is turned on
- Click on 'Load Unpacked' button and load the extensions folder located at ChatbotPortal/extension

# How to test (backend tests and selenium tests)
```
python manage.py test --verbosity=3 --noinput authentication.tests
python manage.py test --verbosity=3 --noinput authentication.functional_tests
python manage.py test --verbosity=3 --noinput resource.tests
python manage.py test --verbosity=3 --noinput review.tests
python manage.py test --verbosity=3 --noinput public.tests
```

# More documentations on our codebase
https://github.com/UAlberta-CMPUT401/ChatbotResources/wiki/10.-Documentations
