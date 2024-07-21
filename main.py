from threading import Thread
from time import sleep
from AirplaneCatcher import AirplaneCatcher
from RunwayGuesser import get_runway_number

WAIT_WRONG_RUNWAY = 1  # default to 60 seconds not to flood FR24 API


o = AirplaneCatcher()
thread1 = Thread(target=o.run, args=[1])

# This should be a while True loop so that the program executes continuously on RasPI
for i in range(4):
    runway_number = get_runway_number()
    if runway_number == 25:
        # If the runway number has approach over my head, check if we have any planes above
        thread1.start()
        thread1.join()
        print(o.flight_over_head)
    else:
        # If it is the opposite runway, keep checking the wind direction
        sleep(WAIT_WRONG_RUNWAY)
print("Koniec programu")
