class Job:
    def __init__(self, uuid, created_at, processed, url, directory, filename):
        self.filename = filename
        self.directory = directory
        self.url = url
        self.processed = processed
        self.uuid = uuid
        self.created_at = created_at
