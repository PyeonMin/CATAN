import random

print([random.randint(0,5) for _ in range(5)])

from innersetting import Item

msg = "deal reciever 0 0 0 0 0 / 0 0 0 0 0" #서버가 받음
msg = "deal 0 0 0 0 0 / 0 0 0 0 0" #클라가 받음

state = "state 0 0 0 0 0"

msg = msg.split(" ")

if msg[0] == 'deal':
    msg.pop(0)


    # take = list(map(int,msg[:5]))
    # give = list(map(int,msg[6:]))
    # print(take,give)
    
    print(" ".join(msg),end="+")
    
    
    
    # a = list(map(int,[i for i in msg if i.isdigit()]))
    # print(a)
        