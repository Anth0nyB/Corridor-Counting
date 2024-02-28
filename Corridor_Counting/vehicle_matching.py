from typing import Dict, List, Optional, TextIO, Tuple
import argparse
import math

import pandas as pd


MTMCT_COLUMNS = [
    "camera_id",
    "obj_id",
    "frame_id",
    "x_min",
    "y_min",
    "width",
    "height",
    "xworld",
    "yworld",
]
COUNTING_COLUMNS = [
    "video_id",
    "frame_id",
    "movement_id",
    "vehicle_class_id",
    "x_min",
    "y_min",
    "width",
    "height",
]
THRESHOLD = 50


def find_distance(vehicle, candidate) -> float:
    return math.dist(
        (vehicle["x_min"] + vehicle["width"] / 2, vehicle["y_min"] + vehicle["height"] / 2),
        (candidate["x_min"] + candidate["width"] / 2, candidate["y_min"] + candidate["height"] / 2),
    )


def find_universal_id(vehicle, all_detections) -> Optional[int]:
    candidate_vehicles = all_detections.loc[
        (all_detections["camera_id"] == int(vehicle["video_id"])) &
        (all_detections["frame_id"] == int(vehicle["frame_id"]))
    ]

    result = None
    closest = THRESHOLD
    for _, candidate in candidate_vehicles.iterrows():
        if (distance := find_distance(vehicle, candidate)) < closest:
            closest = distance
            result = candidate["obj_id"]

    return result


def get_vehicle_movements(
    mtmct_file: TextIO,
    counting_file: TextIO,
) -> Dict[int, List[Tuple[int, int, int]]]:
    """
    Parses MTMCT and counting result files, and associates them.

    :param mtmct_file: The MTMCT file
    :param counting_file: The counting file
    :return: A mapping from universal ID to a list of tuples, consisting of a camera ID, frame #, and movement ID
    """
    mtmct = pd.read_csv(mtmct_file, names=MTMCT_COLUMNS, sep=" ")
    mtmct = mtmct.sort_values(by=["camera_id", "frame_id"])
    counting = pd.read_csv(counting_file, names=COUNTING_COLUMNS, sep=" ")
    results = {}

    for index, candidate_vehicle in counting.iterrows():
        camera, frame, movement = list(map(
            int,
            [candidate_vehicle[label] for label in ["video_id", "frame_id", "movement_id"]]
        ))

        if (vehicle_id := find_universal_id(candidate_vehicle, mtmct)) is not None:
            # TODO: consider sorting by frame
            results.setdefault(vehicle_id, []).append((camera, frame, movement))

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mtmct_file", type=argparse.FileType("r"))
    parser.add_argument("counting_file", type=argparse.FileType("r"))
    args = parser.parse_args()

    for uid, data in get_vehicle_movements(args.mtmct_file, args.counting_file).items():
        print(uid, data)
