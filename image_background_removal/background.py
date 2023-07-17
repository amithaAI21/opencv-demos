from rembg import remove
import tkinter as tk
from tkinter import filedialog
from PIL import Image

input_path = "media/eagle.jpeg"
output_path = 'output.png'
input = Image.open(input_path)
output = result = remove(input)
output.save(output_path) 
