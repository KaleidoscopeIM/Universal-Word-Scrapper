

def handle_error(error_type, details):
    if error_type == "IMAGE_DOWNLOAD_ERROR":
        file = open('D:\Video Work Area\GRE WORDS APP\data\logs\error.log', 'a+')
        file.write("#################################\n")
        file.write("Error in downloading image for : "+details.get("word") + "\n")
        file.write("URL :"+details.get("word_url")+"\n")
        file.write("Image URL: "+details.get("image_url")+"\n")
        file.write("Image name: " + details.get("img_name") + "\n")
        file.flush()
        file.close()


def handle_logging(log_type, details):
    if log_type == "IMAGE_DOWNLOAD_SUCCESS":
        file = open('D:\Video Work Area\GRE WORDS APP\data\logs\error.log', 'a+')
        file.write("#################################\n")
        file.write("successfully downloaded image for : "+details.get("word") + "\n")
        file.write("Image URL: "+details.get("image_url")+"\n")
        file.write("Image name: " + details.get("img_name") + "\n")
        file.flush()
        file.close()
