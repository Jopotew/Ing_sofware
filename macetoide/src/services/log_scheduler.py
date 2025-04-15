from datetime import datetime, timedelta
from repositories.pot import instance as pot_repository
from repositories.log import instance as log_repository
from models.entities.pot import Pot


class LogScheduler:
    def run(self):
        pots: list[Pot] = pot_repository.get_all()
        now = datetime.now()
        for pot in pots:
            if pot.last_checked is None:
                log_repository.trigger_analysis(pot)
                print(f"Log generado desde cero")
                continue
                

            next_time = pot.last_checked + timedelta(hours=pot.analysis_time)
            if now >= next_time:
                
                log_repository.trigger_analysis(pot)
                print(f"Log generado")
            else:
                print("no checkin")
