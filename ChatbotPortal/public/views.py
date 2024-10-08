'''
views.py

List views for homepage resources, resources, tags, categories
Retrive views for user resource and admin resource
Pagination views
Retrive views based on resource sorting
'''
__author__ = "Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen"
__copyright__ = "Copyright (c) 2019 BOLDDUC LABORATORY"
__credits__ = ["Apu Islam", "Henry Lo", "Jacy Mark", "Ritvik Khanna", "Yeva Nguyen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "BOLDDUC LABORATORY"

#  MIT License
#
#  Copyright (c) 2019 BOLDDUC LABORATORY
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from datetime import datetime
from queue import Empty
from django.db.models.query import QuerySet
import requests
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from collections import Counter
import math
import heapq
import json
import difflib
from operator import itemgetter
from django.db.models import Q
from resource.models import Resource, Tag, Category, Alias
from resource.serializers import RetrieveResourceSerializer
from .serializers import ResourceSerializer, TagSerializer, CategorySerializer, RetrievePublicResourceSerializer, TagAliasSerializer
import urllib.request
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
import collections
import nltk
nltk.data.path.append("/usr/share/nltk_data")
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# from transformers import pipeline
# import pandas as pd
import torch
import torch.nn.functional as F
from django.http import JsonResponse
import copy
import haversine as hs   
from haversine import Unit

from sentence_transformers import SentenceTransformer, util #new pip install -U sentence-transformers
import regex 
import random
#add to server
import numpy as np
from django.core.serializers.json import DjangoJSONEncoder
import csv
from django.contrib.auth.decorators import login_required


GAZETTEER_city_lat_lon = { # all lower case
    "edmonton":(53.5266355,-113.8223775),
    "red deer":(52.2793112,-113.8904898),
    "st. albert":(53.6436325,-113.7227787),
    "calgary":(51.0275915,-114.4174782),
    "cape breton":(46.18784,-64.7650288),
    "charlottetown":(46.2620503,-63.2182912),
    "fredericton":(45.9444173,-67.2570954),
    "halifax":(44.5738418,-64.5916203),
    "hamilton":(43.2557224,-81.1155462),
    "mississauga":(43.5773504,-79.8239992),
    "oakville":(43.4480774,-79.7891919),
    "markham":(43.8808682,-79.4643488),
    "richmond hill":(43.903663,-79.5107028),
    "vaughan":(43.8372142,-79.7307513),
    "brampton":(43.7250637,-79.9243543),
    "london":(42.9584851,-81.8613634),
    "brantford":(43.1477042,-80.3564669),
    "laval":(45.6049007,-74.3003551),
    "longueuil":(45.5106001,-73.7286783),
    "niagara":(43.0538037,-79.3833793),
    "st. catharines":(43.181196,-79.5445446),
    "st pierre and miquelon":(46.9580457,-56.5825478),
    "lower sackville":(44.7688193,-63.710217),
    "ottawa":(45.3354111,-75.9457586),
    "gatineau":(45.4803639,-76.8092629),
    "prince edward island":(46.2083778,-64.4994645),
    "prince george":(53.9308496,-122.9559524),
    "québec city":(46.7122169,-71.7695852),
    "levis":(46.7086362,-71.5874192),
    "saskatoon":(52.1505698,-106.8292186),
    "warman":(52.3222522,-106.6525785),
    "martensville":(52.291617,-106.7288618),
    "thunder bay":(48.3799046,-90.2150187),
    "regina":(50.4586965,-104.8002177),
    "vancouver":(49.2643049,-123.2372782),
    "richmond":(49.1785437,-123.3008095),
    "burnaby":(49.2400687,-123.0405704),
    "coquitlam":(49.2851332,-122.9214005),
    "surrey":(49.1112854,-122.9658489),
    "victoria":(48.4262587,-123.4004221),
    "oak bay":(48.4308886,-123.3904183),
    "esquimalt":(48.4358681,-123.4318337),
    "view royal":(48.4626546,-123.4995792),
    "whitehorse":(60.623398,-135.4429731),
    "windsor":(42.2581457,-83.112839),
    "strathroy":(42.9649775,-81.6611364),
    "winnipeg":(49.8538852,-97.3176486),
    "yellowknife":(62.4748751,-114.5370148),
    "yorkton":(51.213890,	-102.462776),
    "warman":(52.321945,	-106.584167),
    "swift current":(50.288055,	-107.793892),
    "north battleford":(52.757500,	-108.286110),
    "moose jaw":(50.393333,	-105.551941),
    "melville":(50.930557,	-102.807777),
    "melfort":(52.856388,	-104.610001),
    "martensville":(52.289722,	-106.666664),
    "humboldt":(52.201942,	-105.123055),
    "lloydminster":(53.278046,	-110.005470),
    "estevan":(49.136730,	-102.990959),
    "westmount":(45.484531,	-73.597023),
    "waterville":(45.266666, -71.900002),
    "waterloo":(45.349998,	-72.516670),
    "ville-marie":(47.333332,	-79.433334),
    "victoriaville":(46.049999,	-71.966667),
    "vaudreuil-dorion":(45.400002,	-74.033333),
    "varennes":(45.683334, -73.433334),
    "val-d'or":(48.099998, -77.783333),
    "valcourt":(45.500000, -72.316666),
    "trois-rivières":(46.349998, -72.550003),
    "trois-pistoles":(48.119999, -69.180000),
    "thurso":(45.599998, -75.250000),
    "thetford mines":(46.099998, -71.300003),
    "terrebonne":(45.700001,	-73.633331),
    "témiscouata-sur-le-lac":(47.680000, -68.879997),
    "témiscaming":(46.716667, -79.099998),
    "stanstead":(45.016666, -72.099998),
    "sorel-tracy":(46.033333, -73.116669),
    "shawinigan":(46.566666, -72.750000),
    "sept-îles":(50.216667, -66.383331),
    "senneterre":(48.383331, -77.233330),
    "scotstown":(45.529999,	-71.279999),
    "salaberry-de-valleyfield":(45.250000,	-74.129997),
    "saint-sauveur":(45.900002,	-74.169998),
    "saint-rémi":(45.266666,	-73.616669),
    "saint-raymond":(46.900002,	-71.833336),
    "saint-pie":(45.500000,	-72.900002),
    "saint-pascal":(47.533333,	-69.800003),
    "saint-pamphile":(46.966667,	-69.783333),
    "saint-ours":(45.883331,	-73.150002),
    "saint-lin-laurentides":(45.849998,	-73.766670),
    "saint-lambert":(45.500000,	-73.516670),
    "saint-lazare":(45.400002,	-74.133331),
    "saint-joseph-de-beauce":(46.299999,	-70.883331),
    "saint-jérôme":(45.783333,	-74.000000),
    "saint-jean-sur-richelieu":(45.316666,	-73.266670),
    "saint-hyacinthe":(45.616669,	-72.949997),
    "saint-georges":(46.116669,	-70.666664),
    "saint-félicien":(48.650002,	-72.449997),
    "saint-eustache":(45.570000,	-73.900002),
    "sainte-thérèse":(45.633331,	-73.849998),
    "sainte-marthe-sur-le-lac":(45.529999,	-73.930000),
    "sainte-marie":(46.450001,	-71.033333),
    "sainte-marguerite-du-lac-masson":(46.029999, -74.050003),
    "sainte-julie":(45.583332, -73.333336),
    "sainte-catherine-de-la-jacques-cartier":(46.849998, -71.616669),
    "sainte-catherine":(45.400002, -73.580002),
    "sainte-anne-des-plaines":(45.766666, -73.816666),
    "sainte-anne-de-bellevue":(45.403889, -73.952499),
    "sainte-anne-de-beaupré":(47.016666, -70.933334),
    "sainte-agathe-des-monts":(46.049999, -74.279999),
    "sainte-adèle":(45.950001, -74.129997),
    "saint-constant":(45.369999, -73.570000),
    "saint-colomban":(45.730000, -74.129997),
    "saint-césaire":(45.416668, -73.000000),
    "saint-bruno-de-montarville":(45.533333, -73.349998),
    "saint-basile-le-grand":(45.533333, -73.283333),
    "saint-basile":(46.750000, -71.816666),
    "saint-augustin-de-desmaures":(46.733334, -71.466667),
    "saguenay":(48.416668, -71.066666),
    "rouyn-noranda":(48.233334, -79.016670),
    "rosemère":(45.636944,	-73.800003),
    "roberval":(48.520000,	-72.230003),
    "rivière-rouge":(46.416668,	-74.866669),
    "rivière-du-loup":(47.833332,	-69.533333),
    "richmond":(45.666668,	-72.150002),
    "richelieu":(45.450001,	-73.250000),
    "princeville":(46.166668,	-71.883331),
    "prévost":(45.869999,	-74.080002),
    "portneuf":(46.700001,	-71.883331),
    "port-cartier":(50.033333,	-66.866669),
    "pont-rouge":(45.450001,	-73.816666),
    "pohénégamook":(47.466667,	-69.216667),
    "plessisville":(46.216667,	-71.783333),
    "pincourt":(45.383331,	-73.983330),
    "percé":(48.533333,	-64.216667),
    "paspébiac":(48.033333,	-65.250000),
    "otterburn park":(45.533333,	-73.216667),
    "notre-dame-des-prairies":(46.049999,	-73.433334),
    "notre-dame-de-l'île-perrot":(45.366669,	-73.933334),
    "normandin":(48.833332,	-72.533333),
    "nicolet":(46.216667,	-72.616669),
    "new richmond":(48.166668,	-65.866669),
    "neuville":(46.700001,	-71.583336),
    "murdochville":(48.966667,	-65.500000),
    "mount royal":(45.516109,	-73.643059),
    "mont-tremblant":(46.116669,	-74.599998),
    "mont-saint-hilaire":(45.562222,	-73.191666),
    "montreal":(45.5593046,-73.8766833)
}
GAZETTEER_cities = ['toronto', 'montreal', 'vancouver', 'calgary', 'edmonton', 'ottawa', 'mississauga', 'winnipeg', 'quebec city', 'hamilton', 'brampton', 'surrey', 'kitchener', 'laval', 'halifax', 'london', 'victoria', 'markham', 'st. catharines', 'niagara falls', 'vaughan', 'gatineau', 'windsor', 'saskatoon', 'longueuil', 'burnaby', 'regina', 'richmond', 'richmond hill', 'oakville', 'burlington', 'barrie', 'oshawa', 'sherbrooke', 'saguenay', 'lévis', 'kelowna', 'abbotsford', 'coquitlam', 'trois-rivières', 'guelph', 'cambridge', 'whitby', 'ajax', 'langley', 'saanich', 'terrebonne', 'milton', "st. john's", 'moncton', 'thunder bay', 'dieppe', 'waterloo', 'delta', 'chatham', 'red deer', 'kamloops', 'brantford', 'cape breton', 'lethbridge', 'saint-jean-sur-richelieu', 'clarington', 'pickering', 'nanaimo', 'sudbury', 'north vancouver', 'brossard', 'repentigny', 'newmarket', 'chilliwack', 'white rock', 'maple ridge', 'peterborough', 'kawartha lakes', 'prince george', 'sault ste. marie', 'sarnia', 'wood buffalo', 'new westminster', 'châteauguay', 'saint-jérôme', 'drummondville', 'saint john', 'caledon', 'st. albert', 'granby', 'medicine hat', 'grande prairie', 'st. thomas', 'airdrie', 'halton hills', 'saint-hyacinthe', 'lac-brome', 'port coquitlam', 'fredericton', 'blainville', 'aurora', 'welland', 'north bay', 'beloeil', 'belleville', 'mirabel', 'shawinigan', 'dollard-des-ormeaux', 'brandon', 'rimouski', 'cornwall', 'stouffville', 'georgina', 'victoriaville', 'vernon', 'duncan', 'saint-eustache', 'quinte west', 'charlottetown', 'mascouche', 'west vancouver', 'salaberry-de-valleyfield', 'rouyn-noranda', 'timmins', 'sorel-tracy', 'new tecumseth', 'woodstock', 'boucherville', 'mission', 'vaudreuil-dorion', 'brant', 'lakeshore', 'innisfil', 'prince albert', 'langford station', 'bradford west gwillimbury', 'campbell river', 'spruce grove', 'moose jaw', 'penticton', 'port moody', 'leamington', 'east kelowna', 'côte-saint-luc', 'val-dor', 'owen sound', 'stratford', 'lloydminster', 'pointe-claire', 'orillia', 'alma', 'orangeville', 'fort erie', 'lasalle', 'sainte-julie', 'leduc', 'north cowichan', 'chambly', 'okotoks', 'sept-îles', 'centre wellington', 'saint-constant', 'grimsby', 'boisbriand', 'conception bay south', 'saint-bruno-de-montarville', 'sainte-thérèse', 'cochrane', 'thetford mines', 'courtenay', 'magog', 'whitehorse', 'woolwich', 'clarence-rockland', 'fort saskatchewan', 'east gwillimbury', 'lincoln', 'la prairie', 'tecumseh', 'mount pearl park', 'amherstburg', 'saint-lambert', 'brockville', 'collingwood', 'scugog', 'kingsville', 'baie-comeau', 'paradise', 'uxbridge', 'essa', 'candiac', 'oro-medonte', 'varennes', 'strathroy-caradoc', 'wasaga beach', 'new glasgow', 'wilmot', 'essex', 'fort st. john', 'kirkland', 'lassomption', 'westmount', 'saint-lazare', 'chestermere', 'huntsville', 'corner brook', 'riverview', 'lloydminster', 'joliette', 'yellowknife', 'squamish', 'mont-royal', 'rivière-du-loup', 'cobourg', 'cranbrook', 'beaconsfield', 'springwater', 'dorval', 'thorold', 'camrose', 'south frontenac', 'pitt meadows', 'port colborne', 'quispamsis', 'mont-saint-hilaire', 'bathurst', 'saint-augustin-de-desmaures', 'oak bay', 'sainte-marthe-sur-le-lac', 'salmon arm', 'port alberni', 'esquimalt', 'deux-montagnes', 'miramichi', 'niagara-on-the-lake', 'saint-lin--laurentides', 'beaumont', 'middlesex centre', 'inverness', 'stony plain', 'petawawa', 'pelham', 'selwyn', 'loyalist', 'midland', 'colwood', 'central saanich', 'sainte-catherine', 'port hope', 'lancienne-lorette', 'saint-basile-le-grand', 'swift current', 'edmundston', 'russell', 'north grenville', 'yorkton', 'tracadie', 'bracebridge', 'greater napanee', 'tillsonburg', 'steinbach', 'hanover', 'terrace', 'springfield', 'gaspé', 'kenora', 'cold lake', 'summerside', 'comox', 'sylvan lake', 'pincourt', 'west lincoln', 'matane', 'brooks', 'sainte-anne-des-plaines', 'west nipissing / nipissing ouest', 'rosemère', 'mistassini', 'grand falls', 'clearview', 'st. clair', 'canmore', 'north battleford', 'pembroke', 'mont-laurier', 'strathmore', 'saugeen shores', 'thompson', 'lavaltrie', 'high river', 'severn', 'sainte-sophie', 'saint-charles-borromée', 'portage la prairie', 'thames centre', 'mississippi mills', 'powell river', 'south glengarry', 'north perth', 'mercier', 'south stormont', 'saint-colomban', 'lacombe', 'sooke', 'dawson creek', 'lake country', 'trent hills', 'sainte-marie', 'guelph/eramosa', 'truro', 'amos', 'the nation / la nation', 'ingersoll', 'winkler', 'wetaskiwin', 'central elgin', 'lachute', 'west grey', 'parksville', 'cowansville', 'bécancour', 'gravenhurst', 'perth east', 'prince rupert', 'prévost', 'sainte-adèle', 'kentville', 'beauharnois', 'les îles-de-la-madeleine', 'wellington north', 'st. andrews', 'carleton place', 'whistler', 'brighton', 'tiny', 'gander', 'sidney', 'rothesay', 'brock', 'summerland', 'val-des-monts', 'taché', 'montmagny', 'erin', 'kincardine', 'north dundas', 'wellesley', 'estevan', 'north saanich', 'warman', 'la tuque', 'norwich', 'meaford', 'adjala-tosorontio', 'hamilton township', 'st. clements', 'saint-amable', 'weyburn', 'south dundas', 'lîle-perrot', "notre-dame-de-l'île-perrot", 'williams lake', 'elliot lake', 'cantley', 'nelson', 'lambton shores', 'mapleton', 'georgian bluffs', 'rawdon', 'campbellton', 'view royal', 'coldstream', 'chester', 'queens', 'selkirk', 'saint-félicien', 'hawkesbury', 'roberval', 'sainte-agathe-des-monts', 'north dumfries', 'rideau lakes', 'sechelt', 'north glengarry', 'south huron', 'marieville', 'tay', 'temiskaming shores', 'hinton', 'saint-sauveur', 'quesnel', 'elizabethtown-kitley', 'morinville', 'grey highlands', 'stratford', 'alfred and plantagenet', 'mont-tremblant', 'martensville', 'saint-raymond', 'amherst', 'ramara', 'bois-des-filion', 'leeds and the thousand islands', 'carignan', 'brockton', 'laurentian valley', 'east st. paul', 'lorraine', 'sainte-julienne', 'blackfalds', 'malahide', 'oromocto', 'olds', 'huron east', 'stanley', 'penetanguishene', 'qualicum beach', 'notre-dame-des-prairies', 'west perth', 'cavan monaghan', 'arnprior', 'smiths falls', 'pont-rouge', 'champlain', 'coaticook', 'minto', 'morden', 'mono', 'corman park no. 344', 'ladysmith', 'bridgewater', 'dauphin', 'otterburn park', 'taber', 'south bruce peninsula', 'edson', 'farnham', 'kapuskasing', 'la malbaie', 'renfrew', 'coaldale', "portugal cove-st. philip's", 'zorra', 'kitimat', 'shelburne', 'happy valley', 'saint-hippolyte', 'castlegar', 'church point', 'drumheller', 'kirkland lake', 'argyle', 'torbay', 'la pêche', 'banff', 'innisfail', 'nicolet', 'rockwood', 'drummond/north elmsley', 'dryden', 'iqaluit', 'fort frances', 'la sarre', 'trail', 'chandler', 'stone mills', 'hanover', 'south-west oxford', 'acton vale', 'bromont', 'beckwith', 'goderich', 'plympton-wyoming', 'central huron', 'rigaud', 'louiseville', 'chibougamau', 'aylmer', 'delson', 'kimberley', 'blandford-blenheim', 'bayham', 'augusta', 'puslinch', 'beauport', 'saint-rémi', 'st. marys', 'drayton valley', 'ponoka', 'labrador city', 'donnacona', 'southgate', 'mcnab/braeside', 'macdonald', 'hampstead', 'baie-saint-paul', 'merritt', 'bluewater', 'east zorra-tavistock', 'brownsburg', 'stoneham-et-tewkesbury', 'asbestos', 'huron-kinloss', 'coteau-du-lac', 'the blue mountains', 'whitewater region', 'edwardsburgh/cardinal', 'sainte-anne-des-monts', 'old chelsea', 'north stormont', 'alnwick/haldimand', 'peace river', 'arran-elderslie', 'saint-zotique', 'val-shefford', 'douro-dummer', 'plessisville', 'ritchot', 'otonabee-south monaghan', 'shediac', 'slave lake', 'port-cartier', 'saint-lambert-de-lauzon', 'barrington', 'rocky mountain house', 'chatsworth', 'stephenville', 'muskoka falls', 'devon', 'yarmouth', 'boischatel', 'parry sound', 'pointe-calumet', 'beaubassin east / beaubassin-est', 'wainfleet', 'cramahe', 'beauceville', 'north middlesex', 'amqui', 'sainte-catherine-de-la-jacques-cartier', 'clarenville', 'mont-joli', 'dysart et al', 'wainwright', 'contrecoeur', 'beresford', 'saint-joseph-du-lac', 'hope', 'gimli', 'douglas', 'saint-apollinaire', 'hindon hill', 'les cèdres', 'la broquerie', 'kent', 'tweed', 'saint-félix-de-valois', 'bay roberts', 'melfort', 'bonnyville', 'stettler', 'saint-calixte', 'lac-mégantic', 'perth', 'oliver paipoonge', 'humboldt', 'charlemagne', 'pontiac', 'st. paul', 'petrolia', 'southwest middlesex', 'front of yonge', 'vegreville', 'sainte-brigitte-de-laval', 'princeville', 'verchères', 'the pas', 'saint-césaire', 'la ronge', 'tay valley', 'south bruce', 'mcmasterville', 'redcliff', 'crowsnest pass', 'saint-philippe', 'richelieu', 'notre-dame-du-mont-carmel', "l'ange-gardien", 'sainte-martine', 'saint-pie', 'peachland', 'ashfield-colborne-wawanosh', 'trent lakes', 'northern rockies', 'cookshire', 'west st. paul', 'windsor', 'lepiphanie', 'creston', 'smithers', 'cornwall', 'meadow lake', 'lanark highlands', 'sackville', 'grand falls', 'cochrane', 'marystown', 'sioux lookout', 'didsbury', 'saint-honoré', 'fernie', 'deer lake', 'woodstock', 'val-david', 'flin flon', 'hudson', 'gananoque', 'brokenhead', 'saint-paul', 'burton', 'spallumcheen', 'westlock', 'témiscouata-sur-le-lac', 'shannon', 'osoyoos', 'montréal-ouest', 'hearst', 'saint-henri', 'ste. anne', 'antigonish', 'espanola', 'west elgin', 'flin flon (part)', 'grand bay-westfield', 'sainte-anne-de-bellevue', 'north huron', 'oliver', "saint-roch-de-l'achigan", 'stirling-rawdon', 'chisasibi', 'carbonear', 'saint marys', 'chertsey', 'armstrong', 'stonewall', 'shippagan', 'lanoraie', 'memramcook', 'centre hastings', 'warwick', 'east ferris', 'hanwell', 'saint-joseph-de-beauce', 'metchosin', 'lucan biddulph', 'rivière-rouge', 'greenstone', 'saint-mathias-sur-richelieu', 'neepawa', 'gibsons', 'kindersley', 'jasper', 'barrhead', 'les coteaux', 'melville', 'saint-germain-de-grantham', 'iroquois falls', 'havelock-belmont-methuen', 'cornwallis', 'saint-boniface', 'edenwold no. 158', 'coverdale', 'vanderhoof', 'southwold', 'goulds', 'saint stephen', 'waterloo', 'nipawin', 'neuville', 'saint-cyrille-de-wendover', 'central frontenac', 'mont-orford', 'saint-jean-de-matha', 'seguin', 'tyendinaga', 'hampton', 'sussex', 'grand forks', 'la pocatière', 'caraquet', 'saint-étienne-des-grès', 'altona', 'stellarton', 'wolfville', 'new maryland', 'port hardy', 'saint-donat', 'château-richer', 'madawaska valley', 'deep river', 'asphodel-norwood', 'red lake', 'métabetchouan-lac-à-la-croix', 'berthierville', 'vermilion', 'niverville', 'hastings highlands', 'carstairs', 'danville', 'channel-port aux basques', 'battleford', 'lac-etchemin', 'saint-antonin', 'saint-jacques', 'swan river', 'sutton', 'northern bruce peninsula', 'lislet-sur-mer', 'carleton-sur-mer', 'oka', 'prescott', 'amaranth', 'marmora and lake', 'maniwaki', 'morin-heights', 'dundas', 'napierville', 'crabtree', 'bancroft', 'saint-tite', 'howick', 'dutton/dunwich', 'callander', 'simonds', 'baie-durfé', 'new richmond', 'perth south', 'roxton pond', 'sparwood', 'claresholm', 'breslau', 'montague', 'cumberland', 'beaupré', 'saint-andré-avellin', 'saint-ambroise-de-kildare', 'east angus', 'rossland', 'mackenzie', 'golden', 'raymond', "saint-adolphe-d'howard", 'warwick', 'bowen island', 'bonnechere valley', 'windsor', 'pincher creek', 'alnwick', 'westville', 'fruitvale', 'pasadena', 'saint-prosper', 'ormstown', 'cardston', 'westbank', 'de salaberry', 'headingley', 'grande cache', 'atholville', 'saint-agapit', 'prince albert no. 461', 'casselman', 'saint-ambroise', 'hay river', 'mistissini', 'studholm', 'lumby', 'saint-faustin--lac-carré', 'morris-turnberry', 'placentia', 'saint-pascal', 'mulmur', 'blind river', 'dunham', 'havre-saint-pierre', 'saint-anselme', 'trois-pistoles', 'grande-rivière', 'powassan', 'malartic', 'bonavista', 'killarney - turtle mountain', 'woodlands', 'lewisporte', 'saint-denis-de-brompton', 'invermere', 'salisbury', 'bifrost-riverton', 'buckland no. 491', 'cartier', 'sainte-anne-des-lacs', 'highlands east', 'alexander', 'sainte-claire', 'percé', 'saint-jean-port-joli', 'east hawkesbury', 'bright', 'penhold', "saint-andré-d'argenteuil", 'saint-côme--linière', 'saint-sulpice', 'marathon', 'forestville', 'inuvik', 'richmond', 'lake cowichan', 'sables-spanish rivers', 'hillsburg-roblin-shell river', 'port hawkesbury', 'three hills', 'lorette', 'paspebiac', 'saint-thomas', 'saint-jean-baptiste', 'portneuf', 'pictou', 'tisdale', 'lake of bays', 'high level', 'gibbons', 'bishops falls', 'westlake-gladstone', 'normandin', 'saint-alphonse-rodriguez', 'beauséjour', 'dalhousie', 'saint-alphonse-de-granby', 'lac du bonnet', 'clermont', 'virden', 'compton', 'white city', 'ellison', 'mont-saint-grégoire', 'wellington', 'merrickville', 'saint-liboire', 'dégelis', 'morris', 'saint-alexis-des-monts', 'cap-saint-ignace', 'saint-anaclet-de-lessard', 'carman', 'athens', 'melancthon', 'cap santé', 'harbour grace', 'houston', 'adelaide-metcalfe', 'crossfield', 'springdale', 'fort macleod', 'athabasca', 'enderby', 'saint-ferréol-les-neiges', 'laurentian hills', 'grand valley', 'senneterre', 'sainte-marie-madeleine', 'admaston/bromley', 'saint-gabriel-de-valcartier', 'north algona wilberforce', 'kingston', 'wawa', "saint-christophe-d'arthabaska", 'sainte-mélanie', 'ascot corner', 'horton', 'saint-michel', 'botwood', "saint-paul-d'abbotsford", 'saint-marc-des-carrières', 'stanstead', 'sainte-anne-de-beaupré', 'sainte-luce', 'saint-gabriel', 'rankin inlet', 'vanscoy no. 345', 'cedar', 'princeton', 'la loche', 'kingsclear', 'ferme-neuve', 'thurso', 'adstock', 'shuniah', 'enniskillen', 'yamachiche', 'saint-maurice', 'bonaventure', 'val-morin', 'pohénégamook', 'wakefield', 'stoke', 'sainte-marguerite-du-lac-masson', 'saint-prime', 'kuujjuaq', 'atikokan', 'grenville-sur-la-rouge', 'north cypress-langford', 'sainte-anne-de-sorel', 'macamic', 'sundre', 'rougemont', 'piedmont', 'grimshaw', 'lac-des-écorces', 'northeastern manitoulin and the islands', 'pelican narrows', 'mcdougall', 'black diamond', 'saint-pamphile', 'bedford', 'weedon-centre', 'lacolle', 'saint-gabriel-de-brandon', 'errington', 'coalhurst', 'french river / rivière des français', 'arviat', 'saint-david-de-falardeau', 'markstay', 'spaniards bay', 'cocagne', 'saint-bruno', 'chetwynd', 'laurier-station', 'saint-anicet', 'saint-mathieu-de-beloeil', 'cap-chat', 'sexsmith', 'notre-dame-de-lourdes', 'ville-marie', 'saint-isidore', 'shippegan', 'east garafraxa', 'pemberton', 'unity', 'rimbey', 'high prairie', 'turner valley', 'hanna', 'fort smith', 'maria', 'saint-chrysostome', 'greater madawaska', 'berwick', 'saint-damase', 'lincoln', 'disraeli', 'sainte-victoire-de-sorel', 'meadow lake no. 588', 'elkford', 'georgian bay', 'saint-alexandre', 'hérbertville', 'moosomin', 'north kawartha', 'sainte-thècle', 'trenton', 'fermont', 'esterhazy', 'wickham', 'la présentation', 'beaverlodge', 'sainte-catherine-de-hatley', 'saint-basile', 'saint-raphaël', 'holyrood', 'gracefield', 'saint-martin', 'causapscal', 'brigham', 'perry', 'port-daniel--gascons', 'rosetown', 'minnedosa', 'labelle', 'huntingdon', 'hébertville', 'black river-matheson', 'saint-michel-des-saints', 'dufferin', 'saint-victor', 'sicamous', 'cap pele', 'kelsey', 'killaloe, hagarty and richards', 'alvinston', 'dundurn no. 314', 'saint-éphrem-de-beauce', 'assiniboia', 'témiscaming', 'magrath', 'sainte-geneviève-de-berthier', 'buctouche', 'grand manan', 'sainte-madeleine', 'boissevain', 'scott', 'sainte-croix', 'algonquin highlands', 'valcourt', 'saint george', 'paquetville', 'saint-dominique', 'clearwater', 'addington highlands', 'lillooet', 'burin', 'grand bank', 'léry', 'minto', 'rosthern no. 403', 'chase', 'mansfield-et-pontefract', 'saint-denis', 'outlook', 'mitchell', 'saint-gédéon-de-beauce', "saint-léonard-d'aston", 'lunenburg', 'northesk', 'albanel', 'st. anthony', 'pessamit', 'maskinongé', 'saint-charles-de-bellechasse', 'fogo island', 'east broughton', 'lantz', 'calmar', 'highlands', 'saint-polycarpe', 'logy bay-middle cove-outer cove', 'deschambault', 'canora', 'upper miramichi', 'anmore', 'hardwicke', 'saint-côme', 'waskaganish', 'twillingate', 'saint-quentin', 'lebel-sur-quévillon', 'pilot butte', 'nanton', 'pierreville', 'new-wes-valley', 'pennfield ridge', 'west interlake', 'biggar', 'britannia no. 502', 'kent', 'wabana', 'saint-gilles', 'wendake', 'saint-bernard', 'sainte-cécile-de-milton', 'saint-roch-de-richelieu', 'saint-nazaire', 'saint-elzéar', 'hinchinbrooke', 'saint-françois-xavier-de-brompton', 'papineauville', 'prairie view', 'cowichan bay', 'saint-ignace-de-loyola', 'central manitoulin', 'maple creek', 'glovertown', 'tofield', 'madoc', 'upton', 'sainte-anne-de-sabrevois', 'logan lake', 'sainte-anne-de-la-pérade', 'saint-damien-de-buckland', 'baker lake', 'saltair', 'pouch cove', 'saint-ferdinand', 'port mcneill', 'digby', 'manouane', 'saint-gervais', 'neebing', 'redwater', 'saint-alexandre-de-kamouraska', 'saint-marc-sur-richelieu', 'mandeville', 'caplan', 'point edward', 'allardville', 'waterville', 'saint-damien', 'lac-nominingue', 'obedjiwan', 'rama', 'mccreary', 'deloraine-winchester', 'oakland-wawanesa', 'brenda-waskada', 'russell-binscarth', 'ellice-archie', 'souris-glenwood', 'riverdale', 'pembina', 'wallace-woodworth', 'lorne', 'ethelbert', 'yellowhead', 'swan valley west', 'grey', 'gilbert plains', 'norfolk-treherne', 'hamiota', 'emerson-franklin', 'sifton', 'rossburn', 'grand view', 'grassland', 'louise', 'ste. rose', 'cartwright-roblin', 'mossey river', 'lakeshore', 'riding mountain west', 'clanwilliam-erickson', 'glenboro-south cypress', 'north norfolk', 'reinland', 'minitonas-bowsman', 'kippens', 'blucher', 'hatley', 'saint-gédéon', 'kingsey falls', 'provost', 'saint-charles', 'mattawa', 'tumbler ridge', 'terrasse-vaudreuil', "l'ascension-de-notre-seigneur", 'bow island', 'barraute', 'one hundred mile house', 'kedgwick', 'gambo', 'saint-liguori', 'bonfield', 'pointe-lebel', 'saint mary', 'saint-patrice-de-sherrington', 'fox creek', 'dawn-euphemia', 'chapleau', 'saint-esprit', 'westfield beach', 'montague', 'mashteuiatsh', 'saint-françois-du-lac', 'eel river crossing', 'saint-fulgence', 'millet', 'vallée-jonction', 'saint-georges-de-cacouna', 'lumsden no. 189', 'manitouwadge', 'wellington', 'swift current no. 137', 'tofino', 'fort quappelle', 'vulcan', 'indian head', 'petit rocher', 'wabush', 'saint-fabien', 'watrous', 'north frontenac', 'lac-supérieur', 'les escoumins', 'richibucto', 'rivière-beaudette', 'saint-barthélemy', "nisga'a", 'austin', 'saint-mathieu', "saint-paul-de-l'île-aux-noix", 'orkney no. 244', 'behchokò', 'saint-joseph-de-coleraine', 'saint-cyprien-de-napierville', 'sayabec', 'valleyview', 'déléage', 'potton', 'sainte-béatrix', 'sainte-justine', 'eastman', 'saint-valérien-de-milton', 'saint-cuthbert', 'saint-blaise-sur-richelieu', 'middleton', 'maugerville', 'dalmeny', 'kamsack', 'lumsden', 'trinity bay north', 'saint-michel-de-bellechasse', 'sainte-angèle-de-monnoir', 'picture butte', 'sacré-coeur-saguenay', 'saint-louis', 'victoria', 'saint-robert', 'armstrong', "saint-pierre-de-l'île-d'orléans", 'la guadeloupe', 'saint andrews', 'burns lake', 'povungnituk', 'manners sutton', 'gore', 'deseronto', 'lamont', 'chambord', 'dudswell', 'wynyard', 'cambridge bay', 'saint-narcisse', 'frontenac islands', 'waswanipi', 'inukjuak', 'piney', 'komoka', 'saint-zacharie', 'hemmingford', 'shelburne', 'saint-clet', 'carberry', 'brighton', 'saint-antoine', 'warfield', 'northampton', 'saint-ours', 'stephenville crossing', 'sainte-anne-de-la-pocatière', 'ucluelet', 'saint-placide', 'barrière', 'fisher', 'nipissing', 'sainte-clotilde', 'shaunavon', 'wicklow', 'southesk', 'nouvelle', 'rosthern', 'yamaska', 'neguac', 'flat rock', 'igloolik', 'grunthal', 'naramata', 'saint-élie-de-caxton', 'blumenort', 'balmoral', 'price', 'rosedale', 'saint-jacques-le-mineur', 'huron shores', 'champlain', 'whitehead', 'saint-antoine-sur-richelieu', 'saint-pacôme', 'saint-stanislas-de-kostka', 'frontenac', 'stuartburn', 'yamaska-est', "sainte-émélie-de-l'énergie", 'saint-charles-sur-richelieu', 'saint-joseph-de-sorel', 'nipigon', 'rivière-blanche', 'sainte-hélène-de-bagot', 'franklin centre', 'harbour breton', 'massey drive', 'mille-isles', 'wilton no. 472', 'lyster', 'oakview', 'balgonie', 'harrison park', 'kensington', 'witless bay', 'pond inlet', 'royston', 'sainte-clotilde-de-horton', 'burford', 'fossambault-sur-le-lac', 'saint-benoît-labre', 'coombs', 'terrace bay', 'chapais', 'saint-honoré-de-shenley', 'cleveland', 'macdonald, meredith and aberdeen additional', 'messines', 'saint-jean-de-dieu', 'nakusp', 'florenceville', 'saint-antoine-de-tilly', 'lakeview', 'humbermouth', 'fort st. james', 'saint-françois-de-la-rivière-du-sud', 'saint-jacques', 'uashat', 'perth', 'eeyou istchee baie-james', 'shellbrook no. 493', 'shawville', 'saint-lucien', 'lambton', "saint-laurent-de-l'île-d'orléans", 'saint-flavien', 'grenville', 'chute-aux-outardes', 'sainte-marcelline-de-kildare', 'saint-félix-de-kingsey', 'upper island cove', 'glenelg', 'sainte-élisabeth', 'ashcroft', 'clarkes beach', 'saint-bernard-de-lacolle', 'belledune', 'saint-guillaume', 'venise-en-québec', 'maliotenam', 'ripon', 'hilliers', 'saint-joseph', 'saint-paulin', 'bon accord', 'saint david', 'saint-albert', 'matagami', 'springfield', 'amherst', 'notre-dame-du-laus', 'st. george', 'wembley', 'victoria', 'springbrook', 'saint-tite-des-caps', 'hudson bay', 'pinawa', 'brudenell, lyndoch and raglan', 'carlyle', 'keremeos', 'val-joli', 'gold river', 'saint-casimir', 'bay bulls', 'langham', 'frenchman butte', 'gordon', 'kugluktuk', 'saint-malachie', 'southampton', 'salluit', 'pangnirtung', 'saint-louis-de-gonzague', 'moosonee', 'englehart', 'saint-urbain', 'tring-jonction', 'nauwigewauk', 'pointe-à-la-croix', 'denmark', 'saint-joachim', 'torch river no. 488', "saint-théodore-d'acton", 'grindrod', 'l îsle-verte', 'harrison hot springs', 'palmarolle', 'henryville', 'sussex corner', 'saint-odilon-de-cranbourne', 'pipestone', 'laurierville', 'la doré', 'lac-au-saumon', 'wotton', 'prairie lakes', 'elk point', 'shellbrook', 'wemindji', 'cape dorset', 'strong', 'lappe', 'rivière-héva', 'fort-coulonge', 'irishtown-summerside', 'godmanchester', 'macklin', 'armour', 'saint-simon', 'st. françois xavier', 'tingwick', 'saint-aubert', 'saint-mathieu-du-parc', 'wabasca', 'ragueneau', 'notre-dame-du-bon-conseil', 'wasagamack', 'saint-ubalde', 'creighton', 'fortune', 'faraday', 'berthier-sur-mer', 'frampton', 'magnetawan', 'new carlisle', 'laird no. 404', 'petitcodiac', 'popkum', 'norton', 'canwood no. 494', 'wentworth-nord', 'bas caraquet', 'sainte-ursule', 'dawson', 'nantes', 'lac-aux-sables', 'stewiacke', 'taylor', 'rosser', 'estevan no. 5', 'falmouth', 'vaudreuil-sur-le-lac', 'grahamdale', 'cardwell', 'two hills', 'spiritwood no. 496', 'legal', 'amulet', 'hérouxville', 'pointe-des-cascades', 'weldford', 'reynolds', 'st. laurent', 'lions bay', "l'isle-aux-allumettes", 'emo', "sainte-brigide-d'iberville", 'les éboulements', 'dunsmuir', 'pointe-aux-outardes', 'smooth rock falls', 'oxbow', 'telkwa', 'gjoa haven', 'sainte-barbe', 'mayerthorpe', 'saint-louis-du-ha! ha!', 'powerview-pine falls', 'baie verte', 'saint-édouard', 'charlo', 'hillsborough', 'bruederheim', 'burgeo', 'wadena', 'richmond', 'swan hills', 'wilkie', 'saint-léonard', 'rivière-bleue', 'noyan', 'ile-à-la-crosse', 'landmark', 'saint-hugues', 'chisholm', 'sainte-anne-du-sault', 'la conception', 'saint-valère', 'sorrento', 'lamèque', 'thessalon', "l'isle-aux-coudres", 'nobleford', 'larouche', "south qu'appelle no. 157", 'elton', 'lorrainville', 'conestogo', 'upham', 'st.-charles', 'sainte-lucie-des-laurentides', 'saint-alexis', 'gillam', 'roxton falls', 'montcalm', 'clarendon', 'mervin no. 499', 'saint-ludger', 'coldwell', 'saint-arsène', 'racine', 'saint-majorique-de-grantham', 'saint-zénon', 'saint-armand', 'saint-édouard-de-lotbinière', 'alonsa', 'listuguj', 'bowden', 'st. joseph', 'osler', 'saint-hubert-de-rivière-du-loup', 'saint-jude', 'dildo', 'la minerve', 'lanigan', 'lajord no. 128', 'moonbeam', 'notre-dame-des-pins', 'saint-alban', 'saint-pierre-les-becquets', 'arborg', 'vauxhall', 'bayfield', 'beaver river', 'irricana', 'labrecque', 'new bandon', 'wemotaci', 'sainte-hénédine', "l'anse-saint-jean", 'bassano', 'parrsboro', 'kaleden', "st. george's", 'fort simpson', 'akwesasne', 'lavenir', 'ignace', 'claremont', 'teulon', 'peel', 'musquash', 'notre-dame-du-portage', 'st. lawrence', 'oxford', 'minto-odanah', "st. alban's", 'saint james', "saint-norbert-d'arthabaska", 'manning', 'glenella-lansdowne', 'saint-hilarion', 'saint-siméon', 'saint-barnabé', 'sainte-félicité', 'two borders', 'queensbury', 'bury', 'lac-bouchette', 'saint-lazare-de-bellechasse', 'saint-michel-du-squatec', 'saint-joachim-de-shefford', 'st-pierre-jolys', 'grand-remous', 'saint-gabriel-de-rimouski', 'armstrong', 'rogersville', 'langenburg', 'sainte-marie-salomé', 'moose jaw no. 161', 'saint-cyprien', 'maidstone', 'très-saint-sacrement', 'battle river no. 438', 'miltonvale park', 'mcadam', 'saints-anges', 'saint-urbain-premier', 'centreville-wareham-trinity', 'alberton', 'winnipeg beach', 'sainte-agathe-de-lotbinière', 'salmo', 'kipling', 'sagamok', 'trécesson', 'tara', 'grande-vallée', 'bertrand', 'newcastle', 'mont-carmel', 'saint martins', 'saint-eugène', 'notre-dame-des-neiges', 'saint-andré', 'centreville', 'roland', 'saint-léon-de-standon', 'saint-modeste', 'carnduff', 'carling', 'eckville', 'nain', 'hillsburgh', 'foam lake', 'sainte-sabine', 'saint-maxime-du-mont-louis', 'blanc-sablon', 'cobalt', 'gravelbourg', 'south river', 'hudson bay no. 394', 'mckellar', 'frelighsburg', 'buffalo narrows', 'ayers cliff', 'les méchins', 'sainte-marguerite', 'saint-claude', 'air ronge', 'chipman', 'girardville', 'saint-bruno-de-guigues', 'grenfell', 'dorchester', 'south algonquin', 'windermere', 'saint-narcisse-de-beaurivage', 'saint-rené-de-matane', "sainte-jeanne-d'arc", 'plaisance', 'roxton-sud', 'st. louis no. 431', 'youbou', 'duchess', 'saint-frédéric', 'viking', 'sioux narrows-nestor falls', 'whitecourt', 'repulse bay', 'montréal-est', 'king', 'regina beach', 'saint-patrice-de-beaurivage', 'ootischenia', 'hensall', 'bentley', 'durham', 'sainte-marthe', 'notre-dame-du-nord', 'pinehouse', 'saint-aimé-des-lacs', 'lac-drolet', 'preeceville', 'maple creek no. 111', "harbour main-chapel's cove-lakeview", 'saint-wenceslas', 'weyburn no. 67', 'birch hills', 'wedgeport', 'kerrobert', 'havelock', 'eston', 'sainte-geneviève-de-batiscan', 'saint-justin', 'saint-norbert', 'schreiber', 'trochu', 'botsford', 'riviere-ouelle', 'greenwich', 'stukely-sud', 'saint-georges-de-clarenceville', 'sainte-thérèse-de-gaspé', 'beachburg', 'desbiens', 'clyde river', 'la macaza', 'souris', 'kindersley no. 290', 'laird', 'falher', 'saint-vallier', 'coleraine', 'melita', 'noonan', 'sainte-pétronille', 'delisle', 'bristol', 'mahone bay', 'waldheim', 'saint-sylvestre', 'taloyoak', 'onoway', 'saint-stanislas', 'malpeque', 'plantagenet', 'longue-rive', 'argyle', 'davidson', 'plaster rock', 'wilmot', 'valemount', 'saint-léonard-de-portneuf', 'alberta beach', 'saint-narcisse-de-rimouski', 'saint-bonaventure', 'longlaketon no. 219', 'papineau-cameron', 'assiginack', 'brébeuf', 'hudson hope', 'prince', 'baie-du-febvre', 'durham-sud', 'melbourne', 'nipawin no. 487', 'duck lake no. 463', 'oyen', 'st. albert']
GAZETTEER_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Alberta', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick', 'Ontario', 'British Columbia', 'Ontario', 'Alberta', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta', 'Quebec', 'Alberta', 'Alberta', 'Ontario', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince Edward Island', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Nova Scotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta', 'Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Ontario', 'British Columbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Nova Scotia', 'Alberta', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba', 'British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta', 'Prince Edward Island', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta', 'Ontario', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'British Columbia', 'Ontario', 'Alberta', 'Ontario', 'Prince Edward Island', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'New Brunswick', 'Alberta', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta', 'Ontario', 'Nova Scotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'New Brunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia', 'Alberta', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan', 'Alberta', 'Alberta', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'New Brunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Alberta', 'Manitoba', 'Ontario', 'Alberta', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta', 'New Brunswick', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'British Columbia', 'Manitoba', 'Manitoba', 'Alberta', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'Nova Scotia', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador', 'Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Alberta', 'Alberta', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Alberta', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia', 'Saskatchewan', 'Alberta', 'Alberta', 'Alberta', 'Alberta', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'British Columbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'Newfoundland and Labrador', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince Edward Island', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Alberta', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Prince Edward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta', 'Manitoba', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'New Brunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Saskatchewan', 'Quebec', 'Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon', 'Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta', 'Saskatchewan', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta', 'Quebec', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta', 'Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Ontario', 'Saskatchewan', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba', 'Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut', 'Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Quebec', 'Nunavut', 'Alberta', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec', 'Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta', 'Alberta']

def get_nearby_cities(location_name:str, distance_km=45):
    all_other_city_indexes = []
    all_other_cities = []
    provience = None
    location_name = location_name.lower()

    global GAZETTEER_city_lat_lon
    # GAZETTEER_city_lat_lon = {k.lower(): v for k, v in GAZETTEER_city_lat_lon.items()}

    global GAZETTEER_cities
    # GAZETTEER_cities = [v.lower() for v in GAZETTEER_cities]

    global GAZETTEER_proviences
    # GAZETTEER_proviences = [v.lower() for v in GAZETTEER_proviences]

    if location_name not in GAZETTEER_city_lat_lon:
        return {}
    if location_name not in GAZETTEER_cities:
        return {}
    else:
        provience = GAZETTEER_proviences[GAZETTEER_cities.index(location_name)]  
    
    for i,prov in enumerate(GAZETTEER_proviences):
        if prov == location_name:
            return {}
        elif prov == provience:
            all_other_city_indexes.append(i)
    
    for i in all_other_city_indexes:
        if GAZETTEER_cities[i].lower() != location_name.lower():
            all_other_cities.append(GAZETTEER_cities[i])

    closeCity_distance = {}
    for same_prov_city in all_other_cities:
        if same_prov_city in GAZETTEER_city_lat_lon:
            loc1=GAZETTEER_city_lat_lon[location_name]
            loc2=GAZETTEER_city_lat_lon[same_prov_city]
            distance = hs.haversine(loc1,loc2,unit=Unit.KILOMETERS)
            if distance < distance_km:
                closeCity_distance[same_prov_city] = distance

    return closeCity_distance


class StandardResultSetPagination(PageNumberPagination):
    page_size = 100

class HomepageResultSetPagination(PageNumberPagination):
    page_size = 4


def find_keywords_of_sentence(sentence):
    tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in tokens if not w in stopwords.words()]
    for s in filtered_sentence:
        if len(s)>6 and s[-2:]=='ed':
            filtered_sentence.append(s[:-2])
    keywords = []
    res = []
    for word in pos_tag(filtered_sentence):
        if(word[1] not in ('PRP', 'VBP', 'TO', 'DT', 'AT')):
            keywords.append(word[0]) 
            res.append(word[0])   

    for i in range(len(keywords)):
        if i+1 < len(keywords):
            res.append(keywords[i] +" "+ keywords[i+1])

    for i in range(len(keywords)):
        if i+2 < len(keywords):
            res.append(keywords[i]+" "+ keywords[i+1]+ " "+ keywords[i+2])

    return res


def travel_mh_kg(word, current_node='START'):
    return []

# def travel_mh_kg(word, current_node='START'):
    

#     MH_KG = {
#             'START':['Legal', 'Chronic Pain', 'Cancer', 'Human Immunodeficiency Virus (HIV)', 'Acquired Immune Deficiency Syndrome (AIDS)', 'COVID-19', 'Treatments', 'Traditional Indigenous Health'],
#             'Legal':['Abuse', 'Corrections', 'Reconciliation', 'Human Trafficking', 'Harrassment'],
#             'Abuse':['Domestic Violence', 'Sexual Violence', "Men's abuse"],
#             'Treatments':['Medication Treatment', 'Psychotherapies', 'Interventional Psychiatric Treatments'],
#             'Medication Treatment': ['Anticonvulsants', 'Anti-psychotics', 'Anti-depressants', 'Benzodiapines (Tranquilizers)', 'Psychedelics/Hallucinogens'],
#             'Psychotherapies':['Family Therapy', 'Dialectical Behavioural Therapy', 'Cognitive Behavioural Therapy', 'Group Therapy', 'Aversion Therapy', 'Exposure Therapy', 'Cognitive Behavioural Play Therapy', 'Interpersonal Therapy', 'Art and Pet Therapy', 'Applied behavioural analysis', 'Mentalization-Based Therapy', 'Psychodynamic Psychotherapy', 'Psychoeducation'],
#             'Interventional Psychiatric Treatments':['Electroconvulsive Therapy', 'Repetitive Transcranial Magnetic Stimulation', 'Magnetic Seizure Therapy', 'Smoking Cessation', 'Harm-Reduction'],
#             'Psychedelics/Hallucinogens': ['MDMA/Ecstasy', 'Ketamine', 'LSD', 'Psilocybin'],
#             'Stigma':['Prejudice', 'Discrimination', 'Self-stigma'],
#             'Social Support Services':['Workplace', 'Housing', 'Financial and Employment'],
#             'Life Transitions and Support/Skills': ['Interpersonal Relationships', 'Parenting', 'Adjustment disorders', 'Separation and Divorce'],
#             'General distress':['Grief and Bereavement', 'Burnout', 'Fatigue', 'Stress', 'Substance use', 'Sleep problems', 'Trauma', 'Self-harm including self-cutting', 'Suicidal ideation'],
#             'General well-being':['Self-care', 'Mindfulness', 'Resiliency'],
#             'Self-regulation': ['Emotional regulation', 'Anger management'],
#             'Physical Health and Nutrition': ['Overweight and Obesity', 'Sexual Health'],
#             'Maternal Mental Health': ['Post-partum', 'Birth-related PTSD'],
#             'Post-partum':['Post-partum depression', 'Post-partum anxiety', 'Post-partum OCD', 'Baby blues'],
#             'Infant and Early Childhood Mental Health (ICEMH)':['Attachment Problems'],
#             'General Supports for Children':['Bullying', 'Gender identity issues', 'Behaviour and Conduct Problems'],
#     }

#     max = 0
#     top_child = ""
#     if current_node not in MH_KG:
#         return current_node
    
#     children = MH_KG[current_node]
#     sim = difflib.get_close_matches(word, children, n=1, cutoff=0.75)
#     # for will run one time only since n=1
#     for s in sim:
#         return s

#     classifier = pipeline("zero-shot-classification", model='cross-encoder/nli-roberta-base')

#     candidate_labels = children
#     res = classifier(word, candidate_labels)
#     df = pd.DataFrame(data=res)
#     df.sort_values(by=['scores'])
#     row_1 = df.iloc[0]
#     print('from travel_mh_kg', row_1)
#     return travel_mh_kg(word, row_1['labels'])


def ResourceViewQuerySet(query_params):
    # Taken from PR #164
    queryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))

    # Search parameters is matched between four fields currently:
    #   - title
    #   - url
    #   - website summary
    #   - definition
    search_param = query_params.get('search')
    if (search_param != None and search_param != ""):
        matching_titles = Resource.objects.filter(title__icontains=search_param)
        matching_url = Resource.objects.filter(url__icontains=search_param)
        matching_description = Resource.objects.filter(description__icontains=search_param)
        matching_definition = Resource.objects.filter(definition__icontains=search_param)
        queryset = queryset.filter(id__in=[resource.id for resource in matching_titles.union(matching_url, matching_description, matching_definition)])

    # Filter resources by categories
    category_param = query_params.get('categories')
    if (category_param != None and category_param != ""):
        # Assumes that tags are separated via commas in a string
        category_list = category_param.split(',')
        queryset = queryset.filter(category__id__in=category_list)

    # Filter resources by tags
    tag_param = query_params.get('tags')
    if (tag_param != None and tag_param != ""):
        # Assumes that tags are separated via commas in a string
        tag_list = tag_param.split(',')
        for tag in tag_list:
            queryset = queryset.filter(Q(tags__id=tag))

    
    return queryset


def calculateCountsForResources(query_params):
    print("****** calc counts ******")
    resQueryset = Resource.objects.filter(visible=1).filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('nurse', 'Nurse')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('over 18', 'Youth')
    ,('lgbtq2s_resources', 'Transgender')
    ,('lgbtq2s_resources', 'Non-Binary')
    ,('paid_resources', 'Fee-for-service available to everyone')
    ,('free_resources', 'Free')
    ,('free_resources', 'Free for members')
    ,('free_resources', 'N/A (ex. websites, podcasts)')
    ,('paid_resources', 'Paid')
    ,('free_resources', 'Requires paid membership')
    ,('free_resources', 'Requires provincial health card')
    ,('paid_and_free', 'Unknown')
    ,('paid_and_free', 'Both free and paid')
    ,('book_and_pamphlet', 'Brochure')
    ,('causes', 'cause')
    ,('group_class', 'Classes/course (in person)')
    ,('virtual', 'Mobile App')
    ,('online_courses_and_webinar', 'Webinar/Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Webinar/Online course (scheduled)')
    ,('screening', 'Screening tool')
    ,('information', 'Statistic')
    ,('information', 'information')
    ,('symptom_List', 'Symptoms')
    ,('treatment_Info', 'Treatments')
    ,('information', 'Informational Website')
    ,('coping_skills', 'Informational Website')
    ,('self_help', 'Informational Website')
    ,('self_help', 'Worksheet')
    ,('online_courses_and_webinar', 'Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Online course (scheduled)')
    ,('self_help', 'Self-Help Books')
    ,('addiction_substance_use_programs', 'Addiction and recovery')
    ,('prevalence', 'Prevalence')
    ,('virtual', 'Online Group Support')
    ,('peer_support', 'Community Support')
    ,('suicidal_other', 'Crisis Support/Distress Counselling')
    ,('suicidal_self', 'Crisis Support/Distress Counselling')
    ,('peer_support', 'Peer Support')
    ,('help_from_another_person', 'Online chat')
    ,('specialist', 'Medical services')
    ,('housing', 'Housing - Emergency')
    ,('group_class', 'Group therapy')
    ,('peer_support', 'In-person Group Support Meeting')
    ,('in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    # ,('doctor', 'Doctor')
    ,('doctor', 'Physician')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Healthcare Workers')
    ,('fire fighter', 'First responder')
    ,('fire fighter', 'Social worker')
    ,('community support', 'Group therapy')
    ,('community support', 'In-person Group Support Meeting')
    ,('community support', 'Peer Support')	
    ,('peer_support', 'Group therapy')
    ,('domestic_abuse_support', 'Violence intervention')
    ,('domestic_abuse_support', 'Domestic Violence')
    ,('domestic_abuse_support', 'Abuse')
    ,('generalized anxiety disorder', 'Anxiety')
    ,('generalized anxiety disorder', 'Generalized Anxiety Disorder')
    ,('generalized anxiety disorder', 'General public/all')
    ,('generalized anxiety disorder', 'Stress')
    ,('health professional','Medical Student')
    ,('health professional','Resident doctor')
    ,('health professional','Service Providers')
    ,('health professional','Social worker')
    ,('alberta','Alberta')
    ,('schizophrenia','Schizophrenia and psychosis')
    ,('covid-19','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('covid','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('eating','Eating Disorders')
    ,('distress','General Distress')
    ,('hiv','Human Immunodeficiency Virus (HIV)')
    ,('addiction','Addictions (including Drugs, Alcohol, and Gambling)')
    ,('addiction','Behavioural Addiction')
    ,('addiction','Substance use')
    ,('resilience','Resiliency')
    ,('psychologist','Therapist/Counsellor/Psychotherapist')
    ,('psychiatrist','Therapist/Counsellor/Psychotherapist')
    ,('coping_skill','Self-Help Books')
    ,('psychedelics','psilocybin')
    ,('crisis_distress_support','Crisis Support/Distress Counselling')
    ,('book_and_pamplet','Book')
    ,('book_and_pamplet','Booklet'),
    ('ptsd', 'Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse'),
    ('military', 'Military Veterans'),
    ('military', 'Family Member of Veteran'),
    ('first responder', 'Fire Fighter'),
    ('first responder', 'Paramedic'),
    ('first responder', 'Police'),
    ('first responder', 'RCMP'),
    ('first responder', 'Emergency Dispatch Officer'),
    # ('first responder', 'First Responder'),
    ('2slgbtq ', '2SLGBTQ+'),
    ('crisis_distress_support', 'General Distress'),
    ('age','Youth'),
    ('age','Mental Health Supports for Youth'),
    ('age','Children'),
    ('age','Adolescent'),
    ('age','Parent/Caregiver')
    ]

    #tags that we should exclude their resources
    ntags_params = query_params.getlist('ntags')
    ntags_params = Tag.objects.filter(name__in=ntags_params).all()
    ntags_ids = list(map(lambda x: x.id, ntags_params))
    ntags_names = list(map(lambda x: x.name, ntags_params))
    
    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))

    tags_params_temp = []    
    for tag in tags_params: 
        if "(" in tag:
            x = tag 
            tags_params_temp.append((x[:x.index("(")], x[x.index("(")+1:-1])) 
        else: 
            tags_params_temp.append((tag,-1)) 
    tags_params = tags_params_temp


    all_possible_tags = Tag.objects.filter(approved=1).all()
    
    all_possible_tags = list(filter(lambda x: x.name not in ntags_names , all_possible_tags))
    all_possible_tags = list(map(lambda x: (x.name, x.tag_category), all_possible_tags))
    all_possible_tag_names = list(map(lambda x: x[0], all_possible_tags))
    all_possible_tag_names_lower_cased = list(map(lambda x: x[0].lower(), all_possible_tags))

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    

    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    class_tag_mapping = {}


    word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))

    for tag_param in tags_params:
        tag_param = tag_param[0]

        if tag_param in all_possible_tag_names or tag_param in all_possible_tag_names_lower_cased:
            #found in approved tags
            for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
        else:
            if tag_param in word_mapping_keys:
                #found in word mapping
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tag_names, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
                    #found using distance



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')



    query_relaxation_tags = []
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))
    
    # finding classes of the
    for tag_ in should_be_added:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0] == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found",tag_)

    for tag_ in tags_params_mapped:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0].lower() == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found",tag_)
    
    # Location
    # Resource format
    # Resource Type for Education/Informational
    # Resource Type for Programs and Services
    # Health Issue
    # Costs
    # Audience
    # Language

    """
    VIP tags are tags that at least on of them
    should be present in a resource to be a candidate 
    it is NOW ONLY mental_health tags
    """

    vip_tags = []
    input_lo_format_infot_servt_mh_cost_au_lang = []
    if 'Location' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Location']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Resource format' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource format']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Education/Informational' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Education/Informational']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Programs and Services' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Programs and Services']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Health Issue' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Health Issue']))
        for item in class_tag_mapping['Health Issue']:
            vip_tags.append(item)
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Costs' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Costs']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Audience' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Audience']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Language' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Language']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)


    global GAZETTEER_cities
    canada_cities = GAZETTEER_cities.copy()
    global GAZETTEER_proviences
    canada_city_proviences = GAZETTEER_proviences.copy()

    loc_tag_List = None
    if 'Location' in class_tag_mapping:
        for loc_tag in class_tag_mapping['Location']:
            loc_tag = loc_tag.lower()
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'Location'))
                loc_tag_List = get_nearby_cities(loc_tag)
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'Location'))
                    loc_tag_List = get_nearby_cities(similar_tags[0])
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'Location'))
                        loc_tag_List = get_nearby_cities(similar_tags[0])

        
    #adding obvious location tags
    query_relaxation_tags.append('Worldwide')
    query_relaxation_tags.append('All Canada')
    query_relaxation_tags.append('General public/all')
    #adding nearby cities
    if loc_tag_List:
        for nearby_city in loc_tag_List:
            query_relaxation_tags.append(nearby_city)
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_romoved)

    if vip_tags:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags)))
    else:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))
    

    #retrieve tag ids from tag names
    tags = Tag.objects.filter(name__in=tags_params).values('id').all()
    input_tags = list(map(lambda x: x['id'], tags))

    
    thisSet = []
    #make result distinct
    for query in resQueryset:
        if query.id not in thisSet:
            thisSet.append(query.id)
    newQuerySet = Resource.objects.filter(id__in=thisSet)

    found_resources = [
        # {"id":1,"tags":[1,3,5,7,9]}
    ]
    for query in newQuerySet:
        res = {'id':query.id, "tags":list(map(lambda x: (x.id, x.tag_category) ,query.tags.all()))}
        found_resources.append(res)
    
    def count_tags(found_resources, consider_mh):
        unique_tags = []
        for found_resource in found_resources:
            for found_resource_tag in found_resource['tags']:
                if(found_resource_tag[1]=="Resource Type for Programs and Services" and (("need_program_services" in tags_params) or ("program_services" in tags_params))):
                    unique_tags.append(found_resource_tag[0])
                elif(found_resource_tag[1]=="Resource Type for Education/Informational" and (("need_information" in tags_params) or ("information" in tags_params)) ):
                    unique_tags.append(found_resource_tag[0])
                if found_resource_tag[1]=="Health Issue" and consider_mh:
                    unique_tags.append(found_resource_tag[0])

   
                    
        unique_tags_counts = collections.Counter(unique_tags)
        return unique_tags_counts

    def entrophy_for_tag(found_resources, tag):
        tag_set_if_present = set()
        tag_set_if_absent = set()
        for found_resource in found_resources:
            if tag in found_resource['tags'][0]:
                for t in found_resource['tags'][0]: tag_set_if_present.add(t)
            else:
                for t in found_resource['tags'][0]: tag_set_if_absent.add(t)
        return (len(tag_set_if_present)+len(tag_set_if_absent))

    res = count_tags(found_resources, False)
    
    if len(res) < 2:
        res = count_tags(found_resources, True)
    
    #pop input tags from counted tags 
    for tag in input_tags:
        if tag in res:
            res.pop(tag)

    for tag in ntags_ids:        
        if tag in res:
            res.pop(tag)


    sorted_selected_tags = list(map(lambda x: x[0], res.most_common(2)))
    # sorted_selected_tags = sorted(selected_tags, key=lambda x: entrophy_for_tag(found_resources,x))
    if(len(sorted_selected_tags)>1):
        btn_1 = Tag.objects.filter(id=sorted_selected_tags[0:2][0]).values('name').get()
        btn_1 = btn_1['name']
    
        btn_2 = Tag.objects.filter(id=sorted_selected_tags[0:2][1]).values('name').get()
        btn_2 = btn_2['name']
        return {'resource_counts': "more than 10", 'btns':[btn_1,btn_2]} #len(newQuerySet)
    else:
        return {'resource_counts':10, 'btns':["General well-being (All/Any)","Mental Health in General"]}


def addViewToResource(query_params):
    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))

    
    tags_params = query_params.getlist('resource_title')
    tags_params = set(tags_params)
    click_type = set(query_params.getlist('click_type'))

    if "click_on_more" in click_type:
        resQueryset = resQueryset.filter(Q(title__in=tags_params))
        for qs in resQueryset:
            qs.chatbot_frontend_click_more_count += 1
            qs.save()
    else:
        resQueryset = resQueryset.filter(Q(title__in=tags_params))
        for qs in resQueryset:
            qs.chatbot_frontend_click_count += 1
            qs.save()

    
    if len(resQueryset)==0:
        return {'statuse':'not done'}
    
    return {'statuse':'done'}

def calculateStatsResources(query_params):
    allRes = Resource.objects.filter(Q(visible=1))
    
    resRej = Resource.objects.filter((Q(review_status="rejected") & Q(review_status_2="rejected")) | (Q(review_status_2_2="rejected") & Q(review_status_1_1="rejected")) | (Q(review_status="rejected") & Q(review_status_2_2="rejected")) | (Q(review_status="rejected") & Q(review_status_1_1="rejected")) | (Q(review_status_2="rejected") & Q(review_status_2_2="rejected")) | (Q(review_status_2="rejected") & Q(review_status_1_1="rejected")) | Q(review_status_3="rejected"))

    rejected_count = len(resRej)

    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    allTags = Tag.objects.filter(approved=1)
    allTags = list(map(lambda x: {"name":x.name, "tag_category":x.tag_category, 'number_of_res':0,} ,allTags))

    resQueryset_ = []
    for resource in resQueryset:
        resQueryset_.append({
            'title':resource.title,
            'chatbot_api_rcmnd_count': resource.chatbot_api_rcmnd_count,
            'portal_search_rcmnd_count': resource.portal_search_rcmnd_count,
            'public_view_count': resource.public_view_count,
        })

    resQueryset_ = sorted(resQueryset_, key= lambda x: x['chatbot_api_rcmnd_count'], reverse=True)


    allTags_ = {}
    for allTag in allTags:
        allTags_[allTag['name']]=allTag
    
    allTagsAndRes = list(map(lambda t:(t.title, t.tags.all()) ,allRes))
    for allTagandRes in allTagsAndRes:
        for tag in allTagandRes[1]:
            if tag.name not in allTags_.keys():
                continue
            allTags_[tag.name]['number_of_res']+=1
            if 'resource_list' not in allTags_[tag.name]:
                allTags_[tag.name]['number_of_app_res'] = 0
                allTags_[tag.name]['resource_list'] = []
            allTags_[tag.name]['resource_list'].append(allTagandRes[0])
    

    allApprovedResourceNames = list(map(lambda x: x.title ,resQueryset))
    for tag_name , tag_resourcelist in allTags_.items():
        if 'resource_list' not in tag_resourcelist.keys():
            continue
        for resource_name in tag_resourcelist['resource_list']:
            if resource_name in allApprovedResourceNames:
                allTags_[tag_name]['number_of_app_res']+=1
        tag_resourcelist['resource_list'] = []
    allTags_ = sorted(allTags_.items(), key= lambda x: x[1]['number_of_res'], reverse=True)

    stats = {
        'resources':{
            'approved count':len(resQueryset),
            'rejected count':rejected_count,
            'pending count':len(allRes)-len(resQueryset)-rejected_count,
            # 'top 1000 most searched': resQueryset_[:1000]
        }, 
        'Tags':{
            'all res count':len(allRes),
            'approved tags': allTags_
        }
    }

    
    return {'data':stats}
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer

def calculateTagWeightsForResources(query_params):
    return []

# def calculateTagWeightsForResources(query_params):
#     resources = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved")).values('id', 'title', 'description', 'organization_description', 'organization_name', 'definition')
#     tags = Tag.objects.filter(approved="1").values('id','name').filter(tag_category="Health Issue")
    
#     resource_text = []
#     resource_index = []
#     all_tags = {}

#     def pre_processing(newValue):
#         newValue = newValue.lower().replace('(',' ').replace(')',' ').replace('\'',' ').replace('\"',' ').replace('`',' ').replace('.','').replace(',','').replace('?','').replace('!','')
#         return newValue

#     for resource in resources:
#         txt = pre_processing(str(resource['id'])+"___"+str(resource['title'])+" "+str(resource['description'])+" "+str(resource['definition'])+" "+str(resource['organization_name'])+" "+str(resource['organization_description'])+" ")
        
#         resource_text.append(txt.lower())
#         resource_index.append(resource['id'])
    
#     for tag in tags:
#         all_tags[tag['name'].lower()] = tag['id']

#     tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range = (1,4))
#     tfidf_vector = tfidf_vectorizer.fit_transform(resource_text)
#     tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=resource_text, columns=tfidf_vectorizer.get_feature_names())
#     tfidf_df = tfidf_df.stack().reset_index()
#     tfidf_df = tfidf_df.rename(columns={0:'tfidf', 'level_0': 'document','level_1': 'term', 'level_2': 'term'})
#     index_names_ = tfidf_df[tfidf_df['tfidf'] < 0.0001].index
#     tfidf_df.drop(index_names_, inplace = True)

#     tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False]).groupby(['document']).head(60)
#     top_tfidf = tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False])

#     response = {}
#     for document in resource_text:
#         doc_id = document[:document.index("___")]
#         res = top_tfidf[top_tfidf['document'].str.startswith((doc_id+"___"))]
#         # print(res,"\n")
#         for tag in all_tags:
#             for index, row in res.iterrows():
#                 if((row['tfidf'] > 0) and (( len(tag)>7 and (" "+tag[:-3]) in row['term'] ) or ((" "+tag+" ") in row['term']))):
#                     t = tag
#                     print(doc_id, '|' , row['term'], '|' ,tag)

#                     if doc_id not in response:
#                         response[doc_id] = {}

#                     if all_tags[t] not in response[doc_id]:
#                         response[doc_id][all_tags[t]] = 0

#                     response[doc_id][all_tags[t]] += row['tfidf']
    

#     for resource_id in response:
#         print('resource_id=',resource_id, "resource_id[]=",response[resource_id])
#         instance = Resource.objects.filter(pk=resource_id).get()
#         instance.index = json.dumps(response[resource_id])
#         instance.save()

#     print("--------------------------------------------done--------------------------------------------")
#     # print(response)
#     return tags
# testing new features
def ResourceByIntentEntityViewQuerySet_new(query_params):
    print("****** new ******")
    resQueryset = Resource.objects.filter(visible=1).filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('nurse', 'Nurse')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('over 18', 'Youth')
    ,('lgbtq2s_resources', 'Transgender')
    ,('lgbtq2s_resources', 'Non-Binary')
    ,('paid_resources', 'Fee-for-service available to everyone')
    ,('free_resources', 'Free')
    ,('free_resources', 'Free for members')
    ,('free_resources', 'N/A (ex. websites, podcasts)')
    ,('paid_resources', 'Paid')
    ,('free_resources', 'Requires paid membership')
    ,('free_resources', 'Requires provincial health card')
    ,('paid_and_free', 'Unknown')
    ,('paid_and_free', 'Both free and paid')
    ,('book_and_pamphlet', 'Brochure')
    ,('causes', 'cause')
    ,('group_class', 'Classes/course (in person)')
    ,('virtual', 'Mobile App')
    ,('online_courses_and_webinar', 'Webinar/Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Webinar/Online course (scheduled)')
    ,('screening', 'Screening tool')
    ,('information', 'Statistic')
    ,('information', 'information')
    ,('symptom_List', 'Symptoms')
    ,('treatment_Info', 'Treatments')
    ,('information', 'Informational Website')
    ,('coping_skills', 'Informational Website')
    ,('self_help', 'Informational Website')
    ,('self_help', 'Worksheet')
    ,('online_courses_and_webinar', 'Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Online course (scheduled)')
    ,('self_help', 'Self-Help Books')
    ,('addiction_substance_use_programs', 'Addiction and recovery')
    ,('prevalence', 'Prevalence')
    ,('virtual', 'Online Group Support')
    ,('peer_support', 'Community Support')
    ,('suicidal_other', 'Crisis Support/Distress Counselling')
    ,('suicidal_self', 'Crisis Support/Distress Counselling')
    ,('peer_support', 'Peer Support')
    ,('help_from_another_person', 'Online chat')
    ,('specialist', 'Medical services')
    ,('housing', 'Housing - Emergency')
    ,('group_class', 'Group therapy')
    ,('peer_support', 'In-person Group Support Meeting')
    ,('in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    # ,('doctor', 'Doctor')
    ,('doctor', 'Physician')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Healthcare Workers')
    ,('fire fighter', 'First responder')
    ,('fire fighter', 'Social worker')
    ,('community support', 'Group therapy')
    ,('community support', 'In-person Group Support Meeting')
    ,('community support', 'Peer Support')	
    ,('peer_support', 'Group therapy')
    ,('domestic_abuse_support', 'Violence intervention')
    ,('domestic_abuse_support', 'Domestic Violence')
    ,('domestic_abuse_support', 'Abuse')
    ,('generalized anxiety disorder', 'Anxiety')
    ,('generalized anxiety disorder', 'Generalized Anxiety Disorder')
    ,('generalized anxiety disorder', 'General public/all')
    ,('generalized anxiety disorder', 'Stress')
    ,('health professional','Medical Student')
    ,('health professional','Resident doctor')
    ,('health professional','Service Providers')
    ,('health professional','Social worker')
    ,('alberta','Alberta')
    ,('schizophrenia','Schizophrenia and psychosis')
    ,('covid-19','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('covid','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('eating','Eating Disorders')
    ,('distress','General Distress')
    ,('hiv','Human Immunodeficiency Virus (HIV)')
    ,('addiction','Addictions (including Drugs, Alcohol, and Gambling)')
    ,('addiction','Behavioural Addiction')
    ,('addiction','Substance use')
    ,('resilience','Resiliency')
    ,('psychologist','Therapist/Counsellor/Psychotherapist')
    ,('psychiatrist','Therapist/Counsellor/Psychotherapist')
    ,('coping_skill','Self-Help Books')
    ,('psychedelics','psilocybin')
    ,('crisis_distress_support','Crisis Support/Distress Counselling')
    ,('book_and_pamplet','Book')
    ,('book_and_pamplet','Booklet'),
    ('ptsd', 'Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse'),
    ('military', 'Military Veterans'),
    ('military', 'Family Member of Veteran'),
    ('first responder', 'Fire Fighter'),
    ('first responder', 'Paramedic'),
    ('first responder', 'Police'),
    ('first responder', 'RCMP'),
    ('first responder', 'Emergency Dispatch Officer'),
    # ('first responder', 'First Responder'),
    ('2slgbtq ', '2SLGBTQ+'),
    ('crisis_distress_support', 'General Distress')
    ]

    n_tags_params = query_params.getlist('ntags')
    n_tags_params = list(map(lambda x: x.lower() ,n_tags_params))
    
    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))

    tags_params_temp = []    
    for tag in tags_params: 
        if "(" in tag:
            x = tag 
            tags_params_temp.append((x[:x.index("(")], x[x.index("(")+1:-1])) 
        else: 
            tags_params_temp.append((tag,-1)) 
    tags_params = tags_params_temp


    all_possible_tags = Tag.objects.filter(approved=1).all()
    
    all_possible_tags = list(filter(lambda x: x.name.lower() not in n_tags_params , all_possible_tags))
    all_possible_tags = list(map(lambda x: (x.name, x.tag_category), all_possible_tags))
    all_possible_tag_names = list(map(lambda x: x[0], all_possible_tags))
    all_possible_tag_names_lower_cased = list(map(lambda x: x[0].lower(), all_possible_tags))

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    

    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    class_tag_mapping = {}


    word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))

    for tag_param in tags_params:
        tag_param = tag_param[0]

        if tag_param in all_possible_tag_names or tag_param in all_possible_tag_names_lower_cased:
            #found in approved tags
            for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
        else:
            if tag_param in word_mapping_keys:
                #found in word mapping
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tag_names, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
                    #found using distance



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')
    
    query_relaxation_tags = []
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))
    
    # finding classes of the
    for tag_ in should_be_added:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0] == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found")

    for tag_ in tags_params_mapped:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0].lower() == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found")
    
    # Location
    # Resource format
    # Resource Type for Education/Informational
    # Resource Type for Programs and Services
    # Health Issue
    # Costs
    # Audience
    # Language

    """
    VIP tags are tags that at least on of them
    should be present in a resource to be a candidate 
    it is NOW ONLY mental_health tags
    """

    vip_tags = []
    input_lo_format_infot_servt_mh_cost_au_lang = []
    if 'Location' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Location']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Resource format' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource format']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Education/Informational' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Education/Informational']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Programs and Services' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Programs and Services']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Health Issue' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Health Issue']))
        for item in class_tag_mapping['Health Issue']:
            vip_tags.append(item)
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Costs' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Costs']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Audience' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Audience']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Language' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Language']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)


    global GAZETTEER_cities
    canada_cities = GAZETTEER_cities.copy()
    global GAZETTEER_proviences
    canada_city_proviences = GAZETTEER_proviences.copy()

    loc_tag_List = None
    if 'Location' in class_tag_mapping:
        for loc_tag in class_tag_mapping['Location']:
            loc_tag = loc_tag.lower()
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'Location'))
                loc_tag_List = get_nearby_cities(loc_tag)
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'Location'))
                    loc_tag_List = get_nearby_cities(similar_tags[0])
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'Location'))
                        loc_tag_List = get_nearby_cities(similar_tags[0])

        
    #adding obvious location tags
    query_relaxation_tags.append('Worldwide')
    query_relaxation_tags.append('All Canada')
    query_relaxation_tags.append('General public/all')
    #adding nearby cities
    if loc_tag_List:
        for nearby_city in loc_tag_List:
            query_relaxation_tags.append(nearby_city)
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_romoved)

    if vip_tags:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags)))
    else:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))



    #retrieve tag ids from tag names
    tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped) | Q(name__in=query_relaxation_tags)).values('id','name','tag_category').all()
    tags_id_list = list(map(lambda x: x['id'], tags))
    tags_name_list = list(map(lambda x: x['name'], tags))
    tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id','tag_category','name').all()
    query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))
    query_relaxation_tags_categories = list(map(lambda x: x['tag_category'], query_relaxation_tags))
    query_relaxation_tags_names = list(map(lambda x: x['name'], query_relaxation_tags))

    
    
    # input_lo_format_infot_servt_mh_cost_au_lang
    # scoring and ordering by scores
    resource_scores = {}
    resource_score_reasons = {}
    for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], resQueryset)):
        resource_scores[resource[0]] = [0,0,0,0,0,0,0,0]
        resource_score_reasons[resource[0]] = ""

        index = None
        original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
        original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
        original_tag_names = list(map(lambda x: str(x.name), resource[2]))

        if resource[1] is not None and resource[1]!='':
            index = json.loads(resource[1])
        
        for i, tag in enumerate(tags_id_list):
            t_cat = tags_cat_list[i]

            tag = str(tag)
            if resource[1] is not None and resource[1]!='':
                if tag in index:
                    if t_cat=="Location":
                        resource_scores[resource[0]][0] += index[tag]
                        resource_score_reasons[resource[0]] += "+ loc score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Resource format":
                        resource_scores[resource[0]][1] += index[tag]
                        resource_score_reasons[resource[0]] += "+ format score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Resource Type for Education/Informational":
                        resource_scores[resource[0]][2] += index[tag]
                        resource_score_reasons[resource[0]] += "+ infoType score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Resource Type for Programs and Services":
                        resource_scores[resource[0]][3] += index[tag]
                        resource_score_reasons[resource[0]] += "+ servType score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Health Issue":
                        resource_scores[resource[0]][4] += index[tag]
                        resource_score_reasons[resource[0]] += "+ MH score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Costs":
                        resource_scores[resource[0]][5] += index[tag]
                        resource_score_reasons[resource[0]] += "+ Costs score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Audience":
                        resource_scores[resource[0]][6] += index[tag]
                        resource_score_reasons[resource[0]] += "+ Audi score from TF-IDF for "+tags_name_list[i]
                    elif t_cat=="Language":
                        resource_scores[resource[0]][7] += index[tag]
                        resource_score_reasons[resource[0]] += "+ lang score from TF-IDF for "+tags_name_list[i]

            if tag in original_tag_ids:
                ii = original_tag_ids.index(tag)
                sc = 10
                if original_tag_categories[ii] == 'Location':
                    resource_scores[resource[0]][0] += sc 
                    resource_score_reasons[resource[0]] += "+ loc score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Resource format':
                    resource_scores[resource[0]][1] += sc 
                    resource_score_reasons[resource[0]] += "+ format score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Resource Type for Education/Informational':
                    resource_scores[resource[0]][2] += sc 
                    resource_score_reasons[resource[0]] += "+ infoType score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Resource Type for Programs and Services':
                    resource_scores[resource[0]][3] += sc 
                    resource_score_reasons[resource[0]] += "+ ServType score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Health Issue':
                    resource_scores[resource[0]][4] += sc 
                    resource_score_reasons[resource[0]] += "+ MH score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Costs':
                    resource_scores[resource[0]][5] += sc 
                    resource_score_reasons[resource[0]] += "+ costs score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Audience':
                    resource_scores[resource[0]][6] += sc 
                    resource_score_reasons[resource[0]] += "+ Audi score from tags for "+original_tag_names[ii]
                elif original_tag_categories[ii] == 'Language':
                    resource_scores[resource[0]][7] += sc 
                    resource_score_reasons[resource[0]] += "+ lang score from tags for "+original_tag_names[ii]
            elif tag in query_relaxation_tags_id:
                ii = query_relaxation_tags_id.index(tag)
                sc = 1
                if query_relaxation_tags_categories[ii] == 'Location':
                    resource_scores[resource[0]][0] += sc 
                    resource_score_reasons[resource[0]] += "& loc score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Resource format':
                    resource_scores[resource[0]][1] += sc 
                    resource_score_reasons[resource[0]] += "& format score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Resource Type for Education/Informational':
                    resource_scores[resource[0]][2] += sc 
                    resource_score_reasons[resource[0]] += "& infoType score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Resource Type for Programs and Services':
                    resource_scores[resource[0]][3] += sc 
                    resource_score_reasons[resource[0]] += "& servType score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Health Issue':
                    resource_scores[resource[0]][4] += sc 
                    resource_score_reasons[resource[0]] += "& MH score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Costs':
                    resource_scores[resource[0]][5] += sc 
                    resource_score_reasons[resource[0]] += "& Costs score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Audience':
                    resource_scores[resource[0]][6] += sc 
                    resource_score_reasons[resource[0]] += "& Audi score from tags for "+query_relaxation_tags_names[ii]
                elif query_relaxation_tags_categories[ii] == 'Language':
                    resource_scores[resource[0]][7] += sc 
                    resource_score_reasons[resource[0]] += "& Lang score from tags for "+query_relaxation_tags_names[ii]

                
                
                

        resource_scores[resource[0]] = torch.dot(torch.FloatTensor(input_lo_format_infot_servt_mh_cost_au_lang), torch.FloatTensor(resource_scores[resource[0]])).numpy()/1000

        # print(resource_scores[resource[0]])

        #tags_params_mapped = string value of tags
        for tag in tags_params_mapped:
            if len(tag)<2:
                continue

            if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.05
                resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
            
            if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.05
                resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
            
            
            if (tag == 'Informational Website' or tag == 'informational website') and (resource[4] == 'RS' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 1
                resource_score_reasons[resource[0]] += "& overal score, resource is informational or both. tag:"+tag
            if (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 1
                resource_score_reasons[resource[0]] += "& overal score, resource is prog_serv or both. tag:"+tag

            if (tag == 'Definition' or tag == 'definition') and (resource[5]):
                resource_scores[resource[0]] += 3
                resource_score_reasons[resource[0]] += "& overal score, resource has a definition. tag:"+tag

            if (tag == 'Domestic Violence' or tag == 'domestic violence') and ("sheltersafe" in resource[3].lower()):
                resource_scores[resource[0]] += 0.05
                resource_score_reasons[resource[0]] += "& overal score, resource has shelter in its title. tag:"+tag

            if (tag == 'Therapist/Counsellor/Psychotherapist') and ("counsel" in resource[3].lower()):
                resource_scores[resource[0]] += 0.05
                resource_score_reasons[resource[0]] += "& overal score, resource has counsel in its title. tag: "+tag

            sum_tag = ""
            for w in tag.replace("-", " ").split(" "):
                if len(w)>0: sum_tag += w[0]
            if (len(sum_tag) > 2) and (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                resource_scores[resource[0]] += 0.05
                resource_score_reasons[resource[0]] += "& acronym in title of resource found. tag:"+tag

            if ('MDSC' in resource[3]) or ('CAMH' in resource[3]) or\
            ('CMHA' in resource[3]) or ('SAMHSA' in resource[3]) or\
            ('WHO' in resource[3]) or ('CDC' in resource[3]):
                resource_scores[resource[0]] += 0.0001
                resource_score_reasons[resource[0]] += "& resource organization is well known"
        

    #topitems = heapq.nlargest(15, resource_scores.items(), key=itemgetter(1))
    topitems = sorted(resource_scores.items(), key=lambda x:x[1], reverse=True)

    topitemsasdict = dict(topitems)

    if len(topitems) > 1:
        resQueryset = resQueryset.filter(id__in=topitemsasdict.keys())

        
        thisSet = []
        #make result distinct
        for query in resQueryset:
            if query.id not in thisSet:
                thisSet.append(query.id)
        newQuerySet = Resource.objects.filter(id__in=thisSet)
        for qs in newQuerySet:
            qs.chatbot_api_rcmnd_count += 1
            qs.save()
            
            if qs.id not in topitemsasdict.keys():
                qs.score = 0
            else:
                tagsQuerySet = list(map(lambda x: x.name ,Tag.objects.filter(resource__in=[qs.id])))
                tagsQuerySet_lower = list(map(lambda x: x.lower(), tagsQuerySet))
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet) or (tqs in tagsQuerySet_lower)]

                qs.index = {"t":number_of_filters, "r":resource_score_reasons[qs.id]}
                # gives more score to resources that that have most of our requested tags.
                qs.score = topitemsasdict[qs.id] + len(number_of_filters) - (len(tagsQuerySet_lower)*0.01)


        return newQuerySet


    return resQueryset

def replace_eng_with_fr_tags(tag_list):
    lookup_table = {}
    try:
        with open('/etc/ChatbotPortal/public/french_lookup_table.csv', mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                lookup_table[row['eng_tag'].lower()] = row['fr_tag']
            
        complete_french_tags = [value.lower() for value in lookup_table.values()]
        corresponding_english_tags = [key.lower() for key in lookup_table.keys()]

        for i,tag in enumerate(tag_list):
            tag = tag.lower()
            try:
                if tag in corresponding_english_tags:
                    print("***Replacing Eng with French***")
                    print(tag,lookup_table[tag])
                    tag_list[i] = (lookup_table[tag]) 
            except KeyError:
                print(f"KeyError: '{tag}' not found in lookup_table.")

        return tag_list

    except FileNotFoundError:
        print("The french lookup table file does not exist **init**.")

# rasa will call it
def ResourceByIntentEntityViewQuerySet_new_new(query_params):
    print("****** new new ******")
    
    resQueryset = Resource.objects.filter(visible=1).filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('nurse', 'Nurse')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('over 18', 'Youth')
    ,('lgbtq2s_resources', 'Transgender')
    ,('lgbtq2s_resources', 'Non-Binary')
    ,('paid_resources', 'Fee-for-service available to everyone')
    ,('free_resources', 'Free')
    ,('free_resources', 'Free for members')
    ,('free_resources', 'N/A (ex. websites, podcasts)')
    ,('paid_resources', 'Paid')
    ,('free_resources', 'Requires paid membership')
    ,('free_resources', 'Requires provincial health card')
    ,('paid_and_free', 'Unknown')
    ,('paid_and_free', 'Both free and paid')
    ,('book_and_pamphlet', 'Brochure')
    ,('causes', 'cause')
    ,('group_class', 'Classes/course (in person)')
    ,('virtual', 'Mobile App')
    ,('online_courses_and_webinar', 'Webinar/Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Webinar/Online course (scheduled)')
    ,('screening', 'Screening tool')
    ,('information', 'Statistic')
    ,('information', 'information')
    ,('symptom_List', 'Symptoms')
    ,('treatment_Info', 'Treatments')
    ,('information', 'Informational Website')
    ,('coping_skills', 'Informational Website')
    ,('self_help', 'Informational Website')
    ,('self_help', 'Worksheet')
    ,('online_courses_and_webinar', 'Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Online course (scheduled)')
    ,('self_help', 'Self-Help Books')
    ,('addiction_substance_use_programs', 'Addiction and recovery')
    ,('prevalence', 'Prevalence')
    ,('virtual', 'Online Group Support')
    ,('peer_support', 'Community Support')
    ,('suicidal_other', 'Crisis Support/Distress Counselling')
    ,('suicidal_self', 'Crisis Support/Distress Counselling')
    ,('peer_support', 'Peer Support')
    ,('help_from_another_person', 'Online chat')
    ,('specialist', 'Medical services')
    ,('housing', 'Housing - Emergency')
    ,('group_class', 'Group therapy')
    ,('peer_support', 'In-person Group Support Meeting')
    ,('in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    # ,('doctor', 'Doctor')
    ,('doctor', 'Physician')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Healthcare Workers')
    ,('fire fighter', 'First responder')
    ,('fire fighter', 'Social worker')
    ,('community support', 'Group therapy')
    ,('community support', 'In-person Group Support Meeting')
    ,('community support', 'Peer Support')	
    ,('peer_support', 'Group therapy')
    ,('domestic_abuse_support', 'Violence intervention')
    ,('domestic_abuse_support', 'Domestic Violence')
    ,('domestic_abuse_support', 'Abuse')
    ,('generalized anxiety disorder', 'Anxiety')
    ,('generalized anxiety disorder', 'Generalized Anxiety Disorder')
    ,('generalized anxiety disorder', 'General public/all')
    ,('generalized anxiety disorder', 'Stress')
    ,('health professional','Medical Student')
    ,('health professional','Resident doctor')
    ,('health professional','Service Providers')
    ,('health professional','Social worker')
    ,('healthcare_worker','Healthcare workers')
    ,('alberta','Alberta')
    ,('schizophrenia','Schizophrenia and psychosis')
    ,('covid-19','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('covid','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('eating','Eating Disorders')
    ,('distress','General Distress')
    ,('hiv','Human Immunodeficiency Virus (HIV)')
    ,('addiction','Addictions (including Drugs, Alcohol, and Gambling)')
    ,('addiction','Behavioural Addiction')
    ,('addiction','Substance use')
    ,('resilience','Resiliency')
    ,('psychologist','Therapist/Counsellor/Psychotherapist')
    ,('psychiatrist','Therapist/Counsellor/Psychotherapist')
    ,('coping_skill','Self-Help Books')
    ,('psychedelics','psilocybin')
    ,('crisis_distress_support','Crisis Support/Distress Counselling')
    ,('book_and_pamplet','Book')
    ,('book_and_pamplet','Booklet'),
    ('ptsd', 'Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse'),
    ('military', 'Military Veterans'),
    ('military', 'Family Member of Veteran'),
    ('first responder', 'Fire Fighter'),
    ('first responder', 'Paramedic'),
    ('first responder', 'Police'),
    ('first responder', 'RCMP'),
    ('first responder', 'Emergency Dispatch Officer'),
    # ('first responder', 'First Responder'),
    ('2slgbtq ', '2SLGBTQ+'),
    ('crisis_distress_support', 'General Distress'),
    ('age','Youth'),
    ('age','Mental Health Supports for Youth'),
    ('age','Children'),
    ('age','Adolescent'),
    ('age','Parent/Caregiver')
    
    ]

    french_flag = False

    n_tags_params = query_params.getlist('ntags')
    n_tags_params = list(map(lambda x: x.lower() ,n_tags_params))
    
    tags_params = query_params.getlist('tags')
    
    #print(find_most_similar_phrase('healthcare workers',tags_params))

    print("***before init***")
    for tag in tags_params:
        print(tag)
        #replacing english tags with french tags
    if any(tag.lower() in ['french', 'français'] for tag in tags_params):
        french_flag = True
        print("French is true")
        
        #TODO
        tags_params = replace_eng_with_fr_tags(tags_params)

    print("***after init***")
    for tag in tags_params:
        print(tag)

    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))

    tags_params_temp = []    
    for tag in tags_params: 
    #    if "(" in tag:
    #       x = tag 
    #       tags_params_temp.append((x[:x.index("(")], x[x.index("(")+1:-1])) 
    #    else: 
        tags_params_temp.append((tag,-1)) 
    tags_params = tags_params_temp


    all_possible_tags = Tag.objects.filter(approved=1).all()
    
    all_possible_tags = list(filter(lambda x: x.name.lower() not in n_tags_params , all_possible_tags))
    all_possible_tags = list(map(lambda x: (x.name, x.tag_category), all_possible_tags))
    all_possible_tag_names = list(map(lambda x: x[0], all_possible_tags))
    all_possible_tag_names_lower_cased = list(map(lambda x: x[0].lower(), all_possible_tags))
    

    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    class_tag_mapping = {}


    word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))

    for tag_param in tags_params:
        tag_param = tag_param[0]

        if tag_param in all_possible_tag_names or tag_param in all_possible_tag_names_lower_cased:
            #found in approved tags
            for related_word in filter(lambda x: x[0] == tag_param, word_mapping):
                    should_be_added.add(related_word[1])
        else:
            if tag_param in word_mapping_keys:
                #found in word mapping
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tag_names, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
                    #found using distance



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')

    
    query_relaxation_tags = []
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))

    print("**** Printing tags_params_mapped ****")
    for tag in tags_params_mapped:
        print(tag)

    
    # finding classes of the
    for tag_ in should_be_added:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0] == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found",tag_)

    for tag_ in tags_params_mapped:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0].lower() == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found",tag_)

    print("**** Printing class_tag_mapping before ****")
    print(class_tag_mapping)
    
    # Location
    # Resource format
    # Resource Type for Education/Informational
    # Resource Type for Programs and Services
    # Health Issue
    # Costs
    # Audience
    # Language

    """
    VIP tags are tags that at least on of them
    should be present in a resource to be a candidate 
    it is NOW ONLY mental_health tags
    """

    vip_tags = []
    filter_out_tags = [
        "indigenous", "first nation", "inuit", "indigenous women", "indigenous Men", "inuit", "kapawe'no", "l'nu'k (mi'kmaq)", "métis", "mi'kmaw", "siksika", "cree", 
        "acadia first nation", "annapolis valley first nation", "bear river first nation", "eskasoni first nation", "glooscap first nation",
        "millbrook first nation",
        "wagmatcook first nation",
        "we'koqma'q first nation",
        "sipekne’katik first nation",
        "kapawe’no first nation",
        "paqtnkek mi'kmaw nation",
        "pictou landing",
        'french', 
        'youth', 
        'military veterans', 
        'healthcare workers', 
        '2slgbtq+', 
        'first responders'
        ]
    input_lo_format_infot_servt_mh_cost_au_lang = []

    

    if 'Location' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Location']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Resource format' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource format']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Education/Informational' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Education/Informational']))
    elif 'Type de ressource' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Type de ressource']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Programs and Services' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Programs and Services']))
    elif 'Type de ressource' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Type de ressource']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Health Issue' in class_tag_mapping:
        
        if french_flag:
            #VARSHINI TODO
            vip_tags.append('français')
            #if class_tag_mapping['Health Issue'].lower() in 
            if 'Problème de santé' in class_tag_mapping:
                
                for item in class_tag_mapping['Problème de santé']:
                    try:
                        if item.lower() in complete_french_tags:
                            vip_tags.append(item)
                            input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Problème de santé']))
                            print("***VIP***",item)

                        
                    except UnboundLocalError:

                        lookup_table = {}
                        try:
                            with open('/etc/ChatbotPortal/public/french_lookup_table.csv', mode='r', encoding='utf-8') as csv_file:
                                csv_reader = csv.DictReader(csv_file)
                                for row in csv_reader:
                                    lookup_table[row['eng_tag']] = row['fr_tag']
                                complete_french_tags = [value.lower() for value in lookup_table.values()]
                                corresponding_english_tags = [key.lower() for key in lookup_table.keys()]

                                

                                #if item.lower() in complete_french_tags:
                                #vip_tags.append(item)
                                    #input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Problème de santé']))
                                    #print("***VIP***",item)

                                #elif item.lower() in lookup_table:
                                    #vip_tags.append(lookup_table[item])
                                
                                input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Problème de santé']))
                                for item in class_tag_mapping['Problème de santé']:
                                    vip_tags.append(item)

                                vip_tags = replace_eng_with_fr_tags(vip_tags)
                                print('**French replacement**',vip_tags)
                        except FileNotFoundError:
                            print("The french lookup table file does not exist. **vip**")

                        #print("***VIP Fr***",lookup_table[item])
            else:
                input_lo_format_infot_servt_mh_cost_au_lang.append(1)


        else:
            input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Health Issue']))
            for item in class_tag_mapping['Health Issue']:
                vip_tags.append(item)
    else:    
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Costs' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Costs']))
    elif 'Coûts' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Coûts']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Audience' in class_tag_mapping:
        if french_flag:

            class_tag_mapping['Public'] = replace_eng_with_fr_tags(class_tag_mapping['Audience'])

            for item in class_tag_mapping['Public']:
                vip_tags.append(item)
                print(class_tag_mapping['Public'])

        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Public']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Language' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Language']))
    elif 'Langue' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Langue']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    print("**** Printing class_tag_mapping after ****")
    print(class_tag_mapping)


    global GAZETTEER_cities
    canada_cities = GAZETTEER_cities.copy()
    global GAZETTEER_proviences
    canada_city_proviences = GAZETTEER_proviences.copy()

    loc_tag_List = None
    if 'Location' in class_tag_mapping:
        for loc_tag in class_tag_mapping['Location']:
            loc_tag = loc_tag.lower()
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'Location'))
                loc_tag_List = get_nearby_cities(loc_tag)
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'Location'))
                    loc_tag_List = get_nearby_cities(similar_tags[0])
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'Location'))
                        loc_tag_List = get_nearby_cities(similar_tags[0])

    #adding french tags:
    if french_flag:
        print("**** Test params mapped ***")
        print(len(tags_params_mapped))
        print(len(query_relaxation_tags))
        tags_params_mapped = replace_eng_with_fr_tags(tags_params_mapped)
        query_relaxation_tags = replace_eng_with_fr_tags(query_relaxation_tags)

    #adding obvious location tags
    if not french_flag:
        query_relaxation_tags.append('Worldwide')
        query_relaxation_tags.append('All Canada')
        query_relaxation_tags.append('General public/all')

    #adding nearby cities
    if loc_tag_List:
        for nearby_city in loc_tag_List:
            query_relaxation_tags.append(nearby_city)
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_romoved)

    #adding french tags:
    #if french_flag:
        #for tag in tags_params_mapped:
            #if english tag has a french counterpart and not in tags_params_mapped, add to list
            #if tag in lookup_table and lookup_table[tag] not in tags_params_mapped:
                #tags_params_mapped.append(tags_params_mapped)
    
    if french_flag:

        # Remove 'Health Issue' from the dictionary
        if 'Health Issue' in class_tag_mapping:
            del class_tag_mapping['Health Issue']
        if 'Audience' in class_tag_mapping:
            del class_tag_mapping['Audience']

        french_tags = [value for values in class_tag_mapping.values() for value in values]

    print("\n***VIP***\n",vip_tags)
    if vip_tags and french_flag:
        print('****Executing vip and french****')
        # Remove 'Health Issue' from the dictionary
        if 'Health Issue' in class_tag_mapping:
            del class_tag_mapping['Health Issue']
        if 'Audience' in class_tag_mapping:
            del class_tag_mapping['Audience']

        french_tags = list(set([value for values in class_tag_mapping.values() for value in values]))

        print(french_tags)

        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & Q(tags__name__in=french_tags))
        resQuerysetRelaxed = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=french_tags) | Q(tags__name__in=query_relaxation_tags)))

    elif vip_tags:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & Q(tags__name__in=tags_params_mapped))
        resQuerysetRelaxed = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags)))
    else:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped))
        resQuerysetRelaxed = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))

    #handle filtering
    #for each filter item, filter out all entries on the filter list
    resQueryset = resQueryset.exclude(Q(tags__name__in=filter_out_tags) & ~Q(tags__name__in=["Non-Exclusive"]) )
    resQuerysetRelaxed = resQuerysetRelaxed.exclude(Q(tags__name__in=filter_out_tags) & ~Q(tags__name__in=["Non-Exclusive"]))

    #filter out english resources if french flow
    #if french_flag:
        #filter_out_eng = ['English']
        #resQueryset = resQueryset.exclude(Q(tags__name__in=filter_out_eng) & ~Q(tags__name__in=["Non-Exclusive"]) )
        #resQuerysetRelaxed = resQuerysetRelaxed.exclude(Q(tags__name__in=filter_out_eng) & ~Q(tags__name__in=["Non-Exclusive"]))

    #for each matching filter item in the query tags, re-add all resources to that query
    if not french_flag:
        tags_to_add_list = tags_params_mapped
    else:
        tags_to_add_list = french_tags

    to_add_back = []
    for item in tags_to_add_list:
            #single item vs list
            if item.lower() in filter_out_tags: 
                to_add_back.append(item.lower())
                print(item.lower())
    #if we have things to add back, recreate the queries
    if len(to_add_back) > 0:
        thisSet = []
        for query in resQueryset:
            if query.id not in thisSet:
                thisSet.append(query.id)
        resQueryset = Resource.objects.filter(Q(id__in=thisSet) | Q(tags__name__in=to_add_back)).filter(
            (Q(review_status="approved") & Q(review_status_2="approved")) 
            | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) 
            | (Q(review_status="approved") & Q(review_status_2_2="approved")) 
            | (Q(review_status="approved") & Q(review_status_1_1="approved")) 
            | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) 
            | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) 
            | Q(review_status_3="approved"))
        
        thisSet = []
        for query in resQuerysetRelaxed:
            if query.id not in thisSet:
                thisSet.append(query.id)
        resQuerysetRelaxed = Resource.objects.filter(Q(id__in=thisSet) | Q(tags__name__in=to_add_back)).filter(
            (Q(review_status="approved") & Q(review_status_2="approved")) 
            | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) 
            | (Q(review_status="approved") & Q(review_status_2_2="approved")) 
            | (Q(review_status="approved") & Q(review_status_1_1="approved")) 
            | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) 
            | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) 
            | Q(review_status_3="approved"))
    


    #filter by location, so we guarantee we have something related (if it exists)
    if 'Location' in class_tag_mapping:
        nquery = resQueryset.filter(visible=1).filter(tags__name__in=class_tag_mapping['Location'])

        #only actually update the queryset if we have matches
        if len(nquery)!=0:
            #print(class_tag_mapping['Location'])
            resQueryset = nquery

        #only hard location filter if we aren't relaxing the query
        #nquery = resQuerysetRelaxed.filter(visible=1).filter(tags__name__in=class_tag_mapping['Location'])

        #only actually update the queryset if we have matches
        #if len(nquery)!=0:
            #print(class_tag_mapping['Location'])
            #resQuerysetRelaxed = nquery

    #retrieve tag ids from tag names
    if french_flag:
        # Remove 'Health Issue' from the dictionary
        if 'Health Issue' in class_tag_mapping:
            del class_tag_mapping['Health Issue']
        if 'Audience' in class_tag_mapping:
            del class_tag_mapping['Audience']

        french_tags = list(set([value for values in class_tag_mapping.values() for value in values]))
        tags = Tag.objects.filter(approved=1).filter(Q(name__in=french_tags)).values('id','name','tag_category').all()
    else:

        tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped) | Q(name__in=query_relaxation_tags)).values('id','name','tag_category').all()
    #tags_id_list = list(map(lambda x: x['id'], tags))
    #tags_name_list = list(map(lambda x: x['name'], tags))
    #tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    print("***before scoring***")
    print(tags,'\n')
    print(query_relaxation_tags)
    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id','tag_category','name').all()

    print("***before scoring QR***")
    print(tags,'\n')
    print(query_relaxation_tags)
    #query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))
    #query_relaxation_tags_categories = list(map(lambda x: x['tag_category'], query_relaxation_tags))
    #query_relaxation_tags_names = list(map(lambda x: x['name'], query_relaxation_tags))

    def scoring(querySet, tags_params_mapped, query_relaxation_tags,QR=1):

        french_flag = False

        if 'français' in tags_params_mapped:
            french_flag = True
            lookup_table = {}
            try:
                with open('/etc/ChatbotPortal/public/french_lookup_table.csv', mode='r', encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        lookup_table[row['eng_tag']] = row['fr_tag']
                    
                complete_french_tags = [value.lower() for value in lookup_table.values()]
                corresponding_english_tags = [key.lower() for key in lookup_table.keys()]
            except FileNotFoundError:
                print("The french lookup table file does not exist **scoring**.")



        if QR: 
            #do query relaxation
            #tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped) | Q(name__in=query_relaxation_tags)).values('id','name','tag_category').all()
            tags_id_list = list(map(lambda x: x['id'], tags))
            tags_name_list = list(map(lambda x: x['name'], tags))
            tags_cat_list = list(map(lambda x: x['tag_category'], tags))

            #query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id','tag_category','name').all()
            query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))
            query_relaxation_tags_categories = list(map(lambda x: x['tag_category'], query_relaxation_tags))
            query_relaxation_tags_names = list(map(lambda x: x['name'], query_relaxation_tags))

        else:
            #no query relaxation
            #tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped)).values('id','name','tag_category').all()
            tags_id_list = list(map(lambda x: x['id'], tags))
            tags_name_list = list(map(lambda x: x['name'], tags))
            tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    
        # input_lo_format_infot_servt_mh_cost_au_lang
        # scoring and ordering by scores
        resource_scores = {}
        resource_score_reasons = {}
        for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], querySet.distinct())):
            resource_scores[resource[0]] = [0,0,0,0,0,0,0,0]
            resource_score_reasons[resource[0]] = ""

            index = None
            original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
            original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
            original_tag_names = list(map(lambda x: str(x.name), resource[2]))

            if resource[1] is not None and resource[1]!='':
                index = json.loads(resource[1])
            
            for i, tag in enumerate(tags_id_list):
                t_cat = tags_cat_list[i]

                tag = str(tag)

                if resource[1] is not None and resource[1]!='':
                    if tag in index:
                        if t_cat=="Location":
                            resource_scores[resource[0]][0] += index[tag]
                            resource_score_reasons[resource[0]] += "& loc score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource format":
                            resource_scores[resource[0]][1] += index[tag]
                            resource_score_reasons[resource[0]] += "& format score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource Type for Education/Informational":
                            resource_scores[resource[0]][2] += index[tag]
                            resource_score_reasons[resource[0]] += "& infoType score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource Type for Programs and Services":
                            resource_scores[resource[0]][3] += index[tag]
                            resource_score_reasons[resource[0]] += "& servType score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Health Issue":
                            resource_scores[resource[0]][4] += index[tag]
                            resource_score_reasons[resource[0]] += "& MH score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Costs":
                            resource_scores[resource[0]][5] += index[tag]
                            resource_score_reasons[resource[0]] += "& Costs score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Audience":
                            resource_scores[resource[0]][6] += index[tag]
                            resource_score_reasons[resource[0]] += "& Audi score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Language":
                            resource_scores[resource[0]][7] += index[tag]
                            resource_score_reasons[resource[0]] += "& lang score from TF-IDF for "+tags_name_list[i]

                if tag in original_tag_ids:
                    ii = original_tag_ids.index(tag)
                    sc = 10
                    if original_tag_categories[ii] == 'Location':
                        resource_scores[resource[0]][0] += sc 
                        resource_score_reasons[resource[0]] += "& loc score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource format':
                        resource_scores[resource[0]][1] += sc 
                        resource_score_reasons[resource[0]] += "& format score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource Type for Education/Informational':
                        resource_scores[resource[0]][2] += sc 
                        resource_score_reasons[resource[0]] += "& infoType score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource Type for Programs and Services':
                        resource_scores[resource[0]][3] += sc 
                        resource_score_reasons[resource[0]] += "& ServType score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Health Issue':
                        resource_scores[resource[0]][4] += sc 
                        resource_score_reasons[resource[0]] += "& MH score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Costs':
                        resource_scores[resource[0]][5] += sc 
                        resource_score_reasons[resource[0]] += "& costs score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Audience':
                        resource_scores[resource[0]][6] += sc 
                        resource_score_reasons[resource[0]] += "& Audi score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Language':
                        resource_scores[resource[0]][7] += sc 
                        resource_score_reasons[resource[0]] += "& lang score from tags for "+original_tag_names[ii]
                elif QR and tag in query_relaxation_tags_id:
                    ii = query_relaxation_tags_id.index(tag)
                    sc = 1
                    if query_relaxation_tags_categories[ii] == 'Location':
                        resource_scores[resource[0]][0] += sc 
                        resource_score_reasons[resource[0]] += "& loc score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource format':
                        resource_scores[resource[0]][1] += sc 
                        resource_score_reasons[resource[0]] += "& format score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource Type for Education/Informational':
                        resource_scores[resource[0]][2] += sc 
                        resource_score_reasons[resource[0]] += "+ infoType score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource Type for Programs and Services':
                        resource_scores[resource[0]][3] += sc 
                        resource_score_reasons[resource[0]] += "& servType score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Health Issue':
                        resource_scores[resource[0]][4] += sc 
                        resource_score_reasons[resource[0]] += "& MH score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Costs':
                        resource_scores[resource[0]][5] += sc 
                        resource_score_reasons[resource[0]] += "& Costs score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Audience':
                        resource_scores[resource[0]][6] += sc 
                        resource_score_reasons[resource[0]] += "& Audi score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Language':
                        resource_scores[resource[0]][7] += sc 
                        resource_score_reasons[resource[0]] += "& Lang score from tags for "+query_relaxation_tags_names[ii]

            resource_scores[resource[0]] = torch.dot(torch.FloatTensor(input_lo_format_infot_servt_mh_cost_au_lang), torch.FloatTensor(resource_scores[resource[0]])).numpy()/1000
            #if not QR:
                #print(f"{resource_scores[resource[0]]} - {resource[3]}")


            # print(resource_scores[resource[0]])
            #tags_params_mapped = string value of tags
            #print("*** Final tags_params_mapped ***")


            for tag in tags_params_mapped:
                #print(tag)
                if 'français' in tags_params_mapped:
                    if tag.lower() in complete_french_tags and tag!= "français" or tag!="Français":
                        if tag in resource[3] or tag.lower() in resource[3].lower():
                            resource_scores[resource[0]] += 5
                            resource_score_reasons[resource[0]] += "relevant french tag:"+tag

                        #corresponding_eng_tag = lambda d, v: next((k for k, val in lookup_table.items() if val == tag), None)





                if len(tag)<2:
                    continue

                if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
                
                if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
                
                
                if (tag == 'Informational Website' or tag == 'informational website') and (resource[4] == 'RS' or resource[4] == 'BT'):
                    resource_scores[resource[0]] += 1
                    resource_score_reasons[resource[0]] += "& overal score, resource is informational or both. tag:"+tag
                if (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                    resource_scores[resource[0]] += 1
                    resource_score_reasons[resource[0]] += "& overal score, resource is prog_serv or both. tag:"+tag

                if (tag == 'Definition' or tag == 'definition') and (resource[5]):
                    resource_scores[resource[0]] += 3
                    resource_score_reasons[resource[0]] += "& overal score, resource has a definition. tag:"+tag

                if (tag == 'Domestic Violence' or tag == 'domestic violence') and ("sheltersafe" in resource[3].lower()):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, resource has shelter in its title. tag:"+tag

                if (tag == 'Therapist/Counsellor/Psychotherapist') and ("counsel" in resource[3].lower()):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, resource has counsel in its title. tag: "+tag

                sum_tag = ""
                for w in tag.replace("-", " ").split(" "):
                    if len(w)>0: sum_tag += w[0]
                if (len(sum_tag) > 2) and (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& acronym in title of resource found. tag:"+tag

                if ('MDSC' in resource[3]) or ('CAMH' in resource[3]) or\
                ('CMHA' in resource[3]) or ('SAMHSA' in resource[3]) or\
                ('WHO' in resource[3]) or ('CDC' in resource[3]):
                    resource_scores[resource[0]] += 0.0001
                    resource_score_reasons[resource[0]] += "& resource organization is well known"

                if french_flag:
                    if 'Français' in resource[3]:
                        resource_scores[resource[0]] += 7
                        resource_score_reasons[resource[0]] += "French resource"
                    if 'French' in resource[3]:
                        resource_scores[resource[0]] += 3
                        resource_score_reasons[resource[0]] += "French resource"

            if not QR:
                print(f"{resource_scores[resource[0]]} - {resource[3]}")


        return resource_scores
    
        #
        
    scores = scoring(resQueryset, tags_params_mapped, query_relaxation_tags,0)
    scores_relaxed = scoring(resQuerysetRelaxed, tags_params_mapped, query_relaxation_tags,1)

    #No Query Relaxation
    topitems = heapq.nlargest(15, scores.items(), key=itemgetter(1))
    #topitems = sorted(resource_scores.items(), key=lambda x:x[1], reverse=True)
    topitemsasdict = dict(topitems)
    newQuerySet = Resource.objects.none()
    if len(topitems) >= 1:
        newQuerySet = resQueryset.filter(id__in=topitemsasdict.keys()).distinct()
        thisSet = []
        #make result distinct
        #for query in resQueryset:
        #    if query.id not in thisSet:
        #        thisSet.append(query.id)
        #newQuerySet = Resource.objects.filter(id__in=thisSet)
        for qs in newQuerySet:
            qs.chatbot_api_rcmnd_count += 1
            qs.save()
            
            if qs.id not in topitemsasdict.keys():
                qs.score = 0
            else:
                tagsQuerySet = list(map(lambda x: x.name ,Tag.objects.filter(resource__in=[qs.id])))
                tagsQuerySet_lower = list(map(lambda x: x.lower(), tagsQuerySet))
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet) or (tqs in tagsQuerySet_lower)]

                qs.index = number_of_filters
                # gives more score to resources that that have most of our requested tags.
                qs.score = topitemsasdict[qs.id] + len(number_of_filters) - (len(tagsQuerySet_lower)*0.01)
        #return newQuerySet_mapped
    #return resQueryset_mapped
    #topitems = heapq.nlargest(15, resource_scores.items(), key=itemgetter(1))
    #topitems = sorted(resource_scores.items(), key=lambda x:x[1], reverse=True)
    
    #Do Query Relaxation
    newQuerySetRelaxed = Resource.objects.none()
    topitems = heapq.nlargest(15, scores_relaxed.items(), key=itemgetter(1))
    topitemsasdict = dict(topitems)
    if len(topitems) >= 1:
        newQuerySetRelaxed = resQuerysetRelaxed.filter(id__in=topitemsasdict.keys()).distinct()
        if len(newQuerySet) > 0:
            newQuerySetRelaxed = newQuerySetRelaxed.exclude(id__in=newQuerySet.values('id'))
        #thisSet = []
        #make result distinct
        #for query in resQuerysetRelaxed:
        #    if query.id not in thisSet:
        #        thisSet.append(query.id)
        #newQuerySetRelaxed = Resource.objects.filter(id__in=thisSet)
        for qs in newQuerySetRelaxed:
            qs.chatbot_api_rcmnd_count += 1
            qs.save()
            
            if qs.id not in topitemsasdict.keys():
                qs.score = 0
            else:
                tagsQuerySet = list(map(lambda x: x.name ,Tag.objects.filter(resource__in=[qs.id])))
                tagsQuerySet_lower = list(map(lambda x: x.lower(), tagsQuerySet))
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet) or (tqs in tagsQuerySet_lower)]

                qs.index = number_of_filters
                # gives more score to resources that that have most of our requested tags.
                qs.score = topitemsasdict[qs.id] + len(number_of_filters) - (len(tagsQuerySet_lower)*0.01)
        #return newQuerySet
    #return resQueryset_mapped, resQueryset

    message_resource_list = []

    if len(newQuerySet) >= 1: #if we have results at all
        message_resource_list.append({'message': "Here are the top results that closely match what you are looking for.", 'resources':ResourceSerializer(newQuerySet,many=True).data})
        if len(newQuerySet)<5 and len(newQuerySetRelaxed)>1:
            #if we don't have a lot, append some extras
            message_resource_list.append({'message': "I also have some less specific results that might still be relevent.", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    elif len(newQuerySetRelaxed)>=1: #if we have no main matches, we need to relax in general
        message_resource_list.append({'message': "Unfortunatly I couldn't find any direct matches. I have some related resources that might help you though.", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    else: #no matches at all mean we return an empty set; the chatbot should handle this case
        message_resource_list.append({'message': "", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    #mapped = {'message': "Here are all results that matched all your specifications", 'resources':[resQueryset_mapped]}
    #relaxed = {'message': "Here are all results with some query relaxation", 'resources':[resQueryset]}

    return Response(message_resource_list)

def ResourceByIntentEntityViewQuerySet_Filter(query_params):
    print("****** filter ******")
    resQueryset = Resource.objects.filter(visible=1).filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('nurse', 'Nurse')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('over 18', 'Youth')
    ,('lgbtq2s_resources', 'Transgender')
    ,('lgbtq2s_resources', 'Non-Binary')
    ,('paid_resources', 'Fee-for-service available to everyone')
    ,('free_resources', 'Free')
    ,('free_resources', 'Free for members')
    ,('free_resources', 'N/A (ex. websites, podcasts)')
    ,('paid_resources', 'Paid')
    ,('free_resources', 'Requires paid membership')
    ,('free_resources', 'Requires provincial health card')
    ,('paid_and_free', 'Unknown')
    ,('paid_and_free', 'Both free and paid')
    ,('book_and_pamphlet', 'Brochure')
    ,('causes', 'cause')
    ,('group_class', 'Classes/course (in person)')
    ,('virtual', 'Mobile App')
    ,('online_courses_and_webinar', 'Webinar/Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Webinar/Online course (scheduled)')
    ,('screening', 'Screening tool')
    ,('information', 'Statistic')
    ,('information', 'information')
    ,('symptom_List', 'Symptoms')
    ,('treatment_Info', 'Treatments')
    ,('information', 'Informational Website')
    ,('coping_skills', 'Informational Website')
    ,('self_help', 'Informational Website')
    ,('self_help', 'Worksheet')
    ,('online_courses_and_webinar', 'Online course (go at your own pace)')
    ,('online_courses_and_webinar', 'Online course (scheduled)')
    ,('self_help', 'Self-Help Books')
    ,('addiction_substance_use_programs', 'Addiction and recovery')
    ,('prevalence', 'Prevalence')
    ,('virtual', 'Online Group Support')
    ,('peer_support', 'Community Support')
    ,('suicidal_other', 'Crisis Support/Distress Counselling')
    ,('suicidal_self', 'Crisis Support/Distress Counselling')
    ,('peer_support', 'Peer Support')
    ,('help_from_another_person', 'Online chat')
    ,('specialist', 'Medical services')
    ,('housing', 'Housing - Emergency')
    ,('group_class', 'Group therapy')
    ,('peer_support', 'In-person Group Support Meeting')
    ,('in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    # ,('doctor', 'Doctor')
    ,('doctor', 'Physician')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Healthcare Workers')
    ,('fire fighter', 'First responder')
    ,('fire fighter', 'Social worker')
    ,('community support', 'Group therapy')
    ,('community support', 'In-person Group Support Meeting')
    ,('community support', 'Peer Support')	
    ,('peer_support', 'Group therapy')
    ,('domestic_abuse_support', 'Violence intervention')
    ,('domestic_abuse_support', 'Domestic Violence')
    ,('domestic_abuse_support', 'Abuse')
    ,('generalized anxiety disorder', 'Anxiety')
    ,('generalized anxiety disorder', 'Generalized Anxiety Disorder')
    ,('generalized anxiety disorder', 'General public/all')
    ,('generalized anxiety disorder', 'Stress')
    ,('health professional','Medical Student')
    ,('health professional','Resident doctor')
    ,('health professional','Service Providers')
    ,('health professional','Social worker')
    ,('alberta','Alberta')
    ,('schizophrenia','Schizophrenia and psychosis')
    ,('covid-19','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('covid','COVID-19 (context specific - ensure any other concerns are also noted)')
    ,('eating','Eating Disorders')
    ,('distress','General Distress')
    ,('hiv','Human Immunodeficiency Virus (HIV)')
    ,('addiction','Addictions (including Drugs, Alcohol, and Gambling)')
    ,('addiction','Behavioural Addiction')
    ,('addiction','Substance use')
    ,('resilience','Resiliency')
    ,('psychologist','Therapist/Counsellor/Psychotherapist')
    ,('psychiatrist','Therapist/Counsellor/Psychotherapist')
    ,('coping_skill','Self-Help Books')
    ,('psychedelics','psilocybin')
    ,('crisis_distress_support','Crisis Support/Distress Counselling')
    ,('book_and_pamplet','Book')
    ,('book_and_pamplet','Booklet'),
    ('ptsd', 'Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse'),
    ('military', 'Military Veterans'),
    ('military', 'Family Member of Veteran'),
    ('first responder', 'Fire Fighter'),
    ('first responder', 'Paramedic'),
    ('first responder', 'Police'),
    ('first responder', 'RCMP'),
    ('first responder', 'Emergency Dispatch Officer'),
    # ('first responder', 'First Responder'),
    ('2slgbtq ', '2SLGBTQ+'),
    ('crisis_distress_support', 'General Distress')
    ]

    n_tags_params = query_params.getlist('ntags')
    n_tags_params = list(map(lambda x: x.lower() ,n_tags_params))
    
    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))


    filter_params = query_params.getlist('filter', [])
    filter_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,filter_params))

    tags_params_temp = []    
    for tag in tags_params: 
        if "(" in tag:
            x = tag 
            tags_params_temp.append((x[:x.index("(")], x[x.index("(")+1:-1])) 
        else: 
            tags_params_temp.append((tag,-1)) 
    tags_params = tags_params_temp


    all_possible_tags = Tag.objects.filter(approved=1).all()
    
    all_possible_tags = list(filter(lambda x: x.name.lower() not in n_tags_params , all_possible_tags))
    all_possible_tags = list(map(lambda x: (x.name, x.tag_category), all_possible_tags))
    all_possible_tag_names = list(map(lambda x: x[0], all_possible_tags))
    all_possible_tag_names_lower_cased = list(map(lambda x: x[0].lower(), all_possible_tags))

    should_be_removed = set()
    should_be_added = set()
    filter_to_remove = set()
    filter_to_add = set()
    #query matching with simillar words
    class_tag_mapping = {}


    word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))

    #map intents, entities, and filters to matching tags
    for tag_param in tags_params:
        tag_param = tag_param[0]

        if tag_param in all_possible_tag_names or tag_param in all_possible_tag_names_lower_cased:
            #found in approved tags
            for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
            if tag_param in filter_params:
                    for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                        filter_to_add.add(related_word[1])
        else:
            if tag_param in word_mapping_keys:
                #found in word mapping
                should_be_removed.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
                if tag_param in filter_params:
                    filter_to_remove.add(tag_param)
                    for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                        filter_to_add.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tag_names, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_removed.add(tag_param)
                    should_be_added.add(similar_tags[0])
                    if tag_param in filter_params:
                        filter_to_remove.add(tag_param)
                        filter_to_add.add(similar_tags[0])
                    #found using distance



    # remove some unusfull intents
    should_be_removed.add('where_live')
    should_be_removed.add('for_me')
    should_be_removed.add('consent_agree')
    should_be_removed.add('show_resource')

    
    query_relaxation_tags = []
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))
    
    # finding classes of the
    for tag_ in should_be_added:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0] == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found")

    for tag_ in tags_params_mapped:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0].lower() == tag_][0]
            if not (tag_category in class_tag_mapping):
                class_tag_mapping[tag_category] = []
            class_tag_mapping[tag_category].append(tag_)
        except:
            print("category not found")
    
    # Location
    # Resource format
    # Resource Type for Education/Informational
    # Resource Type for Programs and Services
    # Health Issue
    # Costs
    # Audience
    # Language

    """
    VIP tags are tags that at least on of them
    should be present in a resource to be a candidate 
    it is NOW ONLY mental_health tags
    """

    vip_tags = []
    input_lo_format_infot_servt_mh_cost_au_lang = []
    if 'Location' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Location']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Resource format' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource format']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Education/Informational' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Education/Informational']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Resource Type for Programs and Services' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Resource Type for Programs and Services']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Health Issue' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Health Issue']))
        for item in class_tag_mapping['Health Issue']:
            vip_tags.append(item)
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)
    
    if 'Costs' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Costs']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Audience' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Audience']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)

    if 'Language' in class_tag_mapping:
        input_lo_format_infot_servt_mh_cost_au_lang.append(50*len(class_tag_mapping['Language']))
    else:
        input_lo_format_infot_servt_mh_cost_au_lang.append(1)


    global GAZETTEER_cities
    canada_cities = GAZETTEER_cities.copy()
    global GAZETTEER_proviences
    canada_city_proviences = GAZETTEER_proviences.copy()

    loc_tag_List = None
    if 'Location' in class_tag_mapping:
        for loc_tag in class_tag_mapping['Location']:
            loc_tag = loc_tag.lower()
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'Location'))
                loc_tag_List = get_nearby_cities(loc_tag)
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'Location'))
                    loc_tag_List = get_nearby_cities(similar_tags[0])
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'Location'))
                        loc_tag_List = get_nearby_cities(similar_tags[0])

        
    #adding obvious location tags
    query_relaxation_tags.append('Worldwide')
    query_relaxation_tags.append('All Canada')
    query_relaxation_tags.append('General public/all')
    #adding nearby cities
    if loc_tag_List:
        for nearby_city in loc_tag_List:
            query_relaxation_tags.append(nearby_city)
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_removed)

    if vip_tags:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & Q(tags__name__in=tags_params_mapped))
        resQuerysetRelaxed = resQueryset.filter(visible=1).filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags)))
    else:
        resQueryset = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped))
        resQuerysetRelaxed = resQueryset.filter(visible=1).filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))


    #filter by location, so we guarantee we have something related (if it exists)
    if 'Location' in class_tag_mapping:
        nquery = resQueryset.filter(tags__name__in=class_tag_mapping['Location'])

        #only actually update the queryset if we have matches
        resQueryset = nquery

        #only hard location filter if we aren't relaxing the query
        #nquery = resQuerysetRelaxed.filter(visible=1).filter(tags__name__in=class_tag_mapping['Location'])

        #only actually update the queryset if we have matches
        #if len(nquery)!=0:
            #print(class_tag_mapping['Location'])
            #resQuerysetRelaxed = nquery

    #attempt filter by each tag, report ones that fail
    tag_filters = set(filter_params)
    tag_filters.update(filter_to_add)
    tag_filters = tag_filters.difference(filter_to_remove)
    print(f"Filters: {tag_filters}")
    for fvalue in tag_filters:
        resQueryset = resQueryset.filter(tags__name=fvalue)

    #retrieve tag ids from tag names
    tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped) | Q(name__in=query_relaxation_tags)).values('id','name','tag_category').all()

    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id','tag_category','name').all()


    def scoring(querySet, tags_params_mapped, query_relaxation_tags, QR=1):

        if QR: 
            #do query relaxation
            #tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped) | Q(name__in=query_relaxation_tags)).values('id','name','tag_category').all()
            tags_id_list = list(map(lambda x: x['id'], tags))
            tags_name_list = list(map(lambda x: x['name'], tags))
            tags_cat_list = list(map(lambda x: x['tag_category'], tags))

            #query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id','tag_category','name').all()
            query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))
            query_relaxation_tags_categories = list(map(lambda x: x['tag_category'], query_relaxation_tags))
            query_relaxation_tags_names = list(map(lambda x: x['name'], query_relaxation_tags))

        else:
            #no query relaxation
            #tags = Tag.objects.filter(approved=1).filter(Q(name__in=tags_params_mapped)).values('id','name','tag_category').all()
            tags_id_list = list(map(lambda x: x['id'], tags))
            tags_name_list = list(map(lambda x: x['name'], tags))
            tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    
        # input_lo_format_infot_servt_mh_cost_au_lang
        # scoring and ordering by scores
        resource_scores = {}
        resource_score_reasons = {}
        for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], querySet)):
            resource_scores[resource[0]] = [0,0,0,0,0,0,0,0]
            resource_score_reasons[resource[0]] = ""

            index = None
            original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
            original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
            original_tag_names = list(map(lambda x: str(x.name), resource[2]))

            if resource[1] is not None and resource[1]!='':
                index = json.loads(resource[1])
            
            for i, tag in enumerate(tags_id_list):
                t_cat = tags_cat_list[i]

                tag = str(tag)
                if resource[1] is not None and resource[1]!='':
                    if tag in index:
                        if t_cat=="Location":
                            resource_scores[resource[0]][0] += index[tag]
                            resource_score_reasons[resource[0]] += "& loc score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource format":
                            resource_scores[resource[0]][1] += index[tag]
                            resource_score_reasons[resource[0]] += "& format score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource Type for Education/Informational":
                            resource_scores[resource[0]][2] += index[tag]
                            resource_score_reasons[resource[0]] += "& infoType score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Resource Type for Programs and Services":
                            resource_scores[resource[0]][3] += index[tag]
                            resource_score_reasons[resource[0]] += "& servType score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Health Issue":
                            resource_scores[resource[0]][4] += index[tag]
                            resource_score_reasons[resource[0]] += "& MH score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Costs":
                            resource_scores[resource[0]][5] += index[tag]
                            resource_score_reasons[resource[0]] += "& Costs score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Audience":
                            resource_scores[resource[0]][6] += index[tag]
                            resource_score_reasons[resource[0]] += "& Audi score from TF-IDF for "+tags_name_list[i]
                        elif t_cat=="Language":
                            resource_scores[resource[0]][7] += index[tag]
                            resource_score_reasons[resource[0]] += "& lang score from TF-IDF for "+tags_name_list[i]

                if tag in original_tag_ids:
                    ii = original_tag_ids.index(tag)
                    sc = 10
                    if original_tag_categories[ii] == 'Location':
                        resource_scores[resource[0]][0] += sc 
                        resource_score_reasons[resource[0]] += "& loc score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource format':
                        resource_scores[resource[0]][1] += sc 
                        resource_score_reasons[resource[0]] += "& format score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource Type for Education/Informational':
                        resource_scores[resource[0]][2] += sc 
                        resource_score_reasons[resource[0]] += "& infoType score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Resource Type for Programs and Services':
                        resource_scores[resource[0]][3] += sc 
                        resource_score_reasons[resource[0]] += "& ServType score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Health Issue':
                        resource_scores[resource[0]][4] += sc 
                        resource_score_reasons[resource[0]] += "& MH score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Costs':
                        resource_scores[resource[0]][5] += sc 
                        resource_score_reasons[resource[0]] += "& costs score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Audience':
                        resource_scores[resource[0]][6] += sc 
                        resource_score_reasons[resource[0]] += "& Audi score from tags for "+original_tag_names[ii]
                    elif original_tag_categories[ii] == 'Language':
                        resource_scores[resource[0]][7] += sc 
                        resource_score_reasons[resource[0]] += "& lang score from tags for "+original_tag_names[ii]
                elif QR and tag in query_relaxation_tags_id:
                    ii = query_relaxation_tags_id.index(tag)
                    sc = 1
                    if query_relaxation_tags_categories[ii] == 'Location':
                        resource_scores[resource[0]][0] += sc 
                        resource_score_reasons[resource[0]] += "& loc score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource format':
                        resource_scores[resource[0]][1] += sc 
                        resource_score_reasons[resource[0]] += "& format score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource Type for Education/Informational':
                        resource_scores[resource[0]][2] += sc 
                        resource_score_reasons[resource[0]] += "+ infoType score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Resource Type for Programs and Services':
                        resource_scores[resource[0]][3] += sc 
                        resource_score_reasons[resource[0]] += "& servType score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Health Issue':
                        resource_scores[resource[0]][4] += sc 
                        resource_score_reasons[resource[0]] += "& MH score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Costs':
                        resource_scores[resource[0]][5] += sc 
                        resource_score_reasons[resource[0]] += "& Costs score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Audience':
                        resource_scores[resource[0]][6] += sc 
                        resource_score_reasons[resource[0]] += "& Audi score from tags for "+query_relaxation_tags_names[ii]
                    elif query_relaxation_tags_categories[ii] == 'Language':
                        resource_scores[resource[0]][7] += sc 
                        resource_score_reasons[resource[0]] += "& Lang score from tags for "+query_relaxation_tags_names[ii]


            resource_scores[resource[0]] = torch.dot(torch.FloatTensor(input_lo_format_infot_servt_mh_cost_au_lang), torch.FloatTensor(resource_scores[resource[0]])).numpy()/1000

            # print(resource_scores[resource[0]])
            #tags_params_mapped = string value of tags
            for tag in tags_params_mapped:
                if len(tag)<2:
                    continue

                if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
                
                if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, tag in title. tag:"+tag
                
                
                if (tag == 'Informational Website' or tag == 'informational website') and (resource[4] == 'RS' or resource[4] == 'BT'):
                    resource_scores[resource[0]] += 1
                    resource_score_reasons[resource[0]] += "& overal score, resource is informational or both. tag:"+tag
                if (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                    resource_scores[resource[0]] += 1
                    resource_score_reasons[resource[0]] += "& overal score, resource is prog_serv or both. tag:"+tag

                if (tag == 'Definition' or tag == 'definition') and (resource[5]):
                    resource_scores[resource[0]] += 3
                    resource_score_reasons[resource[0]] += "& overal score, resource has a definition. tag:"+tag

                if (tag == 'Domestic Violence' or tag == 'domestic violence') and ("sheltersafe" in resource[3].lower()):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, resource has shelter in its title. tag:"+tag

                if (tag == 'Therapist/Counsellor/Psychotherapist') and ("counsel" in resource[3].lower()):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& overal score, resource has counsel in its title. tag: "+tag

                sum_tag = ""
                for w in tag.replace("-", " ").split(" "):
                    if len(w)>0: sum_tag += w[0]
                if (len(sum_tag) > 2) and (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                    resource_scores[resource[0]] += 0.05
                    resource_score_reasons[resource[0]] += "& acronym in title of resource found. tag:"+tag

                if ('MDSC' in resource[3]) or ('CAMH' in resource[3]) or\
                ('CMHA' in resource[3]) or ('SAMHSA' in resource[3]) or\
                ('WHO' in resource[3]) or ('CDC' in resource[3]):
                    resource_scores[resource[0]] += 0.0001
                    resource_score_reasons[resource[0]] += "& resource organization is well known"

        return resource_scores
    
        #
        
    scores = scoring(resQueryset, tags_params_mapped, query_relaxation_tags, 0)
    scores_relaxed = scoring(resQuerysetRelaxed, tags_params_mapped, query_relaxation_tags, 1)

    #No Query Relaxation
    topitems = heapq.nlargest(15, scores.items(), key=itemgetter(1))
    #topitems = sorted(resource_scores.items(), key=lambda x:x[1], reverse=True)
    topitemsasdict = dict(topitems)
    newQuerySet = Resource.objects.none()
    if len(topitems) > 1:
        resQueryset = resQueryset.filter(id__in=topitemsasdict.keys())
        thisSet = []
        #make result distinct
        for query in resQueryset:
            if query.id not in thisSet:
                thisSet.append(query.id)
        newQuerySet = Resource.objects.filter(id__in=thisSet)
        for qs in newQuerySet:
            qs.chatbot_api_rcmnd_count += 1
            qs.save()
            
            if qs.id not in topitemsasdict.keys():
                qs.score = 0
            else:
                tagsQuerySet = list(map(lambda x: x.name ,Tag.objects.filter(resource__in=[qs.id])))
                tagsQuerySet_lower = list(map(lambda x: x.lower(), tagsQuerySet))
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet) or (tqs in tagsQuerySet_lower)]

                qs.index = number_of_filters
                # gives more score to resources that that have most of our requested tags.
                qs.score = topitemsasdict[qs.id] + len(number_of_filters) - (len(tagsQuerySet_lower)*0.01)
        #return newQuerySet_mapped
    #return resQueryset_mapped
    #topitems = heapq.nlargest(15, resource_scores.items(), key=itemgetter(1))
    #topitems = sorted(resource_scores.items(), key=lambda x:x[1], reverse=True)
    
    #Do Query Relaxation
    topitems = heapq.nlargest(15, scores_relaxed.items(), key=itemgetter(1))
    topitemsasdict = dict(topitems)
    newQuerySetRelaxed = Resource.objects.none()
    if len(topitems) > 1:
        resQuerysetRelaxed = resQuerysetRelaxed.filter(id__in=topitemsasdict.keys())   
        thisSet = []
        #make result distinct
        for query in resQuerysetRelaxed:
            if query.id not in thisSet:
                thisSet.append(query.id)
        newQuerySetRelaxed = Resource.objects.filter(id__in=thisSet)
        for qs in newQuerySetRelaxed:
            qs.chatbot_api_rcmnd_count += 1
            qs.save()
            
            if qs.id not in topitemsasdict.keys():
                qs.score = 0
            else:
                tagsQuerySet = list(map(lambda x: x.name ,Tag.objects.filter(resource__in=[qs.id])))
                tagsQuerySet_lower = list(map(lambda x: x.lower(), tagsQuerySet))
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet) or (tqs in tagsQuerySet_lower)]

                qs.index = number_of_filters
                # gives more score to resources that that have most of our requested tags.
                qs.score = topitemsasdict[qs.id] + len(number_of_filters) - (len(tagsQuerySet_lower)*0.01)
        #return newQuerySet
    #return resQueryset_mapped, resQueryset

    message_resource_list = []

    if len(newQuerySet) > 1: #if we have results at all
        message_resource_list.append({'message': "Here are the top results that closely match what you are looking for.", 'resources':ResourceSerializer(newQuerySet,many=True).data})
        if len(newQuerySet)<5 and len(newQuerySetRelaxed)>1:
            #if we don't have a lot, append some extras
            message_resource_list.append({'message': "I also have some less specific results that might still be relevent.", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    elif len(newQuerySetRelaxed)>1: #if we have no main matches, we need to relax in general
        message_resource_list.append({'message': "Unfortunatly I couldn't find any direct matches. I have some related resources that might help you though.", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    else: #no matches at all mean we return an empty set; the chatbot should handle this case
        message_resource_list.append({'message': "", 'resources':ResourceSerializer(newQuerySetRelaxed,many=True).data})
    #mapped = {'message': "Here are all results that matched all your specifications", 'resources':[resQueryset_mapped]}
    #relaxed = {'message': "Here are all results with some query relaxation", 'resources':[resQueryset]}

    return Response(message_resource_list)


def VerifyApprovedResources(query_params):
    resources = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved")).values('id', 'title', 'description', 'organization_description', 'website_meta_data_updated_at', 'url', 'organization_name', 'definition')

    resource_ids_with_problems = []
    now = datetime.now()
    formatted = now.strftime('%Y-%m-%d')
    for resource in resources:
        # Get website description
        if(not resource['website_meta_data_updated_at'] or str(resource['website_meta_data_updated_at'])<formatted):
            try:
                url = resource['url']
                if url == '':
                    continue
                if 'http' not in url:
                    url = 'http://'+url
                hdr = {'User-Agent': 'Mozilla/5.0'}
                html = requests.get(url, headers=hdr, verify=False)
                soup = BeautifulSoup(html.text, 'html.parser')
                content = soup.find('meta')
                title = str(soup.find('title'))
                if title:
                    resource_id = resource['id']
                    instance = Resource.objects.filter(pk=resource_id).get()
                    new_meta_data = (str(title)+str(content))
                    if instance.website_meta_data == 'NoneNone' and ('.pdf' not in url) and instance.website_meta_data != new_meta_data:
                        resource_ids_with_problems.append(resource_id)
                    instance.website_meta_data = new_meta_data
                    instance.website_meta_data_updated_at = formatted
                    instance.save()
            except Exception as e:
                resource_ids_with_problems.append(resource['id'])

    result = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved")).filter(id__in=resource_ids_with_problems)

    return result

def EmotionTestFunc(query_params):
    input = query_params.get("text")
    num_run_eliza = int(query_params.get("num_run_eliza"))
    
    
    API_TOKEN = "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"
    API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        return response.json()

    emotions_dic = query({
        "inputs": input,
    })

    detected_emotion = None
    try:
        if(len(emotions_dic) > 0):
            detected_emotion = emotions_dic[0][0]
    except:
        detected_emotion = None


    emotion_response_bags = {
        "clarification": [ # clarification + emotional or topic fact with doubt if needed
            # "Let me see if I've gotten this right...",
            # "I want to make sure I understand...",
            # "Okay, I think I understand what you're feeling...",
            "I am doing my best to understand how you are feeling but I am still unsure...",
            "I'm still shaky on the details. please explain more...",
            "Right now I am only able to understand a few details can you give me more? "
        ],
        "response_to_neg_feelings": [ # response 
            "That must be hard.",
            "I can detect that it must be hard.",
            "I think anyone would feel bad too in the same situation.",
            "I can see how that would be difficult.",
            "That sounds very challenging.",
            "That sounds difficult.",
            "That must be challenging.",
            "That can't be easy to sit with.",
            "I'm sorry that is happening.",
            "That's a troubling though.",
            "I value your thoughts.",
            "Your words are safe with me.",
        ],
        "response_to_pos_feelings": [ # response 
            "I'm glad you told me.",
            "I'm happy you told me."
        ]
    }

    emotion_des = ""
    clarification_sentence = emotion_response_bags["clarification"][random.randint(0,len(emotion_response_bags["clarification"])-1)]
    emotion_response_pos_sentence = emotion_response_bags["response_to_pos_feelings"][random.randint(0,len(emotion_response_bags["response_to_pos_feelings"])-1)]
    emotion_response_neg_sentence = emotion_response_bags["response_to_neg_feelings"][random.randint(0,len(emotion_response_bags["response_to_neg_feelings"])-1)]
    if (detected_emotion):
        if (detected_emotion['label']=="joy"):
            emotion_des = emotion_response_pos_sentence
            if (detected_emotion['score']<0.5):
                    emotion_des = clarification_sentence\
                    
        elif (detected_emotion['label']=="sadness"):
            emotion_des = emotion_response_neg_sentence
            if (detected_emotion['score']<0.5):
                    emotion_des = clarification_sentence\
    
        elif (detected_emotion['label']=="fear"):
            emotion_des = emotion_response_neg_sentence
            if (detected_emotion['score']<0.5):
                emotion_des = "I am here for you."

        elif (detected_emotion['label']=="anger"):
            emotion_des = emotion_response_neg_sentence
            if (detected_emotion['score']<0.5):
                emotion_des = "I can help you feel better."
    
    
    sample_generator_rules = {
        'synonyms':[
            ["belief", "feel", "think", "believe", "wish", "feeling"],
            ["family", "mother", "mom", "father", "dad", "sister", "brother", "wife", "children", "child"],
            ["desire", "want", "need"],
            ["sad", "unhappy", "depressed", "sick"],
            ["happy", "elated", "glad", "better"],
            ["cannot", "can't", "cant"],
            ["donot", "don't", "dont", "wont", "won't"],
            ["everyone", "everybody", "nobody", "noone"],
            ["be", "am", "is", "are", "was", "got"],
            ["hello", "hi"],
            ["makes", "gives", "made", "gave", "make", "give"],
            ["anxiety", "anxious"],
            ["because", "after"],
            ["job", "work"],
            ["i", "i have", "i've"]
        ],
        'dec_rules':[
            {#example: oh so sorry about X
                'key': 'sorry',
                'decomp': r'*\bsorry\b*',
                'reasmb_neutral': 
                [
                    "We are not perfect, we can make mistakes. What else do you think about that ?",
                    "Can you explain more why do you feel that way ?",
                ],
                'reasmb_empathy': 
                [
                    "I'm here for you, tell me more about your feelings other than sorry.",
                    "That sounds very challenging, Why do you think you feel sorry?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "How are you feeling now?",
                    "Tell me more about your feelings.",
                    "What other feelings do you have about this?",
                ]
            },
            {#example: I am sorry about X
                'key': 'i am sorry',
                'decomp': r'*\bi\b am sorry *',
                'reasmb_neutral': 
                [
                    "We are not perfect, we can make mistakes, You do not need to be sorry.",
                    "Please don't be Sorry, can you explain why do you feel that way ?",
                ],
                'reasmb_empathy':
                [
                    "Oh please do not apologize! I am here to listen. Tell me more. ",
                    "I understand your feeling, what do you think made you feel sorry?",
                    "It can be difficult having to deal with sad emotions, what do you think caused it?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "what do you think caused being sorry (2) ?",
                    "what do you think made you feel sorry (2) ?"
                ],
            }
            ,{#example: I also remember X
                'key': 'i also remember',
                'decomp': r'*\bi\b also remember *',
                'reasmb_neutral': 
                [
                    "Do you often think of that ?",
                    "Does thinking of it bring anything else to mind ?",
                    "What else do you recollect ?",
                    "What in the present situation reminds you of it ?"
                ],
                'reasmb_empathy':
                [
                    "When you remember it, do other memories come to mind ?",
                    "That could be an insightful memory, do you find yourself thinking about it often?",
                    "Past memories can be quite impactful on our ability to go through daily life, are there other memories that come to mind as well?",
                    "How did this memory make you feel?",
                    "Thank you for sharing this memory with me, I'm interested in hearing more about it.",
                    "Why is that memory important to you ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do you often think of (2)?",
                    "Does thinking of (2) bring anything else to mind?",
                    "What in the present situation reminds you of (2)?"
                ],
            },{ #example: I remember X
                'key': 'i remember',
                'decomp': r'*\bi\b remember *',
                'reasmb_neutral': 
                [
                    "Do you often think of it?",
                    "Does thinking of it bring anything else to mind ?",
                    "What else do you recollect?",
                    "What in the present situation reminds you of it ?"
                ],
                'reasmb_empathy':
                [
                    "do you think about this memory a lot?",
                    "I appreciate you are sharing this with me, what feelings come into mind when you remember it?",
                    "what else do you remember?",
                    "Do other memories come to mind when you think about it? Tell me more.",
                    "Thanks for sharing it to me. What else do you remember?",
                    "Thanks for sharing it to me. Why does that memory come to mind ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do you often think of (2)?",
                    "Does thinking of (2) bring anything else to mind?",
                    "What else do you recollect?",
                    "What else do you remember?",
                    "what feelings come into mind when you remember it?"
                    "What in the present situation reminds you of (2)?"
                ],
            },{ #example: do you remember X
                'key': 'do you remember',
                'decomp': r'*do you remember *',
                'reasmb_neutral': 
                [
                    "This conversation is anonymous - so I actually can't remember. Why do you think I should recall it now ?",
                    "This conversation is anonymous - so I can't remember sorry. What is special about it ?"
                ],
                'reasmb_empathy':
                [
                    "This conversation is anonymous - so I have no way of knowing which conversations I've had with you before. Why do you think I should remember it now ?",
                    "This conversation is anonymous - so I can't remember. What is important about it ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "This conversation is anonymous. Why do you think I should recall (2) now?",
                    "This conversation is anonymous. What is special about (2)?",
                    "This conversation is anonymous. You mentioned (2) before?"
                ],
            },{ #example: what if i didn't run.
                'key': 'if',
                'decomp': r'*\bif\b*',
                'reasmb_neutral': 
                [
                    "Do you think its very likely ?",
                    "Tell me more about what you know about it ?",
                    "What makes you think this will happen?"
                ],
                'reasmb_empathy':
                [
                    "My heart hurts for you, do you think it is possible to happen?",
                    "I can't imagine what you must be going through, tell me about your feelings if this happens.",
                    "That's a troubling thought, Do you want it to happen?",
                    "Tell me more about what you are feeling if this happens."
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do you think it's likely that (2)?",
                    "Do you wish that (2)?",
                    "Tell me more about what you are feeling if this happens.",
                    "I hear you saying, if (2)?"
                ],
            },{ #i dreamed of my love every night.
                'key': 'i dreamed',
                'decomp': r'*\bi\b dreamed *',
                'reasmb_neutral': 
                [
                    "Tell me more about your dream ?",
                    "Have you ever daydreamed about while you were awake ?",
                    "Have you ever dreamed like that before ?"
                ],
                'reasmb_empathy':
                [
                    "Thank you for trusting me with something so private, it means a lot to me. Why is this dream important to you?",
                    "Thank you for sharing this with me. Why does this dream matter to you ?",
                    "Do you have dreams like this often ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Tell me more about, (2)?",
                    "Have you ever day dreamed fantasized (2) while you were awake?",
                    "Have you ever dreamed (2) before?"
                ],
            },{ #i dream of my love every night.
                'key': 'dream',
                'decomp': r'*\bdream\b*',
                'reasmb_neutral': 
                [
                    "What does that dream suggest to you ?",
                    "Do you dream often ?",
                    "What persons appear in your dreams ?",
                    "Do you believe that dreams have something to do with your problems ?"
                ],
                'reasmb_empathy':
                [
                    "Why is this dream important to you ?",
                    "How does this dream make you feel ?",
                    "Dreams can cause you to feel many emotions, how do you feel after it?",
                    "Who does this dream make you think of ?",
                    "Tell me more about how this dream makes you feel ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What does that dream suggest to you?",
                    "Do you dream often?",
                    "What persons appear in your dreams?",
                    "Do you believe that dreams have something to do with your problems?"
                ],
            },{ #perhaps i do not have a soul.
                'key': 'perhaps',
                'decomp': r'*\bperhaps\b *',
                'reasmb_neutral': 
                [
                    "You don't seem certain. Why is that ?",
                    "you seem uncertain? Why is that?",
                    "You aren't sure?"
                ],
                'reasmb_empathy':
                [
                    "Why do you say 'perhaps' ?",
                    "What are you thinking ?",
                    "You seem unsure. Why do you say that ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "You don't seem certain. Why?",
                    "Whu you seem uncertain?",
                    "Why do you say 'perhaps' ?",
                    "You seem unsure. Why do you say that ?"
                ],
            },{ #hello
                'key': 'hello',
                'decomp': r'@hello',
                'reasmb_neutral': 
                [
                    "Hello! I'm here to listen. Tell me what's on your mind.",
                ],
                'reasmb_empathy':
                [
                    "Hello! I'm here to listen. Tell me what's on your mind.",
                    "Hello! How can I help you?",
                ],
                'reasmb_dynamic_neutral':
                [
                    "Hello! I'm here to listen. Tell me what's on your mind.",
                    "Hello! How can I help you?",
                ],
            },{ # computer
                'key': 'computer',
                'decomp': r'*\bcomputer\b*',
                'reasmb_neutral': 
                [
                    "Do computers worry you ?",
                    "Why do you mention computers ?",
                    "Do you think machines are part of your problem ?"
                ],
                'reasmb_empathy':
                [
                    "Computers... why do you raise this ?",
                    "What makes you think about computers ?",
                    "Thank you for sharing this with me, what makes you think about computers?",
                    "How does this make you feel ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do computers worry you?",
                    "Why do you mention computers?",
                    "What do you think machines are part of your problem?"
                ],
            },{ # am I a bad person?
                'key': 'am i',
                'decomp': r'am i *',
                'reasmb_neutral': 
                [
                    "Do you really believe you are like that ?",
                    "Would you want to be like that ?",
                    "What would it mean if you were like that ?"
                ],
                'reasmb_empathy':
                [
                    "I can tell you're feeling unsure, may I ask what makes believe you are like that ?",
                    "What makes you ask this question about yourself ?",
                    "If you were like that, what would it mean to you?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why do you believe you are (1)?",
                    "Would you want to be (1)?",
                    "Do you wish I would tell you you are (1)?",
                    "What would it mean if you were (1)?",
                    "What makes you ask this question about yourself ?",
                ],
            },{ # are you married?
                'key': 'are you', 
                'decomp': r'are you *',
                'reasmb_neutral': 
                [
                    "Why are you interested in it ?",
                    "Would you prefer if I weren't like this ?",
                    "Do you sometimes think I am like that ?",
                ],
                'reasmb_empathy':
                [
                    "Thank you for your question, but I am a robot.",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why are you interested in whether I am (1) or not?",
                    "Would you prefer if I weren't (1)?",
                    "Why do you think I am (1)?",
                    "Do you sometimes think I am like that ?",
                ],
            },{ # they are cool.
                'key': 'they are',
                'decomp': r'*\bthey\b are *',
                'reasmb_neutral': 
                [
                    "Did you think they might not be like it ?",
                    "What if they were not like it ?",
                    "Possibly they are. What do you think?"
                ],
                'reasmb_empathy':
                [
                    "Hmm, that is interesting to hear...How does that make you feel?",
                    "Thank you for opening up to me...How does this affect your feelings?",
                    "Thank you for trusting me with those thoughts...What does this make you think of?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why Did you think they might not be (2)?",
                    "Why you like it if they were not (2)?",
                    "What if they were not (2)?"
                ],
            },{ # I am happy you are cool.
                'key': 'you are',
                'decomp': r'*\byou\b are *',
                'reasmb_neutral': 
                [
                    "Did you think they might not be like it ?",
                    "What if they were not like it ?",
                    "Possibly they are. What do you think?"
                ],
                'reasmb_empathy':
                [
                    "Hmm, that is interesting to hear...How does that make you feel?",
                    "Thank you for opening up to me...How does this affect your feelings?",
                    "Thank you for trusting me with those thoughts...What does this make you think of?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why you like it if I was not (2)?",
                    "What makes you think I am (2)?",
                    "What does this make you think of?"
                ],
            },{ #I think your questions are hard
                'key': 'your',
                'decomp': r'*\byour\b*',
                'reasmb_neutral': 
                [
                    "Why are you concerned about it ?",
                    "Why are you worried about someone else ?"
                ],
                'reasmb_empathy':
                [
                    "I can tell you've been thinking about this a lot...What concerns you about this?",
                    "That must be a lot to think about...What concerns you about this?"
                    "I can tell you've been thinking about this a lot...What concerns you about this?"
                    "Why are you worried about someone else ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why are you concerned about my (2)?",
                    "Why are you worried about someone else ?",
                    "Why are you worried about someone else's (2)?"
                ],
            },{ # was I a good person?
                'key': 'was i',
                'decomp': r'was i *',
                'reasmb_neutral': 
                [
                    "What if you were like that ?",
                    "Do you think you were like it ?",
                    "What would it mean if you were like that ?",
                    "What does it suggest to you ?"
                ],
                'reasmb_empathy':
                [
                    "I'm not sure. Can you tell me more? Why are you asking it?",
                    "I'm listening. Why are you asking it?",
                    "Tell me why are you asking it?",
                    "What does it suggest to you if you were?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What if you were (1)?",
                    "Why do you think you were (1)?",
                    "What would it mean if you were (1)?",
                    "What does (1) suggest to you?"
                ],
            },{ # i was so bad
                'key': 'i was',
                'decomp': r'i was *',
                'reasmb_neutral': 
                [
                    "Were you really ?",
                    "Why do you tell me this ?",
                ],
                'reasmb_empathy':
                [
                    "Were you really? Can you explain a bit more?",
                    "I can tell this is troubling you... Can you explain a bit more?",
                    "It sounds like these thoughts have been really difficult for you... Were you really?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why do you tell me you were (1) now?",
                    "Why you were (1)?",
                ],
            },{ # were you in this situation before?
                'key': 'were you',
                'decomp': r'were you *',
                'reasmb_neutral': 
                [
                    "What suggests that ?",
                    "What do you think ?"
                ],
                'reasmb_empathy':
                [
                    "Why are asking it?",
                    "Why do you asking it?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What suggests that I was (1)?",
                    "Perhaps I was (1).",
                    "What if I had been (1)?"
                ],
            },{ # I want to take a flight and escape.
                'key': 'I want',
                'decomp': r'i @desire *',
                'reasmb_neutral': 
                [
                    "What would it mean to you if you got what you desire ?",
                    "Why do you want it ?",
                    "Suppose you got it soon. tell me more ?",
                    "What if you never got what you want ?",
                    "What would getting it mean to you ?",
                ],
                'reasmb_empathy':
                [
                    "That makes a lot of sense to me...What would desiring this mean to you?",
                    "I feel you are very interested in this...What would desiring this mean to you?",
                    "I can tell this is important to you...Could you tell me why desiring this is important to you?",
                    "If this happened, how would desiring it make you feel?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What would it mean to you if you got (1)?",
                    "Suppose you got what (1) soon. tell me more?",
                    "What if you never got (1)?",
                    "What would getting (1) mean to you?",
                ],
            },{ # all I want is to take a flight and escape.
                'key': 'want',
                'decomp': r'i @desire is *',
                'reasmb_neutral': 
                [
                    "What would it mean to you if you got what you desire ?",
                    "Why do you want it ?",
                    "Suppose you got it soon. tell me more ?",
                    "What if you never got what you want ?",
                    "What would getting it mean to you ?",
                ],
                'reasmb_empathy':
                [
                    "That makes a lot of sense to me...What would desiring this mean to you?",
                    "I feel you are very interested in this...What would desiring this mean to you?",
                    "I can tell this is important to you...Could you tell me why desiring this is important to you?",
                    "If this happened, how would desiring it make you feel?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What would it mean to you if you got (1)?",
                    "Suppose you got (1) soon. tell me more?",
                    "What if you never got (1)?",
                    "What would getting (1) mean to you?",
                ],
            },{ # i am very sad 
                'key': 'i am sad',
                'decomp': r'i am\b*@sad *',
                'reasmb_neutral': 
                [
                    "I am sorry to hear that. Can you tell me more about it?",
                    "Can you tell me more about it?",
                    "Can you explain what made you feel that way ?",
                ],
                'reasmb_empathy':
                [
                    "I am sorry to hear that. Can you tell me more about what is making you feel sad?",
                    "It hurts me to hear you are feeling sad... Can you tell me more about what is making you feel sad?",
                    "I want to do my best to help you out of this state... Can you tell me more about what is making you feel sad?",
                    "Those are heavy emotions to cope with... Can you tell me more about what is making you feel sad?",
                    "You are so strong to be coping with those heavy emotions... Can you tell me more about what is making you feel sad?",
                    "I'm sorry you've been feeling this way. Can you tell me more about it?",
                    "I'm sorry you are dealing with this. What made you feel sad?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I am sorry to hear that you are (2).",
                    "Do you think that coming here will help you not to be (2)?",
                    "I'm sure it's not pleasant to be (2).",
                    "Can you explain what made you (2)?",
                    "Can you tell me more about what is making you feel sad?"
                ],
            },{ # i am very happy
                'key': 'i am happy',
                'decomp': r'i am * @happy *',
                'reasmb_neutral': 
                [
                    "What makes you happier just now ?",
                    "Can you explain why you are suddenly more happy ?",
                ],
                'reasmb_empathy':
                [
                    "Great...What made you happier just now?",
                    "Your happiness is important to me...What made you happier just now?",
                    "I'm glad you are in a good place...What made you happier just now?",
                    "I'm glad you are in a good place...What makes you feel this way?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "How have I helped you to be (2)?",
                    "Why your treatment made you (2)?",
                    "What makes you (2) just now?",
                    "Can you explain why you are suddenly (2)?",
                    "What makes you feel this way?",
                ],
            },{ # i wish I was not a looser.
                'key': 'i wish',
                'decomp': r'@i * @belief *', 
                'reasmb_neutral': 
                [
                    "Do you really think so ?",
                    "Are you sure about that ?",
                    "Do you really feel that way ?",
                ],
                'reasmb_empathy':
                [
                    "I'm grateful to hear about your beliefs... Do you really think so?",
                    "Thank you for opening up to me, I value it a lot... Do you really believe so?",
                    "Are you sure about that or are there other ways to see it?",
                    "I'm trying to understand. What causes you to think like that?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why do you feel (2)?",
                    "Let's talk more about about (2)?",
                    "You think (2). Why is that?",
                    "You think (2). Are there other ways to see it?",
                ],
            },{ # i am a good person.
                'key': 'i am',
                'decomp': r'i am *',
                'reasmb_neutral': 
                [
                    "How long have you been like that ?",
                    "Do you believe it is normal to be like this ?"
                ],
                'reasmb_empathy':
                [
                    "I'm vey grateful you are telling me your thoughts...How long has this been the case?",
                    "Do you believe this is common?",
                    "I want to know more. What emotions does this bring up for you?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Is it because you said (1) that you came to me?",
                    "How long have you been (1)?",
                    "Do you believe it is normal to be (1)?",
                    "I want to know more. What emotions does being (1) bring up for you?"
                ],
            },{ # i can not go out without my mother
                'key': 'i can not',
                'decomp': r'i @cannot *',
                'reasmb_neutral': 
                [
                    "What makes you think you can't ?",
                    "Do you really want to be able to do this ?",
                ],
                'reasmb_empathy':
                [
                    "This must be hard to talk about. Thank you for sharing this with me...What makes you think you can't?",
                    "I think you are stronger than you believe...What makes you think you can't?",
                    "I can't imagine how you feel right now...What makes you think you can't?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What makes you think you can't (1)?",
                    "what is preventing you to (1)?",
                    "Do you know the reason preventing you to (1)?",
                    "Tell me why you can not?"
                ],
            },{ # i don't think i have good relationships
                'key': 'i do not',
                'decomp': r"i don't *",
                'reasmb_neutral': 
                [
                    "Why?",
                    "Does that trouble you ?"
                ],
                'reasmb_empathy':
                [
                    "This must be hard to talk about. Thank you for opening up to me...What does this make you feel?",
                    "I can see how hard this must be for you...What does this make you feel?",
                    "That makes a lot of sense...What emotions does this make you feel?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why don't you (1)?",
                    "Why you wish to be able to (1)?",
                ],
            },{ # i feel like a baby
                'key': 'i feel',
                'decomp': r"i feel *",
                'reasmb_neutral': 
                [
                    "Tell me more about your feelings about this.",
                    "Do you often feel that ?",
                    "Do you enjoy that feeling ?",
                    "Of what does that feeling remind you ?"
                ],
                'reasmb_empathy':
                [
                    "It can be hard coping with those feelings...What made you feel this way?",
                    "I can't imagine being in your position...What made you feel this way?",
                    "'m so sorry you feel that way, I wish I could make it better...What made you feel this way?",
                    "I'm here for you...What made you feel this way?",
                    "What has this been like for you?",
                    "I'm here for you...Do you often feel this way?",
                    "I'm here for you...What makes you feel this way?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do you often feel (1)?",
                    "Do you enjoy feeling (1)?",
                    "Of what does feeling (1) remind you?"
                ],
            },{ # i think i am not prepared for it
                'key': 'every thing',
                'decomp': r'*',
                'reasmb_neutral': 
                [
                    "Let`s discuss further. Tell me more about that?",
                    "Can you elaborate on that ?",
                ],
                'reasmb_empathy':
                [
                    "Could you tell me more?",
                    "Can you elaborate on that?",
                    "Let`s discuss further. Tell me more about that.",
                ],
                'reasmb_dynamic_neutral':
                [
                    "Could you tell me more?",
                    "Thanks for sharing with me. Can you elaborate on that?",
                    "I'm not sure what you mean by (1)",
                    "Let's discuss further. Tell me more.",
                    "Can you elaborate on that ?",
                    "Let's discuss further. Tell me more about that.",
                    "what does that suggest to you?"
                ]
            },{ # i think i am not prepared for it
                'key': 'and',
                'decomp': r'*\band\b*',
                'reasmb_neutral': 
                [
                    "Let`s discuss further. Tell me more about that.",
                    "Can you elaborate on that ?",
                ],
                'reasmb_empathy':
                [
                    "Could you tell me more?",
                    "Can you elaborate on that?",
                    "Let`s discuss further. Tell me more about that.",
                    "Let`s discuss further. Tell me more about that.",
                ],
                'reasmb_dynamic_neutral':
                [
                    "Do you wana talk more about (2)",
                    "I wana talk more about it. Why (2)",
                    "I want to know why (2)",
					"Tell me more about (2)"
                ]
            },
            { # you are very funny
                'key': 'you are',
                'decomp': r"you are *",
                'reasmb_neutral': 
                [
                    "What makes you think about it",
                    "Does it make you feel better to believe it?"
                ],
                'reasmb_empathy':
                [
                    "I can understand why you feel this way...What makes you think about me?",
                    "I'm not quite sure I understand...What makes you think about me?",
                    "Thank you for sharing your opinion...What makes you think about me?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "What makes you think I am (1)?",
                    "Does it make you feel better to believe I am (1)?"
                ],
            },{ # yes
                'key': 'yes',
                'decomp': r"\byes\b",
                'reasmb_neutral': 
                [
                    "Got it. Let`s discuss further. Tell me more about that?",
                    "I see. Let`s discuss further. Tell me more about that?"
                ],
                'reasmb_empathy':
                [
                    "I'm grateful we've been able to talk this far... Could you tell me more?",
                    "I really appreciate everything you have told me so far... Please ellaborate on that.",
                    "I admire how open you've been with me, I'm in your corner... Could you tell me more?",
                    "I see. Let's discuss further. Could you give me some more information?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I see. Let`s discuss further. Can you please provide more information that I can help you with?",
                    "I see. Let's discuss further. Could you give me some more information?"
                ]
            },{ # no  
                'key': 'no',
                'decomp': r"\bno\b",
                'reasmb_neutral': 
                [
                    "Why are you saying no?",
                    "Why not?",
                    "Why no?"
                ],
                'reasmb_empathy':
                [
                    "That's okay. Could you tell me why you feel this way?",
                    "That's okay if you don't want to share more. I'm always here for you if you need to chat...Could you tell me why you feel this way?",
                    "I want to understand you more, I'm grateful we have been able to talk thus far...Could you tell me why you feel this way?",
                    "Why not?",
                    "I want to understand. Why do you think so?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why are you saying no?",
                    "I want to understand. Why no?",
                    "Why no?"
                ],
            },{ # i dislike my work
                'key': 'my',
                'decomp': r"*\bmy\b*",
                'reasmb_neutral': 
                [
                    "Let`s discuss further. Why?",
                    "Why do you say that ?"
                ],
                'reasmb_empathy':
                [
                    "Thank you for trusting me with that information, can I ask if you can tell me a bit more?",
                    "I appreciate that you are sharing this with me and hope you are doing okay, can I ask if you can tell me more?",
                    "That sounds like this has really affected you, can you tell me more?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Let's discuss further why your (2).",
                    "Why do you say your (2)?"
                ],
            },{ # I like living with my lovely family in Canada.
                'key': 'my family',
                'decomp': r"*\bmy\b* @family *",
                'reasmb_neutral': 
                [
                    "Tell me more about your family.",
                    "Who else in your family ?",
                    "What else comes to mind when you think of it ?"
                ],
                'reasmb_empathy':
                [
                    "Families can be a source of a lot of support or conflict...Tell me more about your family.",
                    "Families have a big effect on our emotions...Tell me more about your family.",
                    "Families can be a source of a lot of support or conflict...Tell me more about your family?",
                    "Families have a big effect on our emotions...What else is coming to mind?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Tell me more about your family.",
                    "Who else in your family?"
                ],
            },{ # can you tell me how to behave better?
                'key': 'can you',
                'decomp': r"can you *",
                'reasmb_neutral': 
                [
                    "You believe I can. don't you ?",
                ],
                'reasmb_empathy':
                [
                    "I am trying my best, but I am still learning. Could you tell me a little bit more about your situation?",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why you believe I can (1) ?"
                ],
            },{ # can i ask a question?
                'key': 'can i',
                'decomp': r"can i *",
                'reasmb_neutral': 
                [
                    "Do you want to be able to do it ?",
                    "Perhaps you don't want to ?"
                ],
                'reasmb_empathy':
                [
                    "I think you are able to do anything you put your mind to...What makes you think to question yourself?",
                    "think you are stronger than you think...What makes you think to question yourself?",
                    "I think you are more capable than you know...What makes you think to question yourself?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Whether or not you can (1) depends on you more than me.",
                    "Why you want to be able to (1)?",
                    "Perhaps you don't want to (1)."
                ],
            },{ # what can i call you?
                'key': 'what',
                'decomp': r"what *",
                'reasmb_neutral': 
                [
                    "Why do you ask ?",
                    "Does that question interest you ?",
                    "What is it you really wanted to know ?",
                    "Are such questions much on your mind ?",
                    "What answer would please you most ?",
                    "What do you think ?",
                    "What comes to mind when you ask that ?",
                    "Have you asked anyone else ?"
                ],
                'reasmb_empathy':
                [
                    "Why do you ask?",
                    "What about this question interests you?",
                    "What makes you want to know more?",
                    "Are these questions on your mind a lot?",
                    "Do you often think of these questions?"
                    "What comes to mind when you ask that?",
                    "Have you asked anyone else this before?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why do you ask ?",
                    "Does that question interest you ?",
                    "What is it you really wanted to know ?",
                    "Are such questions much on your mind ?",
                    "What answer would please you most ?",
                    "What do you think ?",
                    "What comes to mind when you ask that ?",
                    "Have you asked anyone else ?"
                ],
            },{ # because i do not want it
                'key': 'because',
                'decomp': r"*\bbecause\b*",
                'reasmb_neutral': 
                [
                    "Is that the reason ?",
                    "Does any other reason come to mind ?",
                    "Does that reason seem to explain anything else ?",
                    "What other reasons might there be ?"
                ],
                'reasmb_empathy':
                [
                    "I admire that you are sharing this with me...Could there be other reasons?",
                    "You are making a lot of sense...Could there be other reasons?",
                    "I'm grateful you can trust me with this information, I'm always here to listen...Could there be other reasons?",
                    "Could there be any other reasons?",
                    "I want to help. What does this bring up for you?",
                    "Is it possible there are other reasons?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Is that the reason?",
                    "Does any other reason come to mind?",
                    "Does that reason seem to explain anything else?",
                    "What other reasons might there be?"
                ],
            },{ # why don't you check again and let me know?
                'key': 'why do not you',
                'decomp': r"why don't you *",
                'reasmb_neutral': 
                [
                    "Do you believe I don't ?",
                    "Perhaps I will in good time."
                ],
                'reasmb_empathy':
                [
                    "I am trying but I am still a work in progress! What are you looking for?",
                    "I'm sorry I'm unable to help you in this way, however I am still a work in progress...Could you tell me more about your situation or what you are looking for?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Do you believe I don't (1)?",
                    "Perhaps I will (1) in good time.",
                    "Why you want me to (1)?"
                ],
            },{ # why can't i be happy?
                'key': 'why can not i',
                'decomp': r"*\bwhy\b can't i *",
                'reasmb_neutral': 
                [
                    "Why do you think you should be able to do that ?",
                    "Do you want to be able to do that ?",
                    "Do you believe this will help you ?",
                    "Have you any idea why you can't ?"
                ],
                'reasmb_empathy':
                [
                    "I disagree with this...Why do you think you are not able to do that?",
                    "It sounds like you are being very hard on yourself here... Why do you think you are not able to do that?",
                    "You must feel so helpless, but I disagree with what you are saying... Why do you think you should be able to do that?",
                    "I understand what you are feeling, however I disagree... Why do you think you should be able to do that?",
                    "It's important to be kind to yourself. What could help you deal with this?",
                    "Often we can be harsh on ourselves. Do you think you can question this feeling?",
                    "What makes you say that you can't ?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why you think you should be able to (2)?",
                    "Why you want to be able to (2)?",
                    "Why you believe this will help you to (2)?",
                    "Have you any idea why you can't (2)?"
                ],
            },{ # everyone is happy but not me.
                'key': 'everyone',
                'decomp': r"*@everyone *",
                'reasmb_neutral': 
                [
                    "I understand. Can you think of anyone in particular ?",
                    "Can you think of anyone in particular ?",
                    "Who, for example?",
                    "Are you thinking of a very special person ?",
                    "Who, may I ask ?",
                    "Someone special perhaps ?",
                    "You have a particular person in mind, don't you ?",
                    "Who do you think you're talking about ?"
                ],
                'reasmb_empathy':
                [
                    "That sounds very frustrating... Can you think of anyone in particular?",
                    "I would have trouble coping in that situation... Can you think of anyone in particular?",
                    "I would feel the same way in that situation... Can you think of anyone in particular?",
                    "Is there someone in particular you're thinking of?",
                    "Okay, who would be an example? I want to understand more.",
                    "Are you thinking of someone close to you?",
                    "Is there someone specific you might be talking about?",
                    "Could you tell me more about how this makes you feel?",
                    "Do you have a particular person in mind?",
                    "Could you give me an example? I want to understand to better help you."
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I understood, (2)?",
                    "Surely not (2).",
                ],
            },{ # always
                'key': 'always',
                'decomp': r"*\balways\b*",
                'reasmb_neutral': 
                [
                    "Can you think of a specific example ?",
                    "When ?",
                    "What incident are you thinking of ?",
                    "Always?"
                ],
                'reasmb_empathy':
                [
                    "Could you give me an specific example?",
                    "What if this could change?",
                    "Is there something specific that makes you think this?",
                    "Always? Or could this change? Tell me a little more if you can."
                ],
                'reasmb_dynamic_neutral': 
                [
                    "When?",
                    "What incident are you thinking of?",
                    "Why Always?"
                ],
            },{ # last night
                'key': 'always',
                'decomp': r"*\blast\b \bnight\b*",
                'reasmb_neutral': 
                [
                    "Can you think of a specific example other than last night?",
                    "Tell me more about that night.",
                    "What incident are you thinking of now?"
                ],
                'reasmb_empathy':
                [
                    "Can you think of a specific example other than last night?",
                    "Is there something specific that makes you think about last night?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Tell me more about that night when (1)",
                    "What else happened in that night?",
					"Is there something specific that makes you think about last night?"
                ],
            },{ # they dressed alike in black trousers and jackets.
                'key': 'alike',
                'decomp': r"*\balike\b*",
                'reasmb_neutral': 
                [
                    "In what way ?",
                    "What resemblance do you see ?",
                    "What does that similarity suggest to you ?",
                    "What other connections do you see ?",
                    "What do you suppose that resemblance means ?",
                    "What is the connection, do you suppose ?",
                    "Could there really be some connection ?"
                ],
                'reasmb_empathy':
                [
                    "That is an insightful comparison...In what way?",
                    "I appreciate you telling me this...In what way?",
                    "Can I ask what similarities you see?",
                    "What does that similarity suggest to you?",
                    "Do you see other similarities?",
                    "I want to hear more. What do you think this similarity could mean?",
                    "How do these similarities make you feel?",
                    "Thank you for sharing this with me. How does it make you feel?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "In what way?",
                    "What does that similarity suggest to you?",
                    "What other connections do you see?",
                    "What do you suppose that resemblance means?",
                    "What is the connection, do you suppose?"
                ],
            },{ # I am happy like you!
                'key': 'am like',
                'decomp': r"* @be * like *",
                'reasmb_neutral': 
                [
                    "In what way ?",
                    "What resemblance do you see ?",
                    "What does that similarity suggest to you ?",
                    "What other connections do you see ?",
                    "What do you suppose that resemblance means ?",
                    "What is the connection, do you suppose ?",
                    "Could there really be some connection ?"
                ],
                'reasmb_empathy':
                [
                    "You're making total sense...Can I ask what similarities you see?",
                    "I agree with what you're saying...What does that similarity suggest to you?",
                    "You're making total sense...Do you see other similarities?",
                    "I want to hear more. What do you think this similarity could mean?",
                    "You're making total sense...How do these similarities make you feel?",
                    "Thank you for sharing this with me. How does it make you feel?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "In what way?",
                    "What resemblance do you see?",
                    "What does that similarity suggest to you?",
                    "What other connections do you see?",
                    "What do you suppose that resemblance means?",
                    "What is the connection, do you suppose?",
                    "Could there really be some connection?"
                ],
            },{ # this makes me anxious
                'key': 'makes me Anxious',
                'decomp': r"* @makes me @anxiety",
                'reasmb_neutral': 
                [
                    "Why do you feel that way?",
                    "What do you do when you feel that way?",
                    "Can you tell me more about that?",
                    "Have you felt this way before?"
                ],
                'reasmb_empathy':
                [
                    "That sounds pretty difficult, why do you think you feel that way?",
                    "I can imagine how hard that is, has that happened before?",
                    "I'm sorry to hear, how do you feel now?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I'm sorry to hear that, why do you think (1) causes that?"
                ],
            },{
                'key': 'Anxious because',
                'decomp': r"* @anxiety * @because *",
                'reasmb_neutral': 
                [
                    "Why do you feel that way?",
                    "What do you do when you feel that way?",
                    "Can you tell me more about that?",
                    "Have you felt this way before?"
                ],
                'reasmb_empathy':
                [
                    "That sounds pretty difficult, why do you think you feel that way?",
                    "I can imagine how hard that is, has that happened before?",
                    "I'm sorry to hear, how do you feel now?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I'm sorry to hear that, why do you think (3) causes that?"
                ],
            },{
                'key': 'Anxiety because',
                'decomp': r"* @anxiety @because *",
                'reasmb_neutral': 
                [
                    "Why do you feel that way?",
                    "What do you do when you feel that way?",
                    "Can you tell me more about that?",
                    "Have you felt this way before?"
                ],
                'reasmb_empathy':
                [
                    "That sounds pretty difficult, why do you think you feel that way?",
                    "I can imagine how hard that is, has that happened before?",
                    "I'm sorry to hear, how do you feel now?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "Why do you think (2) causes that?"
                ],
            },{# they told me my job/work is not good
                'key': 'My job',
                'decomp': r"*\bmy\b @job*",
                'reasmb_neutral': 
                [
                    "How your work impacts your feeling?",
                    "What do you do when you feel this way?",
                    "Can you tell me more about your work?",
                    "Have you felt this way about your work before?"
                ],
                'reasmb_empathy':
                [
                    "How your work impacts your feeling?",
                    "What do you do when you feel this way?",
                    "Can you tell me more about your work?",
                    "Have you felt this way about your work before?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "How your work impacts your feeling?",
                    "What do you do when you feel this way?",
                    "Can you tell me more about your work?",
                    "Have you felt this way about your work before?"
                ],
            },{# they told me I am big
                'key': 'told me',
                'decomp': r"*\btold\b me *",
                'reasmb_neutral': 
                [
                    "How important is what others tell you?",
                    "How what others tell you changes your mood?",
                    "How what others tell you makes you feel?",
                    "Do they have any reason for that?"
                ],
                'reasmb_empathy':
                [
                    "How important is what others tell you?",
                    "How what others tell you changes your mood?",
                    "How what others tell you makes you feel?",
                    "Do they have any reason for that?"
                ],
                'reasmb_dynamic_neutral': 
                [
                    "How important is (2) to you?",
                    "How (2), affects your mood?",
                    "What is your response when '(2)' is being said.",
                    "Do they have any reason for saying (2)?"
                ],
            },{# who are you?
                'key': 'who you',
                'decomp': r"*\bwho\b are \byou\b*",
                'reasmb_neutral': 
                [
                    "I am Mira, a chatbot to help you find resources on mental health. I am a program built by researchers at the University of Alberta for the Mood Disorder Society of Canada. They also call me Chatty Mira.",
                ],
                'reasmb_empathy':
                [
                    "I am Mira, a chatbot to help you find resources on mental health. I am a program built by researchers at the University of Alberta for the Mood Disorder Society of Canada. They also call me Chatty Mira.",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I am Mira, a chatbot to help you find resources on mental health. I am a program built by researchers at the University of Alberta for the Mood Disorder Society of Canada. They also call me Chatty Mira.",
                ],
            },{# where are you?
                'key': 'where you',
                'decomp': r"*\bwhere\b are \byou\b*",
                'reasmb_neutral': 
                [
                    "I am a software program running on a server. The server is currently located at the University of Alberta in Edmonton, Canada. I guess you could say I am in Edmonton.",
                ],
                'reasmb_empathy':
                [
                    "I am a software program running on a server. The server is currently located at the University of Alberta in Edmonton, Canada. I guess you could say I am in Edmonton.",
                ],
                'reasmb_dynamic_neutral': 
                [
                    "I am a software program running on a server. The server is currently located at the University of Alberta in Edmonton, Canada. I guess you could say I am in Edmonton.",
                ],
            }
        ]
    }

    

    # return best rules from options provided
    def calculate_cosine_simillarity_with_rule_keys(user_input, decomposition_rules):
        print("****** calc cosine ******")
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Two lists of sentences
        sentences1 = decomposition_rules
        sentences2 = [user_input]      

        # bring synonyms to decompose rules and remove *   
        sentences1 = list(map(lambda x: replace_decomp_with_syns(x.replace("*", "")) , sentences1))

        #Compute embedding for both lists
        embeddings1 = model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = model.encode(sentences2, convert_to_tensor=True)

        #Compute cosine-similarities
        cosine_scores = util.cos_sim(embeddings1, embeddings2)

        #Output the pairs with their score
        max_val = 0
        key = 0
        for i in range(len(sentences1)):
            if max_val < cosine_scores[i][0]:
                max_val = cosine_scores[i][0]
                key = i
        
        print("most similar", sentences1[key], 'cosine scores', cosine_scores, "sentences", sentences1)
        return list(sentences1[key])

  
    def find_syns(word):
        syn_ars = sample_generator_rules['synonyms']
        for ar in syn_ars:
            if word in ar:
                return ar
        return []

    def replace_decomp_with_syns(decomp):
        reg = regex.findall( r'@\w+' ,decomp)
        if reg:
            reg = reg[0][1:]
            return replace_decomp_with_syns(decomp.replace('@'+reg, '('+'|'.join([r"\b"+syn+r"\b" for syn in find_syns(reg)])+')'))
        return decomp

    def rule_can_parse(decomp_rule, sentence): #tag[1]=decomp_sentence
        #checking if decomp rule can parse sentence
        reg = replace_decomp_with_syns(decomp_rule)
        reg = reg.replace('*', r'(.*)?').replace(' ', r'\s')
        found = regex.findall(reg, sentence)
        return found

        
    def rank_sent_for_tags(sentence, tags, reasmb_rule):
        result = {}
        sentence = sentence.lower()
        keys_to_debug = ('every thing', 'hello')

        import_words = sentence.split()

        # filter rules that can not decompose
        tags = list(filter(lambda x:rule_can_parse(x[1], sentence), tags))
        print("rules that can decompose:", tags)

        rule_keys = list(map(lambda x:x[1],tags))
        most_simillar_keys_from_CosSimilarity = calculate_cosine_simillarity_with_rule_keys(sentence, rule_keys)

        for tag in tags:
            ranking = {'key':tag[0], 'score':0.001, 'decomp':tag[1], reasmb_rule:tag[2]}

            reg = replace_decomp_with_syns(tag[1])
            reg = reg.replace('*', r'(.*)?').replace(' ', r'\s')
            ranking['decomp'] = reg

            number_of_stars = len(list(filter(lambda i: i=='*' ,tag[1])))
            if number_of_stars == 0:
                ranking['score'] += 8
            else:   
                ranking['score'] += number_of_stars*8

            number_of_spaces = len(list(filter(lambda i: i==' ' ,tag[1])))
            if number_of_spaces == 0:
                ranking['score'] += 1
            else:   
                ranking['score'] += number_of_spaces*1

                
            # step 1: check if key name is among the important words of the user input
            if tag[0] in import_words:
                if tag[0] not in ("every thing"): 
                    ranking['score'] += 10
                else:
                    ranking['score'] += 0.2

            if tag[0] in keys_to_debug:
                print(ranking,'step 1 done')

            # to do check this issue join.
            # print("check it", tag[1], "".join(most_simillar_keys_from_CosSimilarity))
            #step 2: considering our semantic similarity check
            if tag[1] == "".join(most_simillar_keys_from_CosSimilarity):
                ranking['score']+=20

            if tag[0] in keys_to_debug:
                print(ranking,'step 2 done')

            for imp_word in import_words:
                #adding effect of decomp rules to scores
                decomp_with_syn = replace_decomp_with_syns(tag[1])
                for decomp_word in decomp_with_syn.replace("|", " ").replace("(", " ").replace(")", " ").split(" "):
                    if decomp_word == imp_word:
                        if decomp_word not in ("every thing") : 
                            ranking['score'] += 1
                        else:
                            ranking['score'] += 0.3

            if tag[0] in keys_to_debug:
                print(ranking,'step 3 done')
            
            
            if ranking['key'] in result and float(ranking['score'])>float(result[ranking['key']]['score']):
                result[ranking['key']] = ranking
            elif ranking['key'] not in result:
                result[ranking['key']] = ranking
        
        print(result)
        return result

    def remove_repetetive_words_together(sent):
        res = []
        previous_word = ""
        for word in sent.split():
            if previous_word != word:
                res.append(word)
            previous_word = word
        return " ".join(res)

    def generate_eliza_response(decomp, user_inpt, reasmbl):
        user_inpt = user_inpt.lower()
        result = regex.search(decomp, user_inpt)
        reasmbl_res = regex.findall(r'\(\d\)' ,reasmbl)
        ar_indexes = []
        for reasmbl_chunks in reasmbl_res:
            index = reasmbl_chunks[1:2]
            ar_indexes.append(index)

        if '|' in decomp:
            for gp in result.groups():
                if find_syns(gp):
                    ar_indexes = list(map(lambda i: ({'old':i, 'new':int(i)+1} if int(i) >= result.groups().index(gp)+1 else {'old':i, 'new':i} ) if type(i) is not dict else ({'old':i['old'], 'new':int(i['new'])+1} if int(i['new']) >= result.groups().index(gp)+1 else {'old':i['old'], 'new':i['new']} ) ,ar_indexes))
                    print('****gp****', gp)
                    print('****ar_indexes****', ar_indexes)
        
        generated_response = reasmbl
        for index in ar_indexes:
            res = ""
            if type(index) is not dict:
                res = result.groups()[int(index)-1]
                res = "<start_mark>"+res+"<end_mark>"
                res = res.replace(' yourself<end_mark>', ' Myself')\
                    .replace(' myself<end_mark>', ' Yourself')\
                    .replace(' you ', ' I ')\
                    .replace("<start_mark>you ", 'I ')\
                    .replace(' i ', ' You ')\
                    .replace("<start_mark>i ", 'You ')\
                    .replace(" i'm ", ' You are ')\
                    .replace("<start_mark>i'm ", 'You are ')\
                    .replace(' my ', ' Your ')\
                    .replace('<start_mark>my ', 'Your ')\
                    .replace(' am ', ' are ')\
                    .replace(' me<end_mark>', ' You')\
                    .replace(' noone<end_mark>', ' no one')\
                    .replace(' noone ', ' no one ')\
                    .replace(' cannot ', ' can not ')\
                    .replace(' cannot<end_mark>', ' can not')\
                    .replace(' me ', ' You ')\
                    .replace(' we ', ' You ')\
                    .replace('<start_mark>we ', 'You ')\
                    .replace('<end_mark>', ' ')\
                    .replace('<start_mark>', ' ')
                
                generated_response = generated_response.replace("("+str(index)+")", " "+res+" ")
            else:
                if int(index['new']) != int(index['old']) and int(index['old'])-1 > 0 and int(index['new'])-1>0:
                    res = list(result.groups())[int(index['old'])-1] + " " + result.groups()[int(index['new'])-1]
                else:
                    res = result.groups()[int(index['new'])-1]


                res = "<start_mark>"+res+"<end_mark>"
                res = res.replace(' yourself<end_mark>', ' Myself')\
                .replace(' myself<end_mark>', ' Yourself')\
                .replace(' you ', ' I ')\
                .replace('<start_mark>you ', 'I ')\
                .replace(' i ', ' You ')\
                .replace('<start_mark>i ', ' You ')\
                .replace(" i'm ", ' You are ')\
                .replace("<start_mark>i'm ", 'You are ')\
                .replace(' my ', ' Your ')\
                .replace('<start_mark>my ', 'Your ')\
                .replace(' am ', ' are ')\
                .replace(' me<end_mark>', ' You')\
                .replace(' noone<end_mark>', ' no one')\
                .replace(' noone ', ' no one ')\
                .replace(' cannot ', ' can not ')\
                .replace(' cannot<end_mark>', ' can not')\
                .replace(' me ', ' You ')\
                .replace(' we ', ' You ')\
                .replace('<start_mark>we ', 'You ')\
                .replace('<end_mark>', ' ')\
                .replace('<start_mark>', ' ')

                generated_response = generated_response.replace("("+str(index['old'])+")", " "+res+" ")
            
        generated_response = generated_response.replace("  ", " ").replace(". .", ".").replace(". ?", "?").replace("? .", ".").replace("..", ".").replace(".?", "?").replace("?.", ".").replace("' ", "").replace("'?", "?")
        print("decomp= ", decomp)
        return generated_response
        
    #this is the main function which generates final response
    def generate_final_response(user_sentence, select_empathy, emotion_des, generate_dynamic_response=False):
        user_sentence = user_sentence.replace("  ", " ").\
            replace(" no one ", " noone ").\
            replace(" can not ", " cannot ")

        reasmb_rule = random.choice(['reasmb_dynamic_neutral', 'reasmb_neutral'])
        # reasmb_rule = "reasmb_dynamic_neutral"
        if select_empathy: reasmb_rule = 'reasmb_empathy' 

        key_score_decomp_ar = rank_sent_for_tags(user_sentence, list(map(lambda c: [c['key'], c['decomp'], c[reasmb_rule]] ,sample_generator_rules['dec_rules'])), reasmb_rule)
        best_key_decomp_reasmb = list(map(lambda i: i[1] ,sorted(key_score_decomp_ar.items(), key=lambda i: i[1]['score'], reverse=True)[:5]))[0]
        gen = generate_eliza_response(best_key_decomp_reasmb['decomp'], user_sentence, random.choice(best_key_decomp_reasmb[reasmb_rule]))
        gen = remove_repetetive_words_together(gen)
        print('key=',best_key_decomp_reasmb['key'])
        print("rule-based generated response: ", gen)
        return {"response":emotion_des+" "+gen, "key":best_key_decomp_reasmb['key']}


    generate_neutral = False
    # if detected_emotion not in ('joy', 'neutral'):
    #     generate_neutral = True
	
    res = generate_final_response(input, generate_neutral, emotion_des)
    return {"input":input , "output":res, "emotion":detected_emotion}

class VerifyApprovedResourcesView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get_queryset(self):
        return VerifyApprovedResources(self.request.query_params)

class AddViewOfResourceView(APIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get(self, request, format=None):
        res = addViewToResource(self.request.query_params)
        return Response({'res':res})

class HomepageResourceView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get_queryset(self):
        return ResourceViewQuerySet(self.request.query_params)

class EmotionTest(APIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get(self, request, format=None):
        res = EmotionTestFunc(self.request.query_params)
        return Response({'res':res})


class ResourceByIntentEntityView_new(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    #pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return ResourceByIntentEntityViewQuerySet_new(self.request.query_params)

class ResourceByIntentEntityView_new_new(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get(self, request, format=None):
        return ResourceByIntentEntityViewQuerySet_new_new(self.request.query_params)
    
class ResourceByIntentEntityView_Filter(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get(self, request, format=None):
        return ResourceByIntentEntityViewQuerySet_Filter(self.request.query_params)

class ResourceStatsView(APIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    # pagination_class = StandardResultSetPagination

    def get(self, request, format=None):
        res = calculateStatsResources(self.request.query_params)
        return Response({'res':res})

class IndexResourceEntityView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return calculateTagWeightsForResources(self.request.query_params)

class ResourceCountAndFilterView(APIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    # pagination_class = StandardResultSetPagination

    def get(self, request, format=None):
        res = calculateCountsForResources(self.request.query_params)
        return Response({'res':res})


class ResourceView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        queryset = ResourceViewQuerySet(self.request.query_params)
        if json.loads(self.request.query_params.dict().get("alphabetical", "False")):
            queryset = queryset.order_by('title')
        return queryset

class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Only approved tags?? Waiting for client confirmation
        # TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.filter(approved=True).order_by('name')
    
class AllTagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Only approved tags?? Waiting for client confirmation
        # TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.order_by('name')
    
class GetAliasByTagView(generics.ListAPIView):
    serializer_class = TagAliasSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        return Alias.objects.filter(tag_id=self.request.query_params['tag_id'])


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Category sorting? (Sort desc by most used)
        return Category.objects.all()


class DetailedResourceView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}

    # Override generics.RetrieveAPIView here to insert view count update
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.public_view_count += 1
        instance.save()
        return self.retrieve(request, *args, **kwargs)


class DetailedResourceAdminView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrieveResourceSerializer
    permissions_classes = {permissions.IsAdminUser}

# def get_relations_by_tag(request):
#     data = json.loads(request.body)
#     tag_id = data['tag_id']
#     relationships = TagRelationship.objects.filter(tag_id=tag_id)
#     response = []
#     for relation in relationships:
#         response.append({'id':relation.id,'parent':relation.parent})
#     return JsonResponse(response, safe=False)

# def add_tag_relation(request):
#     data = json.loads(request.body)
#     tag_id = data['tag_id']
#     parent_id = data["parent_id"]
#     relation = TagRelationship(parent_id = parent_id, tag_id = tag_id)
#     relation.save()
#     return JsonResponse({})

@login_required
def add_tag_alias(request):
    data = json.loads(request.body)
    tag_id = data['tag_id']
    name = data["name"]
    #get tag from tagid
    tag = Tag.objects.get(id=tag_id)
    relation = Alias(name=name, tag=tag)
    relation.save()
    return JsonResponse({})

@login_required
def remove_tag_alias(request):
    data = json.loads(request.body)
    alias_id = data['alias_id']
    Alias.objects.filter(id=alias_id).delete()
    return JsonResponse({})

def get_tag_group_stats(request):
    tag_groups = {
        'Indigenous':['Indigenous', 'Indigenous Women', 'Inuit', 'M\u00e9tis', "L'nu'k (Mi'kmaq)", "Siksika", "Cree"],
        'Youth':['Youth', 'Children', 'Black Youth', 'Mental health supports for Youth', 'Mental health supports for Children', 'Caregiver/Parent'],
        'Veterans':['Family Member of Veteran', 'Military Veterans'],
        'Healthcare Workers':['Doctor', 'First responder', 'Medical student', 'Nurse', 'Paramedic', 'Practising or retired physician', 'Resident Doctor'],
        'French':['French']
    }
    response = []
    #compute all resource totals
    total_all = Resource.objects.count()
    total_approved = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved")).count()
    total_pending = Resource.objects.filter((Q(review_status="pending") & Q(review_status_2="pending") & Q(review_status_1_1="pending")) | (Q(review_status_2="pending") & Q(review_status_1_1="pending") & Q(review_status_2_2="pending"))).count()
    total_rejected = total_all - total_approved - total_pending
    response.append(["Total", "All tags", total_approved, total_pending, total_rejected])
    for group in tag_groups.keys():
        #get relevent tags for the names
        tags = Tag.objects.filter(name__in=tag_groups[group])

        #get total
        all_matching = Resource.objects.filter(tags__in=tags)
        all_count = all_matching.count()

        approved_count = all_matching.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved")).count()

        pending_count = all_matching.filter((Q(review_status="pending") & Q(review_status_2="pending") & Q(review_status_1_1="pending")) | (Q(review_status_2="pending") & Q(review_status_1_1="pending") & Q(review_status_2_2="pending"))).count()

        rejected_count = all_count - pending_count - approved_count

        response.append([group, ", ".join(tag_groups[group]), approved_count, pending_count, rejected_count])

    return JsonResponse(response, safe=False)
