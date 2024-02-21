import pandas as pd
import yaml
import os
import argparse

THRESHOLD = 50

def get_mtmct_data(mtmct_file):
    all_detections = pd.read_csv(mtmct_file, names=["camera_id", "obj_id", "frame_id", "xmin", "ymin", "width", "height", "xworld", "yworld"], sep='\s+')
    all_detections = all_detections.sort_values(by=["camera_id", "frame_id"])

    return all_detections



def find_distance(vehicle, candidate):
    (x1, y1) = (vehicle['xmin'] + vehicle['width'] / 2, vehicle['ymin'] + vehicle['height'] / 2)
    (x2, y2) = (candidate['xmin'] + candidate['width'] / 2, candidate['ymin'] + candidate['height'] / 2)

    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def find_universal_id(vehicle, all_detections):
    matched_vehicle = None
    min_dist = THRESHOLD
    candidate_vehicles = all_detections.loc[(all_detections["camera_id"] == int(vehicle["video_id"])) & (all_detections["frame_id"] == int(vehicle["frame_id"]))]

    for index, candidate in candidate_vehicles.iterrows():
        curr_dist = find_distance(vehicle, candidate)
        if curr_dist < min_dist:
            min_dist = curr_dist
            matched_vehicle = candidate

    return matched_vehicle["obj_id"] if matched_vehicle is not None else None     


""" Returns a dictionary 
    {universal_id_0: [(camera, frame, movement_0), (camera, frame, movement_1), ...],
     universal_id_1: [(camera, frame, movement_0), (camera, frame, movement_1), ...],
     ...}"""
def get_vehicle_movements(mtmct_file, counting_dir):
    # project_root = os.environ.get("ROOT")

    all_detections = get_mtmct_data(mtmct_file)
    counting_output_files = os.listdir(counting_dir)

    all_vehicles = {}

    for counting_output_file in counting_output_files[:1]:
        counting_output = open(f"{counting_dir}/{counting_output_file}")
        counted_movements = pd.read_csv(counting_output)

        for index, candidate_vehicle in counted_movements.iterrows():
            movement = int(candidate_vehicle["movement_id"])
            camera = int(candidate_vehicle["video_id"])
            frame = int(candidate_vehicle["frame_id"])
            vehicle_id = find_universal_id(candidate_vehicle, all_detections)

            if vehicle_id is not None:
                if vehicle_id not in all_vehicles:
                    all_vehicles[vehicle_id] = []
                # consider sorting by frame
                all_vehicles[vehicle_id].append((camera, frame, movement))

    return all_vehicles


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mtmct_file", type=argparse.FileType("r"))
    parser.add_argument("counting_dir", type=str)
    args = parser.parse_args()

    print(get_vehicle_movements(args.mtmct_file, args.counting_dir))