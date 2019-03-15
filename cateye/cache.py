from base.cache import EquipmentCache, CacheExpiryTime

class CatEyeCache(EquipmentCache):
    def set_latest_software_version(self, latest, expires_in = CacheExpiryTime.FIVE_MINUTES):
        self.cache.set("cateye_latest_software_version", latest, expires_in)

    def get_latest_software_version(self):
        return self.cache.get("cateye_latest_software_version")

    def set_device_id_last_seen(self, device_id, last_seen, expires_in = CacheExpiryTime.FIVE_MINUTES):
        key = "cateye_{}_last_seen".format(device_id)
        self.cache.set(key, last_seen, expires_in)

    def get_device_id_last_seen(self, device_id):
        key = "cateye_{}_last_seen".format(device_id)
        return self.cache.get(key)
