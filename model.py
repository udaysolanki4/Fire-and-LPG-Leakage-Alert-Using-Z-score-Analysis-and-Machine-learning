import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

#defining Machine Learning Classifier
#reading sensor data
dataset = pd.read_csv("sensorvalues1.csv")

#Converting door state from strings to binary labels.
state_lb = LabelEncoder()
Y = state_lb.fit_transform(dataset['value'])

#Convert features into matrix form
FEATURES =['temperature','gas']
X_data = dataset[FEATURES]

#Defining the Decision tree classifier
clf = DecisionTreeClassifier(random_state=0)

#Training the classifier
clf.fit(X_data,Y)
    
def MachineLearning_model(temp, gas):    
    # converting data into numpy array
    x= np.array([[temp,gas]])
    
    # predicting value 
    state = clf.predict(x)
    
    #Returning state in binary form
    return state



