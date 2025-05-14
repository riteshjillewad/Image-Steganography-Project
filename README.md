# 🕵️ Multimedia Steganography App
A secure and interactive Streamlit web app for hiding encrypted messages in image files using **LSB steganography** and **Fernet encryption**. Users can upload images, encrypt and embed secret messages, then later extract and decrypt them with the correct key.

## 🔐 Features
- User authentication system
- Secure **Fernet encryption** for messages
- Hide secret messages in PNG/JPG images using **Least Significant Bit (LSB)** technique
- Automatically calculate image capacity for message embedding
- Real-time image editing (resize, rotate) before encoding
- Decode hidden messages with decryption key
- PDF report generation after decoding
- Downloadable encoded images
- Light/Dark theme toggle with modern UI styling

# 🧬 What is Steganography?
![Image](https://github.com/user-attachments/assets/3021bcef-ff98-4dd4-ba97-cf7a0f458813)
Steganography is the art and science of **hiding secret information** within ordinary, non-secret files — like images, audio, or video — in such a way that only the sender and intended recipient know of its existence. It differs from encryption, which hides the contents of a message, because steganography hides the existence of the message itself.
In this app, we use a form of image-based steganography:
- The secret message is first encrypted using the Fernet symmetric encryption method.
- Then, the encrypted message is embedded inside the least significant bits (LSBs) of the image pixels.
- These LSB changes are subtle and do not visibly affect the image.
- To retrieve the message, the image is decoded to extract the hidden bits, which are then decrypted using the original key.

**This dual approach of encryption + steganography increases both the security and the secrecy of the message**.

## 📸 App Screenshots

![Image](https://github.com/user-attachments/assets/c346dee2-d80d-4bae-a049-85efd469523a)

![Image](https://github.com/user-attachments/assets/946e2421-4263-4129-bea1-973f329c612b)

![image](https://github.com/user-attachments/assets/97e417a4-9f27-46bb-a0c3-65f80a045822)

![image](https://github.com/user-attachments/assets/40c6dc08-676f-4172-82c0-5e104e0da78e)




