#!/usr/bin/env python3
import psycopg2
DB_name = "news"


def connectToDB():
    # Goal is to create a function that connects to a database
    db = psycopg2.connect('dbname=' + DB_name)
    c = db.cursor()
    return db, c

    if (sycopg2.DataBaseError):
        print("There's an error with the database connection")
        
        
def getArticle():
    # goal is to get top 3 viewed articles
    db, c = connectToDB()
    query1 = "select title, author, count(*) as views from articles,"
    query2 = " log where log.path like concat('%', articles.slug) "
    query3 = "GROUP BY articles.title, articles.author order by views desc; "
    query = query1 + query2 + query3
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print the top three articles
    print("The top three most viewed articles: ")
    for title, views in result:
        print('"{}" --{} views'.format(title, views))
    
    
def getAuthors():
    # 2. Who are the most popular article authors of all time?  
    db, c = connectToDB()
    query1 = "select authors.name,sum(article_view.views) "
    query2 = "as views from article_view,authors where authors.id "
    query3 = " = article_view.author group by authors.name order by views desc"
    query = query1 + query2 + query3
    c.execute(query)
    result = c.fetchall()
    db.commit()
    db.close()

    # print authors of most popular articles
    print("\nMost viewed authors:")
    for author, views in result:
        print('"{}" --- {} views'.format(author, views))


def getErrorRequestThreshold():
        # Return when there's more than 1 percent error requests
        # Select which days had errors
        db, c = connectToDB()
        query = """SELECT to_char(date, 'FMMonth DD, YYYY'),
         per_failed_calls
        FROM percent_failed_calls
        WHERE per_failed_calls > 1.0"""
        c.execute(query)
        result = c.fetchall()
        db.commit()
        db.close()

    # print days with more than 1 percent error request rate
        print("\nDays where more than 1 percent f requests lead to errors:")
        for date, percent_error in result:
            print ('"{}" --- {} percent error'.format(date, percent_error))

if __name__ == "__main__":
    getArticle()
    getAuthors()
    getErrorRequestThreshold()
    