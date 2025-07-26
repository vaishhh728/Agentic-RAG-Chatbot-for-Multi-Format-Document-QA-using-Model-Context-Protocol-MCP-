class DocumentStore:
    def __init__(self):
        self.data = []

    def add_chunks(self, chunks):
        self.data.extend(chunks)

    def get_chunk(self, index):
        return self.data[index] if index < len(self.data) else ""