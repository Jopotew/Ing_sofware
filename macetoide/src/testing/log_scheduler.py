from datetime import time
from macetoide.src.repositorys.log import instance as log_repository


class LogScheduler:
    """
    desde main se ejecuta cada 1 min para verificar si se debe generar un log

    """

    def run():
        # pot manager/repo obtener todos los pot existentes
        all_pots = []
        for pot in all_pots:
            current_time = time.now()
            if (
                pot.last_checked is not None
                and current_time - pot.last_checked >= pot.analysis_time * 60
            ):
                log = pot.generate_log()
                log_repository.save(log)
                pot.set_last_check(current_time)
