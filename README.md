# Jeedom Flower Spray

This program allows you to starting a plant watering scenario from Jeedom according to the level of moisture recovered from the [Mi Flower Exporter](https://github.com/loko-loko/mi-flora-exporter.git).

## How to use

### Config file

Jeedom Flower Spray work with a config file whose contain some informations like:
- Flower(s) to spray (Flower name displayed from exporter)
- Jeedom info (URL, API Key)
- Mi Flower Exporter URL

You can find an example of a config file in: `templates/config.yml`.

### Options

See options of Flower Exporter:
- `-c|--config`: Config file
- `--logs` (Optional): Enable writing logs to a file [Default: `False`]
- `--log-path <path>` (Optional): Log path [Default: `/var/log/jeedom-flower-spray`]
- `--spray-time <seconds>` (Optional): Time of water spray [Default: `20`]
- `--min-moisture-level <level>` (Optional): Level of minimum moisture for spray [Default: `18`]
- `--jeedom-start-id <id>` (Optional): Jeedom scenario ID to start spray [Default: `1`]
- `--jeedom-stop-id <id>` (Optional): Jeedom scenario ID to stop spray [Default: `2`]
- `-d|--debug` (Optional): Debug Mode [Default: `False`]

