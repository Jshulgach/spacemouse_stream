"""
Description: A script that sends the state of a connected Spacemouse device to a server as a JSON string The script will
     run until the user presses Ctrl+C. Only tested in Windows.

Author: Jonathan Shulgach (jonathan@shulgah.com)
Created: 05/21/2024

"""

import argparse
from spacemouse_stream import SpacemouseStream

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Stream SpaceMouse data to a server.')
    parser.add_argument('--host', type=str, default='localhost', help='Server host.')
    parser.add_argument('--port', type=int, default=5003, help='Server port.')
    parser.add_argument('--verbose', action='store_true', help='Print verbose output.')
    args = parser.parse_args()

    # Create a SpaceMouseStream object
    stream = SpacemouseStream(args.host, args.port)
    try:
        stream.start()
    except KeyboardInterrupt:
        stream.stop()
