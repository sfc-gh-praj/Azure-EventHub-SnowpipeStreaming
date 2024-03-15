# Azure-EventHub-SnowpipeStreaming

This repo has the details about how to stream the data from Azure EventHub into Snowflake using Snowpipe streaming. We are using Kafka connect to fetch data from the EH and load into Snowflake tables.

We are using multiple threads to load data into Event Hubs and the below blog talks about the process of setting up the kafka connect and the parameters needed to ingest data from EH into Snowflake tables.

https://medium.com/snowflake/simplifying-real-time-data-ingestion-stream-azure-event-hubs-events-into-snowflake-with-snowpipe-62010d8f479a


To push data into EH you need to update the config properties of the EH like bootstrap.server and sasl.password. You find these details in the blog mentioned above. This code will push 100K messages and will display the duration and the througput numbers. You can even push more messages depending on the TU/PU of the EH that you are creating. 