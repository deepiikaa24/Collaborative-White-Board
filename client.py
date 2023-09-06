import socket
import threading
import tkinter as tk

HOST = 'localhost'
PORT = 5000

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Initialize the Tkinter app
root = tk.Tk()
root.title('Collaborative Whiteboard')

# Set up the canvas for drawing
canvas = tk.Canvas(root, width=550, height=500, bg='white')
canvas.pack()

# Keep track of the current position of the mouse
prev_x, prev_y = None, None

# Handle mouse button presses on the canvas
def mouse_press(event):
    global prev_x, prev_y
    prev_x, prev_y = event.x, event.y

# Handle mouse motion on the canvas
def mouse_motion(event):
    global prev_x, prev_y
    if prev_x and prev_y:
        x, y = event.x, event.y
        canvas.create_line(prev_x, prev_y, x, y, width=5)
        message = f'{prev_x},{prev_y},{x},{y}'
        client_socket.send(message.encode('utf-8'))
        prev_x, prev_y = x, y

# Bind mouse events to the canvas
canvas.bind('<Button-1>', mouse_press)
canvas.bind('<B1-Motion>', mouse_motion)

# Receive data from the server and draw on the canvas
def receive_data():
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                message = data.decode('utf-8')
                x1, y1, x2, y2 = [int(i) for i in message.split(',')]
                canvas.create_line(x1, y1, x2, y2, width=5)
            else:
                client_socket.close()
                break
        except:
            client_socket.close()
            break

# Start a new thread to receive data from the server
receive_thread = threading.Thread(target=receive_data)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()
