class RBFeedback:
    def __init__(self, user_id: int | None = None):
        self.user_id = user_id

    def to_dict(self) -> dict:
        data = {
            'user_id': self.user_id,
        }
        return {key: value for key, value in data.items() if value is not None}
