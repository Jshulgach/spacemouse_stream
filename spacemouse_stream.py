import socket
import json
import spacenavigator as spnav
import asyncio


class SpacemouseStream:
    # Class for collecting data from a spacemouse connected to the PC, converts the data into a json string, and streams
    # it to a server on the specified ip and port.
    def __init__(self, host='localhost', port=5003, rate=10, verbose=True):
        # Initialize the SpacemouseStream object
        self.host = host
        self.port = port
        self.rate = rate
        self.verbose = verbose
        self.socket = None
        self.all_stop = False
        self.t_prev = 0
        self.spacemouse_state = {'t': 0, 'x': 0, 'y': 0, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0, 'buttons': []}

        # Wait for connection to the server
        self.connect(self.host, self.port)

        # Initialize and configure the spacemouse
        print("Searching for Spacemouse devices...")
        self.dev = spnav.open(self.spacemouse_callback)

        print("SpacemouseStream initialized.")

    def connect(self, host, port):
        """ Connect to the server at the specified host and port """
        print("Attempting to connect to server at {}:{}".format(host, port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print('Connected to server at {}:{}'.format(self.host, self.port))

    def spacemouse_callback(self, event):
        # Gets called when there's new data from the spacemouse linear/angular components
        self.spacemouse_state['t'] = event.t
        self.spacemouse_state['x'] = event.x
        self.spacemouse_state['y'] = event.y
        self.spacemouse_state['z'] = event.z
        self.spacemouse_state['roll'] = event.roll
        self.spacemouse_state['pitch'] = event.pitch
        self.spacemouse_state['yaw'] = event.yaw
        self.spacemouse_state['buttons'] = event.buttons

    def start(self):
        """ Makes a call to the asyncronous library to run a main routine """
        asyncio.run(self.main())  # Need to pass the async function into the run method to start

    def stop(self):
        """ Sets a flag to stop running all tasks """
        self.all_stop = True

        # Close the connection to the server
        self.socket.close()
        if self.verbose:
            print('Connection closed')

    async def main(self):
        """ Start main tasks and coroutines in a single main function """
        asyncio.create_task(self.update(self.rate))

        while self.all_stop != True:
            await asyncio.sleep(0)  # Calling #async with sleep for 0 seconds allows coroutines to run

    async def update(self, interval=1):
        """ Asyncronous co-routing that updates the controller. Messages in the queue will be 'dequeued'
            depending on the command type.
        """
        while self.all_stop != True:

            # Make sure we only send data when new data is available
            if self.t_prev == self.spacemouse_state['t']:
                continue

            # Convert the data to a json string
            data_str = json.dumps(self.spacemouse_state)

            # Send the data to the server
            self.socket.send(data_str.encode())
            if self.verbose:
                print('Sent data:', data_str)

            # Update the previous time
            self.t_prev = self.spacemouse_state['t']

            await asyncio.sleep(1 / interval)
            # Uncomment below to handle this as fast as possible (comment above line first)
            # await asyncio.sleep(0)

        print("Updating stopped")

