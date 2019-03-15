from external_api.base import ExternalAPIManager
from external_api.dummy import Dummy
from external_api.haolishi import HaoLiShi
from external_api.bangqi import BangQi
from external_api.samsung_air_conditioner import SamsungAirConditioner

external_api_manager = ExternalAPIManager()


__all__ = [ExternalAPIManager, Dummy, external_api_manager, HaoLiShi, BangQi, SamsungAirConditioner]
