from contextvars import ContextVar

X_REQUEST_ID = "X-Request-ID"


class RequestIdManager:
    def __init__(self):
        self.request_id = ContextVar(X_REQUEST_ID, default=None)

    def get(self):
        return self.request_id.get()

    def set(self, request_id):
        self.request_id.set(request_id)


request_id_manager = RequestIdManager()
