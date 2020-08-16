import re
import time

import requests
from loguru import logger as log


class JeedomApi():

    def __init__(self, host, api_key):
        self.host = host
        self._api_key = api_key

    def _action_scenario(self, action_id, action_name):
        log.info(f"[jeedom] Execution of action: {action_name} [Scenario ID: {action_id}]")
        request = f"{self._endpoint}&type=scenario&id={action_id}&action=start"
        log.debug(f"[jeedom] Send request: {self._format_url_request(request)}")
        result = requests.get(request)
        if result.text != "ok":
            log.error(f"[jeedom] Problem with action: {action_name} [{action_id}]")
            exit(1)

    def spray_execution(self, start_id, stop_id, spray_time=20):
        # Start spray
        log.info(f"[spray] Starting action")
        self._action_scenario(
            action_id=start_id,
            action_name="Starting spray"
        )
        # Waiting
        log.info(f"[spray] Waiting {spray_time}s ..")
        time.sleep(spray_time)
        # Stop spray
        log.info(f"[spray] Stopping action")
        self._action_scenario(
            action_id=stop_id,
            action_name="Stopping spray"
        )

    @property
    def _endpoint(self):
        return f"http://{self.host}/core/api/jeeApi.php?apikey={self._api_key}"

    @staticmethod
    def _format_url_request(request):
        formatted_request = re.sub("apikey=[\w\\/]+", "apikey=*****", request)
        return formatted_request

