class IrrigationEvent:
    def __init__(self, id: int,  time_active: int, watered: bool):
        self.id: int = id
        self.time_active: int = time_active
        self.watered: bool = watered
