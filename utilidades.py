ALLOWED_EXTENSIONS = {'jpeg','jpg', 'png', 'mp4', 'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()            

def get_media_type(extension):
  media_types = {
      "jpeg": "image/jpeg",
      "jpg": "image/jpeg",
      "png": "image/png",
      "mp4": "video/mp4",
      "mp3": "audio/mp3"
  }
  return media_types.get(extension.lower())