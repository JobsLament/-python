import sys
import struct
import xml.etree.ElementTree as ET

COMMANDS = {
    "LOAD_CONST": 0x93,
    "READ_MEM": 0x10,
    "WRITE_MEM": 0xBC,
    "SHIFT_RIGHT": 0xA3
}


def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_code = bytearray()
    root = ET.Element("Log")  # Корневой элемент XML

    for line in lines:
        line = line.strip()
        if line:  # Если строка не пустая
            binary_instruction = assemble_line(line)
            binary_code.extend(binary_instruction)
            print(f"Assembling: {line} -> {binary_instruction.hex()}")  # Отладка

            # Создаем запись в XML-логе
            log_entry = ET.SubElement(root, "Instruction")
            log_entry.set("command", line)
            log_entry.text = binary_instruction.hex()

    # Сохранение бинарного файла
    print("Binary code:", binary_code.hex())  # Отладка
    with open(output_file, 'wb') as f:
        f.write(binary_code)

    # Сохраняем лог-файл
    tree = ET.ElementTree(root)
    tree.write(log_file)


def assemble_line(line):
    parts = line.split()
    cmd = parts[0]
    if cmd == "LOAD_CONST":
        constant = int(parts[1])
        return struct.pack('>B I', COMMANDS[cmd], constant)
    elif cmd == "READ_MEM":
        address = int(parts[1])
        return struct.pack('>B I', COMMANDS[cmd], address)
    elif cmd == "WRITE_MEM":
        address = int(parts[1])
        return struct.pack('>B I', COMMANDS[cmd], address)
    elif cmd == "SHIFT_RIGHT":
        address = int(parts[1])
        return struct.pack(">B I", COMMANDS[cmd], address)
    else:
        raise ValueError(f"Ошибка, непонятная команда: {cmd}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Что вводить в консоль: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, output_file, log_file)
