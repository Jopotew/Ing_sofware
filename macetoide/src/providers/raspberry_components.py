from gpiozero import LED


led_component = [
    {"component" : "led", "function": "processing", "colour": "red", "pin": 17},
    {"component" : "led", "function": "completion", "colour": "green", "pin": 27},
]

dht11 = [{"component" : "dht11", "pin": 2 }]