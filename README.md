## DEND Capstone Project - New York City Airbnb Open Data
Capstone project for Udacity Data Engineering Nanodegree course

### Objective:
The objective of this project is to create a data model and ETL flow for New York City Airbnb Open Data which will load Calendar Data and Listnig details. The data comes from kaggle (https://www.kaggle.com/arthbr11/new-york-city-airbnb-open-data). The data spans across multiple years and have more than a million rows. For this project we have used Calendar Data and Listing Data.

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
- Apache Airflow
- Python
- PostgreSQL

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

### Data Pipeline Design
The data pipeline was designed using Apache Airflow. The whole process was segregated in several phases:
- Creating the staging,dimension and fact tables
- Loading the staging tables
- Loading the dimension tables
- Loading the fact tables
- Performing data quality checks

Following is the airflow dag for the whole process: 

![dag](https://github.com/piyalisarkar1209/udacity-DEND-Capstone/blob/main/dag.png)

### Addressing Other Scenarios

#### The data was increased by 100x.

If the data increased by 100x in size I would continue using Redshift and Airflow but I would increase the number of nodes on my Redshift cluster. However, if my model had more writing involved I would use Apache Spark for distributed computing.

#### The pipelines would be run on a daily basis by 7 am every day.

This can be handled using the existing Airflow DAG using the scheduling feature of Airflow. I would not have dropped the tables before creating and would not have cleared when reloading the data in order to make it go faster.

#### The database needed to be accessed by 100+ people.

I dont see any issue with 100+ people using the Redshift endpoint so this system could handle that. Amazon redshift has clustering abilities and AWS is highly scalable.
