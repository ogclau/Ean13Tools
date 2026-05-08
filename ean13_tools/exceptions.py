class EAN13Error(Exception):
    """Base exception for ean13_tools."""
    pass

class InvalidLengthError(EAN13Error):
    def __init__(self, got: int):
        super().__init__(f"EAN-13 must be 13 digits, got {got}.")

class InvalidCharactersError(EAN13Error):
    def __init__(self):
        super().__init__("EAN-13 must contain only digits (0-9).")

class InvalidCheckDigitError(EAN13Error):
    def __init__(self, expected: int, got: int):
        super().__init__(f"Invalid check digit: expected {expected}, got {got}.")

class InvalidPrefixLengthError(EAN13Error):
    def __init__(self, got: int):
        super().__init__(f"Prefix must be exactly 12 digits, got {got}.")
