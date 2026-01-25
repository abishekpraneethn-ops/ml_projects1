import sys
import traceback
import logging
from logger import get_logger

logger = get_logger(__name__)

def error_message_detail(error, error_detail: sys):
    """
    Extracts detailed error information including file name and line number.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in script: [{file_name}] "
        f"at line number [{line_number}] "
        f"error message [{str(error)}]"
    )

    return error_message


class CustomException(Exception):
    """
    Custom exception class for project-wide error handling.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    import sys

    def test_exception():
        try:
            a = 10 / 0
        except Exception as e:
            logger.info("Divide by zero error")
            raise CustomException(e, sys)

    test_exception()
