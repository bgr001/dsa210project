import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

selected_countries = ['United States', 'United Kingdom', 'Canada']
df = df[df['Country'].isin(selected_countries)]
df = df[(df['Year'] >= 2000) & (df['Year'] <= 2016)]

features = ['Spending', 'Personnel', 'Police', 'Recession', 'Conflict']
age_group_columns = df.columns[3:18].tolist()

# Recession and Conflict are categorical.   
df['Recession'] = df['Recession'].astype(str)
df['Conflict'] = df['Conflict'].astype(str)

# Create a combined feature and scale numerical variables.  
scaler = StandardScaler()
df['Scaled_Spending'] = scaler.fit_transform(df[['Spending']])
df['Scaled_Personnel'] = scaler.fit_transform(df[['Personnel']])
df['Combined_Spending_Personnel'] = (df['Scaled_Spending'] + df['Scaled_Personnel']) / 2
df['Scaled_Police'] = scaler.fit_transform(df[['Police']])

features_combined = ['Combined_Spending_Personnel', 'Scaled_Police', 'Recession', 'Conflict']

X = df[features_combined]
y_multi = df[age_group_columns]

# Define numerical and categorical features.  
numerical_features = ['Combined_Spending_Personnel', 'Scaled_Police']
categorical_features = ['Recession', 'Conflict']

# Create preprocessor.  
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),  # Already scaled
        ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_features)
    ])

# Split the data.  
X_train, X_test, y_multi_train, y_multi_test = train_test_split(
    X, y_multi, test_size=0.2, random_state=42
)

# Random Forest.  
rf_multi_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=500, random_state=1))
])
rf_multi_pipeline.fit(X_train, y_multi_train)
y_pred_rf_multi = rf_multi_pipeline.predict(X_test)

print("\nRandom Forest Results:")
rmse_rf_multi = np.sqrt(mean_squared_error(y_multi_test, y_pred_rf_multi))
r2_rf_multi = r2_score(y_multi_test, y_pred_rf_multi)
print(f"RMSE = {rmse_rf_multi:.4f}, R-squared = {r2_rf_multi:.4f}")

# XGBoost.  
xgb_multi_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(objective='reg:squarederror', n_estimators=500, random_state=1))
])
xgb_multi_pipeline.fit(X_train, y_multi_train)
y_pred_xgb_multi = xgb_multi_pipeline.predict(X_test)

print("\nXGBoost Results:")
rmse_xgb_multi = np.sqrt(mean_squared_error(y_multi_test, y_pred_xgb_multi))
r2_xgb_multi = r2_score(y_multi_test, y_pred_xgb_multi)
print(f"RMSE = {rmse_xgb_multi:.4f}, R-squared = {r2_xgb_multi:.4f}")

# Feature Importance Plots.  
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Random Forest Feature Importance.  
fitted_preprocessor_rf = rf_multi_pipeline.named_steps['preprocessor']
num_feature_names_rf = numerical_features
cat_feature_names_rf = list(fitted_preprocessor_rf.named_transformers_['cat'].get_feature_names_out(categorical_features))
preprocessed_feature_names_rf = num_feature_names_rf + cat_feature_names_rf
rf_feature_importances = rf_multi_pipeline.named_steps['regressor'].feature_importances_
feature_importance_dict_rf = dict(zip(preprocessed_feature_names_rf, rf_feature_importances))
sorted_feature_importance_rf = sorted(feature_importance_dict_rf.items(), key=lambda item: item[1], reverse=False)
features_sorted_rf, importances_sorted_rf = zip(*sorted_feature_importance_rf)

axes[0].barh(features_sorted_rf, importances_sorted_rf, color='blue')
axes[0].set_xlabel("Feature Importance")
axes[0].set_title("Random Forest - Focus Countries 2000-2016")

# XGBoost Feature Importance.  
fitted_preprocessor_xgb = xgb_multi_pipeline.named_steps['preprocessor']
num_feature_names_xgb = numerical_features
cat_feature_names_xgb = list(fitted_preprocessor_xgb.named_transformers_['cat'].get_feature_names_out(categorical_features))
preprocessed_feature_names_xgb = num_feature_names_xgb + cat_feature_names_xgb
xgb_feature_importances = xgb_multi_pipeline.named_steps['regressor'].feature_importances_
feature_importance_dict_xgb = dict(zip(preprocessed_feature_names_xgb, xgb_feature_importances))
sorted_feature_importance_xgb = sorted(feature_importance_dict_xgb.items(), key=lambda item: item[1], reverse=False)
features_sorted_xgb, importances_sorted_xgb = zip(*sorted_feature_importance_xgb)

axes[1].barh(features_sorted_xgb, importances_sorted_xgb, color='blue')
axes[1].set_xlabel("Feature Importance")
axes[1].set_title("XGBoost - Focus Countries 2000-2016")

plt.tight_layout()
plt.subplots_adjust(left=0.190)
plt.savefig('plots/ml_focus_importance.png', dpi=300, bbox_inches='tight')
plt.show()

#Actual vs Predicted Rates Plot.  
actual_average_suicide_rate_test = y_multi_test.mean(axis=1)
predicted_average_suicide_rate_rf = y_pred_rf_multi.mean(axis=1)
predicted_average_suicide_rate_xgb = y_pred_xgb_multi.mean(axis=1)

plt.figure(figsize=(10, 8))
plt.scatter(actual_average_suicide_rate_test, predicted_average_suicide_rate_rf, 
            alpha=0.5, label='Random Forest Predictions (Avg)', color='blue')
plt.scatter(actual_average_suicide_rate_test, predicted_average_suicide_rate_xgb, 
            alpha=0.5, label='XGBoost Predictions (Avg)', color='red')
plt.xlabel("Actual Average Suicide Rate")
plt.ylabel("Predicted Average Suicide Rate")
plt.title("Actual vs. Predicted Average Suicide Rate for RF and XGBoost")
# Ideal Line.  
max_rate = max(actual_average_suicide_rate_test.max(), predicted_average_suicide_rate_rf.max(), predicted_average_suicide_rate_xgb.max())
min_rate = min(actual_average_suicide_rate_test.min(), predicted_average_suicide_rate_rf.min(), predicted_average_suicide_rate_xgb.min())
plt.plot([min_rate, max_rate], [min_rate, max_rate], 'k--', lw=2, label='Ideal Prediction')

plt.grid(True)
plt.legend()
plt.savefig('plots/ml_focus_performance.png', dpi=300, bbox_inches='tight')
plt.show()