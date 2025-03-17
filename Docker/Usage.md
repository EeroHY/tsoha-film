##Usage
1. Install Docker and docker-compose and open terminal in this directory
2. Run `sudo docker build . --no-cache -t tsoha-film`
3. Back to core directory
4. Put database url `postgresql://admin:root@localhost/tsoha-film` in .env
5. Run `sudo docker compose up` in terminal
6. App with Postgresql database should now be running
7. To close ctrl + c or `sudo docker compose down` in terminal 
Might require some additional steps on non-linux os
