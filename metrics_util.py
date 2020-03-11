import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, auc
from lib.detection_metrics import calc_mean_average_precision_from_ap_list, calc_accuracy_metrics

def map_metrics(y_true, y_pred):
    acc_metrics = calc_accuracy_metrics(y_true, y_pred)
    ap_metrics_list = []
    average_recall_list = []
    for metrics in acc_metrics:
        class_name = metrics['class']
        ap = round(metrics['AP'], 3)
        ar = round(metrics['AR'], 3)
        ap_metrics_list.append(f"{class_name}({ap})")
        average_recall_list.append(f"{class_name}({ar})")
    ap_metrics_value = " / ".join(ap_metrics_list)
    average_recall_value = " / ".join(average_recall_list)
    return {
        'mAP': calc_mean_average_precision_from_ap_list(acc_metrics),
        'allAP': ap_metrics_value,
        'allAR': average_recall_value
    }


def auc_metrics(y_true, y_pred):
    fpr_list, tpr_list, _ = roc_curve(y_true, y_pred, drop_intermediate=False)
    fpr_list, tpr_list = np.array(fpr_list), np.array(tpr_list)
    return {
        'AUC': auc(fpr_list, tpr_list),
    }