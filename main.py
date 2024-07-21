from AirplaneCatcher import AirplaneCatcher
from threading import Thread


o = AirplaneCatcher()
# o.run(True)
flight_list = {}

thread1 = Thread(target=o.run, args=[1])

thread1.start()
thread1.join()

print(o.flight_over_head)
print("Koniec programu")
