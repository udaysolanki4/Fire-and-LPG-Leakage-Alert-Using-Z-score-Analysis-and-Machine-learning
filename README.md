# Fire-and-LPG-Leakage-Alert-Using-Z-score-Analysis
detailed description available on:
https://www.hackster.io/uday-solanki/fire-and-lpg-leakage-alert-using-z-score-analysis-e8b7ec

Further how we can integrate the machine learning model in this project follow below methods to acheive that.
So instead of using filters at integromat to know what is actually happening in the room . That is either a fire or a leakage so instead of using if else condition we are going to add machine learning model to determine what message shoud we post to the user.
 
So we are using the DecisionTreeClassifier model.
- you need to install the library as follow: scikit-learn, numpy and pandas
- dataset = pd.read_csv("sensorvalues1.csv") #using this we are making a table and reading sensor data
- state_lb = LabelEncoder()

  Y = state_lb.fit_transform(dataset['value']) #it converts categorial data into numerical i.e smoke=3, Normal=2, fire=1, LPG=0
- FEATURES =['temperature','gas']

  X_data = dataset[FEATURES]  # now we declare the feature on which we are going to predict
- clf = DecisionTreeClassifier(random_state=0) #defining classifier
- clf.fit(X_train,y_train) # training model
- state = clf.predict(x) # predicting now 
you can find this code in model.py and further main_ml.py is used for the project using model you can check them out!!
