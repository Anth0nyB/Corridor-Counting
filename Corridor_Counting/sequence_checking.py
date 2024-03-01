from typing import Any, Dict, List, TextIO, Tuple, TypeAlias
import argparse

from vehicle_matching import get_vehicle_movements


Sequence: TypeAlias = "List[Node]"
Node: TypeAlias = "Tuple[IntersectionID, MovementID]"
IntersectionID: TypeAlias = int
MovementID: TypeAlias = int


def get_sequences(sequence_file: TextIO) -> List[Sequence]:
    """
    Reads and formats all the pre-defined corridors

    :param sequence_file: The file to read the corridors from
    :return: A List containing every corridor sequence, in the form of a List of (intersection, movement_id)
    """
    result = []

    for line in sequence_file.readlines():
        sequence = []
        tokens = line.split()
        for index in range(0, len(tokens), 2):
            sequence.append((int(tokens[index]), int(tokens[index + 1])))
        result.append(sequence)

    return result


def get_intersections(sequence_file: TextIO) -> Dict[int, int]:
    """
    Reads the camera to intersection ID mapping

    :param sequence_file: The file to read the mapping from
    :return: A dictionary mapping the IDs
    """
    return {int(line.split()[0]): int(line.split()[1]) for line in sequence_file.readlines()}


def match_vehicles_to_sequence(vehicles, sequences, intersections_file) -> Dict[int, List[int]]:
    """
    Determines every pre-defined corridor that the vehicles follow

    :param vehicles: A list of every vehicle mapping uid to list of movements
    :param sequences: A list of every pre-defined corridor
    :param intersections_file: A file of camera to intersection ID mapping
    :return: A mapping of uid to every matched sequence for all vehicles
    """
    intersections = get_intersections(intersections_file)
    matches = {}

    for uid, data in vehicles.items():
        vehicle_movements = [(intersections[item[0]], item[2]) for item in data]
        
        for seq_id, seq in enumerate(sequences):
            # TODO: after testing, can be simplified to {uid: List_of_seq_id}
            matches.setdefault(uid, {"movements": vehicle_movements, "matched_sequences": []})
            if seq in vehicle_movements:
                matches[uid]["matched_sequences"].append((seq_id, seq))

    return matches


def main(mtmct_file: TextIO, counting_file: TextIO, sequence_file: TextIO, intersections_file: TextIO):
    vehicles = get_vehicle_movements(mtmct_file, counting_file)
    sequences = get_sequences(sequence_file)

    mappings = match_vehicles_to_sequence(vehicles, sequences, intersections_file)
    print(mappings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mtmct_file", type=argparse.FileType("r"))
    parser.add_argument("counting_file", type=argparse.FileType("r"))
    parser.add_argument("sequence_file", type=argparse.FileType("r"))
    parser.add_argument("intersections_file", type=argparse.FileType("r"))
    args = parser.parse_args()

    main(args.mtmct_file, args.counting_file, args.sequence_file, args.intersections_file)
