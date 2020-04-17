import pprint

import speech_recognition as s_r

pprint.pprint(s_r.Microphone.list_microphone_names())  # print all the microphones connected to your machine
