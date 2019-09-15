import conf2, json, time, math, statistics,requests 
from boltiot import Sms, Bolt

def integromat(temp,gas):
    URL = "https://hook.integromat.com/xxxxxxxxxxxxxxxxxxxxxx"# REPLACE WITH CORRECT URL
    temp=round((temp-32)*(5/9)) # converting temperature from ferhenite to celsius and round up the value
    response = requests.get(URL,data={'temp':temp,'gas':gas})#sending sensor value with web request
    print (response.text)

def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size]
    Mn=statistics.mean(history_data)# calculating mean
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)#calculating variance
    Zn = factor * math.sqrt(Variance / frame_size)#calculating z-score
    High_bound = history_data[frame_size-1]+Zn
    Low_bound = history_data[frame_size-1]-Zn
    return [High_bound,Low_bound]#passing in a list

bolt = Bolt(conf2.API_KEY, conf2.DEVICE_ID)
history_data=[]

while True:
    response=bolt.serialRead('1')
    data=json.loads(response)# converting to dictionary
    sensor_value = list(data['value'].split("\n"))
    
    if data['success'] != 1 or len(sensor_value)<3:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(10)
        continue
    
    try:
        temp_value = int(sensor_value[-3])#extraction of temperature value from data
        gas_value = int(sensor_value[-2])#extraction of gas value from data
        print("Temperature value is "+str(temp_value)+"\n"+"gas value is"+str(gas_value))
    except e:
        print("There was an error while parsing the response: ",e)
        time.sleep(10)
        continue

    bound = compute_bounds(history_data,conf2.FRAME_SIZE,conf2.MUL_FACTOR)
    if not bound:
        required_data_count=conf2.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(temp_value+gas_value)
        time.sleep(10)
        continue

    try:
        if (temp_value+gas_value) > bound[0]:
            print ("Alert")
            integromat(temp_value,gas_value)
        history_data.append(temp_value+gas_value);
    except Exception as e:
        print ("Error",e)
    time.sleep(10)
