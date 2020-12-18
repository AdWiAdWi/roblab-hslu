import paramiko
from navigation.utils.camera import Camera


# Takes picture and downloads it to host using sftp
class TakePicture:

    def __init__(self):
        pass

    # Download a file via SFTP from the pepper to a local file system
    def download_file_from_pepper(self, config, remote_path, local_path):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            config.Ip,
            username=config.Username,
            password=config.Password
        )
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.remove(remote_path)
        sftp.close()
        ssh.close()

    # Take a picture using helper class camera
    def take_picture(self, robot):
        camera = Camera(robot)
        remote_folder_path = "/home/nao/recordings/cameras/"
        file_name = "my_picture.jpg"
        camera.take_picture(remote_folder_path, file_name)

        # Move file to local path and return location
        local = "C:/" + file_name
        remote = remote_folder_path + file_name
        self.download_file_from_pepper(robot.configuration, remote, local)
        print("Downloaded file from PepperTheWaiter")
        return local
