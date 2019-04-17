## Implementation of Google Recaptcha on based of Client's IP address

This repo provides the endpoint for user registration. If the more then 3 user tries to register from the same IP, then the google recaptcha will be shown to end user. Once the user verify the captcha and submit the registration detials, the reponse of the captcha will be verified against the google site verification endpoint.
Local cache is used for storing the no of registration against any client IP address which can be replaced via some more robost caching backend like redis or memcache. The validity of the cache is set as 1 day by default.

### Prerequisite

- python3
- mongodb
- flask
- pymongo
- click
- requests
- flask-caching (redis-optional)


### Setup
1. Clone the repo to your local system
    - `git clone https://github.com/manassolanki/captcha.git`

2. Install the dependancy using the pipenv
    - `pipenv install`

3. Export the environment variables
    - `export FLASK_APP=captcha`
    - `export SECRET_KEY=<some-secret-key>`
    - `export DATABASE=<database-uri>`
    - `export SITE_SECRET=<site-secret-for-recaptcha-verification>`

4. Run the flask server
    - `flask run`
