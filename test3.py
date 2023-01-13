import os
import time

# print("%s(%s)" % (w.decode("utf-8"), c), end="\u3000")
# print!("{}--{esc}[2J{esc}[1;1H", p, esc = 27 as char);

count = 0
while True:
    print('\033[2J\033[1;1H')
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    print(f'{count}' * 77)
    count = count + 1
    time.sleep(1)
