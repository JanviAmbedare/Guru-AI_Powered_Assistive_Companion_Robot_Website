import cloudinary.uploader


class CloudinaryService:


    @staticmethod
    def upload_file(
        file_path,
        folder,
        resource_type="auto"
    ):

        result = cloudinary.uploader.upload(

            file_path,

            folder=folder,

            resource_type=resource_type
        )

        return result
    
    @staticmethod
    def delete_file(public_id):

        return cloudinary.uploader.destroy(
            public_id
        )