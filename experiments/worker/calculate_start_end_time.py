from datetime import datetime
from datetime import timedelta
d1=datetime(2018,9,1,17,30,00)
d2=datetime(2018,9,2,19,00,00)
d3=d2-d1
day=d3.days
h1=d1.hour
m1=d1.minute
h2=d3.seconds/3600
m2=d3.seconds/60
fps=1
def calculate():
    if(m1!=30):
       start=h1*2*fps
    else:
       start=h1*2*fps+1
    if(m2%60==0):
       end=int(day*48*fps+h2*2*fps)
    else:
       end=int(day*48*fps+h2*2*fps+1)

    print(start)
    print(end)


calculate()
