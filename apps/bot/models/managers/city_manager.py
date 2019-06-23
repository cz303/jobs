from bot.models.tables import City


def city_valid(city_name):
    city = City.objects.filter(name=city_name)
    return city
