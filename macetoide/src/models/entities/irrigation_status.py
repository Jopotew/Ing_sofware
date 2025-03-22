class StatusIrrigation:
    """
    Class that represents the irrigation status (0 = no irrigation, 1 = irrigated).
    """

    def __init__(self, status: bool = False):
        """
        Initializes the irrigation status.
        """
        self.status = status
