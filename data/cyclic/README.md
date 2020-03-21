# Compute cyclic data for our CSV

Should be run from data subfolder like this :

python cyclic/build_cyclic.py --csv bigtable.csv --column datetime

This will add 4 new columns for cyclic time (time of the day and time of the year)
using angle and the cyclic logic more friendly for datascience analysis
Also adding a fith feature : the day of the week number

cyclic for time and date: https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/
