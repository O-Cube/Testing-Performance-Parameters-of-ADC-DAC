# """
# Code for The Embedded Systems Test and Verification W22
# Part 1 of 2: Measurement Data Collection
# Obed Oyandut and Rustenis Tolpeznikas
# """

import u3
import pandas as pd
import os
import matplotlib.pyplot as plt

path = 'C:/Users/49152/Desktop/'
d = u3.U3()

# '''
#     IONumber: 0-7=FIO, 8-15=EIO, 16-19=CIO
#     PinList:
#     8-15: B-data line to 245 and 374 (Control)
#     16: Clock for 374 (DAC)
#     17: Clock for 374 (Control)
#     18: 245 Enable 0 - Enable, 1 - Disable
#     19: 245 Direction 0 - input, 1 - Output
# '''

# reversed order look-up-table
LUT = [0, 128, 64, 192, 32, 160, 96, 224, 16, 144, 80, 208, 48, 176, 112, 240,
       8, 136, 72, 200, 40, 168, 104, 232, 24, 152, 88, 216, 56, 184, 120,
       248, 4, 132, 68, 196, 36, 164, 100, 228, 20, 148, 84, 212, 52, 180,
       116, 244, 12, 140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60,
       188, 124, 252, 2, 130, 66, 194, 34, 162, 98, 226, 18, 146, 82, 210, 50,
       178, 114, 242, 10, 138, 74, 202, 42, 170, 106, 234, 26, 154, 90, 218,
       58, 186, 122, 250, 6, 134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214,
       54, 182, 118, 246, 14, 142, 78, 206, 46, 174, 110, 238, 30, 158, 94,
       222, 62, 190, 126, 254, 1, 129, 65, 193, 33, 161, 97, 225, 17, 145, 81,
       209, 49, 177, 113, 241, 9, 137, 73, 201, 41, 169, 105, 233, 25, 153, 89,
       217, 57, 185, 121, 249, 5, 133, 69, 197, 37, 165, 101, 229, 21, 149, 85,
       213, 53, 181, 117, 245, 13, 141, 77, 205, 45, 173, 109, 237, 29, 157,
       93, 221, 61, 189, 125, 253, 3, 131, 67, 195, 35, 163, 99, 227, 19, 147,
       83, 211, 51, 179, 115, 243, 11, 139, 75, 203, 43, 171, 107, 235, 27,
       155, 91, 219, 59, 187, 123, 251, 7, 135, 71, 199, 39, 167, 103, 231, 23,
       151, 87, 215, 55, 183, 119, 247, 15, 143, 79, 207, 47, 175, 111, 239,
       31, 159, 95, 223, 63, 191, 127, 255]


# The bit order on DUT-internal Bus reversed with regard to EIO-Port
# Should not be used on DAC!
def reverse_bit_order(uint8):
    return LUT[uint8]


# produce rising clock edge of control register
def clock_pulse_control():
    d.getFeedback(u3.BitStateWrite(IONumber=17, State=0))
    d.getFeedback(u3.BitStateWrite(IONumber=17, State=1))
    d.getFeedback(u3.BitStateWrite(IONumber=17, State=0))


# produce rising clock edge of DAC register
def clock_pulse_dac():
    d.getFeedback(u3.BitStateWrite(IONumber=16, State=0))
    d.getFeedback(u3.BitStateWrite(IONumber=16, State=1))
    d.getFeedback(u3.BitStateWrite(IONumber=16, State=0))


# read analog voltage from ain0
def get_analog_voltage():
    dac_bits = d.getFeedback(u3.AIN(PositiveChannel=0, NegativeChannel=31, LongSettling=False))
    analog_voltage = d.binaryToCalibratedAnalogVoltage(dac_bits, isLowVoltage=False, channelNumber=0)
    return analog_voltage


def write_results_to_file(results, name):
    # create file of result
    dframe = pd.DataFrame(results)
    # save output to file
    try:
        dframe.to_csv(path + name + '.csv', mode='w')
    except:
        os.rmdir(path + name + '.csv')
        dframe.to_csv(path + name + '.csv', mode='w')

    return dframe


def test_signal_conditioning_circuit():
    d.configU3(FIOAnalog=3,  # set AINs to analog
               DAC1Enable=1,  # enable DACs
               DAC0=1,  # DAC0 enable
               DAC1=1)  # DAC1 enable
    # initialize()
    dac_out = 0x00

    dac0 = []
    dac1 = []
    ain0 = []
    ain1 = []

    for i in range(255):
        d.getFeedback(u3.DAC0_8(Value=dac_out))
        d.getFeedback(u3.DAC1_8(Value=dac_out))
        dac_out += 0x01
        ain0bits, = d.getFeedback(u3.AIN(PositiveChannel=2, NegativeChannel=31, LongSettling=True, QuickSample=False))
        ain1bits, = d.getFeedback(u3.AIN(PositiveChannel=3, NegativeChannel=31, LongSettling=True, QuickSample=False))
        ain0_value = d.binaryToCalibratedAnalogVoltage(ain0bits, isLowVoltage=False, channelNumber=2)
        ain1_value = d.binaryToCalibratedAnalogVoltage(ain1bits, isLowVoltage=False, channelNumber=3)
        print('AIN0: ' + str(ain0_value) + ' Volt')
        print('AIN1: ' + str(ain1_value) + ' Volt')
        dac0.append(dac_out)
        dac1.append(dac_out)
        ain0.append(ain0_value)
        ain1.append(ain1_value)

    print(write_results_to_file({'dac0': dac0, 'dac1': dac1, 'ain0': ain0, 'ain1': ain1}, 'lab02_1'))


def init_dac():
    # EIO and CIO to output
    d.getFeedback(u3.PortDirWrite(Direction=[0x00, 0xff, 0xff], WriteMask=[0x00, 0xff, 0xff]))
    d.getFeedback(u3.PortStateWrite(State=[0x00, 0xff, 0xff], WriteMask=[0x00, 0xff, 0xff]))
    # Pulse on control register clock (CIO1)
    clock_pulse_control()

    d.getFeedback(u3.BitStateWrite(IONumber=18, State=0))
    d.getFeedback(u3.BitStateWrite(IONumber=18, State=0))


def write_DUT_buffer(data_value):
    d.getFeedback(u3.PortDirWrite(Direction=[0x00, 0x00, 0xff], WriteMask=[0x00, 0xff, 0x00]))
    d.getFeedback(u3.BitStateWrite(IONumber=18, State=1))  # 245 disable
    d.getFeedback(u3.BitStateWrite(IONumber=19, State=0))  # 245 B - A
    d.getFeedback(u3.BitStateWrite(IONumber=18, State=0))  # 245 enable

    d.getFeedback(u3.PortDirWrite(Direction=[0x00, 0xff, 0xff], WriteMask=[0x00, 0xff, 0x00]))  # EIO to out
    d.getFeedback(u3.PortStateWrite(State=[0x00, data_value, 0xff], WriteMask=[0x00, 0xff, 0x00]))  # write to EIO

    clock_pulse_dac()

    d.getFeedback(u3.PortDirWrite(Direction=[0x00, 0x00, 0xff], WriteMask=[0x00, 0xff, 0x00]))  # EIO to input
    d.getFeedback(u3.BitStateWrite(IONumber=18, State=1))  # 245 disable


def test_digital_to_analog():
    d.configU3(FIOAnalog=0x03,  # set AINs to analog
               EIOAnalog=0x00,  # set EIO to digital
               EIODirection=0x00,  # EIO to input
               EIOState=0x00,  # EIO null
               CIODirection=0x00,  # CIO to input
               CIOState=0x00  # CIO null
               )

    init_dac()

    ain0 = []
    ain1 = []

    for i in range(256):
        write_DUT_buffer(i)
        ain0bits, = d.getFeedback(u3.AIN(PositiveChannel=0, NegativeChannel=31, LongSettling=True, QuickSample=False))
        ain0_value = d.binaryToCalibratedAnalogVoltage(ain0bits, isLowVoltage=False, channelNumber=0)
        ain1bits, = d.getFeedback(u3.AIN(PositiveChannel=1, NegativeChannel=31, LongSettling=True, QuickSample=False))
        ain1_value = d.binaryToCalibratedAnalogVoltage(ain1bits, isLowVoltage=False, channelNumber=1)

        print('AIN0: ' + str(ain0_value) + ' Volt')
        print('AIN1: ' + str(ain1_value) + ' Volt')
        ain0.append(ain0_value)
        ain1.append(ain1_value)

    print(write_results_to_file({'ain0': ain0, 'ain1': ain1}, 'lab02_2'))
