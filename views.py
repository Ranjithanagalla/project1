
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse
# Importing the libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
# Create your views here.
from Remote_User.models import ClientRegister_Model,kidney_model,kidney_disease_model,detection_ratio_model,detection_accuracy_model


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            detection_accuracy_model.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def Find_Kidney_Disease_Ratio(request):
    detection_ratio_model.objects.all().delete()
    ratio = ""
    kword = 'Positive'
    print(kword)
    obj = kidney_disease_model.objects.all().filter(Q(prediction=kword))
    obj1 = kidney_disease_model.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio_model.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Negative'
    print(kword1)
    obj1 = kidney_disease_model.objects.all().filter(Q(prediction=kword1))
    obj11 = kidney_disease_model.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio_model.objects.create(names=kword1, ratio=ratio1)


    obj = detection_ratio_model.objects.all()
    return render(request, 'SProvider/Find_Kidney_Disease_Ratio.html', {'objs': obj})

def View_Kidney_Disease_Positive_Details(request):

    keyword="Positive"

    obj = kidney_disease_model.objects.all().filter(prediction=keyword)
    return render(request, 'SProvider/View_Kidney_Disease_Positive_Details.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = kidney_disease_model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})


def charts(request,chart_type):
    chart1 = detection_ratio_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def Find_Kidney_Disease_Status(request):

    obj =kidney_disease_model.objects.all()
    return render(request, 'SProvider/Find_Kidney_Disease_Status.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy_model.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="TrainedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = kidney_disease_model.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.id1, font_style)
        ws.write(row_num, 1, my_row.age, font_style)
        ws.write(row_num, 2, my_row.bp, font_style)
        ws.write(row_num, 3, my_row.sg, font_style)
        ws.write(row_num, 4, my_row.al, font_style)
        ws.write(row_num, 5, my_row.su, font_style)
        ws.write(row_num, 6, my_row.rbc, font_style)
        ws.write(row_num, 7, my_row.pc, font_style)
        ws.write(row_num, 8, my_row.pcc, font_style)
        ws.write(row_num, 9, my_row.ba, font_style)
        ws.write(row_num, 10, my_row.bgr, font_style)
        ws.write(row_num, 11, my_row.bu, font_style)
        ws.write(row_num, 12, my_row.sc, font_style)
        ws.write(row_num, 13, my_row.sod, font_style)
        ws.write(row_num, 14, my_row.pot, font_style)
        ws.write(row_num, 15, my_row.hemo, font_style)
        ws.write(row_num, 16, my_row.pcv, font_style)
        ws.write(row_num, 17, my_row.wc, font_style)
        ws.write(row_num, 18, my_row.rc, font_style)
        ws.write(row_num, 19, my_row.htn, font_style)
        ws.write(row_num, 20, my_row.dm, font_style)
        ws.write(row_num, 21, my_row.cad, font_style)
        ws.write(row_num, 22, my_row.appet, font_style)
        ws.write(row_num, 23, my_row.pe, font_style)
        ws.write(row_num, 24, my_row.ane, font_style)
        ws.write(row_num, 25, my_row.prediction, font_style)

    wb.save(response)
    return response


def train_model(request):
    detection_accuracy_model.objects.all().delete()
    # Reading the dataset
    kidney = pd.read_csv("kidney_disease.csv")
    kidney.head()
    # Information about the dataset
    kidney.info()
    # Description of the dataset
    kidney.describe()
    # To see what are the column names in our dataset
    print(kidney.columns)
    # Mapping the text to 1/0 and cleaning the dataset
    kidney[['htn', 'dm', 'cad', 'pe', 'ane']] = kidney[['htn', 'dm', 'cad', 'pe', 'ane']].replace(
        to_replace={'yes': 1, 'no': 0})
    kidney[['rbc', 'pc']] = kidney[['rbc', 'pc']].replace(to_replace={'abnormal': 1, 'normal': 0})
    kidney[['pcc', 'ba']] = kidney[['pcc', 'ba']].replace(to_replace={'present': 1, 'notpresent': 0})
    kidney[['appet']] = kidney[['appet']].replace(to_replace={'good': 1, 'poor': 0, 'no': np.nan})
    kidney['classification'] = kidney['classification'].replace(
        to_replace={'ckd': 1.0, 'ckd\t': 1.0, 'notckd': 0.0, 'no': 0.0})
    kidney.rename(columns={'classification': 'class'}, inplace=True)

    kidney['pe'] = kidney['pe'].replace(to_replace='good', value=0)  # Not having pedal edema is good
    kidney['appet'] = kidney['appet'].replace(to_replace='no', value=0)
    kidney['cad'] = kidney['cad'].replace(to_replace='\tno', value=0)
    kidney['dm'] = kidney['dm'].replace(to_replace={'\tno': 0, '\tyes': 1, ' yes': 1, '': np.nan})
    kidney.drop('id', axis=1, inplace=True)
    kidney.head()
    # This helps us to count how many NaN are there in each column
    len(kidney) - kidney.count()
    # This shows number of rows with missing data
    kidney.isnull().sum(axis=1)
    # This is a visualization of missing data in the dataset
    sns.heatmap(kidney.isnull(), yticklabels=False, cbar=False, cmap='viridis')
    # This shows number of complete cases and also removes all the rows with NaN
    kidney2 = kidney.dropna()
    print(kidney2.shape)
    # Now our dataset is clean
    sns.heatmap(kidney2.isnull(), yticklabels=False, cbar=False, cmap='viridis')
    sns.heatmap(kidney2.corr())
    # Counting number of normal vs. abnormal red blood cells of people having chronic kidney disease
    print(kidney2.groupby('rbc').rbc.count().plot(kind="bar"))
    # This plot shows the patient's sugar level compared to their ages
    kidney2.plot(kind='scatter', x='age', y='su');
    # plt.show()
    # Shows the maximum blood pressure having chronic kidney disease
    print(kidney2.groupby('class').bp.max())
    print(kidney2['dm'].value_counts(dropna=False))
    X_train, X_test, y_train, y_test = train_test_split(kidney2.iloc[:, :-1], kidney2['class'], test_size=0.33,
                                                        random_state=44, stratify=kidney2['class'])
    print(X_train.shape)
    y_train.value_counts()

    print("RANDOM FOREST CLASSFIER")

    rfc = RandomForestClassifier(random_state=22)
    rfc_fit = rfc.fit(X_train, y_train)
    rfc_pred = rfc_fit.predict(X_test)
    print(confusion_matrix(y_test, rfc_pred))
    print(classification_report(y_test, rfc_pred))
    accuracy_score(y_test, rfc_pred)

    print("ACCURACY")
    print(accuracy_score(y_test, rfc_pred) * 100)

    detection_accuracy_model.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfc_pred) * 100)

    print("SVM CLASSFIER")

    svm = SVC()
    svm_fit = svm.fit(X_train, y_train)
    svm_pred = svm_fit.predict(X_test)
    print(confusion_matrix(y_test, svm_pred))
    print(classification_report(y_test, svm_pred))
    accuracy_score(y_test, svm_pred)

    print("ACCURACY")
    print(accuracy_score(y_test, svm_pred) * 100)

    detection_accuracy_model.objects.create(names="SVM",ratio=accuracy_score(y_test, svm_pred) * 100)

    print("KNeighborsClassifier")

    knn = KNeighborsClassifier(n_neighbors=1)
    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=None,
                         n_neighbors=1, p=2, weights='uniform')
    knn.fit(X_train, y_train)

    pred = knn.predict(X_test)

    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred))
    accuracy_score(y_test, pred)

    print("ACCURACY")
    print(accuracy_score(y_test, pred) * 100)

    detection_accuracy_model.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, pred) * 100)

    print("LogisticRegression")

    logmodel = LogisticRegression()
    logmodel.fit(X_train, y_train)
    predictions = logmodel.predict(X_test)
    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))
    accuracy_score(y_test, predictions)

    print("ACCURACY")
    print(accuracy_score(y_test, predictions) * 100)

    detection_accuracy_model.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, predictions) * 100)

    status = ''
    type = ''
    obj1 = kidney_model.objects.values('id1',
    'age',
    'bp',
    'sg',
    'al',
    'su',
    'rbc',
    'pc',
    'pcc',
    'ba',
    'bgr',
    'bu',
    'sc',
    'sod',
    'pot',
    'hemo',
    'pcv',
    'wc',
    'rc',
    'htn',
    'dm',
    'cad',
    'appet',
    'pe',
    'ane'
    )

    kidney_disease_model.objects.all().delete()
    for t in obj1:

        id1= t['id1']
        age= t['age']
        bp= t['bp']
        sg= t['sg']
        al= t['al']
        su= t['su']
        rbc= t['rbc']
        pc= t['pc']
        pcc= t['pcc']
        ba= t['ba']
        bgr= t['bgr']
        bu= t['bu']
        sc= t['sc']
        sod= t['sod']
        pot= t['pot']
        hemo= t['hemo']
        pcv= t['pcv']
        wc= t['wc']
        rc= t['rc']
        htn= t['htn']
        dm= t['dm']
        cad= t['cad']
        appet= t['appet']
        pe= t['pe']
        ane= t['ane']

        pottacium = float(pot)

        if pottacium >= 3.6 and pottacium <= 5.2:
            status = "Negative"
        elif pottacium >= 5.2:
            status = "Positive"
        elif pottacium <= 3.6:
            status = "Positive"

        kidney_disease_model.objects.create(id1=id1,
        age=age,
        bp=bp,
        sg=sg,
        al=al,
        su=su,
        rbc=rbc,
        pc=pc,
        pcc=pcc,
        ba=ba,
        bgr=bgr,
        bu=bu,
        sc=sc,
        sod=sod,
        pot=pot,
        hemo=hemo,
        pcv=pcv,
        wc=wc,
        rc=rc,
        htn=htn,
        dm=dm,
        cad=cad,
        appet=appet,
        pe=pe,
        ane=ane,
        prediction=status
        )

    obj = detection_accuracy_model.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})














