EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Raspberry Pi Infrared Remote Control Circuits"
Date "2021-07-13"
Rev "1.0"
Comp "Michael Paul Korthals"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Transistor_BJT:BC547 Q1
U 1 1 60EFC544
P 3500 2750
F 0 "Q1" H 3691 2796 50  0000 L CNN
F 1 "BC547B" H 3691 2705 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 3700 2675 50  0001 L CIN
F 3 "https://www.onsemi.com/pub/Collateral/BC550-D.pdf" H 3500 2750 50  0001 L CNN
	1    3500 2750
	1    0    0    -1  
$EndComp
$Comp
L Device:LED LED1
U 1 1 60EFE7A8
P 4250 2750
F 0 "LED1" V 4289 2632 50  0000 R CNN
F 1 "yellow (receiving)" V 4198 2632 50  0000 R CNN
F 2 "" H 4250 2750 50  0001 C CNN
F 3 "~" H 4250 2750 50  0001 C CNN
	1    4250 2750
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x01_Female J4
U 1 1 60F0CAC1
P 7200 2350
F 0 "J4" H 7228 2376 50  0000 L CNN
F 1 "GND" H 7228 2285 50  0000 L CNN
F 2 "" H 7200 2350 50  0001 C CNN
F 3 "~" H 7200 2350 50  0001 C CNN
	1    7200 2350
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J1
U 1 1 60F0BD8F
P 7200 1450
F 0 "J1" H 7228 1476 50  0000 L CNN
F 1 "5V" H 7228 1385 50  0000 L CNN
F 2 "" H 7200 1450 50  0001 C CNN
F 3 "~" H 7200 1450 50  0001 C CNN
	1    7200 1450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J2
U 1 1 60F09437
P 7200 1750
F 0 "J2" H 7228 1776 50  0000 L CNN
F 1 "3V3" H 7228 1685 50  0000 L CNN
F 2 "" H 7200 1750 50  0001 C CNN
F 3 "~" H 7200 1750 50  0001 C CNN
	1    7200 1750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J3
U 1 1 60F07E35
P 7200 2050
F 0 "J3" H 7228 2076 50  0000 L CNN
F 1 "GPIO18 (BCM)" H 7228 1985 50  0000 L CNN
F 2 "" H 7200 2050 50  0001 C CNN
F 3 "~" H 7200 2050 50  0001 C CNN
	1    7200 2050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 60F001A7
P 3250 1900
F 0 "R4" H 3320 1946 50  0000 L CNN
F 1 "22 K" H 3320 1855 50  0000 L CNN
F 2 "" V 3180 1900 50  0001 C CNN
F 3 "~" H 3250 1900 50  0001 C CNN
	1    3250 1900
	1    0    0    -1  
$EndComp
$Comp
L irc:VS1838B InfraredReceiver
U 1 1 60EDC766
P 1600 2050
F 0 "InfraredReceiver" H 1588 2475 50  0000 C CNN
F 1 "VS1838B" H 1588 2384 50  0000 C CNN
F 2 "OptoDevice:Vishay_MOLD-3Pin" H 1550 1675 50  0001 C CNN
F 3 "" H 2250 2350 50  0001 C CNN
	1    1600 2050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 60EFABC1
P 3250 2250
F 0 "R2" H 3180 2204 50  0000 R CNN
F 1 "100 K" H 3180 2295 50  0000 R CNN
F 2 "" V 3180 2250 50  0001 C CNN
F 3 "~" H 3250 2250 50  0001 C CNN
	1    3250 2250
	-1   0    0    1   
$EndComp
$Comp
L Device:R R3
U 1 1 60EFDAE3
P 3600 2250
F 0 "R3" H 3530 2204 50  0000 R CNN
F 1 "820 R" H 3530 2295 50  0000 R CNN
F 2 "" V 3530 2250 50  0001 C CNN
F 3 "~" H 3600 2250 50  0001 C CNN
	1    3600 2250
	-1   0    0    1   
$EndComp
$Comp
L Device:CP C2
U 1 1 60EF8CDA
P 2750 3000
F 0 "C2" H 2868 3046 50  0000 L CNN
F 1 "100 uF" H 2868 2955 50  0000 L CNN
F 2 "" H 2788 2850 50  0001 C CNN
F 3 "~" H 2750 3000 50  0001 C CNN
	1    2750 3000
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 60EF81A0
P 2250 3000
F 0 "C1" H 2365 3046 50  0000 L CNN
F 1 "100 nF" H 2365 2955 50  0000 L CNN
F 2 "" H 2288 2850 50  0001 C CNN
F 3 "~" H 2250 3000 50  0001 C CNN
	1    2250 3000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 60EF7799
P 3000 1750
F 0 "R1" V 2793 1750 50  0000 C CNN
F 1 "100 R" V 2884 1750 50  0000 C CNN
F 2 "" V 2930 1750 50  0001 C CNN
F 3 "~" H 3000 1750 50  0001 C CNN
	1    3000 1750
	0    1    1    0   
$EndComp
Text Label 1000 1300 0    236  ~ 0
Receiver
Text Label 1000 4250 0    236  ~ 0
Transmitter
$Comp
L Device:R R1
U 1 1 60F29E17
P 1250 4750
F 0 "R1" H 1320 4796 50  0000 L CNN
F 1 "10 R" H 1320 4705 50  0000 L CNN
F 2 "" V 1180 4750 50  0001 C CNN
F 3 "~" H 1250 4750 50  0001 C CNN
	1    1250 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 60F2A3B8
P 1750 4750
F 0 "R2" H 1820 4796 50  0000 L CNN
F 1 "10 R" H 1820 4705 50  0000 L CNN
F 2 "" V 1680 4750 50  0001 C CNN
F 3 "~" H 1750 4750 50  0001 C CNN
	1    1750 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 60F2ABC9
P 2250 4750
F 0 "R3" H 2320 4796 50  0000 L CNN
F 1 "10 R" H 2320 4705 50  0000 L CNN
F 2 "" V 2180 4750 50  0001 C CNN
F 3 "~" H 2250 4750 50  0001 C CNN
	1    2250 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:LED LED1
U 1 1 60F2B4BB
P 1250 5050
F 0 "LED1" V 1289 4932 50  0000 R CNN
F 1 "ir" V 1198 4932 50  0000 R CNN
F 2 "" H 1250 5050 50  0001 C CNN
F 3 "~" H 1250 5050 50  0001 C CNN
	1    1250 5050
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED LED2
U 1 1 60F2C3AE
P 1750 5050
F 0 "LED2" V 1789 4932 50  0000 R CNN
F 1 "ir" V 1698 4932 50  0000 R CNN
F 2 "" H 1750 5050 50  0001 C CNN
F 3 "~" H 1750 5050 50  0001 C CNN
	1    1750 5050
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED LED3
U 1 1 60F2CC1C
P 2250 5050
F 0 "LED3" V 2289 4932 50  0000 R CNN
F 1 "ir" V 2198 4932 50  0000 R CNN
F 2 "" H 2250 5050 50  0001 C CNN
F 3 "~" H 2250 5050 50  0001 C CNN
	1    2250 5050
	0    -1   -1   0   
$EndComp
$Comp
L Transistor_BJT:BC547 Q1
U 1 1 60F2E573
P 1850 5750
F 0 "Q1" H 2041 5796 50  0000 L CNN
F 1 "BC547B" H 2041 5705 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 2050 5675 50  0001 L CIN
F 3 "https://www.onsemi.com/pub/Collateral/BC550-D.pdf" H 1850 5750 50  0001 L CNN
	1    1850 5750
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 60F31C0E
P 2200 5750
F 0 "R4" V 2407 5750 50  0000 C CNN
F 1 "220 R" V 2316 5750 50  0000 C CNN
F 2 "" V 2130 5750 50  0001 C CNN
F 3 "~" H 2200 5750 50  0001 C CNN
	1    2200 5750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1250 4600 1750 4600
Wire Wire Line
	1750 4600 2250 4600
Connection ~ 1750 4600
Wire Wire Line
	1250 5200 1750 5200
Wire Wire Line
	1750 5200 2250 5200
Connection ~ 1750 5200
Wire Wire Line
	1750 5200 1750 5550
$Comp
L Connector:Conn_01x01_Female J2
U 1 1 60F37B22
P 7200 5750
F 0 "J2" H 7228 5776 50  0000 L CNN
F 1 "GPIO17 (BCM)" H 7228 5685 50  0000 L CNN
F 2 "" H 7200 5750 50  0001 C CNN
F 3 "~" H 7200 5750 50  0001 C CNN
	1    7200 5750
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J1
U 1 1 60F393E6
P 7200 5450
F 0 "J1" H 7228 5476 50  0000 L CNN
F 1 "5V" H 7228 5385 50  0000 L CNN
F 2 "" H 7200 5450 50  0001 C CNN
F 3 "~" H 7200 5450 50  0001 C CNN
	1    7200 5450
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Female J3
U 1 1 60F3A573
P 7200 6050
F 0 "J3" H 7228 6076 50  0000 L CNN
F 1 "GND" H 7228 5985 50  0000 L CNN
F 2 "" H 7200 6050 50  0001 C CNN
F 3 "~" H 7200 6050 50  0001 C CNN
	1    7200 6050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R5
U 1 1 60F3C006
P 2900 6000
F 0 "R5" H 2970 6046 50  0000 L CNN
F 1 "100 K" H 2970 5955 50  0000 L CNN
F 2 "" V 2830 6000 50  0001 C CNN
F 3 "~" H 2900 6000 50  0001 C CNN
	1    2900 6000
	1    0    0    -1  
$EndComp
$Comp
L Transistor_BJT:BC547 Q2
U 1 1 60F3CF67
P 3200 6250
F 0 "Q2" H 3391 6296 50  0000 L CNN
F 1 "BC547B" H 3391 6205 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 3400 6175 50  0001 L CIN
F 3 "https://www.onsemi.com/pub/Collateral/BC550-D.pdf" H 3200 6250 50  0001 L CNN
	1    3200 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:LED LED4
U 1 1 60F3E4BC
P 3300 5250
F 0 "LED4" V 3339 5132 50  0000 R CNN
F 1 "yellow (sending)" V 3248 5132 50  0000 R CNN
F 2 "" H 3300 5250 50  0001 C CNN
F 3 "~" H 3300 5250 50  0001 C CNN
	1    3300 5250
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED LED5
U 1 1 60F3FC1D
P 4100 5250
F 0 "LED5" V 4139 5132 50  0000 R CNN
F 1 "green (power)" V 4048 5132 50  0000 R CNN
F 2 "" H 4100 5250 50  0001 C CNN
F 3 "~" H 4100 5250 50  0001 C CNN
	1    4100 5250
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R6
U 1 1 60F409DE
P 3300 4750
F 0 "R6" H 3370 4796 50  0000 L CNN
F 1 "820 R" H 3370 4705 50  0000 L CNN
F 2 "" V 3230 4750 50  0001 C CNN
F 3 "~" H 3300 4750 50  0001 C CNN
	1    3300 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R7
U 1 1 60F41722
P 4100 4750
F 0 "R7" H 4170 4796 50  0000 L CNN
F 1 "820 R" H 4170 4705 50  0000 L CNN
F 2 "" V 4030 4750 50  0001 C CNN
F 3 "~" H 4100 4750 50  0001 C CNN
	1    4100 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3300 6450 3300 6750
Wire Wire Line
	3300 6750 4100 6750
Wire Wire Line
	5200 6750 5200 6050
Wire Wire Line
	5200 6050 7000 6050
Wire Wire Line
	3300 6050 3300 5400
Wire Wire Line
	4100 5400 4100 6750
Connection ~ 4100 6750
Wire Wire Line
	4100 6750 5200 6750
Wire Wire Line
	4100 5100 4100 4900
Wire Wire Line
	3300 5100 3300 4900
Connection ~ 2250 4600
Wire Wire Line
	3300 4600 4100 4600
Connection ~ 3300 4600
Wire Wire Line
	4100 4600 5200 4600
Wire Wire Line
	5200 4600 5200 5450
Wire Wire Line
	5200 5450 7000 5450
Connection ~ 4100 4600
Wire Wire Line
	1750 5950 1750 6750
Wire Wire Line
	1750 6750 2600 6750
Connection ~ 3300 6750
Wire Wire Line
	2000 3150 2250 3150
Wire Wire Line
	2750 3150 2250 3150
Connection ~ 2250 3150
Wire Wire Line
	2850 1750 2750 1750
Wire Wire Line
	2000 1750 2000 1850
Wire Wire Line
	2000 2250 2000 3150
Wire Wire Line
	3150 1750 3250 1750
Wire Wire Line
	2000 2050 3250 2050
Wire Wire Line
	2250 2850 2250 1750
Connection ~ 2250 1750
Wire Wire Line
	2250 1750 2000 1750
Wire Wire Line
	2750 2850 2750 1750
Connection ~ 2750 1750
Wire Wire Line
	2750 1750 2250 1750
Wire Wire Line
	3600 3150 2750 3150
Connection ~ 2750 3150
Connection ~ 3250 1750
Connection ~ 3250 2050
Wire Wire Line
	3250 1750 7000 1750
Wire Wire Line
	3250 2050 7000 2050
Wire Wire Line
	3250 2100 3250 2050
Wire Wire Line
	3250 2750 3300 2750
Wire Wire Line
	3250 2400 3250 2750
Wire Wire Line
	3600 2100 3600 1450
Wire Wire Line
	3600 1450 7000 1450
Wire Wire Line
	3600 2950 3600 3150
Wire Wire Line
	3600 2400 3600 2500
Wire Wire Line
	3600 2500 4250 2500
Wire Wire Line
	4250 2500 4250 2600
Connection ~ 3600 2500
Wire Wire Line
	3600 2500 3600 2550
Wire Wire Line
	4250 2900 4250 3150
Wire Wire Line
	4250 3150 3600 3150
Connection ~ 3600 3150
Wire Wire Line
	4250 3150 5850 3150
Wire Wire Line
	5850 3150 5850 2350
Wire Wire Line
	5850 2350 7000 2350
Connection ~ 4250 3150
$Comp
L Connector:Raspberry_Pi_2_3 GPIOConnector
U 1 1 60F79429
P 9300 3600
F 0 "GPIOConnector" H 9300 5081 50  0000 C CNN
F 1 "Raspberry Pi Zero W" H 9300 4990 50  0000 C CNN
F 2 "" H 9300 3600 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 9300 3600 50  0001 C CNN
	1    9300 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2350 5750 2900 5750
Wire Wire Line
	2900 6150 2900 6250
Wire Wire Line
	2900 6250 3000 6250
Wire Wire Line
	2900 5850 2900 5750
Connection ~ 2900 5750
Wire Wire Line
	2900 5750 7000 5750
$Comp
L Device:CP C1
U 1 1 60F84BE0
P 2600 5500
F 0 "C1" H 2718 5546 50  0000 L CNN
F 1 "220 uF" H 2718 5455 50  0000 L CNN
F 2 "" H 2638 5350 50  0001 C CNN
F 3 "~" H 2600 5500 50  0001 C CNN
	1    2600 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 5350 2600 4600
Wire Wire Line
	2250 4600 2600 4600
Connection ~ 2600 4600
Wire Wire Line
	2600 4600 3300 4600
Wire Wire Line
	2600 5650 2600 6750
Connection ~ 2600 6750
Wire Wire Line
	2600 6750 3300 6750
$EndSCHEMATC
