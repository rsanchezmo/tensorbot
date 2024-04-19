import requests
from pathlib import Path
from typing import List, Dict, Any
import time
import os
from tensorbot.plotting import plot_tensorboard_experiment


class TensorBot:
    def __init__(self, token: str, chat_id: str, tensorboard_path: str):
        """ Class to send Tensorboard plots to telegram
        :param token: telegram bot token
        :type token: str

        :param chat_id: telegram chat id
        :type chat_id: str

        :param tensorboard_path: path to the Tensorboard logs
        :type tensorboard_path: str

        """
        self._token = token
        self._chat_id = chat_id
        self._tensorboard_path = tensorboard_path
        self._last_modified_time = None

        if not Path(tensorboard_path).exists():
            raise FileNotFoundError(f"Path {tensorboard_path} does not exist")

    def _send_photo(self, photo_path: str):
        url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
        files = {'photo': open(photo_path, 'rb')}
        data = {'chat_id': self._chat_id}
        requests.post(url, files=files, data=data)

    def _send_msg(self, msg: str):
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {'chat_id': self._chat_id, 'text': msg}
        requests.post(url, data=data)

    def _check_for_updates(self):
        current_modified_time = os.path.getmtime(self._tensorboard_path)
        if current_modified_time != self._last_modified_time:
            self._last_modified_time = current_modified_time
            return True
        return False

    def run(self, update_interval: int, plot_config: List[Dict[str, Any]]):
        """ Run the bot

        :param update_interval: interval in minutes to check for updates
        :type update_interval: int

        :param plot_config: configuration for the plots
        :type plot_config: List[Dict[str, Any]]

        """

        while True:
            update_needed = self._check_for_updates()
            if update_needed:
                plot_tensorboard_experiment(exp_path=self._tensorboard_path,
                                            plot_config=plot_config,
                                            tmp_path='tmp.png')
                self._send_photo('tmp.png')

                Path('tmp.png').unlink()

            time.sleep(60 * update_interval)
