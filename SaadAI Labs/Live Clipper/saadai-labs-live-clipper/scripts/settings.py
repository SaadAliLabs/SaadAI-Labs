"""Change a setting without editing the skill folder (it is read-only on Claude web).

  python scripts/settings.py                       # show current settings
  python scripts/settings.py min_speed_ratio 2     # set one (numbers, true/false, null and JSON lists work)

Changes are saved in <data folder>/config.json and override the skill's config.json.
"""
import json
import sys

from common import load_config, load_json, save_json, user_config_path


def parse(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


def main():
    path = user_config_path()
    if len(sys.argv) < 3:
        print(json.dumps(load_config(), ensure_ascii=False, indent=2))
        print(f"\n(your changes: {path})")
        return
    data = load_json(path, {}) or {}
    data[sys.argv[1]] = parse(" ".join(sys.argv[2:]))
    save_json(path, data)
    print(f"{sys.argv[1]} = {data[sys.argv[1]]!r}  (saved in {path})")


if __name__ == "__main__":
    main()
