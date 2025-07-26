from utils.file_parser import parse_file
from utils.chunking import chunk_texts

class IngestionAgent:
    def process_file(self, file):
        text = parse_file(file)
        return chunk_texts(text)