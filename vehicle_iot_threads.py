from confluent_kafka import Producer
import threading
import time
import json
import random

"""
This program simulates the production of vehicle telemetry data and sends it to an Event Hub.

You can adjust the following variables to ingest more data:

    - num_threads: Number of threads to run concurrently for message production.
    - num_messages_per_thread: Number of messages each thread will produce.

The name of the Event Hub is assigned to the variable 'topic', which represents the Kafka topic to send messages to.



"""


# Define Kafka producer configuration
config = {
    'bootstrap.servers': 'vehicletoll.servicebus.windows.net:9093',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '$ConnectionString',
    'ssl.ca.location': 'cacert.pem',  
    'sasl.password': 'Endpoint=sb://vehicletoll.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=lc91264Asw=',
    'client.id': 'python-example-producer_localmachine',
   
}

# Define the message to be sent
message = "This is a test message."
vehicle_ids=['v1','v2','v3','v4','v5','v6']

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


# Define the function that each thread will run
def produce_to_kafka(topic, num_messages):
    producer = Producer(config)
    for i in range(num_messages):
        rotations_per_min = random.randint(500, 800)
        speed = random.randint(40, 100)
        total_kms = random.randint(1000, 100000)
        tyre_pressure = random.randint(28, 32)
        maintenance_required = random.choice([True, False])

        if total_kms >= 50000:
            low_fuel_indicator = random.choice([True, False])
        elif total_kms >= 40000:
            low_fuel_indicator = random.random() <= 0.8
        elif total_kms >= 30000:
            low_fuel_indicator = random.random() <= 0.6
        else:
            low_fuel_indicator = random.random() <= 0.4

        event_timestamp = int(time.time())
        data = {
            "vehicle": random.choice(vehicle_ids),
            "eventtimestamp": int(time.time()),
            "rotations_per_mins": rotations_per_min,
            "low_fuel_indicator": low_fuel_indicator,
            "speed": speed,
            "total_kms": total_kms,
            "tyre_pressure": tyre_pressure,
            "maintenance_required": maintenance_required,
        }
        msg= json.dumps(data).encode("utf-8")
        producer.produce(topic, msg)
        # print(msg)
        # producer.poll(0)
    producer.flush()

# Define the number of threads and messages per thread
num_threads =10
num_messages_per_thread = 1000


# Define the topic to send messages to
topic = 'vehicle_iot_data'

# Start the timer
start_time = time.time()

# Create a list of threads and start them
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=produce_to_kafka, args=(topic, num_messages_per_thread))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()


# Calculate the total time taken
end_time = time.time()
total_time = end_time - start_time

# Calculate and print the throughput
total_messages = num_threads * num_messages_per_thread
throughput = total_messages / total_time
print("Total time taken: {:.2f} seconds".format(total_time))
print("Total messages sent: {}".format(total_messages))
print("Throughput: {:.2f} messages/second with {} threads".format(throughput,num_threads))
