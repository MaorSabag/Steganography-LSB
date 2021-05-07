#!/usr/bin/env python3

from PIL import Image
import binascii

def rgb2hex(r, g, b):
	return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex2rgb(hexcode):
    rgb = tuple((int(hexcode[1:3], 16), int(hexcode[3:5], 16), int(hexcode[5:], 16)))
    return rgb

def str2bin(msg):
    return ''.join([bin(ord(ch))[2:].zfill(8) for ch in msg])

def bin2str(binary):
    try:
        message = str(binascii.unhexlify('%x' % (int(binary, 2))), 'utf-8')
        return message
    except ValueError:
        return False


def encoding(hexcode, digit):
	if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None


def decoding(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None


def hide(file_path, message, bug=0, alpha=255):
    im = Image.open(file_path)
    binary = str2bin(message) + '1111111111111110'
    if im.mode in ('RGBA'):
        data = im.getdata()
        newData = []
        digit = 0

        for item in data:
            if(digit < len(binary)):
                if not bug:
                    newpix = encoding(rgb2hex(item[0], item[1], \
                        item[2]), binary[digit])
                else:
                    newpix = encoding(rgb2hex(item[0], item[1], \
                        item[2]), binary[digit], verb=1)

                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newData.append((r, g, b, alpha))
                    digit += 1
            else:
                newData.append(item)
        im.putdata(newData)
        im.save(file_path, "PNG")
        im.close()
        return "Success!"
    return "Incorrect image mode"



def retr(file_path):
    im = Image.open(file_path)
    binary = ''
    if im.mode in ('RGBA'):
        data = im.getdata()
        for item in data:
            digit = decoding(rgb2hex(item[0], item[1], item[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if(binary[-16:] == '1111111111111110'):
                    print("Message: ")
                    return bin2str(binary[:-16])
        return bin2str(binary)
    return "Incorrect image mode"



def main():
	filename = input("Enter the image location: ")
	users_chose = input("What do you wanna do?\n[1] Encode a message\n[2] Decode a message\n[3] Exit\n> ")
	if int(users_chose) == 1:
		message = input("Enter the message:\n> ")
		print(hide(filename, message))
	elif int(users_chose) == 2:
		print(retr(filename))
	else:
		exit(0)

	

if __name__ == "__main__":
	main()