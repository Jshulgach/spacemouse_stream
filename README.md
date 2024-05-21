# spacemouse_stream
TCP streamer for [3Dconnexion Space Navigator](https://3dconnexion.com/) products in Python using raw HID. Installing the 3Dconnexion drivers is not necessary!

Utilizes the awesome [spacenavigator](https://pypi.org/project/spacenavigator/) package.

---
## Getting Started

Clone repository and navigate to the project directory:
```bash
git clone https://github.com/Jshulgach/spacemouse_stream.git
cd spacemouse_stream
```

Install the dependencies with `pip install -r requirements.txt`
```bash
pip install -r requirements.txt
```

Run the application, include the IP address and port number as arguments:
```bash
python main.py --host '127.0.0.1' --port 5003
```
If everything works, new data will be streamed in the form:
```bash
{"t": 225901.630109, "x": 0.0, "y": 0.0, "z": 0.0, "roll": 0.0, "pitch": 0.0, "yaw": 0.0, "buttons": [0, 0]}
```
