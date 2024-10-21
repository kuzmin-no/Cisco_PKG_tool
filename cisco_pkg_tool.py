#!/usr/bin/env python3

import os
import argparse

def check_file_type(filename):
    '''
    Check PGK file header
    :param filename: PKG file name
    :return: True/False - if PKG file is valid
    '''
    with open(filename, "rb") as binary_file:
        buffer = binary_file.read(3).decode("ascii")
        return buffer == "pkg"

def extract_file(pkg_filename, file_name_to_extract, destination_folder, file_ptr, file_size):
    '''
    Extract one file from PKG archive
    :param pkg_filename: PKG file name
    :param file_name_to_extract: File name to extract
    :param destination_folder: Destination folder where the file will be extracted
    :param file_ptr: Pointer in PKG file
    :param file_size: The size of file to extract
    :return:
    '''
    # Reading a file from PKG archive
    with open(pkg_filename, "rb") as binary_file:
        binary_file.seek(file_ptr)
        buffer = binary_file.read(file_size)
    # Remove non-printable characters from file name
    mapping_non_printable = dict.fromkeys(range(32))
    file_name_to_extract = file_name_to_extract.translate(mapping_non_printable)
    # Prepare full path and create folders if required
    if file_name_to_extract.startswith("/"):
        file_name_to_extract = file_name_to_extract[1:]
    destination_file_name = os.path.join(destination_folder, file_name_to_extract)
    try:
        if not os.path.exists(os.path.dirname(destination_file_name)):
            os.makedirs(os.path.dirname(destination_file_name))
        # Saving the new file
        with open(destination_file_name, "wb") as binary_file:
            binary_file.write(buffer)
    except OSError as error:
        print(f"Error: {error}")

def get_file_description(binary_file):
    # File ID
    file_id = int.from_bytes(binary_file.read(2))
    # File ptr
    file_ptr = int.from_bytes(binary_file.read(4))
    # File size
    file_size = int.from_bytes(binary_file.read(4))
    binary_file.seek(4, 1)
    # File name
    file_name = ''
    while True:
        char = binary_file.read(1)
        if char == b'\00':
            break
        file_name += char.decode("ascii")
    return file_id, file_ptr, file_size, file_name

def list_all_files(filename, directory_ptr, file_count):
    with open(filename, "rb") as binary_file:
        binary_file.seek(directory_ptr)
        print("="*80)
        print("{:>7} {:>15} {:>11}  {}".format("File ID", "Pointer (hex)", "File size", "File name"))
        print("="*80)
        for file_number in range(file_count):
            (file_id, file_ptr, file_size, file_name) = get_file_description(binary_file)
            print("{:>7x} {:>15x} {:>11}  {}".format(file_id, file_ptr, file_size, file_name))

def extract_all_files(pkg_filename, directory_ptr, file_count, destination_folder):
    with open(pkg_filename, "rb") as binary_file:
        binary_file.seek(directory_ptr)
        for file_number in range(file_count):
            (file_id, file_ptr, file_size, file_name_to_extract) = get_file_description(binary_file)
            print("Extracting file: {}".format(file_name_to_extract))
            extract_file(pkg_filename, file_name_to_extract, destination_folder, file_ptr, file_size)
        pkgheader_file_size = binary_file.tell() + 2
    print(f"Writing file: pkgheader {pkgheader_file_size} bytes")
    extract_file(pkg_filename, "pkgheader", destination_folder, 0, pkgheader_file_size)

def get_pkg_file_info(filename):
    '''
    Get "File size", "Directory pointer" and "File count" from PKG archive
    :param filename: PKG file name
    :return: directory_ptr, file_count
    '''
    with open(filename, "rb") as binary_file:
        binary_file.seek(8)
        # File size
        print("File size: %s bytes" % int.from_bytes(binary_file.read(4)))
        binary_file.seek(4, 1)
        # Directory ptr
        directory_ptr = int.from_bytes(binary_file.read(2))
        print("Directory pointer: 0x%04x" % directory_ptr)
        binary_file.seek(2, 1)
        # File count
        file_count = int.from_bytes(binary_file.read(2))
        print("File count: %s" % file_count)
    return directory_ptr, file_count


def main():
    parser = argparse.ArgumentParser(
        prog='Cisco_PKG_tool',
        description='Extract files from Cisco PKG files')
    parser.add_argument('-f', '--filename', metavar='<pkg_filename>', required=True, type=str, help='PKG file name')
    parser.add_argument('-e', '--extract',  metavar='<destination_folder>', type=str, help='Extract files to destination folder')
    parser.add_argument('-l', '--list', action='store_true', help='List files in PKG archive')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print('Error: File "%s" does not exist' % args.filename)
        parser.print_help()
        exit(1)

    if not check_file_type(args.filename):
        print('Error: File "%s" is not PKG archive' % args.filename)
        parser.print_help()
        exit(1)

    (directory_ptr, file_count) = get_pkg_file_info(args.filename)

    if args.list:
        list_all_files(args.filename, directory_ptr, file_count)

    if args.extract:
        extract_all_files(args.filename, directory_ptr, file_count, args.extract)
        exit(0)

if __name__ == "__main__":
    main()
