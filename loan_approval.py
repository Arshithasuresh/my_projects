# -*- coding: utf-8 -*-
"""loan approval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glSp6Xd_X5N0eIsvLYNB9fljC4aCV9bd

Finance companies deals with some kinds of home loans. They may have their presence across urban, semi urban and rural areas. Customer first applies for home loan and after that company validates the customer eligibility for loan.
Mostly Company wants to automate the loan eligibility process (real time) based on customer detail provided while filling online application form. These details are Gender, Marital Status, Education, Number of Dependents, Income, Loan Amount, Credit History and others. To automate this process, I have provided a data set to identify the customers segments that are eligible for loan amount so that they can specifically target these customers. Try to automate this Loan Eligibility Process.

Importing library for loading dataset
"""

import pandas as pd

df = pd.read_csv('Loan_Train.csv')

df.head()

df.tail()

"""Checking whether there are any null values

"""

df.isnull()

df.drop('Loan_ID',1,inplace = True)

df.info()

df.shape

df.isnull().sum()

df.isnull().sum()*100 / len(df)

df.dropna(inplace=True)

df.isnull().sum()

categorical_column=['Gender','Married','Dependents','Education','Self_Employed','Loan_Amount_Term','Property_Area','Loan_Status']

df['Dependents'] = df['Dependents'].replace(to_replace="3+",value='4')
df['Dependents'].unique()

for x in categorical_column:
    print(df[x].unique())

"""##  Data Visualization

Data visualization is done for visualizing every column in the loaded dataset for analysing.
"""

import seaborn as sns
import matplotlib.pyplot as plt


fig,axes = plt.subplots(4,2,figsize=(12,15))
for idx,cat_col in enumerate(categorical_column):
    row,col = idx//2,idx%2
    sns.countplot(x=cat_col,data=df,hue='Loan_Status',ax=axes[row,col])

plt.subplots_adjust(hspace=1)

"""# ***Data preprocessing***

The dataset is preprocessed in order to check missing values, noisy data, and other inconsistencies before executing it to the algorithm.
"""

from sklearn.preprocessing import LabelEncoder
lab = LabelEncoder()

label_encoders = {}
for column in categorical_column:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

df

"""# ***Model Selection and building a model***"""

x=df.iloc[:,df.columns!='Loan_Status']
y=df.iloc[:,df.columns=='Loan_Status']

"""splitting the dataset into training and test sets"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

X_train

X_test

y_train

y_test

"""F1 score is used to check the model's accuracy

"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score,f1_score

tree_clf = DecisionTreeClassifier()
tree_clf.fit(X_train,y_train)
y_pred = tree_clf.predict(X_train)
print("Training Data Set Accuracy: ", accuracy_score(y_train,y_pred))
print("Training Data F1 Score ", f1_score(y_train,y_pred))
print("Validation Mean F1 Score: ",cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='f1_macro').mean())
print("Validation Mean Accuracy: ",cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='accuracy').mean())

"""The accuracy and F1 score are not same. So we should Tune the parameters"""

training_accuracy = []
val_accuracy = []
training_f1 = []
val_f1 = []
tree_depths = []

for depth in range(1,20):
    tree_clf = DecisionTreeClassifier(max_depth=depth)
    tree_clf.fit(X_train,y_train)
    y_training_pred = tree_clf.predict(X_train)

    training_acc = accuracy_score(y_train,y_training_pred)
    train_f1 = f1_score(y_train,y_training_pred)
    val_mean_f1 = cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='f1_macro').mean()
    val_mean_accuracy = cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='accuracy').mean()

    training_accuracy.append(training_acc)
    val_accuracy.append(val_mean_accuracy)
    training_f1.append(train_f1)
    val_f1.append(val_mean_f1)
    tree_depths.append(depth)


Tuning_Max_depth = {"Training Accuracy": training_accuracy, "Validation Accuracy": val_accuracy, "Training F1": training_f1, "Validation F1":val_f1, "Max_Depth": tree_depths }
Tuning_Max_depth_df = pd.DataFrame.from_dict(Tuning_Max_depth)

plot_df = Tuning_Max_depth_df.melt('Max_Depth',var_name='Metrics',value_name="Values")
fig,ax = plt.subplots(figsize=(15,5))
sns.pointplot(x="Max_Depth", y="Values",hue="Metrics", data=plot_df,ax=ax)

tree_clf = DecisionTreeClassifier(max_depth=3)
tree_clf.fit(X_train,y_train)
model=tree_clf
y_pred = tree_clf.predict(X_train)
print("Training Data Set Accuracy: ", accuracy_score(y_train,y_pred))
print("Training Data F1 Score ", f1_score(y_train,y_pred))
print("Validation Mean F1 Score: ",cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='f1_macro').mean())
print("Validation Mean Accuracy: ",cross_val_score(tree_clf,X_train,y_train,cv=5,scoring='accuracy').mean())

import pickle

from google.colab import files
uploaded = files.upload()

from google.colab import drive
drive.mount('/content/drive')

with open('LoanFinal.pickle','wb') as f:
    pickle.dump(model,f)
    f.close()

model = pickle.load(open('LoanFinal.pickle', 'rb'))

y_train.head(10)

answer=[[1,1,2,0,0,8333,3167.0,165.0,7,1.0,0]]

print ("Predicts: " + str(model.predict(answer)))

column_names=['Gender','Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History','Property_Area']

df

from tkinter import *
import joblib
import pandas as pd

model = joblib.load('loan_status_predict')

import pandas as pd
df = pd.DataFrame({
    'Gender':1,
    'Married':1,
    'Dependents':2,
    'Education':0,
    'Self_Employed':0,
    'ApplicantIncome':2889,
    'CoapplicantIncome':0.0,
    'LoanAmount':45,
    'Loan_Amount_Term':180,
    'Credit_History':0,
    'Property_Area':1
},index=[0])

result = model.predict(df)

if result==1:
    print("Loan Approved")
else:
    print("Loan Not Approved")

import joblib

def show_entry():
    p1 = float(input("Gender [1:Male, 0:Female]: "))
    p2 = float(input("Married [1:Yes, 0:No]: "))
    p3 = float(input("Dependents [1, 2, 3, 4]: "))
    p4 = input("Education: ")
    p5 = input("Self-Employed [Yes/No]: ")
    p6 = float(input("Applicant Income: "))
    p7 = float(input("Coapplicant Income: "))
    p8 = float(input("Loan Amount: "))
    p9 = float(input("Loan Amount Term: "))
    p10 = float(input("Credit History [1/0]: "))
    p11 = input("Property Area [Urban/Rural/Semiurban]: ")

    # Load the trained model
    model = joblib.load('loan_status_predict')

    # Create a DataFrame from the user input
    data = pd.DataFrame({
        'Gender': p1,
        'Married': p2,
        'Dependents': p3,
        'Education': p4,
        'Self_Employed': p5,
        'ApplicantIncome': p6,
        'CoapplicantIncome': p7,
        'LoanAmount': p8,
        'Loan_Amount_Term': p9,
        'Credit_History': p10,
        'Property_Area': p11
    }, index=[0])

    # Make a prediction using the trained model
    prediction = model.predict(df)[0]

    # Convert the prediction to a human-readable format
    if prediction == 1:
        prediction_text = "Loan Approved"
    else:
        prediction_text = "Loan Not Approved"

    # Print the predicted outcome
    print("Prediction:", prediction_text)

show_entry()