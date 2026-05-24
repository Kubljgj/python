import socket
# 10.0.3.149

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

receiver.bind(('0.0.0.0', 8080))

receiver.listen(1)
print('ресівер слухае на порту 5000')

connection, address = receiver.accept()
print(f"З'ЄДНАННЯ ВСТАНОВЛЕНО З ПОРТОМ {address}")

data = connection.recv(1024)
message = data.decode('utf-8')

print(f"port {address}: {message}")

connection.close()
receiver.close()



