## DEND Capstone Project - New York City Airbnb Open Data
Capstone project for Udacity Data Engineering Nanodegree course

### Objective:
The objective of this project is to create a data model and ETL flow for New York City Airbnb Open Data which will load Calendar Data and Listnig details. The data comes from kaggle (https://www.kaggle.com/arthbr11/new-york-city-airbnb-open-data). The data spans across multiple years and have more than a million rows. For this project we have used Calendar Data and Listing Data.
The pupose of this data model is to provide the Airbnb user total number of listing, available listing, maximum price, minimum price, average price in a neighbourhood on a given date.
Also, it will provide the Airbnb user information about average rating, review count of the listings in any particular neighbourhood. and if that listing considered as Premium listing( to mark any listing as premium I have used some parameters from staging tables).

### Datasource Details:
The data is gathered from Kaggle. Following datasets are in scope of this project:
- calendar.csv (source: https://www.kaggle.com/arthbr11/new-york-city-airbnb-open-data)
- listing.csv (source: https://www.kaggle.com/arthbr11/new-york-city-airbnb-open-data)

Here are some snippets of the datasets:

Calendar.csv (Column names - listing_id, date, available, price, adjusted_price, minimum_nights, maximum_nights)

![calendar](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/calendar.png)

Listings.csv ( Column names - id, listing_url, scrape_id,last_scraped, name, description, neighborhood_overview, picture_url, host_id, host_url, host_name, host_since, host_location, host_about, host_response_time, host_response_rate, host_acceptance_rate, host_is_superhost, host_thumbnail_url, host_picture_url, host_neighbourhood, host_listings_count, host_total_listings_count, host_verifications, host_has_profile_pic, host_identity_verified, neighbourhood, neighbourhood_cleansed, neighbourhood_group_cleansed, latitude, longitude, property_type, room_type, accommodates, bathrooms, bathrooms_text, bedrooms, beds, amenities, price, minimum_nights, maximum_nights, minimum_minimum_nights, maximum_minimum_nights, minimum_maximum_nights, maximum_maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, calendar_updated, has_availability, availability_30, availability_60, availability_90, availability_365, calendar_last_scraped, number_of_reviews, number_of_reviews_ltm, number_of_reviews_l30d, first_review, last_review, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value, license, instant_bookable, calculated_host_listings_count, calculated_host_listings_count_entire_homes, calculated_host_listings_count_private_rooms, calculated_host_listings_count_shared_rooms, reviews_per_month )

![listings](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/listings.png)

### Project Scope:
The scope of this project is to create a data pipeline which will accept the source files, process and clean them, transform as per the the need of the final data model and load them in dimension and fact tables. We are going to read the source files from local storage, use airflow and python to create a data pipeline, and eventually load the processed and transformed data into the data model created in local postgresql database.

### Technology used:
- Apache Airflow -Allows for easy execution of ETL
- Python
- Amazon Redshift cluster - Data storage

### Data Model
The final data model consists of 6 dimension and 2 fact tables. Following are the names of the tables:
- Dimension table:
       - dim_listing
       - dim_host
       - dim_district
       - dim_neighbourhood
       - dim_property
       - dim_date
- Fact table :
       - f_neighbourhood_listing
       - f_listing

![data_model](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/data%20model.png)

### Data Dictionary for the final Data Model

Table name -DIM_LISTING	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|listing_id |	integer	|Listing id. Primary key|
|Date	|date	|Date. Primary key|
|available	|char(1)	|Availibility of the listing for that given date. Expected values - 't' as true and 'f' as false|
|price |	numeric(18,2)	|Price of the listing on that given date|
|host_id	|integer	|Host id for that listing|

Table name -DIM_PROPERTY	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|listing_id	|integer	|Listing id. Primary key|
|host_id	|integer	|Host id for that listing. Primary key|
|property_type	|varchar(2000)	|Type of the property. Values are like -Entire apartment, Entire house, Private room in apartment etc.|
|room_type	|varchar(256)	|Type of rooms. Values are like - Private room, hotel room, shared room etc.|
|accomodates	|integer	|Number of people could stay in that property|
|bathrooms	|varchar(256)	|Number of bathrooms in that property. values are like-1 bath, 1 shared bath etc.|
|bedrooms	|integer	|number of beed rooms in that property|
|beds	|integer	|number of beds in that property|
|amenities	|varchar(2000)	|List of amenities for that property, like- air conditioning, microwave,hair dryer etc.|
|latitude	|numeric(18,2)	|Latitude of the property|
|longitude	|numeric(18,2)	|Longitude of the property|
|premium_flag	|varchar(1)	|If the property is premium or not. expected values  'Y' as yes and 'N' as no. To get the information I have used few parameters like -<br>         host_has_profile_pic = t,<br>host_identity_verified = t,<br>room_type  = Entire Home/apt,<br>superhost = t,<br> review_scores_rating > 4.5,<br> review_scores_accuracy	>4.5,<br>    review_scores_cleanliness > 4.5,<br> review_scores_communication > 4.5,<br> review_scores_location > 4.5,<br> review_scores_value > 4.5 |

Table name -DIM_HOST	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|host_id	|integer	|Host id. Primary key|
|host_name	|varchar(256)	|Host name|
|host_is_superhost	|varchar(1)	|Indicator for superhost. Expected values - 't' as true and 'f' as false|
|host_url	|varchar(5000)	|URL for host information|
|host_since	|date	|host since |
|host_loaction	|varchar(1000)	|location of the host|

Table name -DIM_DATE	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|id_date	|integer	|id of the date. Primary key|
|date_actual	|date	|actual date|
|day_name	|text	|name of the day|
|day_of_week	|integer	|day of week|
|day_of_month	|integer	|day of month|
|current_date_flag	|integer	|flag for current date|
|week_of_month	|integer	|Week of month|
|week_of_year	|integer	|week of year|
|month_number	|integer	|month number|
|month _name	|text	|month name|
|quarter_actual	|integer	|quarter|
|year_actual	|integer	|year|
|weekend_indicator	|text	|indicator for weekend|

Table name -DIM_DISTRICT	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|district_id	|integer	|District id. Primary Key|
|district	|varchar(256)	|District Name|

Table name -DIM_NEIGHBOURHOOD	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|neighbourhood_id	|integer	|Neighbourhood id. Primary key|
|district_id	|integer	|District id|
|neighbourhood	|varchar(256)|	Neighbourhood name|

Table name -F_LISTING	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|listing_id |	integer |	Listing id. FK to dim_listing table|
|neighbourhood_id |	Integer| Auto generated Neighbourhood Id. FK to dim_neighbourhood table|
|avg_rating	|numeric(18,2)	|Average rating for that listing id|
|review_count	|integer	|Total number of reviews for that listing id|
|Premium flag	|varchar(1)	|This flag is to identify the listing as premium listing. (expected values - 'Y' as yes and 'N' as no)|

Table name -F_NEIGHBOURHOOD_LISTING	
|Field Name    | Data Type | Description                     |
|--------------|-----------|---------------------------------|
|Id_date	|integer	|Id for the actual date. FK to the date dimension table|
|neighbourhood	|varchar (1000)	|Neighbourhood name|
|neighbourhood_id	|Integer|	Auto generated Neighbourhood Id. FK to dim_neighbourhood table|
|total_listing	|integer|	Total number of listngs for any neighbourhood on a given date|
|available_listing	|integer|	Total number of listing where available flag = 't'  for any neighbourhood on a given date|
|min_price	|numeric(18,2)|	Minimum price of the listings for any neighbourhood on a given date|
|max_price	|numeric(18,2)|	Maximum price of the listings for any neighbourhood on a given date|
|avg_price	|numeric(18,2)|	Average price of the listings for any neighbourhood on a given date|

### Data Pipeline Design
The data pipeline was designed using Apache Airflow. The whole process was segregated in several phases:
- Creating the staging,dimension and fact tables
- Loading the staging tables
- Loading the dimension tables
- Loading the fact tables
- Performing data quality checks

Following is the airflow dag for the whole process: 

![dag](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/dag.png)

### Process Result
From the resultset of fact table f_neighbourhood_list, user can get the information that on 3rd July,2021 at Caroll Gardens Neighbourhood, there are 180 Airbnb listings. But only 26 are available. The minimum price, maximum price and average price of the listings are as follows - $39, $1333 and $191.

![f_neighbourhood_listing](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/f_neighbourhood_list.PNG)

From the resultset of fact table f_listing, user can get information about listings in neighbourhood_id 107 (lower east side), with total number of review, average rating and if the listing is a premium listing or not. For example, 46251446 listing id has average rating 4.82 and total 34 reviews are there but the listing is not a premium listing.

![fact_listing](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/f_listing.PNG)

### Addressing Other Scenarios

#### The data was increased by 100x.

If the data increased by 100x in size I would continue using Redshift and Airflow but I would increase the number of nodes on my Redshift cluster. However, if my model had more writing involved I would use Apache Spark for distributed computing.

#### The pipelines would be run on a daily basis by 7 am every day.

This can be handled using the existing Airflow DAG using the scheduling feature of Airflow. I would not have dropped the tables before creating and would not have cleared when reloading the data in order to make it go faster.

#### The database needed to be accessed by 100+ people.

I dont see any issue with 100+ people using the Redshift endpoint so this system could handle that. Amazon redshift has clustering abilities and AWS is highly scalable.
