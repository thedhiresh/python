import random
import time
import threading
import logging

# Constants
FREQUENCY = 100  # Hz
CHANNELS = 10
SIGNAL_STRENGTH = 100  # dBm
JAMMING_SIGNAL_STRENGTH = 200  # dBm

# Logging
logging.basicConfig(level=logging.INFO)

# Network class
class Network:
    def __init__(self):
        self.channels = {}  # Use a dictionary to store channels
        self.signal_strength = SIGNAL_STRENGTH
        self.lock = threading.Lock()

    def add_channel(self, channel):
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = 0
                logging.info(f"Added channel {channel}")

    def remove_channel(self, channel):
        with self.lock:
            if channel in self.channels:
                del self.channels[channel]
                logging.info(f"Removed channel {channel}")

    def transmit(self, channel, data):
        with self.lock:
            if channel in self.channels:
                self.channels[channel] = data
                logging.info(f"Transmitted {data} on channel {channel}")
            else:
                logging.info(f"Channel {channel} does not exist")

    def receive(self, channel):
        with self.lock:
            if channel in self.channels:
                data = self.channels[channel]
                self.channels[channel] = 0
                logging.info(f"Received {data} on channel {channel}")
                return data
            else:
                logging.info(f"Channel {channel} does not exist")
                return None

# Jammer class
class Jammer:
    def __init__(self, network):
        self.network = network
        self.jamming_signal_strength = JAMMING_SIGNAL_STRENGTH

    def jam(self, channel):
        self.network.channels[channel] = self.jamming_signal_strength
        logging.info(f"Jamming channel {channel} with signal strength {self.jamming_signal_strength}")

    def continuous_jam(self):
        while True:
            for channel in self.network.channels:
                self.jam(channel)
                time.sleep(1 / FREQUENCY)

    def pulse_jam(self):
        while True:
            channel = random.choice(list(self.network.channels.keys()))
            self.jam(channel)
            time.sleep(1 / FREQUENCY)

# De-authentication jammer class
class DeAuthJammer(Jammer):
    def __init__(self, network):
        super().__init__(network)

    def de_auth(self, channel):
        self.network.channels[channel] = -1
        logging.info(f"De-authenticating channel {channel}")

    def de_auth_jam(self):
        while True:
            for channel in self.network.channels:
                self.de_auth(channel)
                time.sleep(1 / FREQUENCY)

# Main function
def main():
    network = Network()
    jammer = Jammer(network)
    de_auth_jammer = DeAuthJammer(network)

    # Add channels to the network
    for i in range(CHANNELS):
        network.add_channel(i)

    # Start continuous jamming
    jamming_thread = threading.Thread(target=jammer.continuous_jam)
    jamming_thread.start()

    # Start pulse jamming
    pulse_jamming_thread = threading.Thread(target=jammer.pulse_jam)
    pulse_jamming_thread.start()

    # Start de-authentication jamming
    de_auth_jamming_thread = threading.Thread(target=de_auth_jammer.de_auth_jam)
    de_auth_jamming_thread.start()

    # Simulate network transmission
    while True:
        channel = random.choice(list(network.channels.keys()))
        data = random.randint(0, 100)
        network.transmit(channel, data)
        time.sleep(1 / FREQUENCY)

if __name__ == "__main__":
    main()
