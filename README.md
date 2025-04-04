# tsoha-film
## A web application for film reviews.
### Made for hy-tsoha course.

Planned features:

- User account registration
- Registered users can write film reviews and give them stars
- Users can edit their own reviews
- Users can choose whether to publish the review or not
- Front page shows all published reviews from all users, even without registration
- Registered users can comment on other users' reviews
- Admin user can remove reviews and comments  

### Usage:
You need to have PostgreSQL up and running to use this app. The included Dockerfile can be used for this, see Docker/Usage.md for more.
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
Alternatively use the included Dockerfile that does this.

4. Create a file called `.env` and add the following:
```
DATABASE_URL=postgresql:///tsoha_film
SECRET_KEY=<SOME SECRET KEY HERE>
```
Again, some differences if you use Docker.

5. Now the app can be started with `flask run`
