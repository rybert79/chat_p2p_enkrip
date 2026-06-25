# Encrypted Peer-to-Peer Chat

A simple peer-to-peer chat application built with Python sockets, threading, and Fernet encryption. The application allows two users to communicate securely using a shared room password.

## Features

* Real-time messaging
* End-to-end encrypted chat using Fernet
* Password-protected chat rooms
* Server and client modes
* Concurrent message receiving using threading
* Secure key generation from user passwords
* Command-line interface

## How It Works

### Room Creation

The server creates a chat room and sets a password.

The password is transformed into a Fernet-compatible encryption key using:

* SHA256 hashing
* URL-safe Base64 encoding

This ensures both users generate the same encryption key without directly sharing it.

### Authentication

When a client joins:

1. The client enters the room password.
2. The client encrypts a test message.
3. The server attempts to decrypt it.
4. If successful, access is granted.
5. If decryption fails, the password is rejected.

### Messaging

All chat messages follow this process:

```text id="svx1y7"
User Input
    ↓
Encrypt (Fernet)
    ↓
Socket Send
    ↓
Socket Receive
    ↓
Decrypt (Fernet)
    ↓
Display Message
```

Messages are never transmitted as plain text.

## Encryption

This project uses the Fernet implementation from the Cryptography library.

### Key Generation Flow

```text id="u8teu8"
Password
    ↓
SHA256 Hash
    ↓
Base64 Encoding
    ↓
Fernet Key
```

Both participants generate the same encryption key from the same password.

## Project Structure

```text id="bl1juv"
project/
│
└── main.py
```

## Requirements

### Python Packages

```bash id="y3y1v8"
pip install cryptography
```

### Standard Libraries

* socket
* threading
* hashlib
* base64

## Running the Application

Start the program:

```bash id="4tfx9d"
python main.py
```

Choose a mode:

```text id="cl2v0u"
server/client:
```

### Server

1. Select server mode.
2. Enter an IP address and port.
3. Create a room password.
4. Wait for a client connection.

### Client

1. Select client mode.
2. Enter the server IP address and port.
3. Enter the room password.
4. Start chatting.

## Example Workflow

```text id="efjkdt"
Server Starts
      ↓
Create Password
      ↓
Client Connects
      ↓
Password Verification
      ↓
Encryption Key Generated
      ↓
Secure Chat Session Begins
```

## Learning Objectives

This project was created to practice:

* Socket programming
* Client-server communication
* Threading
* Cryptography fundamentals
* Secure authentication concepts
* Message encryption and decryption
* Designing custom communication protocols

## Future Improvements

* Multi-user chat rooms
* Usernames
* Message timestamps
* Message history
* AES session key exchange
* File transfer support
* GUI version

## Security Note

This project is intended for educational purposes and learning cryptography concepts.

While Fernet provides strong authenticated encryption, this implementation has not been audited for production use.

## License

This project is intended for educational and learning purposes.
