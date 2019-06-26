Linux Server Configuration

# Step 1: make a Ubuntu Linux server instance on Amazon Light sail
- I did Ubuntu 18.04 LTS

##
password for all instances should be "udacity"
-update changed PasswordAuthentication to "no"

- Download SSH key from SSH keys tab. Rename key to .rsa file
- in terminal on local machine:
    - "chmod 600 ~/.ssh/LSDK_1.pem"
- Enter this command to connect to instance via terminal:
    - "ssh -i ~/.ssh/LSDK_1.pem ubuntu@34.207.134.212"

# Step 2: Secure the server
    - Update/upgrade installed packages
        -"sudo apt-get update && sudo apt-get dist-upgrade"
    - Add 2200 SSH port
        Enter: "sudo nano /etc/ssh/sshd_config"
        - add "Port 2200" to line under "#Port 22" 
        - remove hashtag from "#Port 22"
        - change "PermitRootLogin prohibit-password" to "PermitRootLogin no"
        - change "PasswordAuthentication" from no to yes
        - add "AllowUsers grader" at the end of file
        - Save and exit using Control + X and Y
        "sudo service ssh restart"
    - Configure firewall
        - Enter the following:
            - sudo ufw status                  # The UFW should be inactive.
            - sudo ufw default deny incoming   # Deny any incoming traffic.
            - sudo ufw default allow outgoing  # Enable outgoing traffic.
            - sudo ufw allow 2200/tcp          # Allow incoming tcp packets on port 2200.
            - sudo ufw allow www               # Allow HTTP traffic in.
            - sudo ufw allow 123/udp           # Allow incoming udp packets on port 123.
            - sudo ufw enable   #enter 'y'
        - Exit ssh connection with "exit"

    - From local machine , 
        - "ssh -i ~/.ssh/LSDK_1.pem -p 2200 ubuntu@34.207.134.212"
- Add grader and give access
    - Enter to create a new account named grader, while logged in as ubuntu
        -"sudo adduser grader"  
        - enter password. I used "udacity" for grader, which worked for me
    - Give grader permission to sudo 
        - Enter "sudo visudo" on command line on the virtual machine 
        - on the line that looks like "root ALL=(ALL:ALL) ALL"
        - below said line, enter "grader ALL = (ALL:ALL) ALL"
        - save and exit using Control + X and confirm with y
- Create SSH keys for grader:
    - Enter "ssh-keygen" on local machine 
        - save keygen file. one my need to cd into "/.ssh/" folder
        - log into grader account with 
            -"ssh -v grader@34.207.134.212 -p 2200"
                - type password: "udacity"
    - In virtual environment run the following:
        - "su - grader"
        - "mkdir .ssh"
        - "touch .ssh/authorized_keys"
        - "nano .ssh/authorized_keys" <------ copy the SSH key from pub file derived from "ssh-keygen" into there
        - "sudo service ssh restart"
    - disable PermitRootLogin
        - "sudo nano /etc/ssh/sshd_config"  
            - find PermitRootLogin and change it to no
- Set up local time zone
    - "sudo dpkg-reconfigure tzdata" 
        - choose UTC
- install psycop2g
    - "sudo apt-get -qqy install postgresql python-psycopg2"
-Install psql
    -"sudo apt install postgresql-client-common"
- Install Apache application and wsgi module
    - "sudo apt-get install apache2"
        - Should install apache2
- Install mod-wsgi module
    - "sudo apt-get install python-setuptools libapache2-mod-wsgi" to install mod-wsgi module
-Start the server 
    - "sudo service apache2 start"


- Clone the project
    -Run "cd /var/www" 
    -"sudo mkdir catalog"
-sudo nano catalog.wsgi
    - #!/usr/bin/python
        import sys
        import logging
        logging.basicConfig(stream=sys.stderr)
        sys.path.insert(0,"/var/www/FlaskApp/")

        from FlaskApp import app as application
        application.secret_key = 'Add your secret key'

-Directory structure should look like this:
- |--------catalog
|----------------catalog
|-----------------------static
|-----------------------templates
|-----------------------venv
|-----------------------__init__.py
|----------------catalog.wsgi

- sudo service apache2 restart

-Change the owner to grader 
    - "sudo chown -R grader_5:grader_5 catalog"

- Give permision to clone the project
    - "sudo chmod catalog"

- Switch to the catalog directory and clone the Catalog project.
    - cd catalog and git clone https://github.com/cdrectenwald/FSND/catalog.git

- Add catalog.wsgi file.
    - "sudo nano catalog.wsgi"
    - add the following code:
                        #!/usr/bin/python2
                        import sys
                        import logging
                        logging.basicConfig(stream=sys.stderr)
                        sys.path.insert(0, "/var/www/catalog/")

                        from catalog import app as application
                        application.secret_key = 'secret'
                        Modify filenames to deploy on AWS.

                        Rename webserver.py to __init__.py

                        mv webserver.py __init__.py

- edit database_setup.py, categoryApp.py, itemes_log_fake.py, menus.py:
    - engine = create_engine('sqlite:///stock_catalog.db')
    - is now : engine = create_engine('postgresql://catalog:password@localhost/catalog)
- Install virtual environment and Flask framework
    - "sudo apt-get install python-pip"
- Install virtual environment
    - "sudo apt-get install python-virtualenv"

- create db schema
    - "sudo python database_setup.py"


-Make a new  environment with 
    -"sudo virtualenv venv"
    -  and activate it 
    -"source venv/bin/activate"

Change permissions to the virtual environment folder:
    -" sudo chmod -R 777 venv"

Install Flask 
    -"pip install Flask"
     -and dependencies:
        -"pip install bleach httplib2 request oauth2client sqlalchemy python-psycopg2."

- Configure Apache
        Create a config file:
         - "sudo nano /etc/apache2/sites-available/catalog.conf"

- Paste the following code

<VirtualHost *:80>
    ServerName Public-IP-Address
    ServerAdmin admin@Public-IP-Address
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


-Enable the new virtual host sudo a2ensite catalog

- Install and configure PostgressSQL
    - "sudo apt-get install PostgreSQL"
    - See if remote connections are allowed:
        - "sudo vim /etc/postgresql/9.3/main/pg_hba.conf"

- Login to postgress:
    -" sudo su - postgres"
- Open PostgreSQL:
    - "pqsl"
- create the "catalog" user with a password and let them create databases:
    - "postgres=# CREATE ROLE catalog WITH LOGIN PASSWORD 'catalog';
    - "postgres=# ALTER ROLE catalog CREATEDB;"
- Create a new user 
    -"CREATE USER catalog WITH PASSWORD 'password'"
- Create a DB called 'catalog' with:
    - "ALTER USER catalog CREATEDB and CREATE DATABASE catalog WITH OWNER catalog"
- Connect to the DB with \c catalog

- Revoke all rights:
    -" REVOKE ALL ON SCHEMA public FROM public"
- logout from psql and return to grader_5
    - "\q"
    - "exit"
- Restart aoacghe
    - "sudo service apache2 restart"
- check out http://18.232.162.201

## Deploy Project

Logout from postgress and return to the grader user \q and exit

Change the engine inside Flask application.

engine = create_engine('postgresql://catalog:password@localhost/catalog')

Set up the DB with python /var/www/catalog/database_setup.py

-Restart Apache
Run sudo service apache2 restart and check http://18.234.37.129


- Resources:
    - https://wiki.ubuntu.com/Security/Upgrades
    - https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04
    - https://askubuntu.com/questions/138423/how-do-i-change-my-timezone-to-utc-gmt/138442
    - https://blog.udacity.com/2015/03/step-by-step-guide-install-lamp-linux-apache-mysql-python-ubuntu.html
    - https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
    - https://help.ubuntu.com/lts/serverguide/automatic-updates.html
    - https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server