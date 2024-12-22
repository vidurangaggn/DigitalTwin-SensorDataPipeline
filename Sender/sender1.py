import publisher
from pika.exchange_type import ExchangeType

message_sender = publisher.getMessageSender()

#Declare an exchnage
exchange_name = "pubsub1"
message_sender.declare_exchange(exchange_name= exchange_name, exchange_type=ExchangeType.fanout)

message = "Hello, This is producer 1 broadcasting a message to all the consumers"

message_sender.send_message(exchange=exchange_name, routing_key="", body=message)
message_sender.send_message(exchange=exchange_name, routing_key="", body=message)
message_sender.send_message(exchange=exchange_name, routing_key="", body=message)

message_sender.close()