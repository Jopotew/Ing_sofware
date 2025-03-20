class IrrigationEvent():
    def __init__(self, time_active, watered: bool):
        self.time_active: int = time_active
        self.watered: bool = watered