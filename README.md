# form-10k-parser

## How to use

psa: Make sure you are running this code from inside the project folder.

### 1. To Download:

Make sure each company is queried like this, with the correct .htm file
directly from sec.gov:
```
"name": "Palo Alto Networks",
"url": "https://www.sec.gov/Archives/edgar/data/1327567/000132756723000024/panw-20230731.htm",
"save_path": "data/panw_10k.html"
```

After, run the following command:
```
python3 notebook/download_10k.py
```

### 2. To Label with GPT 3.5

It will automatically label all of the files in the array named files located in the first lines of the main function. Will be outputted to /ai_labeled

Files in the array 'files' should be in the form "data/{company}_10k.html

Run the following command:
```
python3 notebook/ai_label.py
```

### 3. To Train Model
Run the following command:
```
python3 notebook/train_logistics.py
```

Example output:
```
Final Evaluation:
Accuracy: 0.6801
Precision (macro avg): 0.5608
Recall (macro avg): 0.6752
F1 Score (macro avg): 0.5968

Detailed Classification Report:

              precision    recall  f1-score   support

           0     0.8436    0.6496    0.7340      1461
           1     0.4252    0.6194    0.5043       381
           2     0.7031    0.8036    0.7500       560
           3     0.3103    0.6716    0.4245        67
           4     0.5217    0.6316    0.5714        19

    accuracy                         0.6801      2488
   macro avg     0.5608    0.6752    0.5968      2488
weighted avg     0.7311    0.6801    0.6928      2488
```
Explanation:
For type 0 (blanks), 
Precision (0.84): 84% of the time the model predicted type 0, it was actually type 0
Recall (0.65): 65% of the time it wasn't type 0, the model accurately agreed it wasn't type 0
F1-score (0.73): balance between precision and recall, 0.73 is relatively strong
Support (1461): there were 1461 examples of type 0 in the data


### 4. To Predict A Company's labels
Run the following command, make sure the 'new_10k_path' variable is changed to represent the location of the company .html file
```
python3 notebook/predict_logistics.py
```

### 5. To Compare Results of Prediction vs. Actual
Run the following command:
```
python3 notebook/calc_scores.py
```

### 6. User Workflow
The following companies 10-k's from 2024 are already a part of the development corpus:
- Alphabet
- Apple
- Coinbase
- Datadog
- Microsoft
- Netflix
- Nvidia
- Palantir
- Salesforce
- Tesla

First, we need to obtain both the prediction and the actual. Let's use
Uber as an example.

Follow (1), using the following data
```
"name": "Uber",
"url": "https://www.sec.gov/Archives/edgar/data/1543151/000154315125000008/uber-20241231.htm",
"save_path": "data/uber_10k.html"
```

Follow (4) and (5)

You should obtain the following output:

TODO: update this following output, and do user input for all of the files
