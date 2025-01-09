import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print("Failed to grab frame")
        break

    # Decode QR codes from the current frame
    codes = decode(frame)

    # Loop through all detected codes
    for code in codes:
        if code.type == 'QRCODE':  # Check if it's a QR code
            # Draw a rectangle around the QR code
            points = code.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # Decode and print QR code data
            qr_data = code.data.decode('utf-8')
            print(f"QR Code Detected: {qr_data}")

            # Split the QR code data into fields
            fields = qr_data.split('|')
            if len(fields) == 4:
                identifier = fields[0]
                model_number = fields[1]
                destination_code = fields[2]
                serial_number = fields[3]

                # Trim the model number to the first 7 characters
                trimmed_model_number = model_number[:7]

                # Display the extracted data
                print(f"Identifier: {identifier}")
                print(f"Model Number: {model_number} (Trimmed: {trimmed_model_number})")
                print(f"Destination Code: {destination_code}")
                print(f"Serial Number: {serial_number}")

                # Display the decoded data on the image
                x, y, w, h = code.rect
                cv2.putText(frame, f"Model: {trimmed_model_number}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the frame with QR codes highlighted
    cv2.imshow('QR Code Scanner', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
