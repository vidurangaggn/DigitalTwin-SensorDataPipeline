from basicClient import BasicPikaClient
import cred

def getMessageSender():
    return BasicMessageSender(
        f"{cred.broker_id}",
        f"{cred.user_name}",
        f"{cred.password}",
        f"{cred.region}"
    )

class BasicMessageSender(BasicPikaClient):

    def declare_exchange(self, exchange_name, exchange_type):
        print(f"Trying to declare exchange({exchange_name})...")
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        
    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)
        print(f"Sent message: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()
    