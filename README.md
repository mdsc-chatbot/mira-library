# ChatbotResources

ChatBot Portal (name tbd) is a place where people with different backgrounds and experiences can share, discuss their resources and their experiences working with individuals suffering from disorders such as ADHD, Autism etc. The portal is used to collect resources that a chatbot can serve to chatters. 

ChatBot Portal allows users to upload a resource and give that resource a rating based on how accurate and helpful resource was for them.Users can add relevant tags to identify the resource, which can be later be used to advise other users. Users can also gain reputation points based on the number of approved resources they submit. They can also choose their own username, create/delete account whenever they want. Chatbot Portal also has reviewer and admin statuses which can approve resource submissions and manage users respectively.

Apart from all this, they can also browse through find a resource section where all the “approved” submitted resources are shown along with different tags as filters.

# How to run

#### Django backend (Go to ChatbotPortal)
```
pip install -r requirements.txt
python manage.py createsuperuser (Create admin user)
python manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver
python manage.py migrate --run-syncdb (If changing db/ switching branch)
```
If encounter 401 error, login to admin site

#### React frontend (Go to ChatbotPortal/frontend/react)
```
npm update
npm install
npm run-script build
```



