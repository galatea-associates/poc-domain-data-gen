class ValidationResult:

    def __init__(self, success, error_message):
        self.error_message = error_message
        self.success = success

    def check_success(self):
        return self.success

    def get_errors(self):
        return self.error_message
