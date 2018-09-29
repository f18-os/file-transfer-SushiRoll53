To make this lab I look at this videos for references:
* https://www.youtube.com/watch?v=1VaBy6ZSIUM
* https://www.youtube.com/watch?v=HrDyqtyT2yk

They helped me to structured a little better and to understand the flow between server and client.
I also discussed and develop some ideas with Stephanie Loya of how to read only 100 bytes at a time and pass only 100 bytes at the time.

One comment, we noticed that when a file reader reads in byte (rb) and it reads a new line (\n) it gets stuck for some reason if it is capped to 100 bytes.
