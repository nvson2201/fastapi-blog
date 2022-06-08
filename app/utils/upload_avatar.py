import secrets
from PIL import Image


async def upload_avatar(file):
    FILEPATH = "./static/images/"
    filename = file.filename

    # test.png >> ["test", "png"]
    extension = filename.split(".")[-1]
    # print(extension)
    if extension not in ["png", "jpg", "jpeg"]:
        return None

    # ./static/images/062b4d26414fdbd1040e.png
    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name

    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)
    file.close()

    return generated_name
