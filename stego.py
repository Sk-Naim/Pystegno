from PIL import Image

DELIMITER = "###"

def to_binary(data):
    return ''.join(format(ord(i), '08b') for i in data)

def encode_image(input_path, message, output_path):
    img = Image.open(input_path)
    img = img.convert("RGB")  # important for JPG

    width, height = img.size
    pixels = img.load()

    message += DELIMITER
    binary_message = to_binary(message)
    index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if index < len(binary_message):
                r = (r & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                g = (g & ~1) | int(binary_message[index])
                index += 1
            if index < len(binary_message):
                b = (b & ~1) | int(binary_message[index])
                index += 1

            pixels[x, y] = (r, g, b)

    img.save(output_path, "PNG")
    return output_path


def decode_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")

    pixels = img.load()
    width, height = img.size

    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""

    for byte in all_bytes:
        message += chr(int(byte, 2))
        if message.endswith(DELIMITER):
            break

    return message.replace(DELIMITER, "")