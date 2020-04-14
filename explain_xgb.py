import pandas as pd
import shap
import xgboost as xgb
import pickle

shap.initjs()

train_data = pd.read_csv('train')
y = train_data.iloc[:,0]
X = train_data.iloc[:,1:]

model = pickle.load(open("xgboost-model", "rb"))

X = shap.sample(X)
explainer = shap.TreeExplainer(model, X)
shap_values = explainer.shap_values(X)


# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])