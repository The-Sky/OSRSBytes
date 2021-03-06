#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
OSRSBytes() is an all-in-one Python library for Old School Runescape (OSRS) that features Item Information Lookup, Hiscores, and Market information.

EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)
"""

# Built-in/Generic Imports
import http.client
import json
import math
import urllib.request
from sys import exit

__author__ = 'Markis Cook'
__copyright__ = 'Copyright 2019, Markis H. Cook'
__credits__ = ['Markis Cook (Lead Programmer, Creator)']
__license__ = 'EPL-2.0 (https://github.com/Coffee-fueled-deadlines/OSRSBytes/blob/master/LICENSE)'
__version__ = '1.0.0.0'
__maintainer__ = 'Ralyks'
__email__ = 'cookm0803@gmail.com'
__status__ = 'Open'

################
#  Exceptions  #
################
class APIDown(Exception):
	pass

class DoNotRunDirectly(Exception):
	pass

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
	raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

############################
#  START: Hiscores Object  #
############################
class Hiscores(object):
	"""Hiscores class
	
	The Hiscores class deals with collecting the required
	information needed to fetch user information from in-game
	API.  After being supplied necessary information, Hiscores
	class then sets self.stats dictionary with user information.
	
	Args:
		self,
		username str: The username of the account that you
			      want to look up information on.
		actype   str: The account type of the account that
		              you want to lookup.  If not supplied
			      this argument defaults to 'N' Normal.
			      
	Returns:
		This object returns nothing.  Instead it sets the 
		value of self.stats with a dictionary of values
		keyed by the skill type. Example: self.stats['attack']
		
	Example Invocation:
		from OSRS-Hiscores import Hiscores
		account = Hiscores('Zezima', 'N')
		print(account.stats['attack']['level']) # displays attack level
	"""
	def __init__(self, username: str, actype='N'):
		self.username = username
		self.accountType = actype.upper()
		self.getHTTPResponse()

	def getHTTPResponse(self):
		"""getHTTPResponse() method
		
		The getHTTPResponse() method communicates with the OSRS Hiscores API
		and supplies the required information from self.username and
		self.actype to pull the given users stats and hiscore information.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			self.processResponse(): This method is always triggered, regardless
			                        of whether or not the query to the API returned
						successfully or not.
		"""

		conn = http.client.HTTPSConnection('secure.runescape.com')
		if self.accountType == 'N':
			conn.request("GET", "/m=hiscore_oldschool/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == 'IM':
			conn.request("GET", "/m=hiscore_oldschool_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "UIM":
			conn.request("GET", "/m=hiscore_oldschool_ultimate/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		elif self.accountType == "HIM":
			conn.request("GET", "/m=hiscore_oldschool_hardcore_ironman/index_lite.ws?player={}".format(self.username))
			self.response = conn.getresponse()
			self.status = self.response.status
		self.processResponse()

	def processResponse(self):
		"""processResponse() method
		
		The processResponse() method processes the response received during the
		getHTTPResponse() method.  It handles potential 404 errors, 403 errors
		and the like and sets self.errorMsg accordingly.  On successful Response
		data is stored in self.data and sent to the self.parseData() method.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			self.error(): This method is triggered whenever the self.status of
			              a request is not 200 (failed).
				      
			self.parseData(): This method is called when self.status is 200 (success)
		"""
		if self.status != 200:
			self.errorMsg = "Player name given not found in account type provided.  Valid account types are, 'N' (Normal), 'IM' (Iron Man), 'UIM' (Ultimate Iron Man), 'HIC' (Hardcore Iron Man)"
			self.error()
		else:
			self.data = self.response.read().decode('ascii')
			self.parseData()

	def parseData(self):
		"""parseData() method
		
		The parseData() method parses the self.data processed in the processResponse()
		method.  Data parsed in placed in the self.stats dictionary.
		
		Args:
			self
			
		Returns:
			None
			
		Triggers:
			None
		"""
		self.data = self.data.replace('\n',',')
		self.data = self.data.split(',')
		subset = {}

		# Totals
		info = {}
		info['rank']       = self.data[0]
		info['level']      = self.data[1]
		info['experience'] = self.data[2]
		subset['total']    = info

		skills = [
			'attack',
			'defense',
			'strength',
			'hitpoints',
			'ranged',
			'prayer',
			'magic',
			'cooking',
			'woodcutting',
			'fletching',
			'fishing',
			'firemaking',
			'crafting',
			'smithing',
			'mining',
			'herblore',
			'agility',
			'thieving',
			'slayer',
			'farming',
			'runecrafting',
			'hunter',
			'construction'
		]

		bountyHunter = [
			'bountyHunter',
			'bountyRouge',
		]

		clueScrolls = [
			'all',
			'beginner',
			'easy',
			'medium',
			'hard',
			'elite',
			'master'
		]

		lastManStanding = [
			'rank'
		]

		bosses = [
			'abyssal_sire',
			'alchemical_hydra',
			'barrows_chests',
			'bryophyta',
			'chambers_of_xeric',
			'chambers_of_xeric:_challenge_mode',
			'chaos_elemental',
			'chaos_fanatic',
			'commander_zilyana',
			'corporeal_beast',
			'crazy_archaeologist',
			'dagannoth_prime',
			'dagannoth_rex',
			'dagannoth_supreme',
			'deranged_archaeologist',
			'general_graardor',
			'giant_mole',
			'grotesque_guardians',
			'hespori',
			'kalphite_queen',
			'king_black_dragon',
			'kraken',
			'kreearra',
			'kril_tsutsaroth',
			'mimic',
			'obor',
			'sarachnis',
			'scorpia',
			'skotizo',
			'the_gauntlet',
			'the_corrupted_gauntlet',
			'theatre_of_blood',
			'thermonuclear_smoke_devil',
			'tzkal-zuk',
			'tztok-jad',
			'venenatis',
			'vetion',
			'vorkath',
			'wintertodt',
			'zalcano',
			'zulrah'
		]

		counter = 0
		# Skills
		for i in range(len(skills)):
			info = {}
			info['rank']       = int(self.data[counter+3])
			info['level']      = int(self.data[counter+4])
			info['experience'] = int(self.data[counter+5])
			level = int(info['level']+1)
			info['next_level_exp'] = math.floor(sum((math.floor(level + 300 * (2 ** (level / 7.0))) for level in range(1, level)))/4)
			info['exp_to_next_level'] = int(info['next_level_exp'] - info['experience'])
			subset[skills[i]] = info
			counter += 3

		# Bounty Hunter
		counter += 2
		for i in range(len(bountyHunter)):
			info = {}
			info['rank']       = int(self.data[counter])
			info['score']      = int(self.data[counter+1])
			subset[bountyHunter[i]] = info
			counter += 2

		# Clue Scrolls
		for i in range(len(clueScrolls)):
			info = {}
			info['rank']       = int(self.data[counter])
			info['score']      = int(self.data[counter+1])
			subset[clueScrolls[i]] = info
			counter += 2


		# Last Man Standing
		for i in range(len(lastManStanding)):
			info = {}
			info['rank']       = int(self.data[counter])
			info['score']      = int(self.data[counter+1])
			subset[lastManStanding[i]] = info
			counter += 2


		# Bosses
		counter += 3
		for i in range(len(bosses)):
			info = {}
			info['rank']       = int(self.data[counter])
			info['score']      = int(self.data[counter+1])
			print(info)
			subset[bosses[i]] = info
			counter += 2

		#print(subset)
		# set stats dictionary
		self.stats = subset

	def skill(self, skill, stype: str = 'level'):
		"""skill() method
		
		The skill() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the skill and stype (level, rank, experience) of the skill
		they wish information on.
		
		Args:
			skill (str): The OSRS skill to get information on
			
			stype (str): One of 'level', 'rank', or 'experience'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'level'
		Returns:
			self.stats[skill][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','level','experience','exp_to_next_level']:
				raise "stype must be 'rank','level', or experience'"
				exit(0)
			else:
				return self.stats[skill.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: skill {} {} does not exist".format(skill, KE))
			exit(0)

	def bounty(self, bounty, stype: str = 'score'):
		"""bounty() method
		
		The bounty() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the bounty and stype (score, rank) of the bounty
		they wish information on.
		
		Args:
			bounty (str): The OSRS bounty to get information on
			
			stype (str): One of 'score', 'rank'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'score'
		Returns:
			self.stats[bounty][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','score']:
				raise "stype must be 'rank','score'"
				exit(0)
			else:
				return self.stats[bounty.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: bounty {} does not exist".format(KE))
			exit(0)


	def lastManStanding(self, lastManStanding, stype: str = 'score'):
		"""lastManStanding() method
		
		The lastManStanding() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the lastManStanding and stype (score, rank) of the lastManStanding
		they wish information on.
		
		Args:
			lastManStanding (str): The OSRS lastManStanding to get information on
			
			stype (str): One of 'score', 'rank'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'score'
		Returns:
			self.stats[lastManStanding][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','score']:
				raise "stype must be 'rank','score'"
				exit(0)
			else:
				return self.stats[lastManStanding.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: lastManStanding {} does not exist".format(KE))
			exit(0)

	def clues(self, clues, stype: str = 'score'):
		"""clues() method
		
		The clues() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the clues and stype (score, rank) of the clues
		they wish information on.
		
		Args:
			clues (str): The OSRS clues to get information on
			
			stype (str): One of 'score', 'rank'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'score'
		Returns:
			self.stats[clues][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','score']:
				raise "stype must be 'rank','score'"
				exit(0)
			else:
				return self.stats[clues.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: clues {} does not exist".format(KE))
			exit(0)

	def boss(self, bosses, stype: str = 'score'):
		"""boss() method
		
		The boss() method is a more dynamic, intuitive way to access stats
		then the self.stats dictionary variable.  It allows for a user to
		provide the boss and stype (score, rank) of the boss
		they wish information on.
		
		Args:
			boss (str): The OSRS boss to get information on
			
			stype (str): One of 'score', 'rank'
			             to receive information for.  If not
				     supplied, stype is assumed to be
				     'score'
		Returns:
			self.stats[boss][stype] (int): The info you requested
		
		"""
		try:
			if stype.lower() not in ['rank','score']:
				raise "stype must be 'rank','score'"
				exit(0)
			else:
				return self.stats[bosses.lower()][stype.lower()]
		except KeyError as KE:
			print("ERROR: boss {} does not exist".format(KE))
			exit(0)

	def error(self):
		print("Error occurred: {}".format(self.errorMsg))
		exit(0)
	##########################
	#  END: Hiscores Object  #
	##########################

############################
#  START: Items Object     #
############################
class Items(object):
	"""Items Object

	The Items Object accepts no arguments.  The Items object is, essentially, a collection
	of two dictionaries on all OSRS Items.  The self.itemname dictionary is, as the name
	implies, a dictionary of items with the item's name as it's key.  the self.itemid
	dictionary, likewise, is a dictionary of items sorted by the item's id value.

	While creating two separate dictionaries can take slightly longer, it allows for more
	flexibility in development by giving developer's access to either method that they
	prefer

	Args:
		None

	Returns:
		None
	"""

	def __init__(self):
		# Grand Exchange item lookup Initialization will go here
		req, buylims = self.getHTTPRequest()
		self.itemname = self.parseResponseByItemName(req, buylims)
		self.itemid   = self.parseResponseByItemID(req, buylims)
		if not (self.itemname or self.itemid):
			raise APIDown('The rsbuddy market API appears to be down')

	def getHTTPRequest(self):
		"""getHTTPRequest method

		The getHTTPRequest method is responsible for establishing a request
		with the rsbuddy API.

		Args:
			None

		Returns:
			string: API JSON Response in String format
		"""
		rsBuddyAPI = 'https://rsbuddy.com/exchange/summary.json'
		githubItemInfo = 'https://raw.githubusercontent.com/Coffee-fueled-deadlines/OSRS-JSON-Item-Information/master/item_information.json'
		return urllib.request.Request(rsBuddyAPI), urllib.request.Request(githubItemInfo)


	def parseResponseByItemName(self, req, buylims):
		"""parseResponseByItemName method

		The parseResponseByItemName() method is responsible for accepting the
		request esablished by the getHTTPRequest() method and loading it into
		the JSON string parser to convert it to a usable python dictionary.

		Once parsed, the dictionary is iterated through and a new dictionary is
		created with identical information except the key value is replaced with
		the item name instead of the item id.

		Args:
			req: The string request received by the getHTTPRequest() method

		Returns:
			itemDict: A dictionary of OSRS Items keyed with item names
			boolval: Returns false on parse error
		"""
		r = urllib.request.urlopen(req).read()
		try:
			parsedJSON =  json.loads(r.decode('utf-8'))
		except:
			return False
		
		r = urllib.request.urlopen(buylims).read()
		try:
			parsedBuyLims = json.loads(r.decode('utf-8'))
		except:
			return False

		# Lets make this item-set not suck
		itemDict = {}
		for idval in parsedJSON:
			itemDict[parsedJSON[idval]['name'].lower()] = parsedJSON[idval]
			try:
				itemDict[parsedJSON[idval]['name'].lower()]['buy_limit'] = parsedBuyLims[parsedJSON[idval]['name'].lower()]['buy_limit']
			except:
				pass

		# Return the dictionary
		return itemDict

	def parseResponseByItemID(self, req, buylims):
		"""parseResponseByItemID method

		The parseResponseByItemID() method is responsible for accepting the
		request established by the getHTTPRequest() method and loading it into
		the JSON string parser to convert it to a usable python dictionary keyed
		with the item ID's of the items.

		Args:
			req: The string request received by the getHTTPRequest() method

		Returns:
			itemDict: dictionary of OSRS Items keyed by item ids
			boolval: Returns false on failure to parse
		"""
		r = urllib.request.urlopen(req).read()
		try:
			parsedJSON = json.loads(r.decode('utf-8'))
		except:
			return False
		
		r = urllib.request.urlopen(buylims).read()
		try:
			parsedBuyLims = json.loads(r.decode('utf-8'))
		except:
			return False
		
		for idval in parsedJSON:
			try:
				if parsedJSON[idval]['name'].lower() == parsedBuyLims[parsedJSON[idval]['name'].lower()]['item_name']:
					parsedJSON[idval]['buy_limit'] = parsedBuyLims[parsedJSON[idval]['name'].lower()]['buy_limit']
			except:
				pass
			
		return parsedJSON

	def getItem(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]
		except KeyError:
			return self.itemid[itemNameOrID.lower()]
		
	def getName(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['name']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['name']

	def getBuyAverage(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['buy_average']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_average']

	def getSellAverage(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['sell_average']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sell_average']

	def getBuyQuantity(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['buy_quantity']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_quantity']

	def getSellQuantity(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['sell_quantity']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sell_quantity']
		
	def getBuyLimit(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['buy_limit']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['buy_limit']
		except:
			return False

	def getShopPrice(self, itemNameOrID: str):
		try:
			return self.itemname[itemNameOrID.lower()]['sp']
		except KeyError:
			return self.itemid[itemNameOrID.lower()]['sp']

	def getLowAlchValue(self, itemNameOrID: str):
		try:
			return math.ceil(self.itemname[itemNameOrID.lower()]['sp']*.40)
		except KeyError:
			return math.ceil(self.itemid[itemNameOrID.lower()]['sp']*.40)

	def getHighAlchValue(self, itemNameOrID: str):
		try:
			return math.ceil(self.itemname[itemNameOrID.lower()]['sp']*.60)
		except KeyError:
			return math.ceil(self.itemid[itemNameOrID.lower()]['sp']*.60)

	def isMembers(self, itemNameOrID: str):
		try:
			return bool(self.itemname[itemNameOrID.lower()]['members'])
		except KeyError:
			return bool(self.itemid[itemNameOrID.lower()]['members'])
	##########################
	#  END: Items Object     #
	##########################
