import sys
from typing import Dict, List, Tuple, Optional


_REQUIRED_KEYS: List[str] = [
    "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
]


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def parsed_args(config_file: str) -> Dict[str, str]:
    config: Dict[str, str] = {}

    try:
        with open(config_file, 'r') as file:
            for line_num, raw in enumerate(file, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    _die(f"Config line {line_num}: "
                         f"expected Key=Value, got {line!r}")
                key, value = line.split("=")
                config[key.strip().upper()] = value.strip()
    except FileNotFoundError:
        _die(f"{config_file} is not found")
    except OSError as exc:
        _die(f"Cannot read config file: {exc}")
    return config


def validate_config(config: Dict[str, str]) -> bool:

    for key in _REQUIRED_KEYS:
        if key not in config:
            _die(f"Missing required key: {key!r}")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        if width < 2 or height < 2:
            raise ValueError("WIDTH and HEIGHT must each be at least 2.")

        e_parts = config["ENTRY"].split(",")
        x_parts = config["EXIT"].split(",")

        if len(e_parts) != 2 or len(x_parts) != 2:
            raise ValueError(
                "Entry and Exit entry must be in a formate of ' x,y ' pairs.")

        entry: Tuple[int, int] = (
            int(e_parts[0].strip()), int(e_parts[1].strip()))
        exit_: Tuple[int, int] = (
            int(x_parts[0].strip()), int(x_parts[1].strip()))

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(
                f"ENTRY {entry} is outside the maze bound ({width}×{height}).")
        if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
            raise ValueError(
                f"EXIT {exit_} is outside the maze bounds ({width}×{height}).")
        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different cells.")

        perfect_str = config["PERFECT"].strip().lower()
        if perfect_str not in ("true", "false"):
            raise ValueError("PERFECT must be 'True' or 'False'.")
        perfect = perfect_str == "true"

        seed: Optional[int] = None
        if "SEED" in config:
            seed = int(config["SEED"])

        output_file = config["OUTPUT_FILE"].strip()
        if not output_file:
            raise ValueError("OUTPUT_FILE must not be empty")

    except ValueError as e:
        _die(f"Invalid Configaration Value: {e}")

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_,
        "perfect": perfect,
        "seed": seed,
        "output_file": output_file
    }
