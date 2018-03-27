from datetime import datetime
from datetime import timedelta
#startDT is the first days date and time(datetime)
#endDT is the last days date and time(datetime)
def calculate(day, h1, m1, h2, m2, duration):
##    d3=endDT-startDT #overall difference(date and time)
##    print(d3)
##    day=d3.days #no. of days in the difference
##    print(day)
##    h1=startDT.hour
##    print(h1)
##    m1=startDT.minute
##    print(m1)
##    h2=endDT.hour 
##    print(h2)
##    #m=d3.seconds/60-m1
##    m2=endDT.minute
##    print(m)
    #calculation of start time
    listTime = []
    if(m1!=30):
       startTime=h1*2*duration
    else:
       startTime=(h1*2+1)*duration #multiplied by 2 for 2 images per hour and added 1 for extra image in the next half hour
    #calculation of end time    
    if(m2 != 30):
       endTime=day*48*duration+h2*2*duration
    else:
       endTime=day*48*duration+(h2*2+1)*duration
    '''
    if(day == 0):#for same day
        endTime = endTime + startTime
    '''
    listTime.append(startTime)
    listTime.append(endTime)
    print(startTime)
    print(endTime)
    return listTime
   


#calculate(datetime(2018,8,1,17,30,00),datetime(2019,9,1,19,30,00),0.5)
