#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd


# In[2]:


trainTestSplitDF = pd.read_csv('./essay_input_data/train-test-split.csv', sep =';',engine='python')
trainTestSplitDF.columns = ['ESSAY_ID','SET']
trainTestSplitDF.head()


# ## ------Training Data--------

# In[3]:


trainOnlyDF = trainTestSplitDF[trainTestSplitDF.SET == 'TRAIN']
trainOnlyDF.head()


# ## -----Confirmation Bias fetching - labels.tsv-----

# In[4]:


confBiasLabelsDF = pd.read_csv('./essay_input_data/labels.tsv', sep ='\\t', engine='python',)
confBiasLabelsDF.columns = ['ESSAY_ID', 'LABEL']
confBiasLabelsDF.head()


# #### Merge ConfBias and Train sample

# In[5]:


confBiasTrain = (
    confBiasLabelsDF.merge(trainOnlyDF, 
              on=['ESSAY_ID'],
              how='right'
              ).drop(columns='SET')
)
confBiasTrain.head()


# ## -----Fetch data-tokenised.tsv-----

# In[6]:


argumentsDF = pd.read_csv('./essay_input_data/data-tokenized.tsv', sep ='\\t', engine='python')
argumentsDF.columns = ['ESSAY', 'ARGUMENT', 'TEXT', 'ANNOTATION']
argumentsDF.head()


# ## -----reading .ann files-----

# ### major, claim and premise for each essay

# In[7]:


def readAnnFile(essayNum):
    annFileRead = pd.read_csv('./essay_input_data/'+essayNum+'.ann', sep ='\\t',engine='python',names=['Index','Type','Text'])
    annFileRead[['Type','SpanFrom','SpanTo']] = annFileRead['Type'].str.split(' ',expand=True)
    premise=[]
    claim=[]
    major=[]
    for Ind,row in annFileRead.iterrows():
        if row['Type'] == "Premise":
            span=[int(row['SpanFrom']),int(row['SpanTo'])]
            premise.append([span,row['Text']])
        elif row['Type'] == "MajorClaim":
            span=[int(row['SpanFrom']),int(row['SpanTo'])]
            major.append([span,row['Text']])
        elif row['Type'] == "Claim":
            span=[int(row['SpanFrom']),int(row['SpanTo'])]
            claim.append([span,row['Text']])
    
    return premise,major,claim


# In[8]:


def addParagraphs(essayNum):
    paragraphDF = argumentsDF[argumentsDF.ESSAY == essayNum]

    paraList=list()
    for ind,row in paragraphDF.iterrows():
        subPara={}
        subPara['text']=row['TEXT']
        if row['ANNOTATION'] != None:
            subPara['sufficient']=False
        else:
            subPara['sufficient']=True
        paraList.append(subPara)

    return paraList


# ## -----Read all Essay files-----

# In[9]:



dataList=list()

#for each iteration, iterate
#items[1][0] refer to essay number
for items in confBiasTrain.iterrows():
    data={}
    with open('./essay_input_data/'+items[1][0]+'.txt','r',encoding='utf8') as eFile:
            data['id']=int(items[1][0][5:])
            data['text']= eFile.read()

    premise,major,claim = readAnnFile(items[1][0])
    
    
    majorList=[]
    
    premiseList=[]

    claimList=[]
 
    ## items[1][1] refer to essay's confirmation bias(Label)

    if items[1][1] == 'positive':
        confBias=True
    else: confBias = False
    
    for textPremise in premise:
        premiseDict={}
        premiseDict['span']=textPremise[0]
        premiseDict['text']=textPremise[1]
        premiseList.append(premiseDict)
        
    for textMajor in major:
        majorDict={}
        majorDict['span']=textMajor[0]
        majorDict['text'] = textMajor[1]
        majorList.append(majorDict)
            
    for textClaim in claim:
        claimDict={}
        claimDict['span']=textClaim[0]
        claimDict['text']=textClaim[1]
        claimList.append(claimDict)
        
    
    
        
    data['major_claim'] = majorList
    data['claims'] = claimList
    data['premises'] = premiseList
    data['confirmation_bias'] = confBias
    data['paragraphs']=addParagraphs(int(items[1][0][5:]))
    dataList.append(data)


# In[10]:


import json
with open('comp_arg_hackers.json', 'w') as outfile:
    json.dump(dataList, outfile)


# In[ ]:




