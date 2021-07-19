import time
from plyer import notification


def slaughter():

    days = " (Days Left) "
    pig_id = " (Pig ID) "

    notification.notify(
        title="Slaughter Recommendation",
        message="Slaughter Pig" + pig_id + " in " + days + "days",
        timeout=2  # displaytime
    )

    time.sleep(7)


slaughter()
