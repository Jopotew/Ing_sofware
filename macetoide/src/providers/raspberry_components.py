from gpiozero import LED


led_component = [
    {"component" : "led", "function": "processing", "colour": "red", "pin": 17},
    {"component" : "led", "function": "completion", "colour": "green", "pin": 27},
]

dht11 = [{"component" : "dht11", "function":"measure air humidity & temperature", "pin": 2 }]


soil_sensor = [{"component": "soil_sensor", "function": "measure soil humidity", "pin_cs": 3, "pin_clk": 3, "pin_dio":3 }]