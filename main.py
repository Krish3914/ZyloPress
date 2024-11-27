import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import heapq
import json

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left_node = None
        self.right_node = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if (other is None) or (not isinstance(other, HeapNode)):
            return False
        return self.freq == other.freq


class HuffmanCoding:
    def __init__(self):
        self.__min_heap = []
        self.__encoding_dict = {}
        self.__decoding_dict = {}
        self.compressed_extension = ".compress"
        self.decompressed_extension = "_decompressed.txt"

    def __make_frequency_dict(self, text):
        frequency_dict = {}
        for character in text:
            if character not in frequency_dict:
                frequency_dict[character] = 1
                continue
            frequency_dict[character] += 1
        return frequency_dict

    def __make_heap(self, frequency_dict:dict):
        for key in frequency_dict:
            node = HeapNode(key, frequency_dict[key])
            heapq.heappush(self.__min_heap, node)

    def __build_tree(self):
        while len(self.__min_heap) > 1:
            node1:HeapNode = heapq.heappop(self.__min_heap)
            node2:HeapNode = heapq.heappop(self.__min_heap)

            merged:HeapNode = HeapNode(None, node1.freq + node2.freq)
            merged.left_node = node1
            merged.right_node = node2

            heapq.heappush(self.__min_heap, merged)

    def __generate_codes(self):
        if not self.__min_heap:
            return
        root:HeapNode = heapq.heappop(self.__min_heap)
        current_code = ""
        self.__generate_codes_helper(root, current_code)

    def __generate_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.__encoding_dict[root.char] = current_code
            self.__decoding_dict[current_code] = root.char
            return

        self.__generate_codes_helper(root.left_node, current_code + "0")
        self.__generate_codes_helper(root.right_node, current_code + "1")

    def __get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.__encoding_dict[character]
        return encoded_text

    def __pad_encoded_text(self, encoded_text:str):
        if not encoded_text:
            return "00000000"  # Handle edge case for empty encoded text

        extra_padding = 8 - len(encoded_text) % 8
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = encoded_text + "0" * extra_padding
        return padded_info + encoded_text

    def __get_byte_array(self, padded_encoded_text):
        length_of_padded_text = len(padded_encoded_text)
        if length_of_padded_text % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray([int(padded_encoded_text[i:i+8], 2) for i in range(0, length_of_padded_text, 8)])
        return b

    def compress(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        output_path = file_name + self.compressed_extension

        with open(file_path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read().rstrip()
            frequency_dict = self.__make_frequency_dict(text)

            if len(frequency_dict) == 1:
                # Handle the single character case
                char = list(frequency_dict.keys())[0]
                self.__encoding_dict[char] = '0'  # Use a single code '0' for the unique character
                self.__decoding_dict['0'] = char
            else:
                self.__encoding_dict = {}  
                self.__decoding_dict = {}
                self.__make_heap(frequency_dict)
                self.__build_tree()
                self.__generate_codes()

            # Convert decoding_dict to JSON string
            decoding_dict_str = json.dumps(self.__decoding_dict)
            # Write the length of decoding_dict_str as a 4-byte integer
            output.write(len(decoding_dict_str).to_bytes(4, byteorder='big'))
            # Write decoding_dict_str as bytes
            output.write(bytes(decoding_dict_str, 'utf-8'))

            encoded_text = self.__get_encoded_text(text)
            padded_encoded_text = self.__pad_encoded_text(encoded_text)
            b = self.__get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print(f"Compressed {file_path} successfully to {output_path}")
        return output_path

    def __remove_padding(self, padded_encoded_text):
        if not padded_encoded_text:
            return ""

        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-extra_padding] if extra_padding else padded_encoded_text

        return encoded_text

    def __decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.__decoding_dict:
                character = self.__decoding_dict[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, compressed_file_path):
        filename, file_extension = os.path.splitext(compressed_file_path)
        if file_extension != self.compressed_extension:
            print('This is not a compressed file.\nSend a compressed file.')
            return
        output_path = filename + self.decompressed_extension

        with open(compressed_file_path, 'rb') as file, open(output_path, 'w') as output:
            # Read the length of decoding_dict_str
            length = int.from_bytes(file.read(4), byteorder='big')
            decoding_dict_str = file.read(length).decode('utf-8')
            self.__decoding_dict = json.loads(decoding_dict_str)

            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.__remove_padding(bit_string)
            decompressed_text = self.__decode_text(encoded_text)
            output.write(decompressed_text)

        print(f"Decompressed {compressed_file_path} successfully to {output_path}")
        return output_path


class HuffmanCodingGUI(tk.Tk):
    def __init__(self, huffman):
        super().__init__()
        self.huffman = huffman
        self.title("Huffman Coding GUI")
        self.geometry("500x350")
        self.configure(bg="#1c1c1c")


        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), background="#333333", foreground="#ffffff", padding=10)
        style.map("TButton", background=[("active", "#555555")])

        style.configure("TLabel", background="#1c1c1c", foreground="#ffffff", font=("Helvetica", 12))


        self.compress_button = ttk.Button(self, text="Compress", command=self.compress_files)
        self.compress_button.pack(pady=20)

        self.decompress_button = ttk.Button(self, text="Decompress", command=self.decompress_files)
        self.decompress_button.pack(pady=20)

        self.notification_label = ttk.Label(self, text="")
        self.notification_label.pack(pady=20)

    def compress_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if files:
            for i, file in enumerate(files):
                output_path = self.huffman.compress(file)
                original_size = os.path.getsize(file)
                compressed_size = os.path.getsize(output_path)
                self.notification_label.config(text=f"Compressed {file}\nOriginal size: {original_size} bytes\nCompressed size: {compressed_size} bytes")
            messagebox.showinfo("Success", "Files compressed successfully.")

    def decompress_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Compressed files", "*.compress")])
        if files:
            for i, file in enumerate(files):
                output_path = self.huffman.decompress(file)
                original_size = os.path.getsize(file)
                decompressed_size = os.path.getsize(output_path)
                self.notification_label.config(text=f"Decompressed {file}\nOriginal size: {original_size} bytes\nDecompressed size: {decompressed_size} bytes")
            messagebox.showinfo("Success", "Files decompressed successfully.")

if __name__ == "__main__":
    huffman = HuffmanCoding()
    app = HuffmanCodingGUI(huffman)
    app.mainloop()

