import os
from datetime import datetime
from picamera2 import Picamera2


class ImageData:
    """
    Data model representing an image captured by the Raspberry Pi camera.
    """

    def __init__(self, file_name: str, capture_time: str):
        """
        Initialize the CameraImageData object with file name and capture time.

        :param file_name: The path or name of the saved image file.
        :param capture_time: A string representing the date and time at which the image was captured.
        """
        self.file_name = file_name
        self.capture_time = capture_time


class Camera:
    """
    Model for managing a Raspberry Pi camera using the picamera2 library.
    Provides a method to capture and save images with a timestamp.
    """

    def __init__(self):
        """
        Initialize the RaspberryPiCamera by creating an instance of Picamera2.
        """
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
        self.camera.start()

    def capture_image(self) -> ImageData:
        """
        Capture an image using the Raspberry Pi camera, save it to the 'captures' folder
        with a timestamp-based file name, and return CameraImageData with relevant details.

        :return: A CameraImageData object containing file name and capture time.
        """
        # Create captures folder if it doesn't exist
        os.makedirs("captures", exist_ok=True)

        # Build timestamp and file name
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M")
        file_name = f"captures/image_{formatted_time}.jpg"

        # Capture the image and save
        self.camera.capture_file(file_name)

        # Return data model with file information
        return ImageData(file_name=file_name, capture_time=formatted_time)
