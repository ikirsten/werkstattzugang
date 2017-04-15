import config
import time #time module
from datetime import date
import holidays


if not date(int(time.strftime("%Y")),int(time.strftime("%m")),int(time.strftime("%d"))) in config.accesstimes['feiertage']:
	t = 1
else:
	t = 0

print(t)
#
