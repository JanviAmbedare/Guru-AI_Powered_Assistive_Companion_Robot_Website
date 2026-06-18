import cloudinary.uploader


class CloudinaryService:

    @staticmethod
    def upload_file(
        file,
        folder,
        resource_type="auto"
    ):

        try:

            # FastAPI UploadFile
            if hasattr(file, "file"):

                file.file.seek(0)

                return cloudinary.uploader.upload(

                    file.file,

                    folder=folder,

                    resource_type=resource_type
                )

            # File-like object
            file.seek(0)

            return cloudinary.uploader.upload(

                file,

                folder=folder,

                resource_type=resource_type
            )

        except Exception as e:

            print(
                "CLOUDINARY UPLOAD ERROR:",
                str(e)
            )

            raise

    @staticmethod
    def delete_file(
        public_id
    ):

        return cloudinary.uploader.destroy(
            public_id
        )