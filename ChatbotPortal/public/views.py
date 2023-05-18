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
from resource.models import Resource, Tag, Category
from resource.serializers import RetrieveResourceSerializer
from .serializers import ResourceSerializer, TagSerializer, CategorySerializer, RetrievePublicResourceSerializer, TagRelationship
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
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from django.http import JsonResponse

from sentence_transformers import SentenceTransformer, util #new pip install -U sentence-transformers
import regex 
import random
#add to server
import numpy as np


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

        # adding provience of a city to tags (query relaxation)
        canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-dOr', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'LAssomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'LAncienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'LÎle-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'LEpiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'LIslet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-dUrfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort QuAppelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'LAvenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayers Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen',]
        canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Alberta', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick', 'Ontario', 'British Columbia', 'Ontario', 'Alberta', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta', 'Quebec', 'Alberta', 'Alberta', 'Ontario', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince Edward Island', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Nova Scotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta', 'Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Ontario', 'British Columbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Nova Scotia', 'Alberta', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba', 'British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta', 'Prince Edward Island', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta', 'Ontario', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'British Columbia', 'Ontario', 'Alberta', 'Ontario', 'Prince Edward Island', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'New Brunswick', 'Alberta', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta', 'Ontario', 'Nova Scotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'New Brunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia', 'Alberta', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan', 'Alberta', 'Alberta', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'New Brunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Alberta', 'Manitoba', 'Ontario', 'Alberta', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta', 'New Brunswick', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'British Columbia', 'Manitoba', 'Manitoba', 'Alberta', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'Nova Scotia', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador', 'Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Alberta', 'Alberta', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Alberta', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia', 'Saskatchewan', 'Alberta', 'Alberta', 'Alberta', 'Alberta', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'British Columbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'Newfoundland and Labrador', 'Alberta', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince Edward Island', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Alberta', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Prince Edward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta', 'Manitoba', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'New Brunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Saskatchewan', 'Quebec', 'Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon', 'Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta', 'Saskatchewan', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta', 'Quebec', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta', 'Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Ontario', 'Saskatchewan', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba', 'Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut', 'Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Quebec', 'Nunavut', 'Alberta', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec', 'Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta', ]
        query_relaxation_tags = []
        location_tags = Tag.objects.filter(id__in=tag_list).values('name').all()
        query_relaxation_tags = list(map(lambda x: x['name'], location_tags))

        for tag in location_tags:   
            tag = tag['name']
            try:         
                index = canada_cities.index(tag)
                if index >= 0:
                    query_relaxation_tags.append(canada_city_proviences[index])
                    canada_cities.pop(index)
                    canada_city_proviences.pop(index)
            except ValueError:
                print('error!')
                continue


        #adding obvious location tags
        query_relaxation_tags.append('World-wide')
        query_relaxation_tags.append('All Canada')

        # queryset = queryset.exclude(tags__name__in=canada_cities)
        queryset = queryset.filter(Q(tags__id__in=tag_list) | Q(tags__name__in=query_relaxation_tags))


        # scoring and ordering by scores
        resource_scores = {}
        for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title], queryset)):
            resource_scores[resource[0]] = 0
            if resource[1] is None or resource[1]=='':
                continue
            index = json.loads(resource[1])
            original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
            for tag in tag_list:
                if tag in index:
                    resource_scores[resource[0]] += index[tag]
                if tag in original_tag_ids:
                    resource_scores[resource[0]] += 0.65

        topitems = heapq.nlargest(30, resource_scores.items(), key=itemgetter(1))
        # topitemsasdict = dict(filter(lambda x: x[1]>0, topitems))
        topitemsasdict = dict(topitems)
        if len(topitems) > 1:
            queryset = queryset.filter(id__in=topitemsasdict.keys())
            
            #this set
            thisSet = []
            #make result distinct
            for query in queryset:
                if query.id not in thisSet:
                    thisSet.append(query.id)
            newQuerySet = Resource.objects.filter(id__in=thisSet)

            for qs in newQuerySet:
                if qs.id not in topitemsasdict.keys():
                    qs.score = 0
                else:
                    qs.score = topitemsasdict[qs.id]

            newQuerySet.order_by('score')
            return newQuerySet
    
    return queryset


def calculateCountsForResources(query_params):
    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    # mapping between chatbot inten/entity names and our tags
    word_mapping = {'family_member': 'Caregiver/Parent'
    ,'family_member': 'Children'
    ,'employer_resources': 'Employer/Administrator'
    ,'family_member': 'Family member (other)'
    ,'family_member': 'Family member of physician or medical learner'
    ,'female_resources': 'Female'
    ,'healthcare_worker': 'First responder'
    ,'lgbtq2s_resources': 'Gender fluid, non-binary, and/or two spirit'
    ,'lgbtq2s_resources': 'LGBTQ2S+'
    ,'male_resources': 'Male'
    ,'healthcare_worker': 'Medical student'
    ,'veteran': 'Military Veterans'
    ,'new_canadian': 'New Canadian'
    ,'healthcare_worker': 'Nurse'
    ,'healthcare_worker': 'Practising or retired physician'
    ,'healthcare_worker': 'Resident doctor'
    ,'employment': 'Social worker'
    ,'employment': 'Student (postsecondary)'
    ,'family_member': 'Family Member of Veteran'
    ,'indigenous_resources': 'Indigenous'
    ,'employment': 'fire fighter'
    ,'Over 18': 'Youth'
    ,'healthcare_worker': 'Service Providers'
    ,'lgbtq2s_resources': 'Transgender'
    ,'lgbtq2s_resources': 'Non-Binary'
    ,'paid_resources': 'Fee-for-service available to everyone'
    ,'free_resources': 'Free'
    ,'free_resources': 'Free for members'
    ,'free_resources': 'N/A (ex. websites, podcasts)'
    ,'paid_resources': 'Paid'
    ,'free_resources': 'Requires paid membership'
    ,'free_resources': 'Requires provincial health card'
    ,'paid_and_free': 'Unknown'
    ,'paid_and_free': 'Both free and paid'
    ,'book_and_pamphlet': 'Brochure'
    ,'causes': 'cause'
    ,'group_class': 'Classes/course (in person)'
    ,'definition': 'Definition'
    ,'virtual': 'Mobile App'
    ,'online_courses_and_webinar': 'Webinar/Online course (go at your own pace)'
    ,'online_courses_and_webinar': 'Webinar/Online course (scheduled)'
    ,'screening': 'Screening tool'
    ,'information': 'Statistic'
    ,'symptom_List': 'Symptoms'
    ,'treatment_Info': 'Treatments'
    ,'information': 'Informational Website'
    ,'coping_skills': 'Informational Website'
    ,'self_help': 'Informational Website'
    ,'self_help': 'Worksheet'
    ,'online_courses_and_webinar': 'Online course (go at your own pace)'
    ,'online_courses_and_webinar': 'Online course (scheduled)'
    ,'self_help': 'Self-Help Books'
    ,'addiction_substance_use_programs': 'Addiction and recovery'
    ,'prevalence': 'Prevalence'
    ,'virtual': 'Online Group Support'
    ,'peer_support': 'Community Support'
    ,'suicidal_other': 'Crisis Support/Distress Counselling'
    ,'suicidal_self': 'Crisis Support/Distress Counselling'
    ,'peer_support': 'Peer Support'
    ,'help_from_another_person': 'Online chat'
    ,'specialist': 'Medical services'
    ,'housing': 'Housing - Emergency'
    ,'group_class': 'Group therapy'
    ,'doctor': 'Family Doctor'
    ,'peer_support': 'In-person Group Support Meeting'
    ,'need_in_person': 'In-person Group Support Meeting'
    ,'help_from_another_person': 'Phone line/call centre'
    ,'psychiatrist': 'Psychiatrist'
    ,'psychologist': 'Psychologist'
    ,'addiction_substance_use_programs': 'Rehabilitation'
    ,'specialist': 'Therapist/Counsellor/Psychotherapist'
    ,'counsellor_psychotherapist': 'Therapist/Counsellor/Psychotherapist'
    ,'healer': 'Traditional Indigenous Healer'
    ,'children': 'Youth'
    ,'youth': 'Children'
    ,'doctor': 'Resident doctor'
    ,'doctor': 'Practising or retired physician'
    ,'fire fighter': 'First responder'
    ,'fire fighter': 'Social worker'
    ,'community support': 'Group therapy'
    ,'community support': 'In-person Group Support Meeting'
    ,'community support': 'Peer Support'		
    ,'peer_support': 'Group therapy'
    ,'domestic_abuse_support': 'Violence intervention'
    ,'domestic_abuse_support': 'Domestic Violence'
    ,'domestic_abuse_support': 'Abuse'
    ,'generalized anxiety disorder': 'Anxiety'
    ,'generalized anxiety disorder': 'General public/all'
    ,'generalized anxiety disorder': 'Stress'
    ,'generalized anxiety disorder': 'Depression'
    ,'health professional':'Psychologist'
    ,'health professional':'Family Doctor'
    ,'alberta':'Alberta'
    ,'schizophrenia':'Schizophrenia and psychosis'
    ,'covid-19':'COVID-19 (context specific - ensure any other concerns are also noted)'
    ,'covid':'COVID-19 (context specific - ensure any other concerns are also noted)'
    ,'eating':'Eating Disorders'
    ,'distress':'General Distress'
    ,'hiv':'Human Immunodeficiency Virus (HIV)'
    ,'addiction':'Addictions (including Drugs, Alcohol, and Gambling)'
    ,'addiction':'Behavioural Addiction'
    ,'addiction':'Substance use'
    ,'resilience':'Resiliency'
    ,'psychologist':'Therapist/Counsellor/Psychotherapist'
    ,'psychiatrist':'Therapist/Counsellor/Psychotherapist'
    ,'need_coping_skill':'Self-Help Books'
    ,'need_symptom_list': 'Symptoms'
    ,'psychedelics': 'psilocybin'
    ,'crisis_distress_support':'Crisis Support/Distress Counselling',
    'military': 'Military Veterans'
    }

    #tags that we should exclude their resources
    ntags_params = query_params.getlist('ntags')
    ntags_params = Tag.objects.filter(name__in=ntags_params).all()
    ntags_ids = list(map(lambda x: x.id, ntags_params))
    

    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if x.startswith('need_') else x.lower() ,tags_params))
    

    tags_params = list(map(lambda x: x[:x.index("(")] if "(" in x else x ,tags_params))


    all_possible_tags = Tag.objects.filter(approved=1).all()
    all_possible_tags = list(map(lambda x: x.name, all_possible_tags))

    should_be_romoved = set()
    should_be_added = set()
    

    #query matching with simillar words
    for tag_param in tags_params:
        if tag_param in all_possible_tags:
            continue
        else:
            #checking our small word mapping array
            if tag_param.lower() in word_mapping.keys():
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param.lower() ,word_mapping.items()):
                    should_be_added.add(related_word[1])
            else: #using edit distance
                similar_tags = difflib.get_close_matches(tag_param.lower(), all_possible_tags, n=2, cutoff=0.61)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
    
    #replace input with actuall tag names
    tags_params = set(tags_params)
    tags_params.update(should_be_added)
    tags_params = tags_params.difference(should_be_romoved)



    # adding provience of a city to tags list (query relaxation)
    canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-dOr', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'LAssomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'LAncienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'LÎle-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'LEpiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'LIslet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-dUrfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort QuAppelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'LAvenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayers Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen',]
    canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Alberta', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia','Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick','Ontario', 'British Columbia', 'Ontario', 'Alberta', 'British Columbia', 'Ontario', 'NovaScotia', 'Alberta', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'BritishColumbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'BritishColumbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta','British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta','Quebec', 'Alberta', 'Alberta', 'Ontario', 'Alberta', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince EdwardIsland', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta','Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec','Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'Quebec', 'Alberta','Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Alberta', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario','Alberta', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland andLabrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'NovaScotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Alberta', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta','Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'BritishColumbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Ontario', 'BritishColumbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick','Ontario', 'Quebec', 'Alberta', 'Ontario', 'Nova Scotia', 'Alberta', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario','Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba','British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta', 'Prince Edward Island','British Columbia', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Manitoba', 'Quebec','Alberta', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'BritishColumbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'NovaScotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta', 'Ontario', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'NewBrunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia','Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta','Quebec', 'British Columbia', 'Ontario', 'Alberta', 'Ontario', 'Prince Edward Island','Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario','Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'NewBrunswick', 'Alberta', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec','Alberta', 'Ontario', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta', 'Ontario', 'NovaScotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta', 'Alberta', 'Quebec','Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Alberta','Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick','Alberta', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta', 'Ontario', 'Newfoundland andLabrador', 'Ontario', 'Alberta', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'BritishColumbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'BritishColumbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta','Alberta', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec','Alberta', 'Ontario', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'NewBrunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta','Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia','Alberta', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec','Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia','Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan','Alberta', 'Alberta', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario','Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario','Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'BritishColumbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'NewBrunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Alberta', 'Manitoba', 'Ontario', 'Alberta', 'Quebec','Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec','New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'NewBrunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'BritishColumbia', 'Ontario', 'Nova Scotia', 'Alberta', 'New Brunswick', 'Nova Scotia', 'BritishColumbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'British Columbia','Manitoba', 'Manitoba', 'Alberta', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec','Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba','Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick','Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'NovaScotia', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia','Saskatchewan', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador','Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario','Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta','Newfoundland and Labrador', 'Alberta', 'Alberta', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'BritishColumbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec','Alberta', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Saskatchewan','Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Alberta', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia','Saskatchewan', 'Alberta', 'Alberta', 'Alberta', 'Alberta', 'NorthwestTerritories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec','Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan','Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba','Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'BritishColumbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick','Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec','Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta','British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'NewBrunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta', 'Quebec', 'Newfoundlandand Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick','Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'Newfoundland and Labrador', 'Alberta', 'Ontario', 'Quebec', 'Quebec','British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'New Brunswick', 'Ontario','British Columbia', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick','Quebec', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince EdwardIsland', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Quebec', 'Quebec','Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan','Alberta', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'BritishColumbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec','Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan','Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'NewBrunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta','Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec','Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick','New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador','Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec','Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland andLabrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'PrinceEdward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia','Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta', 'NewBrunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta', 'Manitoba', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario','Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland andLabrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'NewBrunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'NewBrunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Saskatchewan', 'Quebec','Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'BritishColumbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon','Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'NovaScotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta', 'Saskatchewan', 'Alberta','Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia','Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta', 'Quebec', 'Manitoba','Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta','Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta', 'Saskatchewan','New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta','Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Ontario', 'Saskatchewan', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Alberta', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador','Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick','New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundlandand Labrador', 'New Brunswick', 'Quebec', 'Alberta', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec','Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'NewBrunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba','Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick','Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta','Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec','British Columbia', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador','Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'New Brunswick','Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut','Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan','Quebec', 'Nunavut', 'Alberta', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec','Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec','Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'BritishColumbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta', ]
    
    query_relaxation_tags = []
    # tags_params.add("General public/all")
    for tag in tags_params:
        # tag = tag['name']
        if tag in canada_cities:         
            index = canada_cities.index(tag)
            query_relaxation_tags.append(canada_city_proviences[index])
            canada_cities.pop(index)
            canada_city_proviences.pop(index)
        else:
            similar_tags = difflib.get_close_matches(tag_param.lower(), canada_cities, n=1, cutoff=0.61)
            if (len(similar_tags)>0):
                index = canada_cities.index(similar_tags[0])
                query_relaxation_tags.append(canada_city_proviences[index])
                query_relaxation_tags.append(similar_tags[0])
                canada_cities.pop(index)
                canada_city_proviences.pop(index)

    resource_type = ["BT"]
    if "program_services" in tags_params:
        resource_type.append("SR")
    if "information" in tags_params:
        resource_type.append("RS")

    resQueryset = resQueryset.filter((Q(resource_type__in=resource_type)) & (Q(tags__name__in=tags_params) | Q(tags__name__in=query_relaxation_tags)))
    

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
        return {'resource_counts':len(newQuerySet), 'btns':[btn_1,btn_2]}
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
    allRes = Resource.objects.all()
    
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

# rasa will call it 
def ResourceByIntentEntityViewQuerySet_new(query_params):
    resQueryset = Resource.objects.filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('healthcare_worker', 'First responder')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('healthcare_worker', 'Medical student')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('healthcare_worker', 'Nurse')
    ,('healthcare_worker', 'Practising or retired physician')
    ,('healthcare_worker', 'Resident doctor')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('Over 18', 'Youth')
    ,('healthcare_worker', 'Service Providers')
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
    ,('definition', 'Definition')
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
    ,('doctor', 'Family Doctor')
    ,('peer_support', 'In-person Group Support Meeting')
    ,('need_in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    ,('children', 'Youth')
    ,('youth', 'Children')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Practising or retired physician')
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
    ,('health professional','Psychologist')
    ,('health professional','Family Doctor')
    ,('alberta','Alberta Wide')
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
    ('first responder', 'First responder')
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
    all_possible_tags = list(map(lambda x: x.name, all_possible_tags))

    #######################calculate tag embeddings
    #Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    # Sentences we want embeddings for
    sentences = [
        "Abuse",
        "Acquired Immune Deficiency Syndrome (AIDS)",
        "Addictions (including Drugs, Alcohol and Gambling)",
        "Adjustment disorders",
        "Anger",
        "Anorexia",
        "Antisocial Personality Disorder (ASPD)",
        "Anxiety",
        "Asperger Syndrome",
        "Attachment Problems",
        "Attention Deficit Disorders (ADD/ADHD)",
        "Auditory Processing Disorder (APD)",
        "Autism and Autism Spectrum Disorders",
        "Behaviour and Conduct Problems",
        "Bipolar Disorders",
        "Body dysmorphic disorder (BDD)",
        "Borderline Personality Disorder (BPD)",
        "Bulimia",
        "Bullying",
        "Burnout",
        "Cancer",
        "Chronic Pain",
        "Conduct Disorder",
        "Corrections",
        "COVID-19 (context specific - ensure any other concerns are also noted)",
        "Delirium",
        "Dementia including Alzheimer's",
        "Depression",
        "Developmental Coordination Disorder (DCD)",
        "Developmental, Intellectual Delay and Disabilities",
        "Domestic Violence",
        "Down syndrome",
        "Eating Disorders",
        "Elimination Disorders",
        "Fatigue",
        "Fetal Alcohol and Fetal Alcohol Spectrum Disorders (FASD)",
        "Financial and Employment",
        "Firesetting",
        "Gender Identity Issues",
        "General Distress",
        "General Supports for Children",
        "General well-being (All/Any)",
        "Generalized Anxiety Disorder",
        "Grief and Bereavement",
        "Harassment",
        "Harm-Reduction",
        "Hoarding",
        "Housing",
        "Human Trafficking",
        "Infant and Early Childhood Mental Health (IECMH)",
        "Insomnia",
        "Learning Disorders",
        "Legal",
        "Maternal Mental Health",
        "Medication Treatment",
        "Men's abuse",
        "Mental Health in General",
        "Mood Disorders",
        "Obsessive Compulsive Disorder (OCD)",
        "Operational Stress Injury (OSI)",
        "Oppositional behaviours including oppositional defiant disorder (ODD)",
        "Other, please specify",
        "Overweight and Obesity",
        "Pandemic (e.g. COVID/Coronavirus), Disasters and Related Emergencies",
        "Panic",
        "Parenting",
        "Personality disorders",
        "Phobia",
        "Physical Disabilities",
        "Physical Health and Nutrition",
        "Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse",
        "Psychopathy",
        "Reconciliation",
        "Resiliency",
        "Schizophrenia and Psychosis",
        "School Refusal (and School Phobia)",
        "Self-care",
        "Self-harm including Self-cutting",
        "Self-Regulation",
        "Sensory Processing Disorders and Self-Regulation Problems",
        "Separation and Divorce",
        "Sexual Health",
        "Sexual Violence",
        "Sleep",
        "Smoking Cessation",
        "Social Skills and Life Skills",
        "Somatoform Disorders",
        "Speech and Language",
        "Stigma",
        "Stress",
        "Substance use",
        "Suicidal Ideation",
        "Technology Issues, including Internet, Cellphone, Social Media Addiction",
        "Tourette Syndrome and Tic Disorders",
        "Trauma",
        "Workplace",
        "Agoraphobia",
        "Selective Mutism",
        "Post-Partum",
        "Seasonal Affective Disorder",
        "Interpersonal Relationships",
        "Behavioural Addiction",
        "Gambling",
        "Social Anxiety Disorder",
        "resilience",
        "Human Immunodeficiency Virus (HIV)",
        "Foster Care",
        "Traditional Aboriginal Health",
        "Other Treatment Types (Non-Medicinal/Pharmaceutical)"
    ]
    len_tag_embedding = len(sentences)
    for t in tags_params:
        if t[1] == 'mh_concern':
            sentences.append(t[0])

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)


    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    class_tag_mapping = {}


    for tag_param in tags_params:
        if not str(tag_param[1]).isnumeric():
            if not (tag_param[1] in class_tag_mapping):
                class_tag_mapping[tag_param[1]] = []
            class_tag_mapping[tag_param[1]].append(tag_param[0])

        tag_param = tag_param[0]

        word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))
        # word_mapping_values = list(map(lambda x: x[1] ,word_mapping))

        if tag_param in all_possible_tags:
            continue
        else:
            if tag_param in word_mapping_keys:
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    # print(tag_param, 'look up table ', related_word[1])
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tags, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')
    

    input_location_type_mh = []
    if 'city' in class_tag_mapping:
        input_location_type_mh.append(100)
    else:
        input_location_type_mh.append(0.01)
    
    if 'resource_type' in class_tag_mapping:
        input_location_type_mh.append(100)
    else:
        input_location_type_mh.append(0.01)
    
    if 'mh_concern' in class_tag_mapping:
        input_location_type_mh.append(100)
    else:
        input_location_type_mh.append(0.01)

    #provience2city mapping 
    canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-dOr', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'LAssomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'LAncienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'LÎle-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'LEpiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'LIslet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-dUrfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort QuAppelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'LAvenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayers Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen', 'Nova Scotia']
    
    canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia','Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick','Ontario', 'British Columbia', 'Ontario', 'Alberta Wide', 'British Columbia', 'Ontario', 'NovaScotia', 'Alberta Wide', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'BritishColumbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'BritishColumbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta Wide','British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta Wide','Quebec', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince EdwardIsland', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta Wide','Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec','Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'British Columbia', 'Quebec', 'Alberta Wide','Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario','Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland andLabrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'NovaScotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Alberta Wide', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta Wide','Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'BritishColumbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Ontario', 'BritishColumbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick','Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario','Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba','British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta Wide', 'Prince Edward Island','British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta Wide', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Manitoba', 'Quebec','Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'BritishColumbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'NovaScotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta Wide', 'Ontario', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'NewBrunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia','Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide','Quebec', 'British Columbia', 'Ontario', 'Alberta Wide', 'Ontario', 'Prince Edward Island','Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario','Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta Wide', 'Ontario', 'NewBrunswick', 'Alberta Wide', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec','Alberta Wide', 'Ontario', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'NovaScotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec','Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Alberta Wide','Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick','Alberta Wide', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'Newfoundland andLabrador', 'Ontario', 'Alberta Wide', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'BritishColumbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'BritishColumbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta Wide','Alberta Wide', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec','Alberta Wide', 'Ontario', 'Ontario', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'NewBrunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta Wide','Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia','Alberta Wide', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec','Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia','Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan','Alberta Wide', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario','Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario','Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'BritishColumbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'NewBrunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Alberta Wide', 'Manitoba', 'Ontario', 'Alberta Wide', 'Quebec','Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec','New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'NewBrunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta Wide','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'BritishColumbia', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'New Brunswick', 'Nova Scotia', 'BritishColumbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'British Columbia','Manitoba', 'Manitoba', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec','Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba','Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick','Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Ontario', 'New Brunswick', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'NovaScotia', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia','Saskatchewan', 'Ontario', 'Alberta Wide', 'Alberta Wide', 'Newfoundland and Labrador','Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario','Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta Wide','Newfoundland and Labrador', 'Alberta Wide', 'Alberta Wide', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'BritishColumbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec','Alberta Wide', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Ontario', 'Saskatchewan','Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Alberta Wide', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia','Saskatchewan', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'NorthwestTerritories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec','Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan','Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba','Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta Wide','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'BritishColumbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick','Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec','Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta Wide','British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'NewBrunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'Newfoundlandand Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick','Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'Newfoundland and Labrador', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec','British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'New Brunswick', 'Ontario','British Columbia', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick','Quebec', 'Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince EdwardIsland', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec','Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan','Alberta Wide', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'BritishColumbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec','Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan','Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'NewBrunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta Wide','Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec','Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick','New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador','Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec','Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland andLabrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'PrinceEdward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia','Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta Wide', 'NewBrunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta Wide', 'Manitoba', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario','Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland andLabrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'NewBrunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'NewBrunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Saskatchewan', 'Quebec','Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'BritishColumbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon','Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'NovaScotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta Wide', 'Saskatchewan', 'Alberta Wide','Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia','Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta Wide', 'Quebec', 'Manitoba','Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta Wide','Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta Wide', 'Saskatchewan','New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta Wide','Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Alberta Wide', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador','Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick','New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundlandand Labrador', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec','Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'NewBrunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba','Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick','Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta Wide','Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta Wide', 'Quebec', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec','British Columbia', 'Ontario', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador','Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'New Brunswick','Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut','Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan','Quebec', 'Nunavut', 'Alberta Wide', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec','Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec','Alberta Wide', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'BritishColumbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta Wide', 'Nova Scotia Wide']
    
    query_relaxation_tags = []
    
    # print('class_tag_mapping',class_tag_mapping)
    canada_cities = list(map(lambda x: x.lower() ,canada_cities))

    if 'city' in class_tag_mapping:
        for loc_tag in class_tag_mapping['city']:
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'city'))
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'city'))
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'city'))

        
    #adding obvious location tags
    query_relaxation_tags.append('World-wide')
    query_relaxation_tags.append('All Canada')
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_romoved)

    print('tags_params_mapped', tags_params_mapped)
    # print('query_relaxation_tags', query_relaxation_tags)
    
    # print('query_relaxation_tags',query_relaxation_tags)
    # print('tags_params', tags_params)

    
    resQueryset = resQueryset.filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))



    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id').all()
    query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))

    #retrieve tag ids from tag names
    tags = Tag.objects.filter(name__in=tags_params_mapped).values('id','tag_category').all()
    tags_id_list = list(map(lambda x: x['id'], tags))
    tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    
    
    
    # input_location_type_mh
    # scoring and ordering by scores
    resource_scores = {}
    res_counter = 0
    for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], resQueryset)):
        resource_scores[resource[0]] = [0,0,0]
        if resource[1] is None or resource[1]=='':
            resource_scores[resource[0]] = 0
            continue

        index = json.loads(resource[1])
        original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
        original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
        
        for tag in tags_id_list:
            t_cat = tags_cat_list[tags_id_list.index(tag)]

            tag = str(tag)
            if tag in index:
                if t_cat=="Health Issue":
                    resource_scores[resource[0]][2] += index[tag]
                elif t_cat=="Location":
                    resource_scores[resource[0]][0] += index[tag]
                elif t_cat in ("Resource Type for Education/Informational", "Resource Type for Programs and Services"):
                    resource_scores[resource[0]][1] += index[tag]

                
            if tag in original_tag_ids:
                i = original_tag_ids.index(tag)

                if original_tag_categories[i] == 'Location':
                    resource_scores[resource[0]][0] += 10
                elif original_tag_categories[i] == 'Health Issue':
                    resource_scores[resource[0]][2] += 20
                elif original_tag_categories[i] in ('Resource Type for Programs and Services', 'Resource Type for Education/Informational'):
                    resource_scores[resource[0]][1] += 10

        for original_tag_id in original_tag_ids:
            if original_tag_id in query_relaxation_tags_id:
                #for query relaxation
                i = original_tag_ids.index(original_tag_id)

                if original_tag_categories[i] == 'Location':
                    resource_scores[resource[0]][0] += 6
                elif original_tag_categories[i] == 'Health Issue':
                    resource_scores[resource[0]][2] += 12
                elif original_tag_categories[i] in ('Resource Type for Programs and Services', 'Resource Type for Education/Informational'):
                    resource_scores[resource[0]][1] += 6

        #added like a rule 
        if "Informational Website" in tags_params_mapped:
            resource_scores[resource[0]][1] = 10

        resource_scores[resource[0]] = cos(torch.FloatTensor(input_location_type_mh), torch.FloatTensor(resource_scores[resource[0]])).numpy()*10

        # print(resource_scores[resource[0]])

        #tags_params_mapped = string value of tags
        for tag in tags_params_mapped:
            if len(tag)<2:
                continue

            if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.55
            
            if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.55
            
            
            if (tag == 'Informational Website') and (resource[4] == 'RS' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 2
            elif (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 2

            if (tag == 'Definition') and (resource[5]):
                resource_scores[resource[0]] += 0.45

            if (tag == 'Domestic Violence') and ("sheltersafe" in resource[3].lower()):
                resource_scores[resource[0]] += 15.5

            if (tag == 'Therapist/Counsellor/Psychotherapist') and ("counsel" in resource[3].lower()):
                resource_scores[resource[0]] += 0.95

            sum_tag = ""
            for w in tag.replace("-", " ").split(" "):
                if len(w)>0: sum_tag += w[0]
            if (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                resource_scores[resource[0]] += 0.55
        
        res_counter+=1


    topitems = heapq.nlargest(15, resource_scores.items(), key=itemgetter(1))

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
                qs.score = topitemsasdict[qs.id] 
        return newQuerySet



    #  tags = Tag.objects.filter(name__in=tags_params).values('id').all()
    #  tagsList = list(map(lambda x: x.id, tags))
    # print(tagsList)
    
    # resQueryset = resQueryset.filter(tags__id__in=tagsList)
    # resQueryset = resQueryset.order_by('public_view_count')

    return resQueryset

# new new
def ResourceByIntentEntityViewQuerySet_new_new(query_params):
    resQueryset = Resource.objects.filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) | (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) | (Q(review_status="approved") & Q(review_status_2_2="approved")) | (Q(review_status="approved") & Q(review_status_1_1="approved")) | (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | Q(review_status_3="approved"))
    
    word_mapping = [('family_member', 'Caregiver/Parent')
    ,('family_member', 'Children')
    ,('employer_resources', 'Employer/Administrator')
    ,('family_member', 'Family member (other)')
    ,('family_member', 'Family member of physician or medical learner')
    ,('female_resources', 'Female')
    ,('healthcare_worker', 'First responder')
    ,('lgbtq2s_resources', 'Gender fluid, non-binary, and/or two spirit')
    ,('lgbtq2s_resources', 'LGBTQ2S+')
    ,('male_resources', 'Male')
    ,('healthcare_worker', 'Medical student')
    ,('veteran', 'Military Veterans')
    ,('new_canadian', 'New Canadian')
    ,('healthcare_worker', 'Nurse')
    ,('healthcare_worker', 'Practising or retired physician')
    ,('healthcare_worker', 'Resident doctor')
    ,('employment', 'Social worker')
    ,('employment', 'Student (postsecondary)')
    ,('family_member', 'Family Member of Veteran')
    ,('indigenous_resources', 'Indigenous')
    ,('employment', 'fire fighter')
    ,('Over 18', 'Youth')
    ,('healthcare_worker', 'Service Providers')
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
    ,('definition', 'Definition')
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
    ,('need_in_person', 'In-person Group Support Meeting')
    ,('help_from_another_person', 'Phone line/call centre')
    ,('psychiatrist', 'Psychiatrist')
    ,('psychologist', 'Psychologist')
    ,('addiction_substance_use_programs', 'Rehabilitation')
    ,('specialist', 'Therapist/Counsellor/Psychotherapist')
    ,('counsellor_psychotherapist', 'Therapist/Counsellor/Psychotherapist')
    ,('healer', 'Traditional Indigenous Healer')
    ,('children', 'Youth')
    ,('youth', 'Children')
    ,('doctor', 'Resident doctor')
    ,('doctor', 'Practising or retired physician')
    ,('doctor', 'Doctor')
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
    ,('health professional','Psychologist')
    ,('health professional','Family Doctor')
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
    ('first responder', 'First responder')
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

    cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
    

    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    class_tag_mapping = {}


    word_mapping_keys = list(map(lambda x: x[0] ,word_mapping))

    for tag_param in tags_params:
        tag_param = tag_param[0]
        print("tag_param", tag_param)

        if tag_param in all_possible_tag_names:
            print("found in approved tags")
            continue
        else:
            if tag_param in word_mapping_keys:
                print("found in word mapping")
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param ,word_mapping):
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param, all_possible_tag_names, n=2, cutoff=0.7)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
                    print("found using distance")



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')


    for tag_ in should_be_added:
        try:
            tag_category = [tag[1] for tag in all_possible_tags if tag[0] == tag_][0]
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

    #VIP tags are tags that all should be present in a resource to be a candidate 
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
                                                           


    #provience2city mapping 
    canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-dOr', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'LAssomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'LAncienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'LÎle-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'LEpiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'LIslet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-dUrfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort QuAppelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'LAvenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayers Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen', 'Nova Scotia']
    
    canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Alberta', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia','Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick','Ontario', 'British Columbia', 'Ontario', 'Alberta', 'British Columbia', 'Ontario', 'NovaScotia', 'Alberta', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'BritishColumbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'BritishColumbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta','British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta','Quebec', 'Alberta', 'Alberta', 'Ontario', 'Alberta', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince EdwardIsland', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta','Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec','Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Alberta', 'British Columbia', 'Quebec', 'Alberta','Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Alberta', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario','Alberta', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland andLabrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'NovaScotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Alberta', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta','Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'BritishColumbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Ontario', 'BritishColumbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick','Ontario', 'Quebec', 'Alberta', 'Ontario', 'Nova Scotia', 'Alberta', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario','Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba','British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta', 'Prince Edward Island','British Columbia', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta', 'Ontario', 'Manitoba', 'Quebec','Alberta', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'BritishColumbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'NovaScotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta', 'Ontario', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'NewBrunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia','Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta','Quebec', 'British Columbia', 'Ontario', 'Alberta', 'Ontario', 'Prince Edward Island','Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario','Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta', 'Ontario', 'NewBrunswick', 'Alberta', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec','Alberta', 'Ontario', 'Alberta', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta', 'Ontario', 'NovaScotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta', 'Alberta', 'Quebec','Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Alberta','Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick','Alberta', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta', 'Ontario', 'Newfoundland andLabrador', 'Ontario', 'Alberta', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'BritishColumbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'BritishColumbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta','Alberta', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec','Alberta', 'Ontario', 'Ontario', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'NewBrunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta','Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia','Alberta', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec','Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia','Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan','Alberta', 'Alberta', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario','Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario','Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'BritishColumbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'NewBrunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Alberta', 'Manitoba', 'Ontario', 'Alberta', 'Quebec','Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec','New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'NewBrunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Alberta', 'Quebec', 'Ontario', 'BritishColumbia', 'Ontario', 'Nova Scotia', 'Alberta', 'New Brunswick', 'Nova Scotia', 'BritishColumbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'British Columbia','Manitoba', 'Manitoba', 'Alberta', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec','Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba','Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick','Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Ontario', 'New Brunswick', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'NovaScotia', 'Alberta', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia','Saskatchewan', 'Ontario', 'Alberta', 'Alberta', 'Newfoundland and Labrador','Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario','Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta','Newfoundland and Labrador', 'Alberta', 'Alberta', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'BritishColumbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec','Alberta', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Ontario', 'Saskatchewan','Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Alberta', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia','Saskatchewan', 'Alberta', 'Alberta', 'Alberta', 'Alberta', 'NorthwestTerritories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec','Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan','Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba','Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'BritishColumbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick','Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec','Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta','British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'NewBrunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta', 'Quebec', 'Newfoundlandand Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick','Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'Newfoundland and Labrador', 'Alberta', 'Ontario', 'Quebec', 'Quebec','British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta', 'New Brunswick', 'Ontario','British Columbia', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'British Columbia', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick','Quebec', 'Alberta', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince EdwardIsland', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta', 'Quebec', 'Quebec','Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan','Alberta', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'BritishColumbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec','Quebec', 'Quebec', 'Alberta', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan','Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'NewBrunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta','Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec','Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick','New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador','Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec','Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland andLabrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'PrinceEdward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia','Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta', 'NewBrunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta', 'Manitoba', 'Alberta', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario','Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland andLabrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'NewBrunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'NewBrunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Saskatchewan', 'Quebec','Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'BritishColumbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon','Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'NovaScotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta', 'Saskatchewan', 'Alberta','Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia','Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta', 'Quebec', 'Manitoba','Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta','Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta', 'Saskatchewan','New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta','Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta', 'Ontario', 'Saskatchewan', 'Alberta', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Alberta', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador','Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick','New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundlandand Labrador', 'New Brunswick', 'Quebec', 'Alberta', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec','Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'NewBrunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba','Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick','Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta','Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta', 'Quebec', 'Alberta', 'Ontario', 'Alberta', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec','British Columbia', 'Ontario', 'Alberta', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador','Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta', 'New Brunswick','Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut','Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta', 'Quebec', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan','Quebec', 'Nunavut', 'Alberta', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec','Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec','Alberta', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'BritishColumbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta', 'Nova Scotia Wide']
    
    query_relaxation_tags = []
    
    # print('class_tag_mapping',class_tag_mapping)
    canada_cities = list(map(lambda x: x.lower() ,canada_cities))

    if 'Location' in class_tag_mapping:
        for loc_tag in class_tag_mapping['Location']:
            if loc_tag in canada_cities: 
                index = canada_cities.index(loc_tag)
                query_relaxation_tags.append(canada_city_proviences[index])
                tags_params.append((canada_city_proviences[index], 'Location'))
            else:
                similar_tags = difflib.get_close_matches(loc_tag, canada_cities, n=2, cutoff=0.9)
                if len(similar_tags) > 0:
                    index = canada_cities.index(similar_tags[0])
                    query_relaxation_tags.append(canada_city_proviences[index])
                    tags_params.append((canada_city_proviences[index], 'Location'))
                else:
                    similar_tags = difflib.get_close_matches(loc_tag, canada_city_proviences, n=2, cutoff=0.60)
                    if len(similar_tags) > 0:
                        query_relaxation_tags.append(similar_tags[0])
                        tags_params.append((similar_tags[0], 'Location'))

        
    #adding obvious location tags
    query_relaxation_tags.append('World-wide')
    query_relaxation_tags.append('All Canada')
    # queryset = queryset.exclude(tags__name__in=canada_cities)
    tags_params_mapped = list(map(lambda x: x[0] ,tags_params))

    tags_params_mapped = set(tags_params_mapped)
    tags_params_mapped.update(should_be_added)
    tags_params_mapped = tags_params_mapped.difference(should_be_romoved)

    if vip_tags:
        resQueryset = resQueryset.filter(Q(tags__name__in=vip_tags) & (Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags)))
    else:
        resQueryset = resQueryset.filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))



    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id').all()
    query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))

    #retrieve tag ids from tag names
    tags = Tag.objects.filter(name__in=tags_params_mapped).values('id','tag_category').all()
    tags_id_list = list(map(lambda x: x['id'], tags))
    tags_cat_list = list(map(lambda x: x['tag_category'], tags))

    
    
    
    # input_lo_format_infot_servt_mh_cost_au_lang
    # scoring and ordering by scores
    resource_scores = {}
    res_counter = 0
    for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], resQueryset)):
        resource_scores[resource[0]] = [0,0,0,0,0,0,0,0]
        if resource[1] is None or resource[1]=='':
            resource_scores[resource[0]] = 0
            continue

        index = json.loads(resource[1])
        original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
        original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
        
        for i, tag in enumerate(tags_id_list):
            t_cat = tags_cat_list[i]

            tag = str(tag)
            if tag in index:
                if t_cat=="Location":
                    resource_scores[resource[0]][0] += index[tag]
                elif t_cat=="Resource format":
                    resource_scores[resource[0]][1] += index[tag]
                elif t_cat=="Resource Type for Education/Informational":
                    resource_scores[resource[0]][2] += index[tag]
                elif t_cat=="Resource Type for Programs and Services":
                    resource_scores[resource[0]][3] += index[tag]
                elif t_cat=="Health Issue":
                    resource_scores[resource[0]][4] += index[tag]
                elif t_cat=="Costs":
                    resource_scores[resource[0]][5] += index[tag]
                elif t_cat=="Audience":
                    resource_scores[resource[0]][6] += index[tag]
                elif t_cat=="Language":
                    resource_scores[resource[0]][7] += index[tag]

                
            if tag in original_tag_ids:
                i = original_tag_ids.index(tag)

                if original_tag_categories[i] == 'Location':
                    resource_scores[resource[0]][0] += 10
                elif original_tag_categories[i] == 'Resource format':
                    resource_scores[resource[0]][1] += 10
                elif original_tag_categories[i] == 'Resource Type for Education/Informational':
                    resource_scores[resource[0]][2] += 10
                elif original_tag_categories[i] == 'Resource Type for Programs and Services':
                    resource_scores[resource[0]][3] += 10
                elif original_tag_categories[i] == 'Health Issue':
                    resource_scores[resource[0]][4] += 10
                elif original_tag_categories[i] == 'Costs':
                    resource_scores[resource[0]][5] += 10
                elif original_tag_categories[i] == 'Audience':
                    resource_scores[resource[0]][6] += 10
                elif original_tag_categories[i] == 'Language':
                    resource_scores[resource[0]][7] += 10
                
                

        for i,original_tag_id in enumerate(original_tag_ids):
            if original_tag_id in query_relaxation_tags_id:
                #for query relaxation
                if original_tag_categories[i] == 'Location':
                    resource_scores[resource[0]][0] += 1
                

        resource_scores[resource[0]] = cos(torch.FloatTensor(input_lo_format_infot_servt_mh_cost_au_lang), torch.FloatTensor(resource_scores[resource[0]])).numpy()*10

        # print(resource_scores[resource[0]])

        #tags_params_mapped = string value of tags
        for tag in tags_params_mapped:
            if len(tag)<2:
                continue

            if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.1
            
            if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.1
            
            
            if (tag == 'Informational Website') and (resource[4] == 'RS' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 5
            elif (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 5

            if (tag == 'Definition') and (resource[5]):
                resource_scores[resource[0]] += 1

            if (tag == 'Domestic Violence') and ("sheltersafe" in resource[3].lower()):
                resource_scores[resource[0]] += 0.2

            if (tag == 'Therapist/Counsellor/Psychotherapist') and ("counsel" in resource[3].lower()):
                resource_scores[resource[0]] += 0.2

            sum_tag = ""
            for w in tag.replace("-", " ").split(" "):
                if len(w)>0: sum_tag += w[0]
            if (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                resource_scores[resource[0]] += 0.2
        
        res_counter+=1


    topitems = heapq.nlargest(15, resource_scores.items(), key=itemgetter(1))

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
                number_of_filters = [tqs for tqs in tags_params_mapped if (tqs in tagsQuerySet) or (tqs+"\xa0" in tagsQuerySet)]
                qs.index = number_of_filters
                qs.score = topitemsasdict[qs.id] + len(number_of_filters)

        return newQuerySet


    return resQueryset


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
            "Let me see if I've gotten this right...",
            "I want to make sure I understand...",
            "Okay, I think I understand what you're feeling...",
            "I am doing my best to understand how you are feeling but I am still unsure...",
            "I'm still shaky on the details can you explain more....",
            "Right now I am only able to understand a few details can you give me more..."
        ],
        "response_to_neg_feelings": [ # response 
            "That must be hard.",
            "I can detect that must be hard.",
            "I think anyone would feel bad too in the same situation.",
            "I can see how that would be difficult.",
            "That sounds very challenging.",
            "That sounds difficult.",
            "I am sorry that is happening.",
            "That can't be easy to sit with.",
            "I'm sorry that is happening.",
            "That's a troubling though.",
            "I value your thoughts.",
            "Your words are safe with me.",
        ],
        "response_to_pos_feelings": [ # response 
            "I support your position here.",
            "That seems like a good thing.",
            "I'm glad you told me.",
            "That seems good.",
            "Feeling that way could be good.",
            "Seems like that could make things easier.",
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
                if(num_run_eliza<2):
                    emotion_des = clarification_sentence\
                    + "I can detect you feel happy. "
                else:
                    emotion_des = "I am here for you. "
        elif (detected_emotion['label']=="sadness"):
            emotion_des = emotion_response_neg_sentence
            if (detected_emotion['score']<0.5):
                if(num_run_eliza<2):
                    emotion_des = clarification_sentence\
                    + "I can detect you are sad."
                else:
                    emotion_des = "Your words are valued with me. "
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
                'decomp': '* sorry *',
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
                    "There is no need to apologize, you're okay.",
                    "Apologies are not necessary. Tell me more about your feelings",
                    "What feelings do you have about this?",
                ],
            },
            {#example: I am sorry about X
                'key': 'i am sorry',
                'decomp': '* i am sorry *',
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
                    "There is no need to apologize, let's move on.",
                    "Apologies are not necessary.",
                    "what do you think caused being sorry (2) ?",
                    "what do you think made you feel sorry (2) ?"
                ],
            }
            ,{#example: I also remember X
                'key': 'i also remember',
                'decomp': '*i also remember *',
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
                    "What else do you recollect?",
                    "What in the present situation reminds you of (2)?"
                ],
            },{ #example: I remember X
                'key': 'i remember',
                'decomp': '*i remember *',
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
                'decomp': '*do you remember *',
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
                'decomp': '* if *',
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
                'decomp': '*i dreamed *',
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
                'decomp': '* dream *',
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
                'decomp': '*perhaps *',
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
                'decomp': '@hello',
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
                'decomp': '* computer *',
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
                'decomp': 'am i *',
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
                'decomp': 'are you *',
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
                'decomp': '* they are *',
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
                'decomp': '* you are *',
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
                'decomp': '* your *',
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
                'decomp': 'was i *',
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
                'decomp': 'i was *',
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
                'decomp': 'were you *',
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
                'decomp': 'i @desire *',
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
                'decomp': 'i @desire is *',
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
                'decomp': 'i am * @sad *',
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
                'decomp': 'i am * @happy *',
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
                'decomp': '@i * @belief *', 
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
                'decomp': 'i am *',
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
                'decomp': 'i @cannot *',
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
                'decomp': "i don't *",
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
                'decomp': "i feel *",
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
                    "Tell me more about your feelings about this.",
                    "Do you often feel (1)?",
                    "Do you enjoy feeling (1)?",
                    "Of what does feeling (1) remind you?"
                ],
            },{ # i think i am not prepared for it
                'key': 'every thing',
                'decomp': '*',
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
                    "I'm sorry, I'm not sure what you mean by (1)",
                    "Let's discuss further. Tell me more.",
                    "Can you elaborate on that ?",
                    "Let's discuss further. Tell me more about that.",
                    "what does that suggest to you?"
                ]
            },{ # i think i am not prepared for it
                'key': 'and',
                'decomp': '* and *',
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
                    "Let`s discuss further. Tell me more about that.",
                ],
                'reasmb_dynamic_neutral':
                [
                    "Do you wana talk more about (2)",
                    "I wana talk more why (2)",
                    "I want to know why (2)",
                ]
            },
            { # you are very funny
                'key': 'you are',
                'decomp': "you are *",
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
                'decomp': "yes",
                'reasmb_neutral': 
                [
                    "great. Let`s discuss further. Tell me more about that?",
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
                    "I see. Let`s discuss further. Can you please provide more information that I can help you with?"
                ]
            },{ # no  
                'key': 'no',
                'decomp': "no",
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
                'decomp': "* my *",
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
                'decomp': "* my * @family *",
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
                'decomp': "can you *",
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
                'decomp': "can i *",
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
                'decomp': "what *",
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
                'decomp': "*because *",
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
                'decomp': "why don't you *",
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
                'decomp': "*why can't i *",
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
                'decomp': "*@everyone *",
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
                'decomp': "*always*",
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
            },{ # they dressed alike in black trousers and jackets.
                'key': 'alike',
                'decomp': "* alike *",
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
                'decomp': "* @be * like *",
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
                'decomp': "* @makes me @anxiety",
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
                'decomp': "* @anxiety * @because *",
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
                'decomp': "* @anxiety @because *",
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
                'decomp': "* my @job *",
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
                'decomp': "* told me *",
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
            }
        ]
    }
    # return best rules from options provided
    def calculate_cosine_simillarity_with_rule_keys(user_input, decomposition_rules):
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
                # print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[0], cosine_scores[i][0]))
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
            return replace_decomp_with_syns(decomp.replace('@'+reg, '('+'|'.join(find_syns(reg))+')'))
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
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return ResourceByIntentEntityViewQuerySet_new(self.request.query_params)

class ResourceByIntentEntityView_new_new(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return ResourceByIntentEntityViewQuerySet_new_new(self.request.query_params)

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
        return ResourceViewQuerySet(self.request.query_params)


class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Only approved tags?? Waiting for client confirmation
        # TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.filter(approved=True).order_by('name')


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

def get_relations_by_tag(request):
    data = json.loads(request.body)
    tag_id = data['tag_id']
    relationships = TagRelationship.objects.filter(tag_id=tag_id)
    response = []
    for relation in relationships:
        response.append({'id':relation.id,'parent':relation.parent})
    return JsonResponse(response, safe=False)

def add_tag_relation(request):
    data = json.loads(request.body)
    tag_id = data['tag_id']
    parent_id = data["parent_id"]
    relation = TagRelationship(parent_id = parent_id, tag_id = tag_id)
    relation.save()
    return JsonResponse({})

def get_tag_group_stats(request):
    tag_groups = {
        'Indigenous':['Indigenous', 'Indigenous Women', 'Inuit', 'Mأ©tis'],
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