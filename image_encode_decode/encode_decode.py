# Encoding and Decoding the image 

# importing libraries
import base64 #  encoding and decoding data in base64 format
import sys
import warnings
warnings.filterwarnings("ignore")

# Opening and reading the image file in binary form
image = open('/images/nature.jpeg','rb')
image_read = image.read()
image_read

# Encoding the image as a base64 string
image_64_encode = base64.encodebytes(image_read)
print("Image to Encoded string:",image_64_encode)

# Decoding the base64-encoded string to its original binary representation
image_64_decode = base64.decodebytes(image_64_encode)

# Opening a file to write the decoded image data in binary write mode
image_result = open('/images/new_scenary.jpg', 'wb')

# Printing the number of bytes written
print("The size of the decoded image:",image_result.write(image_64_decode))