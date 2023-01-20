# ride_hailing_project

This project developed with the python, we used redis and postgres to store data on disk and memory and kafka as 
message broker.


This project contain 4 service:
1. Request threshold coefficient rest service :
   
        This part contains simple crud(add/update/retrieve/delete)
        You can manage  price coefficient and request threshold
2. Price coefficient service
        
        In this part you send latitude and longitude to get  price coefficient for this region.
        It will find region with geopy library and just accept region of tehran.
        Then get price coefficient for this region and also produce this region in kafka.
3. Region request service

        In part number 2 we produce region in kafka . The main reason of this approach is if we have many request in current time 
        it has load to save each request in database in current time so we send request to kafka and consume that in this part.
        Then save this request in database
4. Region price coefficient calculator service

        Beacause of rate of request and load we don't want calcuate count of request for region in time.
        So we have process that will trigger in every 10 second and calculate price coefficient for all region base on 
        count of request for that region(all request  in the last 10 minutes.)
    

Run project:
    
        docker-compose up -d

