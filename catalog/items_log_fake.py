#!/usr/bin/env python 2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryStock, User

engine = create_engine('sqlite:///stock_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Chris Rectenwald", email="cdrectemwald@gmail.com")
session.add(User1)
session.commit()

# Items for FinTech stocks 
category1 = Category(name="FinTech Stocks", user_id=User1.id)

session.add(category1)
session.commit()


# Item for FinTech Stocks
item1 = Item(name="JPMorgan Chase",
             description="""
            Jamie Dimon's Kingdom 
             """,
             category_id=category1.id,
             user_id=User1.id)
session.add(item1)
session.commit()

item2 = Item(name="Square",
             description="""Square is a commerce ecosystem. it enables its sellers to start, run, and grow their own busines. Cobination of software and hardware to enable sellers
             turn mobile devices and computing devices into payments and point-of-sale solutions.""",
             category_id=category1.id,
             user_id=User1.id)
session.add(item2)
session.commit()

item3 = Item(name="Q2 Holdings ",
             description="""A Digital Banking platform. It provides cloud-based digital banking solutions to regional and community financial institutions in the United States. """,
             category_id=category1.id,
             user_id=User1.id)
session.add(item3)
session.commit()

item4 = Item(name="PayPal",
             description="""
             Elon Musk and Peter Theil. Owns Venmo.
               """,
             category_id=category1.id,
             user_id=User1.id)
session.add(item4)
session.commit()

# Items for BioPharmaceuticals
category2 = Category(name="Biotech Stocks", user_id=User1.id)

session.add(category2)
session.commit()


item5 = Item(name="Alexion Pharmaceuticals, Inc",
             description="""
            Focuses on serving patients with devastating and ultra-rare disorders through the development and commercialization of life-transforming 
            thereapeutic products.
             """,
             category_id=category2.id,
             user_id=User1.id)
session.add(item5)
session.commit()

# Items for Commodities
category3 = Category(name="Commodities", user_id=User1.id)

session.add(category3)
session.commit()


item6 = Item(name="AT&T",
             description="""
             The telecom company disguised as a media one.
             """,
             category_id=category3.id,
             user_id=User1.id)
session.add(item6)
session.commit()

item7 = Item(name="Uber",
             description="""
            Something something cannibalization
             """,
             category_id=category3.id,
             user_id=User1.id)
session.add(item7)
session.commit()

# Items for 'Deep Value Companies'
category4 = Category(name="Long term investments", user_id=1)

session.add(category4)
session.commit()


item8 = Item(name="GE",
             description="""
             When you beat an arbitrary number for 10+ years at the expense for longer term planning. 
             """,
             category_id=category4.id,
             user_id=User1.id)
session.add(item8)
session.commit()

# Items for AnonAnalytics Fund 
category5 = Category(name="AnonAnalytics Fund", user_id=User1.id)

session.add(category5)
session.commit()


item9 = Item(name="CRM",
             description="""
               The most robust company that's ever lived
                """,
             category_id=category5.id,
             user_id=User1.id)
session.add(item9)
session.commit()


item10 = Item(name="Bitcoin ",
             description="""
               Fiat has failed us.
                """,
             category_id=category5.id,
             user_id=User1.id)
session.add(item10)
session.commit()

item10 = Item(name="Tesla",
             description="""
               Actually a battery company
                """,
             category_id=category5.id,
             user_id=User1.id)
session.add(item10)
session.commit()



print "added items" 