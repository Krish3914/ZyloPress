# DataSqueeze File Compression/Decompression Tool

This repository contains a Python implementation of a Huffman Coding GUI application that allows users to compress and decompress text files. The application uses the Tkinter library for the graphical user interface (GUI).

## Demo Video
Watch it Here https://drive.google.com/file/d/14yzkUoFC6oEp2mPFhxY-9QcPc1T4p8Mo/view?usp=sharing

## Features
- Can compress and decompress <b>multiple files at once</b>.
- Compresses the <b>original file with upto 50% file size reduction</b>.
- Display the <b>original and compressed file sizes</b>.

## Limitations

- The Huffman Coding algorithm may take longer to compress and decompress larger text files as it compresses and decompresses one character at a time instead of a chunk of
characters.
- The compressed file may be larger than the original file if the original file size is too small. This is because the compressed file needs to include the decoding dictionary to decode, which increases the file size.

## Installation

To run the Huffman Coding GUI application, you need to have Python installed on your system. You can download Python from the official website: https://www.python.org/downloads/

Once Python is installed, follow these steps:

1. Clone this repository:
```
git clone https://github.com/your-username/huffman-coding-gui.git
```

3. Navigate to the cloned repository:
```
cd huffman-coding-gui
```

## Usage

To run the Huffman Coding GUI application, execute the following command in the terminal or command prompt:

```
python main.py
```

This will open the GUI window where you can select the text files you want to compress or decompress.

## Executable

An executable named `main.exe` is also provided in the repository for Windows users. You can download it and run it directly on your system.

## Code Explanation

The code provided is a Python script that implements the Huffman Coding algorithm and creates a GUI using Tkinter. The main components of the code are:

1. `HeapNode` class: Represents a node in the Huffman tree.
2. `HuffmanCoding` class: Implements the Huffman Coding algorithm for compression and decompression.
3. `HuffmanCodingGUI` class: Creates the GUI using Tkinter and integrates the HuffmanCoding class for file compression and decompression.

The code uses the `heapq` module to create a min-heap for the Huffman tree construction.

## Contributing

If you would like to contribute to this project, please fork the repository, make your changes, and submit a pull request. I would be happy to review and merge your contributions.
