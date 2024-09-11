import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC  
from sklearn.neural_network import MLPClassifier  
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load data
# data = pd.read_csv(r"D:\สหกิจศึกษา\00-โครงงานพิเศษ\ข้อมูลจริงจากสปสช\ระหว่าง Preprocess\00\ByBas\00new_BC_00-Bootstrap_10000.csv")
data = pd.read_csv(r"D:\สหกิจศึกษา\00-โครงงานพิเศษ\ข้อมูลจริงจากสปสช\หลัง Preprocess-เสร็จสิ้นพร้อมเข้าสู่ ML\คนที่ตรวจBRCA-BC\BC_bstrap10000-n.csv")
# Select features and target
# X = data[['BMI_NEW_GROUP', 'AGE_NEW_GROUP','PROVINCE_DIAG_GROUP','GENDER_N','STATUS','HCODE','HOSP_DIAG']]
X = data[['BRCA','BMI_NEW_GROUP', 'AGE_NEW_GROUP','PROVINCE_NEW_GROUP','GENDER_N']]
y = data['D1']

# One-Hot Encoding for categorical columns (if applicable)
X = pd.get_dummies(X)

# Check data
print("Shape of X:", X.shape)
print("Unique classes in y:", np.unique(y))

##---นับจำนวนคลาสก่อนเข้าโมเดล---
# Count occurrences of each class in the target variable (y)
class_counts = y.value_counts()
print("\nClass distribution before training:")
print(class_counts)

# Plot class distribution
plt.figure(figsize=(6, 4))
class_counts.plot(kind='bar', color='lightblue')
plt.title('Class Distribution Before Training')
plt.xlabel('Classes')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Split data into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define models
models = {
    'Random Forest': RandomForestClassifier(random_state=42, class_weight='balanced'),
    'SVM': SVC(random_state=42, class_weight='balanced'),
    'Neural Net': MLPClassifier(random_state=42, max_iter=500)
}

# Train and evaluate models
for name, model in models.items():
    print(f"\nTraining {name} model...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Overall performance
    macro_avg = report['macro avg']
    precision_avg = macro_avg['precision']
    recall_avg = macro_avg['recall']
    f1_avg = macro_avg['f1-score']
    
    # Specificity calculation for all classes (based on confusion matrix)
    tn, fp, fn, tp = conf_matrix.ravel() if conf_matrix.shape == (2, 2) else (np.nan, np.nan, np.nan, np.nan)
    specificity_avg = tn / (tn + fp) if (tn + fp) > 0 else np.nan
    
    print(f"\n{name} Performance (Overall):")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Average Precision: {precision_avg:.4f}")
    print(f"Average Recall: {recall_avg:.4f}")
    print(f"Average F1-score: {f1_avg:.4f}")
    print(f"Average Specificity: {specificity_avg:.4f}")
    
    # Extract metrics for each class
    for class_label in report.keys():
        if class_label not in ['accuracy', 'macro avg', 'weighted avg']:
            precision = report[class_label]['precision']
            recall = report[class_label]['recall']
            f1 = report[class_label]['f1-score']
            specificity = conf_matrix[0, 0] / (conf_matrix[0, 0] + conf_matrix[0, 1]) if conf_matrix.shape[0] > 1 else np.nan
            
            print(f"\nClass {class_label}:")
            print(f"Precision: {precision:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1-score: {f1:.4f}")
            print(f"Specificity: {specificity:.4f}")

# Save the best model
    model_filename = f"{name.replace(' ', '_')}_model.joblib"
    dump(best_model, model_filename)
    print(f"Saved {name} model to {model_filename}")