from PIL import Image

def encode_message(image_path, secret_message, output_image="encoded_image.png"):
    """Encodes a secret message inside an image using LSB steganography."""
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure it's RGB mode
    
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'  # End delimiter
    pixels = list(image.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message too large to encode in image.")

    new_pixels = []
    message_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & 0xFE) | int(binary_message[message_index])  # Modify LSB of red channel
            message_index += 1
        if message_index < len(binary_message):
            g = (g & 0xFE) | int(binary_message[message_index])  # Modify LSB of green channel
            message_index += 1
        if message_index < len(binary_message):
            b = (b & 0xFE) | int(binary_message[message_index])  # Modify LSB of blue channel
            message_index += 1
        new_pixels.append((r, g, b))

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_image)

    print(f"✅ Secret message encoded successfully into {output_image}.")

def decode_message(image_path):
    """Decodes a secret message hidden inside an image using LSB steganography."""
    image = Image.open(image_path)
    pixels = list(image.getdata())

    binary_message = ''
    for pixel in pixels:
        for color in pixel[:3]:  # Only extract from RGB values
            binary_message += str(color & 1)

    # Convert binary to text
    message_bits = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join(chr(int(bit, 2)) for bit in message_bits)

    # Find the stop delimiter
    end_index = message.find('þ')  # End delimiter
    if end_index != -1:
        message = message[:end_index]

    print(f"🔓 Hidden message extracted: {message}")

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("🔒 Encode: python steganography.py encode <image_path> '<secret_message>'")
        print("🔓 Decode: python steganography.py decode <encoded_image>")
        sys.exit(1)

    action = sys.argv[1].lower()
    image_path = sys.argv[2]

    if action == "encode":
        if len(sys.argv) < 4:
            print("❌ Error: Please provide a secret message to encode.")
            sys.exit(1)
        secret_message = sys.argv[3]
        encode_message(image_path, secret_message)

    elif action == "decode":
        decode_message(image_path)

    else:
        print("❌ Invalid action. Use 'encode' or 'decode'.")
