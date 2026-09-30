"""Physical constants and unit conversions.

Values are standard references and are not study assumptions, so they live in
code rather than in the configuration file.
"""

from typing import Final

#: Standard gravity [m/s^2] (CGPM 1901, exact by definition).
G0: Final[float] = 9.80665

#: Lunar gravitational parameter [km^3/s^2] (JPL DE440 value, rounded).
MU_MOON_KM3_S2: Final[float] = 4902.800

#: Mean lunar radius [km] (IAU).
R_MOON_KM: Final[float] = 1737.4

#: Seconds per day [s].
SECONDS_PER_DAY: Final[float] = 86_400.0

#: Julian year [days].
DAYS_PER_YEAR: Final[float] = 365.25

#: Seconds per hour [s].
SECONDS_PER_HOUR: Final[float] = 3_600.0
