import random
import datetime
events = [random.random() for _ in range(100000)]

events.append({"type":"atk"})
events.append({"type":"heal"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
events.append({"type":"atk"})
print(datetime.datetime.now())
first=events.pop(0)
print(first)
print(datetime.datetime.now())

from collections import deque
q = deque()
q.append({"type":"atk"})
q.append({"type":"heal"})
first = q.popleft()
s = deque(maxlen=3)
s.append("a");s.append("b")
s.append("c");s.append("d")
print(s)