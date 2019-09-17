import conf2, json, time, math, statistics, requests 
from boltiot import Bolt
import model

def integromat(temp,gas):
    s=['LPG Leakage', 'Fire','Normal','Smoke']
    URL = "https://hook.integromat.com/"# REPLACE WITH CORRECT URL
    temp=round((temp-32)*(5/9))# converting temperature into celsius
    state = model.MachineLearning_model(ldr_value) # calling model methode for state
    response = requests.get(URL,data={'temp':temp,'gas':gas, 'status':s[state[0]}])#making web request and sending data
    print (response.text)

def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size]
    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1]+Zn
    Low_bound = history_data[frame_size-1]-Zn
    return [High_bound,Low_bound]

bolt = Bolt(conf2.API_KEY, conf2.DEVICE_ID)
history_data=[]

while True:
    response=bolt.serialRead('1')
    data=json.loads(response)
    sensor_value = list(data['value'].split("\n"))
    
    if data['success'] != 1 or len(sensor_value)<3:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(10)
        continue
    
    try:
        temp_value = int(sensor_value[-3])
        gas_value = int(sensor_value[-2])
        print("Temperature value is "+str(temp_value)+"\n"+"gas value is"+str(gas_value))
    except Exception as e:
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
