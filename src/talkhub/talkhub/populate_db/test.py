from datetime import date

from rand_gen import RandGen
from rand_gen.providers import RandText

randgen = RandGen(provider=RandText)

print(date(1999, 12, 1))
