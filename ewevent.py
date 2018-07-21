import ewutils
import ewcfg

"""
	Database persistence object describing some discrete event. Player
	death/resurrection, item discovery, etc.
"""
class EwEvent:
	id_server = ""

	event_type = None

	id_user = None
	id_target = None

	def __init__(
		self,
		id_server = "",
		event_type = None,
		id_user = None,
		id_target = None
	):
		self.id_server = id_server
		self.event_type = event_type
		self.id_user = id_user
		self.id_target = id_target

	"""
		Write event to the database.
	"""
	def persist(self):
		# TODO
		pass
