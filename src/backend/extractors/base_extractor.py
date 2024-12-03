import os
import fireworks.client


from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    def __init__(self):
        self.api_key = os.getenv("FIREWORKS_API_KEY")
        fireworks.client.api_key = self.api_key

    @abstractmethod
    def extract(self, file_path: str):
        pass