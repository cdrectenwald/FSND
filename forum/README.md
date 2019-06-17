# Log Analysis

## Description
Log Analysis project for the Udacity Full Stack Nanodegree. The project consists of answering three questions given a database and data.

The data is for a fictional news website. The database is a PostgreSQL database and the schema contains three tables: authors, articles, and log.

## Prerequisites
- Python 2
- PostgreSQL
- psycopg2
- [Vagrant](https://www.vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Installing
To create an environment to run the project, install Vagrant and Virtual Box.

Start the Virtual Machine(VM) by running `vagrant up` in the directory that contains the "Vagrantfile" and then SSH into the VM using `vagrant ssh`. The first time `vagrant up` is run the VM will be configured based on information in the "Vagrantfile". Navigate to `/vagrant` to access the files shared between the VM and your computer.

Create the database schema and load the data by running `psql -d news -f newsdata.sql`. 

Note: When done with the VM, type exit and then `vagrant suspend` to pause the VM and maintain the state of the VM.

## Running the Program
To run the program, first create the views by running `psql -d news -f create_views.sql`. For completeness, below are the VIEW statements.

- Create View of Popular Articles
```
CREATE OR REPLACE VIEW favorite_articles as \
    SELECT distinct(count(log.path)) as page_views, log.path \
    FROM log \
    WHERE log.status = '200 OK' \
    and log.path like '/article/%' \
    GROUP BY log.path \
    ORDER BY page_views desc
```

- Create a view of the percentage of failed calls per day.
```
 create view error_log_view as select date(time),round(100.0*sum(case log.status when '200 OK' 
  then 0 else 1 end)/count(log.status),2) as "Percent Error" from log group by date(time) 
  order by "Percent Error" desc;
```


Then execute the program as `python log_analysis.py`. The output is written to the Terminal.

## Example Output

Top three most viewed articles:
"Candidate is jerk, alleges rival" --- 338647
"Bears love berries, alleges bear" --- 253801
"Bad things gone, say good people" --- 170098

Most viewed authors:
"Ursula La Multa" --- 507594 views
"Rudolf von Treppenwitz" --- 423457 views
"Anonymous Contributor" --- 170098 views
"Markoff Chaney" --- 84557 views

Days where more than 1 percent f requests lead to errors:
"July 17, 2016" --- 2.3 percent error
```