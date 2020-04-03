ECHO is on.

Please note that when running this app for the first time initially, before using makemigrations & migrate, the following fields must be commented out in forms.py:

'SPORTS_CHOICES', 'LOCATION_CHOICES', 'sport_id', and 'location_id'

After commenting these out, you can use:

python manage.py makemigrations 
python manage.py migrate 

In order to create the database, then run populate.py to populate the app.
Once that is done, you need to uncomment these lines and fields then run the app using:
python manage.py runserver.
