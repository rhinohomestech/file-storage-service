import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="de83kdkfj",
    api_key="578558818658942",
    api_secret="ZtYAlEe2yTdJEHAjIMSHuaHF75g"
)

def upload_file_to_cloudinary(file):
    response = cloudinary.uploader.upload(file)
    return {
        "cloudinary_id": response.get("public_id"),
        "url": response.get("secure_url"),
    }
