# Vaishnavi Ladda PRN:21610076
import pyodbc
import io
from PIL import Image, ImageOps
import io

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-U4LPBNM\SQLEXPRESS;DATABASE=ADT;UID=sa;PWD=1234')
cursor = conn.cursor()

def compress_image(image_path, target_width, target_height):
    with Image.open(image_path) as img:
        compressed_img = ImageOps.fit(img, (target_width, target_height))
        compressed_img_byte_array = io.BytesIO()
        compressed_img.save(compressed_img_byte_array, format='PNG')
        return compressed_img_byte_array.getvalue()

image_path = './cart.png'
with Image.open(image_path) as img:
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format=img.format)
    img_data = img_byte_array.getvalue()
    size_in_memory = len(img_data)
    print(f"Size of img_data: {size_in_memory} bytes")
    
    cursor.execute('''
        INSERT INTO ImageTable (ImageName, ImageData)
        VALUES (?, ?)
    ''', (image_path, pyodbc.Binary(img_data)))
    conn.commit()
    print("Image data stored in the database.")

cursor.close()
conn.close()