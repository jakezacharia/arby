from pydantic import BaseModel, computed_field

class WatchlistEntry(BaseModel):
    card_name: str
    set_name: str
    printing: str # ex. "Halo Foil", "Normal", "Foil"
    snipe_threshold: float # 1.10 = lowest <=110% of market, for example
    url: str # tcgplayer product url 

class CardPrice(BaseModel):
    card_name: str
    set_name: str
    product_id: int
    market_price: float
    lowest_listing: float
    
    @computed_field
    @property
    def ratio(self) -> float:
        if self.market_price != 0:
            return self.lowest_listing / self.market_price
        else: 
            return 0.0

class ArbitrageAlert(BaseModel):
    entry: WatchlistEntry
    price: CardPrice
    message: str