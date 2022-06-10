The spimplest way to test it is to:
1. Clone the repository on your own computer et ouvrir le dossier:

        git clone https://github.com/XDevant/P10_devant_xavier.git as P10
        cd P10

2. Create a new virtual environment in the root folder (the one this file):

        python -m venv env

3. Activate the virtual environment:
    + unix: source env/bin/activate
    + windows: env/Scripts/activate.ps1

4. Install the dependencies via the requirement.txt file:

        pip install -r requirements.txt

5. Navigate to the root of the app:

        cd SoftDesk

6. Run the server:

        python manage.py runserver

7. Click the link in your command line interface or copy the url in your web browser:
    It looks like: Starting development server at http://127.0.0.1:8000/

8. Create admin account:

        python manage.py createsuperuser

9. Admin url: http://127.0.0.1:8000/admin

Note: respects PEP8 thanks to flake8