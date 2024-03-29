from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
ListView,DetailView,
CreateView,DeleteView,
UpdateView)
from . import models
from .forms import *
from django.core.files.storage import FileSystemStorage
#from topicApp.Topicfun import Topic
#from ckdApp.funckd import ckd
from sklearn.tree import export_graphviz #plot tree
from sklearn.metrics import roc_curve, auc #for model evaluation
from sklearn.metrics import classification_report #for model evaluation
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(df2.drop('classification_yes', 1), df2['classification_yes'], test_size = .2, random_state=10)
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

import time
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import pickle
import matplotlib.pyplot as plt
import eli5 #for purmutation importance
from eli5.sklearn import PermutationImportance
import shap
#for SHAP values
#from pdpbox import pdp, info_plots #for partial plots
np.random.seed(123) #ensure reproduc



class ckd:
    def __init__(self):
        pass
    def SelectKBest(self,indep_X,dep_Y):
        test = SelectKBest(score_func = chi2, k=5)
        fit1 = test.fit(indep_X,dep_Y)

        features = indep_X.columns.values.tolist()
        np.set_printoptions(precision=2)
        print(features)
        print(fit1.scores_)

        feature_series = pd.Series(data=fit1.scores_,index=features)
        feature_series.plot.bar()
#
        selectk_features = fit1.transform(indep_X)
        return selectk_features

###

    def random(self, features, indep_X, dep_Y):
        X_train, X_test, y_train, y_test = train_test_split(indep_X, dep_Y, test_size=0.25, random_state=10)

        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=1)
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)

        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)

        from sklearn.metrics import accuracy_score
        from sklearn.metrics import classification_report

        Accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return classifier, Accuracy, report, X_test, y_test, cm#,X_test1


    def blockbox(self,model,patient):


        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(patient)
        shap.initjs()
        return shap.force_plot(explainer.expected_value[1],shap_values[1],patient,matplotlib = True,show=True)
