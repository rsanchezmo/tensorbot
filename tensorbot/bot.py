import requests
from pathlib import Path
from typing import List, Dict, Any
import time
import os
from tensorbot.plotting import plot_tensorboard_experiment


class TensorBot:
    def __init__(self, token: str, chat_id: str):
        """ Class to send Tensorboard plots to telegram
        :param token: telegram bot token
        :type token: str

        :param chat_id: telegram chat id
        :type chat_id: str

        """
        self._token = token
        self._chat_id = chat_id

    def _send_photo(self, photo_path: str):
        url = f"https://api.telegram.org/bot{self._token}/sendPhoto"
        files = {'photo': open(photo_path, 'rb')}
        data = {'chat_id': self._chat_id}
        requests.post(url, files=files, data=data)

    def _send_msg(self, msg: str):
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {'chat_id': self._chat_id, 'text': msg}
        requests.post(url, data=data)

    @staticmethod
    def _check_for_updates(last_modified_time: float | None, tensorboard_path: str):
        # get the list of the files in the tensorboard path
        files = os.listdir(tensorboard_path)
        current_modified_time = max([os.path.getmtime(os.path.join(tensorboard_path, file)) for file in files])
        if current_modified_time != last_modified_time:
            return True, current_modified_time
        return False, last_modified_time

    def run(self, experiment_name: str,
            update_interval: int,
            plot_config: List[Dict[str, Any]],
            tensorboard_path: str):
        """ Run the bot

        :param experiment_name: name of the experiment
        :type experiment_name: str

        :param update_interval: interval in minutes to check for updates
        :type update_interval: int

        :param plot_config: configuration for the plots
        :type plot_config: List[Dict[str, Any]]

        :param tensorboard_path: path to the Tensorboard logs
        :type tensorboard_path: str

        :raises FileNotFoundError: if the tensorboard path does not exist

        """
        if not Path(tensorboard_path).exists():
            raise FileNotFoundError(f"Path {tensorboard_path} does not exist")

        self._send_msg(f'TensorBot started to monitor experiment: {experiment_name} 🚀')
        self._send_msg('Checking for updates every {} minutes'.format(update_interval))

        last_modified_time = None
        while True:
            update_needed, last_modified_time = self._check_for_updates(last_modified_time, tensorboard_path)
            if update_needed:
                tmp_paths, train_info = plot_tensorboard_experiment(exp_path=tensorboard_path,
                                                                    plot_config=plot_config)

                self._send_msg(f'Experiment: {experiment_name} updated! 🚀')
                self._send_msg(f'Training time: {train_info["training_time"]/3600:.2f} hours')
                self._send_msg(f'Training steps: {train_info["training_steps"]}')
                for tmp_path in tmp_paths:
                    self._send_photo(tmp_path)
                    Path(tmp_path).unlink()

            time.sleep(60 * update_interval)
