""" A weather object. Pure flavor. """
class EwWeather:
	# The identifier for this weather pattern.
	name = ""

	str_sunrise = ""
	str_day = ""
	str_sunset = ""
	str_night = ""

	def __init__(
		self,
		name="",
		sunrise="",
		day="",
		sunset="",
		night=""
	):
		self.name = name
		self.str_sunrise = sunrise
		self.str_day = day
		self.str_sunset = sunset
		self.str_night = night
