import json
from typing import List, Dict
from .lib.BoundingBoxes import BoundingBoxes
from .lib.BoundingBox import BoundingBox
from .lib.utils import BBType
from .lib.Evaluator import Evaluator


def _convert_dict_to_bboxes(bbox_list: List[Dict], bb_type: BBType) -> BoundingBoxes:
    ret = BoundingBoxes()

    for elem in bbox_list:
        image_name = elem["image_file_name"]
        bboxes_elem = elem["annotations"]

        for b in bboxes_elem:
            conf = b.get("conf")
            bbx = BoundingBox(
                imageName=image_name,
                # imgSize=image_size,
                classId=b["class"],
                x=b["xmin"],
                y=b["ymin"],
                w=(b["xmax"] - b["xmin"]),
                h=(b["ymax"] - b["ymin"]),
                bbType=bb_type,
                classConfidence=conf
            )
            ret.addBoundingBox(bbx)
    return ret


def _get_json_str(json_path: str) -> str:
    return open(json_path).read().replace("\n", "")


def calc_accuracy_metrics(gt_json: str, dt_json: str) -> List[Dict]:
    gt_json = gt_json.replace("\n", "")
    dt_json = dt_json.replace("\n", "")

    gt_dict = json.loads(gt_json)  # type: List[Dict]
    dt_dict = json.loads(dt_json)  # type: List[Dict]

    gt_bboxes = _convert_dict_to_bboxes(gt_dict, BBType.GroundTruth)
    dt_bboxes = _convert_dict_to_bboxes(dt_dict, BBType.Detected)

    all_boxes = BoundingBoxes()
    all_boxes._boundingBoxes.extend(gt_bboxes._boundingBoxes)
    all_boxes._boundingBoxes.extend(dt_bboxes._boundingBoxes)

    eval = Evaluator()
    ret = eval.GetPascalVOCMetrics(all_boxes)
    return ret


def calc_mean_average_precision(gt_json: str, dt_json: str) -> float:
    all_metrics = calc_accuracy_metrics(gt_json, dt_json)
    return calc_mean_average_precision_from_ap_list(all_metrics)


def calc_mean_average_precision_from_ap_list(all_metrics: list)-> float:
    valid_classes = 0
    ap_sum = 0
    for metrics_per_class in all_metrics:
        ap = metrics_per_class['AP']
        totalPositives = metrics_per_class['total positives']

        if totalPositives > 0:
            valid_classes += 1
            ap_sum += ap
    mAP = ap_sum / valid_classes
    return mAP

def calc_accuracy_metrics_from_file(gt_json_path: str, dt_json_path: str) -> List[Dict]:
    gt_str = _get_json_str(gt_json_path)
    dt_str = _get_json_str(dt_json_path)
    ret = calc_accuracy_metrics(gt_str, dt_str)
    return ret


def calc_mean_average_precision_from_file(gt_json_path: str, dt_json_path: str) -> float:
    gt_str = _get_json_str(gt_json_path)
    dt_str = _get_json_str(dt_json_path)
    ret = calc_mean_average_precision(gt_str, dt_str)
    return ret


if __name__ == "__main__":
    ret = calc_mean_average_precision_from_file(
        "json/gt_bbox_format.json", "json/dt_bbox_format.json")
    print(ret)
