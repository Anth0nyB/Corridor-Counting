import argparse
from typing import TextIO, List, Dict, Tuple, Any

from vehicle_matching import get_vehicle_movements

def get_sequences(sequence_file: TextIO) -> List[List[Tuple[int, int]]]:
    """
    Reads and formats all the pre-defined corridors

    :param sequence_file: The file to read the corridors from
    :return: A List containing every corridor sequence, in the form of a List of (intersection, movement_id)
    """
    raise NotImplementedError("get_sequences is not implemented yet.")


def get_intersection(cam_id) -> int:
    """
    Finds the intersection associated with the given camera

    :param cam_id: The id of the camera
    :return: The id of the intersection that cam_id is in 
    """
     
    raise NotImplementedError("get_intersection is not implemented yet.")


def match_vehicles_to_sequence(vehicles, sequences) -> Dict[int, Dict[str, List[Tuple[Any]]]]:
    """
    Determines every pre-defined corridor that the vehicles follow

    :param vehicles: A list of every vehicle mapping uid to list of movements
    :param sequences: A list of every pre-defined corridor
    :return: A mapping of uid to every matched sequence for all vehicles
    """
    matches = {}

    for uid, data in vehicles.items():
        vehicle_movements = [(get_intersection(item[0]), item[2]) for item in data]
        
        for seq_id, seq in enumerate(sequences):
            #TODO: after testing, can be simplified to {uid: List_of_seq_id}
            matches.setdefault(uid, {"movements": vehicle_movements, "matched_sequences": []})
            if seq in vehicle_movements:
                matches[uid]["matched_sequences"].append((seq_id, seq))

    return matches

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mtmct_file", type=argparse.FileType("r"))
    parser.add_argument("counting_file", type=argparse.FileType("r"))
    parser.add_argument("sequence_file", type=argparse.FileType("r"))
    args = parser.parse_args()

    vehicles = get_vehicle_movements(args.mtmct_file, args.counting_file)
    sequences = get_sequences(args.sequence_file)

    mappings = match_vehicles_to_sequence(vehicles, sequences)
    print(mappings)