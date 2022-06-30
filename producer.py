import time
import os
from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.exceptions import EventHubError
#import faker
from datafaker import LoginData
import json

CONNECTION_STR = os.environ['EVENT_HUB_CONN_STR']
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

print ("***conection string is ***" + CONNECTION_STR + "\n")

print ("***event hub name is ***" + EVENTHUB_NAME)

print ("____________________________________________")

def datagen(size):
    output = list()
    for i in range(0, size):
        logindata = LoginData()
        output.append(logindata.get_json())
    return output

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

def send_event_data_batch(producer,dataList):
    print ("Send single message...")
    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    event_data_batch = producer.create_batch()
    
    for record in dataList:
        print (record)
        event_data_batch.add(EventData( json.dumps(record) )  )
    producer.send_batch(event_data_batch)

def send_event_data_batch_with_limited_size(producer,data):
    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    event_data_batch_with_limited_size = producer.create_batch(max_size_in_bytes=1000)

    while True:
        try:
            event_data_batch_with_limited_size.add(EventData('Message inside EventBatchData'))
        except ValueError:
            # EventDataBatch object reaches max_size.
            # New EventDataBatch object can be created here to send more data.
            break

    producer.send_batch(event_data_batch_with_limited_size)


start_time = time.time()
with producer:
    
    for i in range (1000):
        dataList = datagen(100)
        send_event_data_batch(producer,dataList)
    print ("Done ....")
    #send_event_data_batch_with_limited_size(producer)
    #send_event_data_batch_with_partition_key(producer)
    #send_event_data_batch_with_partition_id(producer)
    #send_event_data_batch_with_properties(producer)
    #send_event_data_list(producer)

print("Send messages in {} seconds.".format(time.time() - start_time))
