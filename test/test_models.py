from datetime import datetime, timedelta
from pprint import pp

from src.maps import create_place, create_business
from src.models import Errand, Trip

business_input = "Great Wall Market Monterey Park"
gw_supermarket_mpk = create_business(business_input)

pp(gw_supermarket_mpk)

buy_asian_groceries = Errand(name="Buy asian groceries",
                             duration=timedelta(minutes=30),
                             business=gw_supermarket_mpk,
                             notes=[
                                 "frozen dumplings",
                                 "kimchi",
                                 "korean BBQ marinade",
                                 "Brown rice",
                                 "stir fry sauce",
                                 "natto"
                             ])

pp(buy_asian_groceries)

home = "242 Keller St. Monterey Park"
origin = create_place(home)

trip = Trip(day=datetime.now(),
            origin=origin,
            destination=origin,
            depart_after="2PM",
            arrive_by="5PM")

pp(trip)