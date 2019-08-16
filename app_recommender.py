import pandas as pd
import copy,pickle
import numpy as np
import matplotlib.pyplot as plt
from flask_cors import CORS
#from neuralmodel import model_call
from flask import Flask,request
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
raw=pd.read_csv("data.csv",index_col=0)
units=list(set(raw["Units"].values))
raw["Units"]=raw["Units"].apply(lambda x: units.index(x)+1)
roles=list(set(raw["Roles"].values))
raw["Roles"]=raw["Roles"].apply(lambda x: roles.index(x)+1)

raw_w_nums=copy.deepcopy(raw)

train_data=raw_w_nums[:2500]
test_data=raw_w_nums[2500:]
test_data.reset_index(drop=True,inplace=True)


#recomendations based on euclidian distance similarity between the entire data
ar=train_data.values
with open("recos_bits","rb") as doosri_file:
    
    doldi=pickle.load(doosri_file)


def funky(user_number):
    emp=[]
    thresh=1.3
    while (len(emp)==0):
        for i in range(0,len(doldi[user_number])):
            if doldi[user_number][i]<=thresh:
                emp.append(i)
        thresh =thresh+1
    same=train_data.loc[train_data.index.isin(emp)]
    return same[same.columns.tolist()[2:22]].mean().values

test = test_data.columns[2:22]


def recommender_org(cusid):
        
    to_send=eval(cusid)   
    assert type(to_send) is int and to_send <=498, "the input should be an integer and should not be greater than 498" 
    user_reco=funky(int(to_send))
    to_reco=np.argsort(-user_reco)[:3] #change this number to change the number of recomendations    
    names=list(test[to_reco])

    #to_pri=[ {k,v} for k,v in zip([user_reco[x] for x in to_reco],names)]
    #to_pri=[list(x) for x in to_pri]
    data=json.dumps(names)    
    return data 


def recommender_cat(cusid):
    
    to_send=eval(cusid)
    to_val=[]
    assert type(to_send) is int, "the input should be an integer" 
    if to_send!=500:
        user_reco=funky(int(to_send))
        to_reco=np.argsort(-user_reco) #change this number to change the number of recomendations    
        names=list(test[to_reco])

        trading =['Credit Scoring', 'Trade Reconstruction' ,'Investment Advisory','Portfolio Construction','Asset Valuation','Trade Execution','Capital Optimization']
        risk=['Dispute Management','Fraud Detection','Smart Surveillance','Model  Management','Account Reconciliations']
        compliance=['Customer Onboarding','KYC & AML','Contract Analysis','Content Reviews']
        operations=['Product Recommendations','Collections','Operations Assistant','Product Pricing']

        if names[0] in trading:
            final_list=[x for x in names if x in trading]
        if names[0] in risk:
            final_list=[x for x in names if x in risk]
        if names[0] in compliance:
            final_list=[x for x in names if x in compliance]
        if names[0] in operations:
            final_list=[x for x in names if x in operations] 
        #print(final_list)
       # comb=[user_reco[x] for x in to_reco]
        #to_pri=[ {k,v} for k,v in zip(comb,final)]
        #to_pri=[list(x) for x in to_pri]

        #for x in to_pri[:3]:
         #   to_val.append(x[1])
        #print (len(final_list))
        if (len(final_list)>=8):
            to_val=final_list[:8]
        else:
            to_val=final_list

    else:
        to_val=[x for x in test]

    
    data_val= json.dumps(to_val)
    return data_val


def recommender_twocat(cusid):
      
    #to_send=cusid
    to_send=eval(cusid )
    to_val=[]
    assert type(to_send) is int, "the input should be an integer" 
    if to_send!=500:
        user_reco=funky(int(to_send))
        to_reco=np.argsort(-user_reco) #change this number to change the number of recomendations    
        names=list(test[to_reco])

                
        trading =['Credit Scoring', 'Trade Reconstruction' ,'Investment Advisory','Portfolio Construction','Asset Valuation','Trade Execution','Capital Optimization']
        risk=['Dispute Management','Fraud Detection','Smart Surveillance','Model Risk Management','Account Reconciliations']
        compliance=['Customer Onboarding','KYC & AML','Contract Analysis','Content Reviews']
        operations=['Product Recommendations','Collections','Operations Assistant','Product Pricing']
        
        first=names[0]
        second= names[1]
        #print("first",first)
        #print("second",second)
        def high_mac(high=first,low=second):
            two=[high,low]
            dat=[]
            dat.append(high)
            dat.append(low)
            #first we test if both belong to same category if they do then return the entire thing
            if high in trading and low in trading:
                final_tree=[x for x in names if x in trading]
                return final_tree
            if high in risk and low in risk:
                final_tree=[x for x in names if x in risk]
                return final_tree
            if high in compliance and low in compliance:
                final_tree=[x for x in names if x in compliance]
                return final_tree
            if high in operations and low in operations:
                final_tree=[x for x in names if x in operations] 
                return final_tree
            if high in trading:
                final_tree=[x for x in names if x in trading]
                ret=[x for x in final_tree if x not in two]
                
            if high in risk:
                final_tree=[x for x in names if x in risk]
                ret=[x for x in final_tree if x not in two]
                
            if high in compliance:
                final_tree=[x for x in names if x in compliance]
                ret=[x for x in final_tree if x not in two]
                
            if high in operations:
                final_tree=[x for x in names if x in operations]
                ret=[x for x in final_tree if x not in two]
            
            if low in trading:
                final_tree_l=[x for x in names if x in trading]
                ret_l=[x for x in final_tree_l if x not in two]
                
            if low in risk:
                final_tree_l=[x for x in names if x in risk]
                ret_l=[x for x in final_tree_l if x not in two]
                
            if low in compliance:
                final_tree_l=[x for x in names if x in compliance]
                ret_l=[x for x in final_tree_l if x not in two]
                
            if low in operations:
                final_tree_l=[x for x in names if x in operations]
                ret_l=[x for x in final_tree_l if x not in two]
              
            for x in ret:
                dat.append(x)
            for x in ret_l:
                dat.append(x)
            return dat
            #final_tree.remove(high)
            
                  

        
        #comb=[user_reco[x] for x in to_reco]
        #to_pri=[ {k,v} for k,v in zip(comb,first_list)]
        #to_pri=[list(x) for x in to_pri]
        

        #for x in to_pri[:3]:
        #to_val.append(x[1])
        final_list=high_mac()
        if (len(final_list)>=8):
            to_val=final_list[:8]
        else:
            to_val=final_list
    else:
        to_val=[x for x in test]
        
    data=json.dumps(to_val) 
    #print(type(data))
    
    return data

@app.route("/recommender_cat",methods=['GET'])
def call_cat():
    cusid= request.args.get('user') 
    data=recommender_cat(cusid)
    return data

@app.route("/recommender_org",methods=['GET'])
def call_org():
    cusid= request.args.get('user') 
    data=recommender_org(cusid)
    return data

@app.route("/recommender_twocat",methods=['GET'])
def call_twocat():
    cusid= request.args.get('user')
    #print("cusid:::::",cusid,"\n\n\n")
    data=recommender_twocat(cusid)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)
    #app.run(debug=True)
    



