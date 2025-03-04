# Helper class for taking a picture
class Camera:
    __camera_id = 0  # Id for camera (0 = top camera)
    __resolution = 3  # Id for ALPhotoCapture 640x480px
    __picture_format = "jpg"

    def __init__(self, robot):
        self.__al_photo = robot.ALPhotoCapture
        self.configure_camera(self.__camera_id, self.__resolution, self.__picture_format)

    def configure_camera(self, camera_id, resolution, format):
        self.__al_photo.setCameraID(camera_id)
        self.__al_photo.setResolution(resolution)
        self.__al_photo.setPictureFormat(format)

    def take_picture(self, path, file_name):
        self.__al_photo.takePicture(path, file_name)
