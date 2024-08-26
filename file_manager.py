import os
import json
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any, List

class FileManager:
    def __init__(self, base_url: str):
        self.domain = urlparse(base_url).netloc
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = f"output_{self.domain}_{self.timestamp}"
        self.scraped_dir = os.path.join(self.base_dir, "scraped_content")
        self.summary_dir = os.path.join(self.base_dir, "summaries")
        self.metadata_file = os.path.join(self.base_dir, "metadata.json")
        
        self._create_directories()

    def _create_directories(self) -> None:
        os.makedirs(self.scraped_dir, exist_ok=True)
        os.makedirs(self.summary_dir, exist_ok=True)

    def save_scraped_content(self, url: str, content: str) -> None:
        filename = self._url_to_filename(url)
        filepath = os.path.join(self.scraped_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_summary(self, url: str, summary: str) -> None:
        filename = self._url_to_filename(url)
        filepath = os.path.join(self.summary_dir, f"{filename}_summary.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)

    def save_meta_summary(self, summary: str) -> None:
        with open(os.path.join(self.base_dir, f"{self.domain}_FULL_SUMMARY.txt"), 'w', encoding='utf-8') as f:
            f.write(summary)

    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

    def _url_to_filename(self, url: str) -> str:
        path = urlparse(url).path
        return (path.strip('/').replace('/', '_') or 'index') + '.txt'

    def get_scraped_files(self) -> List[str]:
        return [f for f in os.listdir(self.scraped_dir) if f.endswith('.txt')]

    def summary_exists(self) -> bool:
        return os.path.exists(os.path.join(self.summary_dir, "detailed_summary.txt"))