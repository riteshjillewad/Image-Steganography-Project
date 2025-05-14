import streamlit as st
from PIL import Image
import os
from cryptography.fernet import Fernet
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

# Ensure directories for saving files
UPLOAD_FOLDER = 'uploads'
ENCODED_FOLDER = 'encoded'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)


# Generate a new encryption key
def generate_key():
    return Fernet.generate_key()


# Encode message into an image
def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    binary_message = iter(binary_message)
    pixels = list(img.getdata())
    encoded_pixels = []

    for pixel in pixels:
        pixel = list(pixel)
        for i in range(3):  # Modify R, G, B channels
            try:
                pixel[i] = pixel[i] & ~1 | int(next(binary_message))
            except StopIteration:
                pass
        encoded_pixels.append(tuple(pixel))

    img.putdata(encoded_pixels)
    img.save(output_path)


# Decode message from an image
def decode_message(image_path):
    img = Image.open(image_path)
    binary_message = ''
    for pixel in list(img.getdata()):
        for channel in pixel[:3]:
            binary_message += str(channel & 1)
            if binary_message.endswith('1111111111111110'):
                binary_message = binary_message[:-16]
                byte_data = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
                decoded_message = ''.join([chr(int(byte, 2)) for byte in byte_data])
                return decoded_message
    return "No hidden message found or the image is not encoded properly."


# Encrypt a message
def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(message.encode()).decode()


# Decrypt a message
def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_message.encode()).decode()


# Calculate maximum message length based on the image size
def calculate_max_message_length(image_path):
    img = Image.open(image_path)
    # Image dimensions multiplied by 3 (RGB channels) divided by 8 to get the number of bits per character
    return (img.size[0] * img.size[1] * 3) // 8


# Decode hidden message from an image
def extract_message_from_image(image_path):
    img = Image.open(image_path)
    binary_message = ''
    for pixel in list(img.getdata()):
        for channel in pixel[:3]:  # Considering only RGB channels
            binary_message += str(channel & 1)  # Extract least significant bit
            if binary_message.endswith('1111111111111110'):  # End of message delimiter
                binary_message = binary_message[:-16]  # Remove delimiter
                byte_data = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
                decoded_message = ''.join([chr(int(byte, 2)) for byte in byte_data])
                return decoded_message
    return "No hidden message found or the image is not encoded properly."


# Function to generate the PDF report
def generate_pdf_report(img_info, decoding_result, decoded_message):
    # Create an in-memory PDF buffer
    buffer = BytesIO()

    # Create a PDF document
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 10)

    # Add title
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 750, "Steganography Decoding Report")

    # Add image details
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Image Filename: {img_info[0]}")
    c.drawString(50, 715, f"Image Resolution: {img_info[1]}")
    c.drawString(50, 700, f"Image File Size: {img_info[2]:.2f} MB")
    c.drawString(50, 685, f"Image Format: {img_info[3]}")

    # Add decryption details
    c.drawString(50, 655, f"Decryption Key: {decoding_result[1]}")
    c.drawString(50, 640, f"Decoding Result: {decoding_result[2]}")

    # Add decoded message
    c.drawString(50, 600, "Decoded Message:")
    c.setFont("Helvetica", 8)
    c.drawString(50, 585, decoded_message)

    # Save the PDF file to the buffer
    c.save()

    # Get the PDF content as bytes
    buffer.seek(0)
    pdf_content = buffer.read()

    return pdf_content


# Login page with animations and icons
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Multimedia Steganography App")
    st.write(
        "Securely hide messages in images, videos, and audio files. Discover the power of multimedia steganography! "
        "🔐🎤📹")

    st.write("**Please Login to Continue**")

    # Add a modern login form with animations and icons
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #667eea, #764ba2);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }
        .stTextInput input {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 5px;
            border: 2px solid #ffffff;
            padding: 10px;
            color: black;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stTextInput input:focus {
            border-color: #764ba2;
            box-shadow: 0 0 8px rgba(118, 75, 162, 0.8);
        }
        .stButton button {
            background-color: #764ba2;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #667eea;
            transform: translateY(-2px);
        }
        .login-icon {
            font-size: 50px;
            margin-bottom: 20px;
            animation: bounce 1.5s infinite;
        }
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-15px);
            }
        }
        </style>
        """, unsafe_allow_html=True)

    # Add icon for login
    st.markdown('<div class="login-icon">🔒</div>', unsafe_allow_html=True)

    username = st.text_input("**Username**", placeholder="Enter your username")
    password = st.text_input("**Password**", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
    st.stop()

# Streamlit app continues here after login
st.set_page_config(page_title="Image Steganography", layout="wide", initial_sidebar_state="expanded")

# Sidebar for settings like theme toggle
with st.sidebar:
    st.title("Settings")
    theme = st.radio("Select Theme", ("Light", "Dark"))
    if theme == "Dark":
        st.markdown(
            """
            <style>
            body {
                background-color: #121212;
                color: white;
            }
            .stButton button {
                background-color: #6200ea;
                color: white;
                border-radius: 8px;
            }
            .stButton button:hover {
                background-color: #3700b3;
            }
            .stTextInput input {
                background-color: #333333;
                color: white;
                border-color: #6200ea;
            }
            .stTextArea textarea {
                background-color: #333333;
                color: white;
                border-color: #6200ea;
            }
            .stSelectbox select {
                background-color: #333333;
                color: white;
                border-color: #6200ea;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <style>
            body {
                background-color: white;
                color: black;
            }
            .stButton button {
                background-color: #0047ab;
                color: white;
                border-radius: 8px;
            }
            .stButton button:hover {
                background-color: #002d72;
            }
            .stTextInput input {
                background-color: white;
                color: black;
                border-color: #0047ab;
            }
            .stTextArea textarea {
                background-color: white;
                color: black;
                border-color: #0047ab;
            }
            .stSelectbox select {
                background-color: white;
                color: black;
                border-color: #0047ab;
            }
            </style>
            """, unsafe_allow_html=True)

    st.header("Advanced Settings")
    custom_filename = st.text_input("Custom Encoded File Name", value="encoded_image")

# Main UI
st.title("Please choose a module to continue..")

tab1, tab2 = st.tabs(["**Encode Message**", "**Decode Message**"])

# Encoding Tab
with tab1:
    st.subheader("Encode a Message ✍️🔒")
    uploaded_file = st.file_uploader("**Upload an Image** 📸", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Save the uploaded file temporarily
        temp_file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Uploaded Image 📷", width=300)

        # Display image editing options
        img = Image.open(temp_file_path)
        st.sidebar.subheader("Edit Image Before Encoding")
        resize = st.sidebar.slider("Resize Image", 50, 200, 100)  # Resize percentage
        rotate = st.sidebar.slider("Rotate Image", 0, 360, 0)  # Rotation angle

        # Show image metadata
        img_size = os.path.getsize(temp_file_path)  # Get file size in bytes
        img_resolution = img.size  # Resolution (width, height)
        img_mode = img.mode  # Color mode (RGB, RGBA, etc.)

        st.subheader("Image Metadata 📸")
        st.write(f"**File Size:** {img_size / 1024:.2f} KB")
        st.write(f"**Resolution:** {img_resolution[0]} x {img_resolution[1]} pixels")
        st.write(f"**Color Mode:** {img_mode}")

        # Apply resize and rotate
        img = img.resize((int(img.width * resize / 100), int(img.height * resize / 100)))
        img = img.rotate(rotate)

        st.image(img, caption="Edited Image Preview", width=300)

    message = st.text_area("**Enter the Message to Encode** 📝", placeholder="Type your secret message here...")

    # Show real-time message length estimation
    if uploaded_file:
        max_length = calculate_max_message_length(temp_file_path)
        st.write(f"Maximum characters that can be encoded: {max_length} characters")

    if message:
        message_length = len(message)
        st.write(f"Message Length: {message_length} characters")

        remaining_capacity = max_length - message_length
        if remaining_capacity >= 0:
            st.write(f"Remaining capacity: {remaining_capacity} characters")
        else:
            st.warning("The message exceeds the maximum capacity! Reduce the message size.")

    if st.button("Encode 🔒"):
        if uploaded_file and message.strip():
            key = generate_key()
            cipher_suite = Fernet(key)
            encrypted_message = encrypt_message(message, key)
            output_filename = custom_filename + ".png"
            output_path = os.path.join(ENCODED_FOLDER, output_filename)

            try:
                encode_message(temp_file_path, encrypted_message, output_path)
                st.success("**Message encoded successfully!** 🔑🎉")
                st.image(output_path, caption="Encoded Image 🖼️", width=300)
                st.write("**Encryption Key 🔑 (Save this key to decode the message):**")
                st.code(key.decode(), language="plaintext")
                st.download_button("Download Encoded Image ⬇️", data=open(output_path, "rb").read(),
                                   file_name=output_filename)
            except Exception as e:
                st.error(f"Error during encoding: {e} ⚠️")
        else:
            st.error("Please upload an image and provide a valid message (not empty or just spaces). ⚠️")

# In the Decoding Tab
with tab2:
    st.subheader("Decode a Message")
    uploaded_file = st.file_uploader("**Upload an Encoded Image**", type=["png", "jpg", "jpeg"], key="decode_uploader")
    decryption_key = st.text_input("**Enter the Encryption Key**", type="password")

    if st.button("Decode"):
        if uploaded_file and decryption_key.strip():
            input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            # Save the uploaded file temporarily
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                # Extract the hidden message from the image
                extracted_message = extract_message_from_image(input_path)

                if extracted_message != "No hidden message found or the image is not encoded properly.":
                    # Display the decoded message in a sidebar or overlay
                    st.sidebar.subheader("Extracted Hidden Message 📝")
                    st.sidebar.text_area("Hidden Message", value=extracted_message, height=200)

                    # Now, decrypt the message if it exists
                    decrypted_message = decrypt_message(extracted_message, decryption_key.encode())
                    st.markdown(
                        f"<div style='padding: 20px; border-radius: 10px; background-color: #f9f9f9; box-shadow: 0 "
                        f"4px 8px rgba(0,0,0,0.2);'><strong>Decoded Message:</strong><br>{decrypted_message}</div>",
                        unsafe_allow_html=True)

                    # Generate report after decoding
                    if st.button("Generate Decoding Report 📑"):
                        # Get image info (filename, resolution, etc.)
                        img_info = (
                            uploaded_file.name, img.size, os.path.getsize(input_path) / (1024 * 1024), img.format)
                        decoding_result = ("Success", decryption_key, "Message decoded successfully")

                        # Generate the PDF report
                        report_pdf = generate_pdf_report(img_info, decoding_result, decrypted_message)

                        # Convert PDF to base64 to display in the Streamlit app
                        pdf_base64 = base64.b64encode(report_pdf).decode("utf-8")

                        # Embed the PDF in the Streamlit app using an iframe
                        st.markdown(
                            f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>',
                            unsafe_allow_html=True)

                else:
                    st.error(extracted_message)
            except Exception as e:
                st.error(f"Error during decoding: {e}")
        else:
            st.error("Please upload an encoded image and provide a valid encryption key (not empty or just spaces). ⚠️")
