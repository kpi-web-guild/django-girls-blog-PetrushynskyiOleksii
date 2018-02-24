# Django Girls blog Petrushynskyi
[![Build Status](https://travis-ci.org/kpi-web-guild/django-girls-blog-PetrushynskyiOleksii.svg?branch=master)](https://travis-ci.org/kpi-web-guild/django-girls-blog-PetrushynskyiOleksii)

### Installation
- [Locally](#locally)
- [Heroku](#heroku)

##### Locally:  
1. Clone this repository and cd into cloned folder
2. Install [pyenv](https://github.com/yyuu/pyenv#installation).
3. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation).
5. Install Python 3.6.4 : `pyenv install 3.6.4`.
6. Create a new virtualenv : `pyenv virtualenv 3.6.4 <name of virtualenv>`.
7. Activate virtualenv : `pyenv local <name of virtualenv>`.
8. Install requirements for a project : `pip install -r requirements.txt`
9. Add .env in mysite folder, like in .env.example.
10. Run migrate : `python manage.py migrate`
11. Run server : `python manage.py runserver`

   Also you can create superuser for admin page : `python manage.py createsuperuser`

##### Heroku:
*Before you start deployment on Heroku, you need to clone this repository.*
1. Register account on [Heroku](https://www.heroku.com/)
2.  Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) locally
3. Login to Heroku : `heroku login`
> If you wish to use SSH instead of the default HTTPS git transport,
> you’ll need to [create a public/private keypair](https://devcenter.heroku.com/articles/keys) to deploy code.
4. Create name of your site : `heroku create <name-of-site>`
5. Push your local repository to heroku : `git push heroku master`
6. Start web process : `heroku ps:scale web=1`
7. Run migrate and create superuser :
   ```
   heroku run python manage.py
   heroku run python manage.py createsuperuser
   ```
