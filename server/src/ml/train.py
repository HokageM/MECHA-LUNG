"""
Training script for lung cancer risk assessment.
"""
import pandas as pd
import numpy as np
import joblib
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, confusion_matrix, precision_recall_curve


def prepare_data(path: str = "data/lung_cancer.csv") -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare data for training
    :param path: Path to the data file
    :return: Tuple of features and labels
    """
    data = pd.read_csv(path)
    
    X = data.drop("LUNG_CANCER", axis=1)
    y = data["LUNG_CANCER"]

    # Convert Female to 0, Male to 1
    X["GENDER"] = X["GENDER"].map({"F": 0, "M": 1})

    # Convert Lung_Cancer to 0, 1
    y = y.map({"YES": 1, "NO": 0})
    return X, y

def oversample_data(X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    """
    Oversample data using SMOTE
    :param X: Features
    :param y: Labels
    :return: Oversampled data
    """
    smote = SMOTE(random_state=420)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res


def train_lung_cancer_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Training function for lung cancer risk assessment
    :param X_train: Training data
    :param y_train: Training labels
    :return: Trained model
    """
    model = RandomForestClassifier(class_weight="balanced", n_estimators=100, random_state=420)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate model
    :param model: Trained model
    :param X_test: Test data
    :param y_test: Test labels
    """
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("Balanced Accuracy:", balanced_accuracy_score(y_test, y_pred))
    
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)
    print("ROC-AUC:", roc_auc)

    print("Confusion Matrix:", confusion_matrix(y_test, y_pred))

    # calculate PR-AUC curve for lung cancer
    precision, recall, _ = precision_recall_curve(y_test, y_pred)
    pr_auc = auc(recall, precision)
    print("PR-AUC:", pr_auc)

    # calculate PR-AUC curve for no lung cancer
    y_test_invert = 1 - y_test
    y_pred_invert = 1 - y_pred
    precision, recall, _ = precision_recall_curve(y_test_invert, y_pred_invert)
    pr_auc_no_lung_cancer = auc(recall, precision)
    print("PR-AUC for no lung cancer:", pr_auc)
    print("macro PR-AUC:", (pr_auc + pr_auc_no_lung_cancer) / 2)    


if __name__ == "__main__":
    X, y = prepare_data()

    # Data is unbalanced, 87% (270) lung cancer, 13% (39) no lung cancer
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=420, stratify=y
    )

    # Oversample only on training data using SMOTE
    X_train, y_train = oversample_data(X_train, y_train)

    model = train_lung_cancer_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    # save model
    joblib.dump(model, "server/src/ml/model/lung_cancer_model.joblib")
