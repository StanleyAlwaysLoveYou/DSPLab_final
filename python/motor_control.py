import argparse
import serial
import sys
import time

# TODO: Make sure teensy_port matches the port for Teensy
# given in the Arduino IDE, and bt_port matches the output
# of the Bluetooth manager when opening a serial connection
# to the HC-05
teensy_port = '/dev/ttyACM1'  # Teensy Serial port
bt_port = '/dev/rfcomm0'    # HC-05 port
bt_baud = 38400

serbt = serial.Serial(bt_port, bt_baud)


def send(command):
    
    print('Sending data...')
    # Sleep for a second for a chance to connect
    # time.sleep(1)
    serbt.write(command.encode('utf-8'))
    print(command)
    

def fft_bin_to_motor():
    ''' Control servo motors via bluetooth based on FFT of signal
        fed into the Teensy '''
    serbt = serial.Serial(bt_port, bt_baud)

    # initialize Serial port for Teensy connection
    ser = serial.Serial()
    ser.port = teensy_port  # Teensy Serial port
    ser.baudrate = 9600
    ser.timeout = None  # specify timeout when using readline()
    ser.open()
    if ser.is_open:
        print('Serial port now open. Configuration:\n')
        print(ser, '\n')  # print serial parameters
    while True:
        # Acquire and parse data from Serial port
        try:
            line = ser.readline()  # ascii
        except serial.SerialException:
            ser = serial.Serial()
            ser.port = teensy_port  # Teensy Serial port
            ser.baudrate = 9600
            ser.timeout = None  # specify timeout when using readline()
            try:
                ser.open()
            except serial.SerialException:
                continue
            if ser.is_open:
                continue

        # split incoming CSV by commas and store in a list
        line_as_list = line.strip().split(b' ')
        map_object = map(float, line_as_list)
        list_of_int = list(map_object)
        # print(list_of_int)

        # find FFT bin with max coefficient, skip if its 0
        max_bin = list_of_int.index(max(list_of_int))
        if max_bin == 0:
            continue
        print(max_bin)  # uncomment to see the index

        # TODO: Write 'L' to move the left servo, and 'R' to move the right servo.
        # Create your own logic that will move one of the servos at a time
        # based on the maximum FFT bin form the Teensy

        if max_bin <= 256:
            command = 'L'
        elif max_bin > 256:
            command = 'R'
        
        serbt.write(command.encode('utf-8'))  # write to the HC-05
        print(command)


def latency():
    ''' Measure the latency in a round-trip bluetooth packet
        to the HC-05 unit '''
    ser = serial.Serial(bt_port, bt_baud)

    print('Sending data...')
    temp = ""
    start = False
    start_time = time.time()
    ser.write('From RasPi'.encode('ascii'))

    # Define start_char and end_char
    start_char = 60
    end_char = 62

    while (True):
        if (ser.inWaiting() > 0):
            # Grab single character and find its ASCII code
            character = ser.read()
            latency = time.time() - start_time
            asciiOrd = ord(character)

            if (asciiOrd == start_char and start is True):
                temp = ""  # start over
            elif (asciiOrd == start_char and start is False):
                start = True
            elif (asciiOrd != start_char and asciiOrd != end_char and start is True):
                temp += character.decode('ascii')
            elif (asciiOrd == end_char and start is True):
                # Print our message + latency
                if len(temp) > 0:
                    try:
                        print('Receiving new reading:', temp, '\n')
                        # Acknowledge receipt of data
                        print(latency)
                        break
                    except Exception as e:
                        print(e)
                start = False
                temp = ""


def rate():
    ''' Measure data rate of bluetooth connection to HC-05 '''
    ser = serial.Serial(bt_port, bt_baud)

    print('Sending data...')
    # Sleep for a second for a chance to connect
    time.sleep(1)

    for i in range(100):
        ser.write((str(i) + '\n').encode('ascii'))
    print('End')


def size():
    ''' Output size of message sent in 'rate' '''
    s = ""
    for i in range(100):
        s += str(i) + '\n'
    print(sys.getsizeof(s), "bytes")


def main():
    global bt_baud, bt_port, teensy_port
    parser = argparse.ArgumentParser(description='EECS 452 Bluetooth Driver')
    parser.add_argument('function', metavar='function', type=str,
                        choices=['bt_fft', 'latency', 'rate', 'size', 'milestone1'],
                        help='The name of the function to run: "bt_fft", "latency", "rate", or "size"')
    parser.add_argument('-b', '--bt-baud', type=int, dest='bt_baud', default=bt_baud,
                        help='Baud Rate for HC-05 Module')
    parser.add_argument('-p', '--bt-port', type=str, dest='bt_port', default=bt_port,
                        help='/dev/<port> for HC-05 Module')
    parser.add_argument('--teensy-port', type=str, dest='teensy_port', default=teensy_port,
                        help='/dev/<port> for Teensy')
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='Print out serial port information for HC-05 and Teensy')
    parser.add_argument('-c', '--command', type=str, dest='command', default='s')
    args = parser.parse_args()

    if args.bt_baud is not None:
        bt_baud = args.bt_baud
    if args.bt_port is not None:
        bt_port = args.bt_port
    if args.teensy_port is not None:
        teensy_port = args.teensy_port
    if args.command is not None:
        command = args.command
        
    
    if args.debug:
        print("Debug:")
        print("bt_baud: ", bt_baud)
        print("bt_port: ", bt_port)
        print("teensy_port: ", teensy_port)
        print()

    if args.function == 'bt_fft':
        fft_bin_to_motor()
    elif args.function == 'latency':
        latency()
    elif args.function == 'rate':
        rate()
    elif args.function == 'size':
        size()
    elif args.function == 'milestone1':
        send(command)
        
    print('the end of the code')


if __name__ == '__main__':
    main()
