import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor #Solving this problem using a decision tree, I will explain my thinking here through comments

#I define a mock-up csv file since i couldn't find a dataset in the repo
df = pd.read_csv("appointment.csv")
#I assume that this csv contatins these features --> scheduled_time, actual_time, doctor_id, queue_length
df['delay'] = (pd.to_datetime(df['actual_time']) - pd.to_datetime(df['scheduled_time'])).dt.total_seconds() / 60 #here i have defined my own feature  delay, to calculate the difference 
                                                                                                                #between between the time current time and the scheduled time

df['hour'] = pd.to_datetime(df['scheduled_time']).dt.hour
df['day_of_week']=pd.to_datetime(df['scheduled_time']).dt.dayofweek #Taking the current day

#Now i am creating a new dataframe first in order to apply the features into my decision tree
df = df[['doctor_id','hour','day_of_week','queue_length','delay']]

X=df[['doctor_id','hour','day_of_week','queue_length']]
y=df['delay']
#We are trying to predict the delay here, which will allow us to prioritize patients accordingly and adjust them into the queue
dt_model = DecisionTreeRegressor()
dt_model.fit(X,y)

def select_best_doctor(available_doc, hour, day_of_week, queue_lengths):
    predictions = {} #First we create a dict to store our model prediction in 
    for doctor_id in available_doc:
        queue_lengths = queue_lengths.get(doctor_id,0)
        predicted_wait = dt_model.predict([[doctor_id,hour,day_of_week,queue_lengths]])[0]
        predictions[doctor_id] = predicted_wait #Now once we get the prediction, the work is now to simply return the minimum possible value in the dictionary 

    best_doctor = min(predictions, key=predictions.get)
    return best_doctor, predictions[best_doctor]


#We can now call this function, it is expected to return the best_doctor and predict the time it takes to check in on the patient!



