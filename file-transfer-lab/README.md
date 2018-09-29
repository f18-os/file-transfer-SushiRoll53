## File Transfer Lab

This lab implements:
* put (file name)

The Server then checks if it is a valid file name and starts to receive the data by 100 bytes.
It also works with and without the proxy, but with the proxy goes slower.

The server also handles multiple clients.
If a client tries to upload a file that it is already in the server, the server will sent the client a hint, so both stop, and prints
that the file is already there.

PD: I also include the lab for the parser in file-transfer-SushiRoll53/simple-echo/
