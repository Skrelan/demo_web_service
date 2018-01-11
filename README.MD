# Shuffle
Web application built using rewardStyle API

The Goal of this application is to :
  1. download list of products listed by the Vendors
  2. allow one to search over downloaded products using filters
  3. **BONUS FEATURE**: A Tinder like full-stack app to allow Influencers to browse through items in local DB

## Contents
1. [Software Stack](software-stack)
2. [Endpoints](endpoints)
3. [Notes](notes)
----
## Software Stack
1. **Back-end** :  Python, web.py Framework
2. **Front-end**: Javascript, HTML, CSS
3. **Database** : Postgres DB
-----
## Endpoints
* Vendor :
  * description : adds a new vendor
  * endpoint : `/addVendor`
  * request type : `POST`
  * parameters :


* Item Search :
  * description : Searches for Items based on filters passed
  * endpoint :`/search`
  * request type : `GET`
  * parameters :


* Products:
  * description :
  * endpoint :`/products`
  * request type : `POST`
  * parameters : something

  <br>
  * description :
  * endpoint :`/products`
  * request type : `GET`
  * parameters :  something



* Landing Page :
  * description : Renders landing page
  * endpoint : `/`
  * request type : `GET`
  * parameters :

-----
## Notes
1. Please note the configs file are not included in this repo and it contains the tokens, db_configs, rewardStyle APIs etc.

2. To run this you will require the web.py Framework. [Read more here](https://medium.com/@Skrelan/setting-up-your-first-web-application-c92aa28d0f03)