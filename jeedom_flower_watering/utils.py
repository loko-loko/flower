from loguru import logger as log
from yaml import safe_load

 
def get_config(conf_file):
    log.debug(f"[config] Get data from: {conf_file}")
    try:
        with open(conf_file) as f:
            data = safe_load(f)
        return data["configs"]
    except FileNotFoundError as e:
        log.error(f"[config] File not found: {e}")
        exit(1)
    except Exception as e:
        log.error(f"[config] File cannot be parsed: {e}")
        exit(1)


def check_config_options(config, defaults):
    for key, value in defaults.items():
        if key in config.keys():
            continue
        if value is None:
            log.error(f"[config] Option missing in config: {key}")
            exit(1)
        else:
            log.warning(f"[config] Option not present in config: <{key}>. Used default value: {value}")
            config[key] = value
    return config




