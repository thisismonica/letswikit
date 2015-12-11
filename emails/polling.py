from receiveEmail3 import getEmail
import threading
import time

while True:
    try:
        # print "Polling email at: ",time.ctime(time.time())
        # thread.start_new_thread(getEmail, ())
        t = threading.Thread(target=getEmail())
        t.start()

    except Exception as e:
        print(e)
        print("Error: cannot call receiveEmail3")
    time.sleep(1)
