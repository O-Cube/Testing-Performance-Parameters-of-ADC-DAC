# '''
# Code for The Embedded Systems Test and Verification W22
# Part 2 of 2: Analysis of the Measurement Data
# Obed Oyandut and Rustenis Tolpeznikas
# '''

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_test_signal_conditioning_results():
    # Please keep the python file with the csv data files
    # Else, adjust the path
    cfile = pd.read_csv('lab02_1.csv')
    ain0 = cfile['ain0'].values.tolist()
    ain1 = cfile['ain1'].values.tolist()
    voltage = np.arange(0, 5, 5 / 255)
    ain0_la = np.polyfit(ain0, voltage, 1)
    ain0_la_arr = []
    ain1_la = np.polyfit(ain1, voltage, 1)
    ain1_la_arr = []

    for i in range(255):
        ain0_la_arr.append((ain0_la[0] * i + ain0_la[1]) / 255 * 5)
        ain1_la_arr.append((ain1_la[0] * i + ain1_la[1]) / 255 * 5)

    # AIN0

    gain = ain0[254] / ain0_la_arr[254]
    offset = ain0_la_arr[0] - ain0[0]
    inl0_arr = abs(np.array(ain0) - np.array(ain0_la_arr))

    f = plt.figure()
    plt.plot(voltage, ain0, label="Measured Output Voltage")
    plt.plot(voltage, ain0_la_arr, label="Input Voltage")
    plt.plot(voltage, inl0_arr, label="Absolute difference of Input and Output")
    plt.xlabel('Input (V)oltage at Input 0')
    plt.ylabel('Measured (V) at Output 0')
    plt.legend()
    plt.show()

    print("For AIN0")
    print("The gain was calculated to be: " + str(gain) + " Volt, while the offset is: " + str(offset) + " Volt.")

    # AIN1

    gain = ain1[254] / ain1_la_arr[254]
    offset = ain1_la_arr[0] - ain1[0]
    inl1_arr = abs(np.array(ain1) - np.array(ain1_la_arr))

    f = plt.figure()
    plt.plot(voltage, ain1, label="Measured Output Voltage")
    plt.plot(voltage, ain1_la_arr, label="Input Voltage")
    plt.plot(voltage, inl1_arr, label="Absolute difference of Input and Output")
    plt.xlabel('Input (V)oltage at Input 1')
    plt.ylabel('Measured (V) at Output 1')
    plt.legend()
    plt.show()

    print("For AIN1")
    print("The gain was calculated to be: " + str(gain) + " Volt, while the offset is: " + str(offset) + " Volt.")


def plot_test_dac_results():
    cfile = pd.read_csv('lab02_2.csv')
    ain0 = cfile['ain0'].values.tolist()
    ain1 = cfile['ain1'].values.tolist()

    expected = np.arange(0, 5, 5 / 255)
    expected_inverted = expected[::-1]

    dnl0 = []
    dnl1 = []
    for i in ain0:
        min_i = np.abs(expected - i).argmin()
        dnl0.append(abs(expected[min_i] - i))

    for i in ain1:
        min_i = np.abs(expected - i).argmin()
        dnl1.append(abs(expected[min_i] - i))

    gain0 = ain0[254] / expected[254]
    offset0 = ain0[1] - expected[1]

    gain1 = ain1[1] / expected_inverted[1]
    offset1 = ain1[254] - expected_inverted[254]

    # For regular output
    f = plt.figure()
    plt.step(x=[x for x in range(255)], y=ain0)
    plt.step(x=[x for x in range(255)], y=expected)
    plt.step(x=[x for x in range(255)], y=abs(expected - ain0))

    plt.xlabel('DAC inputs')
    plt.ylabel('Voltage')
    plt.legend(['ain1 Measured ', 'ain1 expected', 'INL'])
    plt.title('AIN0 DAC output voltage Vs input bits (Regular)')

    plt.show()

    # For inverted output
    f = plt.figure()
    plt.step(x=[x for x in range(255)], y=ain1)
    plt.step(x=[x for x in range(255)], y=expected_inverted)
    plt.step(x=[x for x in range(255)], y=abs(expected_inverted - ain1))

    plt.xlabel('DAC inputs')
    plt.ylabel('(V)oltage')
    plt.legend(['ain1 Measured ', 'ain1 expected', 'INL'])
    plt.title('AIN1 DAC output voltage Vs input bits (Regular)')

    plt.show()

    # DNL regular
    f = plt.figure()
    plt.step(x=[x for x in range(255)], y=dnl0)

    plt.xlabel('DNL error value (Regular)')
    plt.ylabel('Size from 0 to 1 LSB')
    plt.title('AIN0 (Regular) DAC output DNL')

    plt.ylim([0, (5 / 255)])

    plt.show()

    # DNL inverted

    f = plt.figure()
    plt.step(x=[x for x in range(255)], y=dnl1)

    plt.xlabel('DNL error value (Inverted)')
    plt.ylabel('Size from 0 to 1 LSB')
    plt.title('AIN0 (Inverted) DAC output DNL')

    plt.ylim([0, (5 / 255)])

    plt.show()

    print("For AIN0")
    print("The gain was calculated to be: " + str(gain0) + " Volt, while the offset is: " + str(offset0) + " Volt.")

    print("For AIN1")
    print("The gain was calculated to be: " + str(gain1) + " Volt, while the offset is: " + str(offset1) + " Volt.")


plot_test_signal_conditioning_results()
plot_test_dac_results()
