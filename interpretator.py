import sys
import struct
import xml.etree.ElementTree as ET

def interpret(binary_file, output_file, memory_range):
    memory = {}
    accumulator = 0

    with open(binary_file, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            opcode = ord(byte)

            if opcode == 0x93:  
                constant = struct.unpack('>I', f.read(4))[0]
                accumulator = constant
            elif opcode == 0x10: 
                address = struct.unpack('>I', f.read(4))[0]
                accumulator = memory.get(address, 0)
            elif opcode == 0xBC: 
                address = struct.unpack('>I', f.read(4))[0]
                memory[address] = accumulator
            elif opcode == 0xA3:  
                address = struct.unpack('>I', f.read(4))[0]
                accumulator >>= 1  
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

    # Сохранение результата в XML
    root = ET.Element("Results")
    for address, value in memory.items():
        if memory_range[0] <= address <= memory_range[1]:
            child = ET.SubElement(root, "result")
            child.set("address", str(address))
            child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(output_file)

if __name__ == "__main__":
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = (int(sys.argv[3]), int(sys.argv[4]))
    interpret(binary_file, output_file, memory_range)
