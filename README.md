# tsoha-film
## A web application for film reviews.
### Made for hy-tsoha course.

Features:

- User account registration
- Registered users can write film reviews and give them stars
- Registered users can comment on other users' reviews
- Users can remove their own reviews and comments
- Reviews page shows all published reviews from all users, even without registration
- Users can set a profile picture and change their username and password

### Usage:
Docker usage:

0. You need Docker and Docker compose.
1. Clone this repository and `cd` into it.
2. Create the SECRET_KEY environmental variable in docker-compose.yml
3. Run 
```
sudo docker compose up
```
4. The app is now available at localhost:5000.

Manual usage:

0. You need to have PostgreSQL up and running.
1. Clone this repository and `cd` into it.
2. Create a python venv and install dependencies (note: this app requires Python version 3.12, otherwise it might not work):
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
3. Create a new PostgreSQL database called `tsoha_film` and add the required tables:
```
psql < schema.sql
```

4. Create a file called `.env` and add the following:
```
DATABASE_URL=postgresql:///tsoha_film
SECRET_KEY=<SOME SECRET KEY HERE>
```

5. Now the app can be started with `flask run`. The app will be available at localhost:5000.

Credits:
Stars images: [Yasir72.multan](https://commons.wikimedia.org/wiki/File:Star_rating_1_of_5.png)
Default profile image: [Paulo Selke](https://commons.wikimedia.org/wiki/File:Unknown_person.jpg)