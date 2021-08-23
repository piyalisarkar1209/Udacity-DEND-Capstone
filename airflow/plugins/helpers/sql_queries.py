class SqlQueries:
    dim_listing_table_insert = ("""
        SELECT distinct
        c.listing_id::INTEGER,
        c.date::DATE, 
        c.available::CHAR(1),
        case when LENGTH(c.price) = 0 then NULL else replace(replace(c.price,'$',''),',','')::numeric end as price,
        l.host_id::INTEGER
        FROM staging_calendar c
        JOIN staging_listing l
        ON c.listing_id::INTEGER = l.id::INTEGER
        where c.price <> 0
    """)
    
    dim_host_table_insert = ("""
        SELECT distinct
        host_id::INTEGER,
        host_name,
        host_is_superhost,
        host_url,
        to_date(host_since, 'YYYYMMDD') ::DATE as host_since,
        host_location
        from staging_listing
    """)
    
    dim_district_table_insert = ("""
        (district) SELECT distinct neighbourhood_group_cleansed as district
        FROM staging_listing 
    """)
    
    dim_neighbourhood_table_insert = ("""
        (district_id, neighbourhood) SELECT distinct d.district_id , l.neighbourhood_cleansed as neighbourhood
         from dim_district d
         left join staging_listing l
         on d.district = l.neighbourhood_group_cleansed
     """)
    
    dim_property_table_insert = ("""
        SELECT id :: INTEGER as listing_id ,
        host_id :: INTEGER,
        property_type,
        room_type,
        accommodates:: INTEGER,
        bathrooms,
        bedrooms :: INTEGER,
        beds :: INTEGER,
        amenities,
        latitude :: numeric(18,0),
        longitude :: numeric(18,0),
        case when
            host_has_profile_pic = 't' AND
            host_identity_verified = 't' AND
            lower(room_type) = 'entire home/apt' AND
            host_is_superhost = 't' AND
            review_scores_rating >= 4.5 AND
            review_scores_accuracy >= 4.5 AND
            review_scores_cleanliness >= 4.5 AND
            review_scores_communication >= 4.5 AND
            review_scores_location >= 4.5 AND
            review_scores_value >= 4.5 then 'Y'
            else 'N' end as premium_flag
        from staging_listing
    """)
   
    dim_date_table_insert = ("""
        with DQ as(
            with digit as (
                select 0 as d union all 
                select 1 union all select 2 union all select 3 union all
                select 4 union all select 5 union all select 6 union all
                select 7 union all select 8 union all select 9        
            ),
            seq as (
                select a.d + (10 * b.d) + (100 * c.d) + (1000 * d.d) as num
                from digit a
                    cross join
                    digit b
                    cross join
                    digit c
                    cross join
                    digit d
                order by 1        
            )
            select (getdate()::date - seq.num)::date as "datum"
            from seq
            union
            select (getdate()::date+1 + seq.num)::date
            from seq
            )
            select distinct 
            TO_CHAR(datum,'yyyymmdd')::INT AS id_date,
            datum AS date_actual,
            TO_CHAR(datum,'Day') AS day_name,
            CAST(DATE_PART(dow ,datum) AS INT) AS day_of_week,
            CAST(DATE_PART(DAY ,datum) AS INT) AS day_of_month,
            CASE WHEN DQ.datum = CURRENT_DATE THEN 1 ELSE 0 END AS current_date_flag,        
            TO_CHAR(datum,'W')::INT AS week_of_month,
            CAST(DATE_PART(week ,datum) AS INTEGER) AS week_of_year,
            CAST(DATE_PART(MONTH ,datum) AS INTEGER) AS month_number,
            TO_CHAR(datum,'Month') AS month_name,
            CAST(DATE_PART(quarter ,datum) AS INTEGER) AS quarter_actual,
            CAST(DATE_PART(year ,datum) AS INTEGER) AS year_actual,
            CASE
                WHEN DATE_PART(dow ,datum) IN (6,0) THEN 'Y'
                ELSE 'N'
            END AS weekend_ind 
            from DQ
    """)  
    
    f_neighbourhood_listing_insert = ("""
            with stg_cal as (select listing_id,date,available,replace(replace(price,'$',''),',','')::numeric price 
            from staging_calendar
            where replace(replace(price,'$',''),',','')::numeric != 0)
                select d.id_date, l.neighbourhood_cleansed, n.neighbourhood_id,
                count(distinct c.listing_id) total_listing,
                count(distinct case when lower(c.available) = 't' then c.listing_id end) available_listing,
                min(c.price) min_price,
                max(c.price) max_price,
                avg(c.price) avg_price
                from stg_cal c 
                left join dim_date d 
                on c.date = d.date_actual
                left join staging_listing l 
                on c.listing_id = l.id
                left join dim_neighbourhood n
                on l.neighbourhood_cleansed = n.neighbourhood
                group by d.id_date, l.neighbourhood_cleansed, n.neighbourhood_id
                order by d.id_date, l.neighbourhood_cleansed, n.neighbourhood_id
    """)
    
    f_listing_insert = ("""
        select l.id::INTEGER,
        n.neighbourhood_id::INTEGER ,
        l.review_scores_rating::NUMERIC(18,2),
        l.number_of_reviews::INTEGER,
        p.premium_flag
        from staging_listing l
        left join dim_property p
        on l.id = p.listing_id
        left join dim_neighbourhood n
        on l.neighbourhood_cleansed = n.neighbourhood
    """)
 