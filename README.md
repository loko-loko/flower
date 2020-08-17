# Jeedom Flower Watering

This tool allows you to starting a plant watering scenario from Jeedom according to the level of moisture recovered from the [Mi Flower Exporter](https://github.com/loko-loko/mi-flora-exporter.git).

## How to use

### Config file

The tool works with a config file whose contain some informations:
- Flower(s) to watering (Flower name displayed from exporter)
- Jeedom info (URL, API Key and Scenario IDs to start and stop watering)
- Mi Flower Exporter URL

You can find an example of a config file in: `templates/config.yml`.

### Options

See options of Flower Exporter:
- `--config`: Config file
- `--logs` (Optional): Enable writing logs to a file [Default: `False`]
- `--log-path <path>` (Optional): Log path [Default: `/var/log/jeedom-flower-watering`]
- `--watering-time <seconds>` (Optional): Time of water watering [Default: `20`]
- `--moisture-level-limit <level>` (Optional): Level of minimum moisture for watering [Default: `20`]
- `--only-watering` (Optional): Run only watering, without check of moisture level [Default: `False`]
- `--debug` (Optional): Debug Mode [Default: `False`]

