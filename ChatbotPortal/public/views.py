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
from .serializers import ResourceSerializer, TagSerializer, CategorySerializer, RetrievePublicResourceSerializer
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
    queryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved"))

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

        # calculating which tags should be excluded
        canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-d’Or', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'L’Assomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'L’Ancienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'L’Île-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'L’Epiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'L’Islet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-d’Urfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort Qu’Appelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L’ Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'L’Avenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayer’s Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen',]
        canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick', 'Ontario', 'British Columbia', 'Ontario', 'Alberta Wide', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta Wide', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta Wide', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince Edward Island', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta Wide', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'British Columbia', 'Quebec', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario', 'Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Nova Scotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta Wide', 'Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Ontario', 'British Columbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba', 'British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta Wide', 'Prince Edward Island', 'British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta Wide', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Manitoba', 'Quebec', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'British Columbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta Wide', 'Ontario', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide', 'Quebec', 'British Columbia', 'Ontario', 'Alberta Wide', 'Ontario', 'Prince Edward Island', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta Wide', 'Ontario', 'New Brunswick', 'Alberta Wide', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'Nova Scotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Alberta Wide', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick', 'Alberta Wide', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta Wide', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta Wide', 'Ontario', 'Ontario', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'New Brunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta Wide', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia', 'Alberta Wide', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'New Brunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Alberta Wide', 'Manitoba', 'Ontario', 'Alberta Wide', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta Wide', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'British Columbia', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'New Brunswick', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'British Columbia', 'Manitoba', 'Manitoba', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'Nova Scotia', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Alberta Wide', 'Newfoundland and Labrador', 'Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta Wide', 'Newfoundland and Labrador', 'Alberta Wide', 'Alberta Wide', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'British Columbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'Alberta Wide', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia', 'Saskatchewan', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta Wide', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'British Columbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta Wide', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'Newfoundland and Labrador', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince Edward Island', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Alberta Wide', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'Prince Edward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta Wide', 'Manitoba', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'New Brunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Saskatchewan', 'Quebec', 'Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon', 'Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta Wide', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta Wide', 'Quebec', 'Manitoba', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta Wide', 'Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta Wide', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador', 'Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba', 'Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta Wide', 'Quebec', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia', 'Ontario', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut', 'Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan', 'Quebec', 'Nunavut', 'Alberta Wide', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec', 'Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta Wide', ]
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

        topitems = heapq.nlargest(25, resource_scores.items(), key=itemgetter(1))
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
    else:
        tag_categories = {
            'health':['Addict', 'stress', 'depressed', 'anxious'], 
            'family':['son', 'wife', 'husband', 'daughter'], 
            'canada':['Alberta', 'Scotia', 'Edmonton']
            }
        
        
        
        search_params = query_params.get('search')
        imp_words = find_keywords_of_sentence(search_params)

        if not imp_words:
            return queryset

        categories = set()
        imp_word_mapping = {}
        for imp_word in imp_words:
            # classifier = pipeline("zero-shot-classification", model='cross-encoder/nli-roberta-base')
            # # sent = "Apple just announced the newest iPhone X"
            # # todo retrieve location
            # candidate_labels = ["health", "family"]
            # res = classifier(imp_word, candidate_labels)

            # print(res)

            # health_score = res['scores'][res['labels'].index("health")]
            # family_score = res['scores'][res['labels'].index("family")]

            # most_related_health_issue = ""
            # if health_score > family_score and health_score > 0.60:
            most_related_health_issue = travel_mh_kg(imp_word)

            # else:
            #     continue

            imp_word_mapping[imp_word] = {'category':'Health Issue'}
            categories.add('Health Issue')

            print('most_related_health_issue', most_related_health_issue)
        
        print('categories', categories)
        approved_tags = Tag.objects.filter(approved=1).filter(tag_category__in=categories).values('name','id','tag_category').all()
        approved_tag_names = list(map(lambda x: x['name'], approved_tags))

        actual_tags = []
        probable_tags = {}

        for imp_word in imp_word_mapping:
            similar_tags = difflib.get_close_matches(imp_word, approved_tag_names, n=2, cutoff=0.61)
            if similar_tags:
                for t in similar_tags: actual_tags.append(t)
            for app_tag in approved_tags:
                if imp_word_mapping[imp_word]['category'] == app_tag['tag_category']:
                    if app_tag['name'] not in probable_tags:
                        probable_tags[app_tag['name']] = 0
                    if list(filter(lambda x: x.pos() =='n' ,wordnet.synsets(app_tag['name'], pos='n'))) and list(filter(lambda x: x.pos() =='n' ,wordnet.synsets(imp_word, pos='n'))):
                        probable_tags[app_tag['name']] += float(wordnet.path_similarity(list(filter(lambda x: x.pos() =='n' ,wordnet.synsets(imp_word, pos='n')))[0], list(filter(lambda x: x.pos() =='n' ,wordnet.synsets(app_tag['name'], pos='n')))[0], simulate_root=True))


        # actual_tags
        probable_tags = list(map(lambda x: x[0], filter(lambda x: x[1]>0, probable_tags.items())))

        ids = list(map(lambda x: x.id ,queryset))
        queryset_ = Resource.objects.filter(Q(tags__name__in=actual_tags) | Q(tags__name__in=probable_tags) | Q(id__in=ids))


        tag_list = set()
        for probable_tag in probable_tags: tag_list.add(probable_tag)
        for actual_tag in actual_tags: tag_list.add(actual_tag)

        tagg = Tag.objects.filter(name__in=tag_list)
        tag_list = list(map(lambda x: str(x.id) ,tagg))

        # scoring and ordering by scores
        resource_scores = {}
        for resource in list(map(lambda x: [x.id,x.index, list(x.tags.all()), x.title], queryset_)):
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

        topitems = heapq.nlargest(20, resource_scores.items(), key=itemgetter(1))
        
        topitemsasdict = dict(topitems)
        if len(topitems) > 1:
            queryset_ = queryset_.filter(id__in=topitemsasdict.keys())
            
            thisSet = []
            #make result distinct
            for query in queryset_:
                if query.id not in thisSet:
                    thisSet.append(query.id)
            newQuerySet_ = Resource.objects.filter(id__in=thisSet)

            for qs in newQuerySet_:
                qs.portal_search_rcmnd_count += 1
                qs.save()
                if qs.id not in topitemsasdict.keys():
                    qs.score = 0
                else:
                    qs.score = topitemsasdict[qs.id]


            newQuerySet_.order_by('score')
            return newQuerySet_


    return queryset


def calculateCountsForResources(query_params):
    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved"))
    
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
    ,'generalized anxiety disorder': 'Anxiety'
    ,'generalized anxiety disorder': 'General public/all'
    ,'generalized anxiety disorder': 'Stress'
    ,'generalized anxiety disorder': 'Depression'
    ,'health professional':'Psychologist'
    ,'health professional':'Family Doctor'
    ,'alberta':'Alberta Wide'
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
    ,'crisis_distress_support':'Crisis Support/Distress Counselling'
    }

    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))
    # tags_params = list(map(lambda x: (x[:x.index("(")], x[x.index("(")+1:-1]) ,tags_params))

    tags_params = list(map(lambda x: x[:x.index("(")] ,tags_params))


    all_possible_tags = Tag.objects.filter(approved=1).all()
    all_possible_tags = list(map(lambda x: x.name, all_possible_tags))

    should_be_romoved = set()
    should_be_added = set()
    #query matching with simillar words
    for tag_param in tags_params:
        if tag_param in all_possible_tags:
            continue
        else:
            if tag_param.lower() in word_mapping.keys():
                should_be_romoved.add(tag_param)
                for related_word in filter(lambda x: x[0] == tag_param.lower() ,word_mapping.items()):
                    should_be_added.add(related_word[1])
            else:
                similar_tags = difflib.get_close_matches(tag_param.lower(), all_possible_tags, n=2, cutoff=0.61)
                if len(similar_tags) > 0:
                    should_be_romoved.add(tag_param)
                    should_be_added.add(similar_tags[0])
    
    tags_params = set(tags_params)
    tags_params.update(should_be_added)
    tags_params.difference(should_be_romoved)

    #query relaxation 
    canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-d’Or', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'L’Assomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'L’Ancienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'L’Île-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'L’Epiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'L’Islet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-d’Urfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort Qu’Appelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L’ Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'L’Avenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayer’s Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen',]
    canada_city_proviences = ['Ontario', 'Quebec', 'British Columbia', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Ontario', 'Quebec', 'Nova Scotia', 'Ontario', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec', 'British Columbia','Saskatchewan', 'British Columbia', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'British Columbia', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia','Quebec', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Ontario', 'New Brunswick','Ontario', 'British Columbia', 'Ontario', 'Alberta Wide', 'British Columbia', 'Ontario', 'NovaScotia', 'Alberta Wide', 'Quebec', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'BritishColumbia', 'Quebec', 'Quebec', 'Ontario', 'British Columbia', 'British Columbia', 'BritishColumbia', 'Ontario', 'Ontario', 'British Columbia', 'Ontario', 'Ontario', 'Alberta Wide','British Columbia', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'Alberta Wide','Quebec', 'Alberta Wide', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'British Columbia', 'Quebec', 'Ontario', 'Prince EdwardIsland', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Ontario', 'Ontario','Saskatchewan', 'British Columbia', 'Ontario', 'British Columbia', 'Alberta Wide','Saskatchewan', 'British Columbia', 'British Columbia', 'Ontario', 'British Columbia', 'Quebec','Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'British Columbia', 'Quebec', 'Alberta Wide','Quebec', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'Quebec', 'Yukon', 'Ontario', 'Ontario','Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Newfoundland andLabrador', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'NovaScotia', 'Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Alberta Wide', 'Ontario', 'Newfoundland and Labrador', 'New Brunswick', 'Alberta Wide','Quebec', 'Northwest Territories', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'BritishColumbia', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Ontario', 'BritishColumbia', 'Ontario', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'British Columbia', 'British Columbia', 'Quebec', 'New Brunswick','Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Ontario', 'British Columbia', 'British Columbia', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario','Saskatchewan', 'New Brunswick', 'Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Manitoba','British Columbia', 'Manitoba', 'Quebec', 'Ontario', 'Alberta Wide', 'Prince Edward Island','British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Ontario', 'Ontario', 'Alberta Wide', 'Saskatchewan', 'Ontario', 'Quebec', 'Alberta Wide', 'Ontario', 'Manitoba', 'Quebec','Alberta Wide', 'Ontario', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario', 'BritishColumbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Alberta Wide', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Ontario', 'Quebec', 'Ontario', 'NovaScotia', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Alberta Wide', 'Ontario', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'British Columbia','Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Manitoba', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Newfoundland and Labrador', 'British Columbia', 'NewBrunswick', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan', 'Quebec', 'Ontario','Ontario', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Quebec','Quebec', 'British Columbia', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Quebec', 'New Brunswick', 'British Columbia', 'British Columbia', 'Nova Scotia','Nova Scotia', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide','Quebec', 'British Columbia', 'Ontario', 'Alberta Wide', 'Ontario', 'Prince Edward Island','Ontario', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Ontario', 'Quebec', 'Ontario','Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec', 'Alberta Wide', 'Ontario', 'NewBrunswick', 'Alberta Wide', 'Ontario', 'Manitoba', 'Ontario', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Ontario','Manitoba', 'Ontario', 'Saskatchewan', 'British Columbia', 'Nova Scotia', 'Manitoba', 'Quebec','Alberta Wide', 'Ontario', 'Alberta Wide', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Alberta Wide', 'Newfoundland and Labrador', 'Ontario', 'British Columbia', 'Ontario', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'NovaScotia', 'Newfoundland and Labrador', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec','Manitoba', 'Ontario', 'Ontario', 'Nunavut', 'Ontario', 'Quebec', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Ontario', 'Ontario','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Alberta Wide','Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','British Columbia', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec','Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Alberta Wide','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Ontario', 'New Brunswick','Alberta Wide', 'Quebec', 'Quebec', 'Nova Scotia', 'Alberta Wide', 'Ontario', 'Newfoundland andLabrador', 'Ontario', 'Alberta Wide', 'Nova Scotia', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'Ontario', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'BritishColumbia', 'Manitoba', 'New Brunswick', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'BritishColumbia', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Saskatchewan', 'Alberta Wide','Alberta Wide', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec','Alberta Wide', 'Ontario', 'Ontario', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'Alberta Wide', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'NewBrunswick', 'New Brunswick', 'Ontario', 'Newfoundland and Labrador', 'Ontario', 'Alberta Wide','Quebec', 'British Columbia', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','Saskatchewan', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'New Brunswick', 'British Columbia','Alberta Wide', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario', 'Quebec','Manitoba', 'Nova Scotia', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick', 'Quebec','Ontario', 'British Columbia', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Manitoba', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'British Columbia','Ontario', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'British Columbia', 'Saskatchewan','Alberta Wide', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Quebec', 'Ontario', 'Ontario','Manitoba', 'Quebec', 'Saskatchewan', 'New Brunswick', 'British Columbia', 'Ontario','Newfoundland and Labrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'New Brunswick', 'New Brunswick', 'BritishColumbia', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba', 'Nova Scotia', 'Nova Scotia', 'NewBrunswick', 'British Columbia', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Ontario','Quebec', 'Quebec', 'Alberta Wide', 'Manitoba', 'Ontario', 'Alberta Wide', 'Quebec','Newfoundland and Labrador', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'Quebec', 'Quebec','New Brunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'Ontario', 'Ontario', 'NewBrunswick', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'British Columbia', 'Alberta Wide','Ontario', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'BritishColumbia', 'British Columbia', 'British Columbia', 'Alberta Wide', 'Quebec', 'Ontario', 'BritishColumbia', 'Ontario', 'Nova Scotia', 'Alberta Wide', 'New Brunswick', 'Nova Scotia', 'BritishColumbia', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'British Columbia','Manitoba', 'Manitoba', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'New Brunswick', 'British Columbia', 'Quebec','Ontario', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador', 'Manitoba','Manitoba', 'Newfoundland and Labrador', 'Quebec', 'British Columbia', 'New Brunswick','Manitoba', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Ontario', 'New Brunswick', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Northwest Territories', 'Quebec', 'British Columbia', 'Ontario', 'Manitoba', 'NovaScotia', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nova Scotia','Saskatchewan', 'Ontario', 'Alberta Wide', 'Alberta Wide', 'Newfoundland and Labrador','Manitoba', 'Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec','Manitoba', 'Quebec', 'Saskatchewan', 'British Columbia', 'Quebec', 'New Brunswick', 'Ontario','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Ontario', 'Ontario','Quebec', 'Newfoundland and Labrador', 'British Columbia', 'Ontario', 'Alberta Wide','Newfoundland and Labrador', 'Alberta Wide', 'Alberta Wide', 'British Columbia', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Ontario', 'New Brunswick','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Newfoundland and Labrador','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Nunavut', 'Saskatchewan', 'BritishColumbia', 'British Columbia', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec','Alberta Wide', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Ontario', 'Saskatchewan','Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'British Columbia','Alberta Wide', 'Ontario', 'Nunavut', 'Quebec', 'Ontario', 'Newfoundland and Labrador', 'NewBrunswick', 'Quebec', 'British Columbia', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Ontario', 'British Columbia','Saskatchewan', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'Alberta Wide', 'NorthwestTerritories', 'Quebec', 'Quebec', 'Ontario', 'Nova Scotia', 'Quebec', 'New Brunswick', 'Quebec','Quebec', 'Saskatchewan', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Saskatchewan','Ontario', 'Quebec', 'Nova Scotia', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Manitoba', 'Quebec', 'British Columbia', 'New Brunswick', 'Manitoba','Ontario', 'Ontario', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Alberta Wide','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario','Quebec', 'New Brunswick', 'New Brunswick', 'Quebec', 'British Columbia', 'Ontario', 'BritishColumbia', 'Newfoundland and Labrador', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick','Saskatchewan', 'British Columbia', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec','Quebec', 'Nova Scotia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Nova Scotia', 'Alberta Wide','British Columbia', 'Quebec', 'Newfoundland and Labrador', 'Quebec', 'Saskatchewan', 'NewBrunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Quebec', 'Newfoundland andLabrador', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'Newfoundlandand Labrador', 'New Brunswick', 'Manitoba', 'Saskatchewan', 'Saskatchewan', 'New Brunswick','Newfoundland and Labrador', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'Newfoundland and Labrador', 'Alberta Wide', 'Ontario', 'Quebec', 'Quebec','British Columbia', 'Quebec', 'Quebec', 'Nunavut', 'British Columbia', 'Newfoundland andLabrador', 'Quebec', 'British Columbia', 'Nova Scotia', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba','Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Manitoba', 'Newfoundland and Labrador','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide', 'New Brunswick', 'Ontario','British Columbia', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'British Columbia', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Ontario', 'Quebec', 'New Brunswick','Quebec', 'Alberta Wide', 'Ontario', 'Ontario', 'Quebec', 'New Brunswick', 'Prince EdwardIsland', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec','Saskatchewan', 'Ontario', 'Ontario', 'Saskatchewan', 'British Columbia', 'Saskatchewan','Alberta Wide', 'Saskatchewan', 'New Brunswick', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'BritishColumbia', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Northwest Territories', 'Quebec','Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Nova Scotia', 'New Brunswick', 'Saskatchewan', 'Saskatchewan','Saskatchewan', 'Newfoundland and Labrador', 'Quebec', 'Quebec', 'Alberta Wide', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'NewBrunswick', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'Ontario', 'Alberta Wide','Quebec', 'Quebec', 'Saskatchewan', 'Nunavut', 'Quebec', 'Ontario', 'Quebec', 'Quebec','Manitoba', 'Ontario', 'Quebec', 'Quebec', 'Nova Scotia', 'Quebec', 'Manitoba', 'New Brunswick','New Brunswick', 'British Columbia', 'New Brunswick', 'Quebec', 'Newfoundland and Labrador','Quebec', 'British Columbia', 'Quebec', 'British Columbia', 'Manitoba', 'Ontario', 'Quebec','Saskatchewan', 'New Brunswick', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'NewBrunswick', 'Newfoundland and Labrador', 'Nunavut', 'Manitoba', 'British Columbia', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Manitoba', 'Quebec', 'Ontario', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Ontario', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Newfoundland andLabrador', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba', 'Saskatchewan', 'Manitoba', 'PrinceEdward Island', 'Newfoundland and Labrador', 'Nunavut', 'British Columbia', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'British Columbia','Newfoundland and Labrador', 'British Columbia', 'Quebec', 'New Brunswick', 'Quebec', 'NewBrunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'New Brunswick', 'Quebec','British Columbia', 'Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Quebec', 'Alberta Wide', 'NewBrunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick', 'Alberta Wide', 'Manitoba', 'Alberta Wide', 'Quebec', 'Saskatchewan', 'Manitoba', 'Ontario','Saskatchewan', 'British Columbia', 'Quebec', 'British Columbia', 'Quebec', 'Newfoundland andLabrador', 'Saskatchewan', 'Saskatchewan', 'New Brunswick', 'Nunavut', 'Quebec', 'NewBrunswick', 'Quebec', 'Nunavut', 'Quebec', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'NewBrunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'British Columbia','Quebec', 'British Columbia', 'Quebec', 'Quebec', 'New Brunswick', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Saskatchewan', 'Quebec','Nunavut', 'Ontario', 'Ontario', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Ontario', 'Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Quebec', 'Alberta Wide','Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Newfoundland and Labrador','Ontario', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Saskatchewan', 'New Brunswick', 'BritishColumbia', 'New Brunswick', 'Saskatchewan', 'Quebec', 'New Brunswick', 'Quebec', 'Yukon','Quebec', 'Quebec', 'Nova Scotia', 'British Columbia', 'Manitoba', 'Saskatchewan', 'NovaScotia', 'Quebec', 'Manitoba', 'New Brunswick', 'Alberta Wide', 'Saskatchewan', 'Alberta Wide','Quebec', 'Quebec', 'Quebec', 'New Brunswick', 'Manitoba', 'Manitoba', 'British Columbia','Quebec', 'Ontario', 'Quebec', 'Quebec', 'British Columbia', 'Quebec', 'Ontario','Saskatchewan', 'British Columbia', 'Nunavut', 'Quebec', 'Alberta Wide', 'Quebec', 'Manitoba','Newfoundland and Labrador', 'Quebec', 'New Brunswick', 'New Brunswick', 'Alberta Wide','Newfoundland and Labrador', 'Saskatchewan', 'New Brunswick', 'Alberta Wide', 'Saskatchewan','New Brunswick', 'Quebec', 'Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'Quebec','Quebec', 'Quebec', 'British Columbia', 'New Brunswick', 'Ontario', 'Quebec', 'Alberta Wide','Quebec', 'Saskatchewan', 'Manitoba', 'Quebec', 'Ontario', 'New Brunswick', 'Ontario', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Manitoba', 'Quebec', 'Saskatchewan', 'Quebec', 'Manitoba','Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Quebec', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Quebec','Saskatchewan', 'Saskatchewan', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Manitoba', 'Alberta Wide', 'Ontario', 'Saskatchewan', 'Alberta Wide', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec','Quebec', 'Alberta Wide', 'Nova Scotia', 'British Columbia', 'Newfoundland and Labrador','Northwest Territories', 'Quebec', 'Quebec', 'Ontario', 'Ontario', 'Manitoba', 'New Brunswick','New Brunswick', 'Quebec', 'Newfoundland and Labrador', 'Nova Scotia', 'Manitoba', 'Newfoundlandand Labrador', 'New Brunswick', 'Quebec', 'Alberta Wide', 'Manitoba', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Manitoba', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Manitoba', 'Quebec', 'Quebec', 'Ontario', 'New Brunswick', 'Saskatchewan', 'Quebec','Saskatchewan', 'Quebec', 'Saskatchewan', 'Quebec', 'Saskatchewan', 'Prince Edward Island', 'NewBrunswick', 'Quebec', 'Quebec', 'Newfoundland and Labrador', 'Prince Edward Island', 'Manitoba','Quebec', 'British Columbia', 'Saskatchewan', 'Ontario', 'Quebec', 'Ontario', 'Quebec', 'NewBrunswick', 'New Brunswick', 'Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'New Brunswick','Nova Scotia', 'Manitoba', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Alberta Wide','Newfoundland and Labrador', 'Ontario', 'Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario','Saskatchewan', 'Ontario', 'Saskatchewan', 'Ontario', 'Quebec', 'Saskatchewan', 'Quebec','Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'New Brunswick', 'Ontario', 'British Columbia', 'Quebec', 'Quebec', 'Quebec','Quebec', 'Quebec', 'Saskatchewan', 'British Columbia', 'Alberta Wide', 'Quebec', 'Alberta Wide', 'Ontario', 'Alberta Wide', 'Nunavut', 'Quebec', 'Ontario', 'Saskatchewan', 'Quebec','British Columbia', 'Ontario', 'Alberta Wide', 'New Brunswick', 'Quebec', 'Quebec','Saskatchewan', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Newfoundland and Labrador','Quebec', 'Saskatchewan', 'Saskatchewan', 'Nova Scotia', 'Saskatchewan', 'New Brunswick','Saskatchewan', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Alberta Wide', 'New Brunswick','Quebec', 'New Brunswick', 'Quebec', 'Quebec', 'Quebec', 'Ontario', 'Quebec', 'Nunavut','Quebec', 'Prince Edward Island', 'Saskatchewan', 'Ontario', 'Alberta Wide', 'Quebec', 'Quebec','Manitoba', 'New Brunswick', 'Quebec', 'Saskatchewan', 'Quebec', 'Nova Scotia', 'Saskatchewan','Quebec', 'Nunavut', 'Alberta Wide', 'Quebec', 'Prince Edward Island', 'Ontario', 'Quebec','Manitoba', 'Saskatchewan', 'New Brunswick', 'New Brunswick', 'British Columbia', 'Quebec','Alberta Wide', 'Quebec', 'Quebec', 'Saskatchewan', 'Ontario', 'Ontario', 'Quebec', 'BritishColumbia', 'Ontario', 'Quebec', 'Quebec', 'Quebec', 'Saskatchewan', 'Saskatchewan', 'Alberta Wide', ]
    
    query_relaxation_tags = []
    location_tags = Tag.objects.filter(name__in=tags_params).values('name').all()
    query_relaxation_tags = list(map(lambda x: x['name'], location_tags))
    for tag in location_tags:
        tag = tag['name']
        if tag in canada_cities:         
            index = canada_cities.index(tag)
            query_relaxation_tags.append(canada_city_proviences[index])
            canada_cities.pop(index)
            canada_city_proviences.pop(index)
        
    #adding obvious location tags
    # query_relaxation_tags.append('World-wide')
    # query_relaxation_tags.append('All Canada')
    # queryset = queryset.exclude(tags__name__in=canada_cities)

    resQueryset = resQueryset.filter(Q(tags__name__in=tags_params) | Q(tags__name__in=query_relaxation_tags))
    

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

    res = count_tags(found_resources, True)
    
    # if len(res) < 2:
    #     res = count_tags(found_resources, True)
    


    kg = {
        'START':['Legal', 'Chronic Pain', 'Cancer', 'Human Immunodeficiency Virus (HIV)', 'Acquired Immune Deficiency Syndrome (AIDS)', 'COVID-19', 'Treatments', 'Traditional Indigenous Health'],

        'Legal':['Abuse', 'Corrections', 'Reconciliation', 'Human Trafficking', 'Harrassment'],
        'Abuse':['Domestic Violence', 'Sexual Violence', "Men's abuse"],
        'Treatments':['Medication Treatment', 'Psychotherapies', 'Interventional Psychiatric Treatments'],
        'Medication Treatment': ['Anticonvulsants', 'Anti-psychotics', 'Anti-depressants', 'Benzodiapines (Tranquilizers)', 'Psychedelics/Hallucinogens'],
        'Psychotherapies':['Family Therapy', 'Dialectical Behavioural Therapy', 'Cognitive Behavioural Therapy', 'Group Therapy', 'Aversion Therapy', 'Exposure Therapy', 'Cognitive Behavioural Play Therapy', 'Interpersonal Therapy', 'Art and Pet Therapy', 'Applied behavioural analysis', 'Mentalization-Based Therapy', 'Psychodynamic Psychotherapy', 'Psychoeducation'],
        'Interventional Psychiatric Treatments':['Electroconvulsive Therapy', 'Repetitive Transcranial Magnetic Stimulation', 'Magnetic Seizure Therapy', 'Smoking Cessation', 'Harm-Reduction'],
        'Psychedelics/Hallucinogens': ['MDMA/Ecstasy', 'Ketamine', 'LSD', 'Psilocybin'],
        'Stigma':['Prejudice', 'Discrimination', 'Self-stigma'],
        'Social Support Services':['Workplace', 'Housing', 'Financial and Employment'],
        'Life Transitions and Support/Skills': ['Interpersonal Relationships', 'Parenting', 'Adjustment disorders', 'Separation and Divorce'],
        'General distress':['Grief and Bereavement', 'Burnout', 'Fatigue', 'Stress', 'Substance use', 'Sleep problems', 'Trauma', 'Self-harm including self-cutting', 'Suicidal ideation'],
        'General well-being':['Self-care', 'Mindfulness', 'Resiliency'],
        'Self-regulation': ['Emotional regulation', 'Anger management'],
        'Physical Health and Nutrition': ['Overweight and Obesity', 'Sexual Health'],
        'Maternal Mental Health': ['Post-partum', 'Birth-related PTSD'],
        'Post-partum':['Post-partum depression', 'Post-partum anxiety', 'Post-partum OCD', 'Baby blues'],
        'Infant and Early Childhood Mental Health (ICEMH)':['Attachment Problems'],
        'General Supports for Children':['Bullying', 'Gender identity issues', 'Behaviour and Conduct Problems'],
    }

    _res = {}
    for item in res.items():
        _res[item[0]] = item[1]
        # print(item[0], item[1])

    
    
    # for tag_ in tags_params:
    #     if tag_ in kg:
    #         all_possible_subcat = kg[tag_]
    #         print('all_possible_subcat', all_possible_subcat, '\n\n\n')
    #         # print('all_possible_subcat', all_possible_subcat, '\n\n\n')
    #         t = Tag.objects.filter(name__in=all_possible_subcat).values('id').all()
    #         print('tttttttttttttttttttt', t, '\n\n\n')
    #         it = list(map(lambda x: x['id'], t))
    #         sorted_selected_tags = sorted(it, key=lambda x: _res[x])

    #         btn_1 = Tag.objects.filter(id=sorted_selected_tags[0:2][0]).values('name').get()
    #         btn_1 = btn_1['name']
            
    #         btn_2 = ""
    #         if len(sorted_selected_tags) >1:
    #             btn_2 = Tag.objects.filter(id=sorted_selected_tags[0:2][1]).values('name').get()
    #             btn_2 = btn_2['name']
            
    #         return {'resource_counts':len(newQuerySet), 'btns':[btn_1,btn_2]}

        
    #     return {'data':stats}


    # using Resource Type for Education/Informational


    # using Resource Type for Programs/Services



    

    #pop input tags from counted tags 
    for tag in input_tags:
        if tag in res:
            res.pop(tag)

    #select a tag to be a btn
    # selected_tags = []
    # for key in res:
    #     if res[key]>=(len(found_resources)/2)-1 and res[key]<=(len(found_resources)/2)+1 :
    #         selected_tags.append(key)

    selected_tags = list(map(lambda x: x[0], res.most_common(2)))

    #select a tag to be a btn 
    # if(len(selected_tags)<2):
    #     i=0
    #     for key in res.most_common():
    #         if i<=(len(res)/2)+1 and i>=(len(res)/2)-1:
    #             selected_tags.append(key[0])
    #         i+=1


    # sorted_selected_tags = sorted(selected_tags, key=lambda x: entrophy_for_tag(found_resources,x))
    sorted_selected_tags = selected_tags

    btn_1 = Tag.objects.filter(id=sorted_selected_tags[0:2][0]).values('name').get()
    btn_1 = btn_1['name']
    
    btn_2 = Tag.objects.filter(id=sorted_selected_tags[0:2][1]).values('name').get()
    btn_2 = btn_2['name']
    
    return {'resource_counts':len(newQuerySet), 'btns':[btn_1,btn_2]}


def calculateStatsResources(query_params):
    allRes = Resource.objects.all()
    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved"))
    
    allTags = Tag.objects.all()
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
            allTags_[tag.name]['number_of_res']+=1
            if 'resource_list' not in allTags_[tag.name]:
                allTags_[tag.name]['resource_list'] = []
            allTags_[tag.name]['resource_list'].append(allTagandRes[0])
    
    
    allTags_ = sorted(allTags_.items(), key= lambda x: x[1]['number_of_res'], reverse=True)

    stats = {
        'resources':{
            'approved count':len(resQueryset),
            'rejected + pending count':len(allRes)-len(resQueryset),
            'top ten most searched': resQueryset_[:10]
        },
        'Tags':{
            'approved count':len(allRes),
            'approved tags':allTags_
        }
    }

    
    return {'data':stats}

# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer

def calculateTagWeightsForResources(query_params):
    return []

# def calculateTagWeightsForResources(query_params):
    # resources = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved")).values('id', 'title', 'description', 'organization_description', 'organization_name', 'definition')
    # tags = Tag.objects.filter(approved="1").values('id','name')
    # # .filter(tag_category="Health Issue")
    
    # resource_text = []
    # resource_index = []
    # all_tags = {}

    # def pre_processing(newValue):
    #     newValue = newValue.lower().replace('(',' ').replace(')',' ').replace('\'',' ').replace('\"',' ').replace('`',' ').replace('.','').replace(',','').replace('?','').replace('!','')
    #     return newValue

    # for resource in resources:
    #     txt = pre_processing(str(resource['id'])+"___"+str(resource['title'])+" "+str(resource['description'])+" "+str(resource['definition'])+" "+str(resource['organization_name'])+" "+str(resource['organization_description'])+" ")
        
    #     resource_text.append(txt.lower())
    #     resource_index.append(resource['id'])
    
    # for tag in tags:
    #     all_tags[tag['name'].lower()] = tag['id']

    # tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range = (1,4))
    # tfidf_vector = tfidf_vectorizer.fit_transform(resource_text)
    # tfidf_df = pd.DataFrame(tfidf_vector.toarray(), index=resource_text, columns=tfidf_vectorizer.get_feature_names())
    # tfidf_df = tfidf_df.stack().reset_index()
    # tfidf_df = tfidf_df.rename(columns={0:'tfidf', 'level_0': 'document','level_1': 'term', 'level_2': 'term'})
    # index_names_ = tfidf_df[tfidf_df['tfidf'] < 0.0001].index
    # tfidf_df.drop(index_names_, inplace = True)

    # tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False]).groupby(['document']).head(60)
    # top_tfidf = tfidf_df.sort_values(by=['document','tfidf'], ascending=[True,False])

    # response = {}
    # for document in resource_text:
    #     doc_id = document[:document.index("___")]
    #     res = top_tfidf[top_tfidf['document'].str.startswith((doc_id+"___"))]
    #     # print(res,"\n")
    #     for tag in all_tags:
    #         for index, row in res.iterrows():
    #             if((row['tfidf'] > 0) and (( len(tag)>7 and (" "+tag[:-3]) in row['term'] ) or ((" "+tag+" ") in row['term']))):
    #                 t = tag
    #                 print(doc_id, '|' , row['term'], '|' ,tag)

    #                 if doc_id not in response:
    #                     response[doc_id] = {}

    #                 if all_tags[t] not in response[doc_id]:
    #                     response[doc_id][all_tags[t]] = 0

    #                 response[doc_id][all_tags[t]] += row['tfidf']
    

    # for resource_id in response:
    #     print('resource_id=',resource_id, "resource_id[]=",response[resource_id])
    #     instance = Resource.objects.filter(pk=resource_id).get()
    #     instance.index = json.dumps(response[resource_id])
    #     instance.save()

    # print("--------------------------------------------done--------------------------------------------")
    # # print(response)
    # return tags



    # from here
    # tags = Tag.objects.filter(Q(approved="1") and ~Q(tag_category="Location") and ~Q(tag_category="Language")).values('id','name')

    # for tag in tags:
    #     all_tags.append({
    #         'id':tag['id'],
    #         'value':tag['name']
    #     })

    # # # # 2 text cleaning & 3 preprocessing
    # # # def pre_processing(word):
    # # #     newValue = word['value']
    # # #     newValue = newValue.lower().replace('(',' ').replace(')',' ').replace('\'',' ').replace('\"',' ').replace('`',' ').replace('.','').replace(',','').replace('?','').replace('!','')
    # # #     word['value'] = newValue
    # # #     return word

    # # # all_tags = [pre_processing(tag) for tag in all_tags]
    # # # resource_text = [pre_processing(resource) for resource in resource_text]


    # # # # 4 feature extraction & 5 modeling
    # def tf_idf(doc_array, words_arr):
    #     doc_token_counts = {}
    #     response = {}
    #     token_counter = {}
    #     for doc in doc_array:
    #         doc_id = doc['id']
    #         doc_value = doc['value']
    #         tokens = doc_value.split()
    #         t_counts = Counter(tokens)
    #         doc_token_counts[doc_id] = t_counts
    #         for word in words_arr:
    #             word_value = word['value']
    #             if t_counts[word_value]>0:
    #                 if word_value not in token_counter:
    #                     token_counter[word_value]=0
    #                 token_counter[word_value] +=1        

    #     for doc in doc_array:
    #         doc_id = doc['id']
    #         doc_value = doc['value']
    #         response[doc_id] = {}
    #         for word in words_arr:
    #             word_value = word['value']
    #             word_id = word['id']
    #             if word_value not in token_counter or token_counter[word_value]==0:
    #                 response[doc_id][word_id] = 0
    #             else:    
    #                 response[doc_id][word_id] = (doc_token_counts[doc_id][word_value])/math.log2(len(doc_array)/token_counter[word_value])
            
    #     for doc in doc_array:
    #         doc_id = doc['id']
    #         items = response[doc_id]
    #         topitems = heapq.nlargest(70, items.items(), key=itemgetter(1))
    #         topitemsasdict = dict(filter(lambda x: x[1]>0, topitems))
    #         response[doc_id] = topitemsasdict
        
    #     return response

    # res = tf_idf(resource_text, all_tags)

    # # for resource in resource_text:
    # #     resource_id = resource['id']
    # #     instance = Resource.objects.filter(pk=resource_id).get()
    # #     instance.index = json.dumps(res[resource_id])
    # #     instance.save()

    # # return tags

# rasa will call it
def ResourceByIntentEntityViewQuerySet(query_params):
    resQueryset = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved"))
    
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
    ('ptsd', 'Post-Traumatic Stress Disorder (PTSD), Trauma and Abuse')
    ]

    
    tags_params = query_params.getlist('tags')
    tags_params = list(map(lambda x: (x[5:]).lower() if 'need_' in x else x.lower() ,tags_params))

    tags_params = list(map(lambda x: (x[:x.index("(")], x[x.index("(")+1:-1]) ,tags_params))


    all_possible_tags = Tag.objects.filter(approved=1).all()
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
        "Men’s abuse",
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

    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

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
                elif tag_param in sentences:
                    f = sentence_embeddings[sentences.index(tag_param)]
                    sim = ''
                    max_sim = 0.75
                    for i in range(len_tag_embedding):
                        cos_sim = cos(f, sentence_embeddings[i]).numpy()
                        # print('cos_sim', tag_param, sentences[i], cos_sim)
                        if max_sim < cos_sim:
                            max_sim = cos_sim
                            sim = sentences[i]
                    if not sim=='':
                        # print(sim, '$$$$$$$$$$ added using embedding $$$$$$$$$$$ \n')
                        should_be_added.add(sim)



    # remove some unusfull intents
    should_be_romoved.add('where_live')
    should_be_romoved.add('for_me')
    should_be_romoved.add('consent_agree')
    should_be_romoved.add('show_resource')
    
    

    #provience2city mapping 
    canada_cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Mississauga', 'Winnipeg', 'Quebec City', 'Hamilton', 'Brampton', 'Surrey', 'Kitchener', 'Laval', 'Halifax', 'London', 'Victoria', 'Markham', 'St. Catharines', 'Niagara Falls', 'Vaughan', 'Gatineau', 'Windsor', 'Saskatoon', 'Longueuil', 'Burnaby', 'Regina', 'Richmond', 'Richmond Hill', 'Oakville', 'Burlington', 'Barrie', 'Oshawa', 'Sherbrooke', 'Saguenay', 'Lévis', 'Kelowna', 'Abbotsford', 'Coquitlam', 'Trois-Rivières', 'Guelph', 'Cambridge', 'Whitby', 'Ajax', 'Langley', 'Saanich', 'Terrebonne', 'Milton', "St. John's", 'Moncton', 'Thunder Bay', 'Dieppe', 'Waterloo', 'Delta', 'Chatham', 'Red Deer', 'Kamloops', 'Brantford', 'Cape Breton', 'Lethbridge', 'Saint-Jean-sur-Richelieu', 'Clarington', 'Pickering', 'Nanaimo', 'Sudbury', 'North Vancouver', 'Brossard', 'Repentigny', 'Newmarket', 'Chilliwack', 'White Rock', 'Maple Ridge', 'Peterborough', 'Kawartha Lakes', 'Prince George', 'Sault Ste. Marie', 'Sarnia', 'Wood Buffalo', 'New Westminster', 'Châteauguay', 'Saint-Jérôme', 'Drummondville', 'Saint John', 'Caledon', 'St. Albert', 'Granby', 'Medicine Hat', 'Grande Prairie', 'St. Thomas', 'Airdrie', 'Halton Hills', 'Saint-Hyacinthe', 'Lac-Brome', 'Port Coquitlam', 'Fredericton', 'Blainville', 'Aurora', 'Welland', 'North Bay', 'Beloeil', 'Belleville', 'Mirabel', 'Shawinigan', 'Dollard-des-Ormeaux', 'Brandon', 'Rimouski', 'Cornwall', 'Stouffville', 'Georgina', 'Victoriaville', 'Vernon', 'Duncan', 'Saint-Eustache', 'Quinte West', 'Charlottetown', 'Mascouche', 'West Vancouver', 'Salaberry-de-Valleyfield', 'Rouyn-Noranda', 'Timmins', 'Sorel-Tracy', 'New Tecumseth', 'Woodstock', 'Boucherville', 'Mission', 'Vaudreuil-Dorion', 'Brant', 'Lakeshore', 'Innisfil', 'Prince Albert', 'Langford Station', 'Bradford West Gwillimbury', 'Campbell River', 'Spruce Grove', 'Moose Jaw', 'Penticton', 'Port Moody', 'Leamington', 'East Kelowna', 'Côte-Saint-Luc', 'Val-d’Or', 'Owen Sound', 'Stratford', 'Lloydminster', 'Pointe-Claire', 'Orillia', 'Alma', 'Orangeville', 'Fort Erie', 'LaSalle', 'Sainte-Julie', 'Leduc', 'North Cowichan', 'Chambly', 'Okotoks', 'Sept-Îles', 'Centre Wellington', 'Saint-Constant', 'Grimsby', 'Boisbriand', 'Conception Bay South', 'Saint-Bruno-de-Montarville', 'Sainte-Thérèse', 'Cochrane', 'Thetford Mines', 'Courtenay', 'Magog', 'Whitehorse', 'Woolwich', 'Clarence-Rockland', 'Fort Saskatchewan', 'East Gwillimbury', 'Lincoln', 'La Prairie', 'Tecumseh', 'Mount Pearl Park', 'Amherstburg', 'Saint-Lambert', 'Brockville', 'Collingwood', 'Scugog', 'Kingsville', 'Baie-Comeau', 'Paradise', 'Uxbridge', 'Essa', 'Candiac', 'Oro-Medonte', 'Varennes', 'Strathroy-Caradoc', 'Wasaga Beach', 'New Glasgow', 'Wilmot', 'Essex', 'Fort St. John', 'Kirkland', 'L’Assomption', 'Westmount', 'Saint-Lazare', 'Chestermere', 'Huntsville', 'Corner Brook', 'Riverview', 'Lloydminster', 'Joliette', 'Yellowknife', 'Squamish', 'Mont-Royal', 'Rivière-du-Loup', 'Cobourg', 'Cranbrook', 'Beaconsfield', 'Springwater', 'Dorval', 'Thorold', 'Camrose', 'South Frontenac', 'Pitt Meadows', 'Port Colborne', 'Quispamsis', 'Mont-Saint-Hilaire', 'Bathurst', 'Saint-Augustin-de-Desmaures', 'Oak Bay', 'Sainte-Marthe-sur-le-Lac', 'Salmon Arm', 'Port Alberni', 'Esquimalt', 'Deux-Montagnes', 'Miramichi', 'Niagara-on-the-Lake', 'Saint-Lin--Laurentides', 'Beaumont', 'Middlesex Centre', 'Inverness', 'Stony Plain', 'Petawawa', 'Pelham', 'Selwyn', 'Loyalist', 'Midland', 'Colwood', 'Central Saanich', 'Sainte-Catherine', 'Port Hope', 'L’Ancienne-Lorette', 'Saint-Basile-le-Grand', 'Swift Current', 'Edmundston', 'Russell', 'North Grenville', 'Yorkton', 'Tracadie', 'Bracebridge', 'Greater Napanee', 'Tillsonburg', 'Steinbach', 'Hanover', 'Terrace', 'Springfield', 'Gaspé', 'Kenora', 'Cold Lake', 'Summerside', 'Comox', 'Sylvan Lake', 'Pincourt', 'West Lincoln', 'Matane', 'Brooks', 'Sainte-Anne-des-Plaines', 'West Nipissing / Nipissing Ouest', 'Rosemère', 'Mistassini', 'Grand Falls', 'Clearview', 'St. Clair', 'Canmore', 'North Battleford', 'Pembroke', 'Mont-Laurier', 'Strathmore', 'Saugeen Shores', 'Thompson', 'Lavaltrie', 'High River', 'Severn', 'Sainte-Sophie', 'Saint-Charles-Borromée', 'Portage La Prairie', 'Thames Centre', 'Mississippi Mills', 'Powell River', 'South Glengarry', 'North Perth', 'Mercier', 'South Stormont', 'Saint-Colomban', 'Lacombe', 'Sooke', 'Dawson Creek', 'Lake Country', 'Trent Hills', 'Sainte-Marie', 'Guelph/Eramosa', 'Truro', 'Amos', 'The Nation / La Nation', 'Ingersoll', 'Winkler', 'Wetaskiwin', 'Central Elgin', 'Lachute', 'West Grey', 'Parksville', 'Cowansville', 'Bécancour', 'Gravenhurst', 'Perth East', 'Prince Rupert', 'Prévost', 'Sainte-Adèle', 'Kentville', 'Beauharnois', 'Les Îles-de-la-Madeleine', 'Wellington North', 'St. Andrews', 'Carleton Place', 'Whistler', 'Brighton', 'Tiny', 'Gander', 'Sidney', 'Rothesay', 'Brock', 'Summerland', 'Val-des-Monts', 'Taché', 'Montmagny', 'Erin', 'Kincardine', 'North Dundas', 'Wellesley', 'Estevan', 'North Saanich', 'Warman', 'La Tuque', 'Norwich', 'Meaford', 'Adjala-Tosorontio', 'Hamilton Township', 'St. Clements', 'Saint-Amable', 'Weyburn', 'South Dundas', 'L’Île-Perrot', "Notre-Dame-de-l'Île-Perrot", 'Williams Lake', 'Elliot Lake', 'Cantley', 'Nelson', 'Lambton Shores', 'Mapleton', 'Georgian Bluffs', 'Rawdon', 'Campbellton', 'View Royal', 'Coldstream', 'Chester', 'Queens', 'Selkirk', 'Saint-Félicien', 'Hawkesbury', 'Roberval', 'Sainte-Agathe-des-Monts', 'North Dumfries', 'Rideau Lakes', 'Sechelt', 'North Glengarry', 'South Huron', 'Marieville', 'Tay', 'Temiskaming Shores', 'Hinton', 'Saint-Sauveur', 'Quesnel', 'Elizabethtown-Kitley', 'Morinville', 'Grey Highlands', 'Stratford', 'Alfred and Plantagenet', 'Mont-Tremblant', 'Martensville', 'Saint-Raymond', 'Amherst', 'Ramara', 'Bois-des-Filion', 'Leeds and the Thousand Islands', 'Carignan', 'Brockton', 'Laurentian Valley', 'East St. Paul', 'Lorraine', 'Sainte-Julienne', 'Blackfalds', 'Malahide', 'Oromocto', 'Olds', 'Huron East', 'Stanley', 'Penetanguishene', 'Qualicum Beach', 'Notre-Dame-des-Prairies', 'West Perth', 'Cavan Monaghan', 'Arnprior', 'Smiths Falls', 'Pont-Rouge', 'Champlain', 'Coaticook', 'Minto', 'Morden', 'Mono', 'Corman Park No. 344', 'Ladysmith', 'Bridgewater', 'Dauphin', 'Otterburn Park', 'Taber', 'South Bruce Peninsula', 'Edson', 'Farnham', 'Kapuskasing', 'La Malbaie', 'Renfrew', 'Coaldale', "Portugal Cove-St. Philip's", 'Zorra', 'Kitimat', 'Shelburne', 'Happy Valley', 'Saint-Hippolyte', 'Castlegar', 'Church Point', 'Drumheller', 'Kirkland Lake', 'Argyle', 'Torbay', 'La Pêche', 'Banff', 'Innisfail', 'Nicolet', 'Rockwood', 'Drummond/North Elmsley', 'Dryden', 'Iqaluit', 'Fort Frances', 'La Sarre', 'Trail', 'Chandler', 'Stone Mills', 'Hanover', 'South-West Oxford', 'Acton Vale', 'Bromont', 'Beckwith', 'Goderich', 'Plympton-Wyoming', 'Central Huron', 'Rigaud', 'Louiseville', 'Chibougamau', 'Aylmer', 'Delson', 'Kimberley', 'Blandford-Blenheim', 'Bayham', 'Augusta', 'Puslinch', 'Beauport', 'Saint-Rémi', 'St. Marys', 'Drayton Valley', 'Ponoka', 'Labrador City', 'Donnacona', 'Southgate', 'McNab/Braeside', 'Macdonald', 'Hampstead', 'Baie-Saint-Paul', 'Merritt', 'Bluewater', 'East Zorra-Tavistock', 'Brownsburg', 'Stoneham-et-Tewkesbury', 'Asbestos', 'Huron-Kinloss', 'Coteau-du-Lac', 'The Blue Mountains', 'Whitewater Region', 'Edwardsburgh/Cardinal', 'Sainte-Anne-des-Monts', 'Old Chelsea', 'North Stormont', 'Alnwick/Haldimand', 'Peace River', 'Arran-Elderslie', 'Saint-Zotique', 'Val-Shefford', 'Douro-Dummer', 'Plessisville', 'Ritchot', 'Otonabee-South Monaghan', 'Shediac', 'Slave Lake', 'Port-Cartier', 'Saint-Lambert-de-Lauzon', 'Barrington', 'Rocky Mountain House', 'Chatsworth', 'Stephenville', 'Muskoka Falls', 'Devon', 'Yarmouth', 'Boischatel', 'Parry Sound', 'Pointe-Calumet', 'Beaubassin East / Beaubassin-est', 'Wainfleet', 'Cramahe', 'Beauceville', 'North Middlesex', 'Amqui', 'Sainte-Catherine-de-la-Jacques-Cartier', 'Clarenville', 'Mont-Joli', 'Dysart et al', 'Wainwright', 'Contrecoeur', 'Beresford', 'Saint-Joseph-du-Lac', 'Hope', 'Gimli', 'Douglas', 'Saint-Apollinaire', 'Hindon Hill', 'Les Cèdres', 'La Broquerie', 'Kent', 'Tweed', 'Saint-Félix-de-Valois', 'Bay Roberts', 'Melfort', 'Bonnyville', 'Stettler', 'Saint-Calixte', 'Lac-Mégantic', 'Perth', 'Oliver Paipoonge', 'Humboldt', 'Charlemagne', 'Pontiac', 'St. Paul', 'Petrolia', 'Southwest Middlesex', 'Front of Yonge', 'Vegreville', 'Sainte-Brigitte-de-Laval', 'Princeville', 'Verchères', 'The Pas', 'Saint-Césaire', 'La Ronge', 'Tay Valley', 'South Bruce', 'McMasterville', 'Redcliff', 'Crowsnest Pass', 'Saint-Philippe', 'Richelieu', 'Notre-Dame-du-Mont-Carmel', "L'Ange-Gardien", 'Sainte-Martine', 'Saint-Pie', 'Peachland', 'Ashfield-Colborne-Wawanosh', 'Trent Lakes', 'Northern Rockies', 'Cookshire', 'West St. Paul', 'Windsor', 'L’Epiphanie', 'Creston', 'Smithers', 'Cornwall', 'Meadow Lake', 'Lanark Highlands', 'Sackville', 'Grand Falls', 'Cochrane', 'Marystown', 'Sioux Lookout', 'Didsbury', 'Saint-Honoré', 'Fernie', 'Deer Lake', 'Woodstock', 'Val-David', 'Flin Flon', 'Hudson', 'Gananoque', 'Brokenhead', 'Saint-Paul', 'Burton', 'Spallumcheen', 'Westlock', 'Témiscouata-sur-le-Lac', 'Shannon', 'Osoyoos', 'Montréal-Ouest', 'Hearst', 'Saint-Henri', 'Ste. Anne', 'Antigonish', 'Espanola', 'West Elgin', 'Flin Flon (Part)', 'Grand Bay-Westfield', 'Sainte-Anne-de-Bellevue', 'North Huron', 'Oliver', "Saint-Roch-de-l'Achigan", 'Stirling-Rawdon', 'Chisasibi', 'Carbonear', 'Saint Marys', 'Chertsey', 'Armstrong', 'Stonewall', 'Shippagan', 'Lanoraie', 'Memramcook', 'Centre Hastings', 'Warwick', 'East Ferris', 'Hanwell', 'Saint-Joseph-de-Beauce', 'Metchosin', 'Lucan Biddulph', 'Rivière-Rouge', 'Greenstone', 'Saint-Mathias-sur-Richelieu', 'Neepawa', 'Gibsons', 'Kindersley', 'Jasper', 'Barrhead', 'Les Coteaux', 'Melville', 'Saint-Germain-de-Grantham', 'Iroquois Falls', 'Havelock-Belmont-Methuen', 'Cornwallis', 'Saint-Boniface', 'Edenwold No. 158', 'Coverdale', 'Vanderhoof', 'Southwold', 'Goulds', 'Saint Stephen', 'Waterloo', 'Nipawin', 'Neuville', 'Saint-Cyrille-de-Wendover', 'Central Frontenac', 'Mont-Orford', 'Saint-Jean-de-Matha', 'Seguin', 'Tyendinaga', 'Hampton', 'Sussex', 'Grand Forks', 'La Pocatière', 'Caraquet', 'Saint-Étienne-des-Grès', 'Altona', 'Stellarton', 'Wolfville', 'New Maryland', 'Port Hardy', 'Saint-Donat', 'Château-Richer', 'Madawaska Valley', 'Deep River', 'Asphodel-Norwood', 'Red Lake', 'Métabetchouan-Lac-à-la-Croix', 'Berthierville', 'Vermilion', 'Niverville', 'Hastings Highlands', 'Carstairs', 'Danville', 'Channel-Port aux Basques', 'Battleford', 'Lac-Etchemin', 'Saint-Antonin', 'Saint-Jacques', 'Swan River', 'Sutton', 'Northern Bruce Peninsula', 'L’Islet-sur-Mer', 'Carleton-sur-Mer', 'Oka', 'Prescott', 'Amaranth', 'Marmora and Lake', 'Maniwaki', 'Morin-Heights', 'Dundas', 'Napierville', 'Crabtree', 'Bancroft', 'Saint-Tite', 'Howick', 'Dutton/Dunwich', 'Callander', 'Simonds', 'Baie-d’Urfé', 'New Richmond', 'Perth South', 'Roxton Pond', 'Sparwood', 'Claresholm', 'Breslau', 'Montague', 'Cumberland', 'Beaupré', 'Saint-André-Avellin', 'Saint-Ambroise-de-Kildare', 'East Angus', 'Rossland', 'Mackenzie', 'Golden', 'Raymond', "Saint-Adolphe-d'Howard", 'Warwick', 'Bowen Island', 'Bonnechere Valley', 'Windsor', 'Pincher Creek', 'Alnwick', 'Westville', 'Fruitvale', 'Pasadena', 'Saint-Prosper', 'Ormstown', 'Cardston', 'Westbank', 'De Salaberry', 'Headingley', 'Grande Cache', 'Atholville', 'Saint-Agapit', 'Prince Albert No. 461', 'Casselman', 'Saint-Ambroise', 'Hay River', 'Mistissini', 'Studholm', 'Lumby', 'Saint-Faustin--Lac-Carré', 'Morris-Turnberry', 'Placentia', 'Saint-Pascal', 'Mulmur', 'Blind River', 'Dunham', 'Havre-Saint-Pierre', 'Saint-Anselme', 'Trois-Pistoles', 'Grande-Rivière', 'Powassan', 'Malartic', 'Bonavista', 'Killarney - Turtle Mountain', 'Woodlands', 'Lewisporte', 'Saint-Denis-de-Brompton', 'Invermere', 'Salisbury', 'Bifrost-Riverton', 'Buckland No. 491', 'Cartier', 'Sainte-Anne-des-Lacs', 'Highlands East', 'Alexander', 'Sainte-Claire', 'Percé', 'Saint-Jean-Port-Joli', 'East Hawkesbury', 'Bright', 'Penhold', "Saint-André-d'Argenteuil", 'Saint-Côme--Linière', 'Saint-Sulpice', 'Marathon', 'Forestville', 'Inuvik', 'Richmond', 'Lake Cowichan', 'Sables-Spanish Rivers', 'Hillsburg-Roblin-Shell River', 'Port Hawkesbury', 'Three Hills', 'Lorette', 'Paspebiac', 'Saint-Thomas', 'Saint-Jean-Baptiste', 'Portneuf', 'Pictou', 'Tisdale', 'Lake of Bays', 'High Level', 'Gibbons', 'Bishops Falls', 'WestLake-Gladstone', 'Normandin', 'Saint-Alphonse-Rodriguez', 'Beauséjour', 'Dalhousie', 'Saint-Alphonse-de-Granby', 'Lac du Bonnet', 'Clermont', 'Virden', 'Compton', 'White City', 'Ellison', 'Mont-Saint-Grégoire', 'Wellington', 'Merrickville', 'Saint-Liboire', 'Dégelis', 'Morris', 'Saint-Alexis-des-Monts', 'Cap-Saint-Ignace', 'Saint-Anaclet-de-Lessard', 'Carman', 'Athens', 'Melancthon', 'Cap Santé', 'Harbour Grace', 'Houston', 'Adelaide-Metcalfe', 'Crossfield', 'Springdale', 'Fort Macleod', 'Athabasca', 'Enderby', 'Saint-Ferréol-les-Neiges', 'Laurentian Hills', 'Grand Valley', 'Senneterre', 'Sainte-Marie-Madeleine', 'Admaston/Bromley', 'Saint-Gabriel-de-Valcartier', 'North Algona Wilberforce', 'Kingston', 'Wawa', "Saint-Christophe-d'Arthabaska", 'Sainte-Mélanie', 'Ascot Corner', 'Horton', 'Saint-Michel', 'Botwood', "Saint-Paul-d'Abbotsford", 'Saint-Marc-des-Carrières', 'Stanstead', 'Sainte-Anne-de-Beaupré', 'Sainte-Luce', 'Saint-Gabriel', 'Rankin Inlet', 'Vanscoy No. 345', 'Cedar', 'Princeton', 'La Loche', 'Kingsclear', 'Ferme-Neuve', 'Thurso', 'Adstock', 'Shuniah', 'Enniskillen', 'Yamachiche', 'Saint-Maurice', 'Bonaventure', 'Val-Morin', 'Pohénégamook', 'Wakefield', 'Stoke', 'Sainte-Marguerite-du-Lac-Masson', 'Saint-Prime', 'Kuujjuaq', 'Atikokan', 'Grenville-sur-la-Rouge', 'North Cypress-Langford', 'Sainte-Anne-de-Sorel', 'Macamic', 'Sundre', 'Rougemont', 'Piedmont', 'Grimshaw', 'Lac-des-Écorces', 'Northeastern Manitoulin and the Islands', 'Pelican Narrows', 'McDougall', 'Black Diamond', 'Saint-Pamphile', 'Bedford', 'Weedon-Centre', 'Lacolle', 'Saint-Gabriel-de-Brandon', 'Errington', 'Coalhurst', 'French River / Rivière des Français', 'Arviat', 'Saint-David-de-Falardeau', 'Markstay', 'Spaniards Bay', 'Cocagne', 'Saint-Bruno', 'Chetwynd', 'Laurier-Station', 'Saint-Anicet', 'Saint-Mathieu-de-Beloeil', 'Cap-Chat', 'Sexsmith', 'Notre-Dame-de-Lourdes', 'Ville-Marie', 'Saint-Isidore', 'Shippegan', 'East Garafraxa', 'Pemberton', 'Unity', 'Rimbey', 'High Prairie', 'Turner Valley', 'Hanna', 'Fort Smith', 'Maria', 'Saint-Chrysostome', 'Greater Madawaska', 'Berwick', 'Saint-Damase', 'Lincoln', 'Disraeli', 'Sainte-Victoire-de-Sorel', 'Meadow Lake No. 588', 'Elkford', 'Georgian Bay', 'Saint-Alexandre', 'Hérbertville', 'Moosomin', 'North Kawartha', 'Sainte-Thècle', 'Trenton', 'Fermont', 'Esterhazy', 'Wickham', 'La Présentation', 'Beaverlodge', 'Sainte-Catherine-de-Hatley', 'Saint-Basile', 'Saint-Raphaël', 'Holyrood', 'Gracefield', 'Saint-Martin', 'Causapscal', 'Brigham', 'Perry', 'Port-Daniel--Gascons', 'Rosetown', 'Minnedosa', 'Labelle', 'Huntingdon', 'Hébertville', 'Black River-Matheson', 'Saint-Michel-des-Saints', 'Dufferin', 'Saint-Victor', 'Sicamous', 'Cap Pele', 'Kelsey', 'Killaloe, Hagarty and Richards', 'Alvinston', 'Dundurn No. 314', 'Saint-Éphrem-de-Beauce', 'Assiniboia', 'Témiscaming', 'Magrath', 'Sainte-Geneviève-de-Berthier', 'Buctouche', 'Grand Manan', 'Sainte-Madeleine', 'Boissevain', 'Scott', 'Sainte-Croix', 'Algonquin Highlands', 'Valcourt', 'Saint George', 'Paquetville', 'Saint-Dominique', 'Clearwater', 'Addington Highlands', 'Lillooet', 'Burin', 'Grand Bank', 'Léry', 'Minto', 'Rosthern No. 403', 'Chase', 'Mansfield-et-Pontefract', 'Saint-Denis', 'Outlook', 'Mitchell', 'Saint-Gédéon-de-Beauce', "Saint-Léonard-d'Aston", 'Lunenburg', 'Northesk', 'Albanel', 'St. Anthony', 'Pessamit', 'Maskinongé', 'Saint-Charles-de-Bellechasse', 'Fogo Island', 'East Broughton', 'Lantz', 'Calmar', 'Highlands', 'Saint-Polycarpe', 'Logy Bay-Middle Cove-Outer Cove', 'Deschambault', 'Canora', 'Upper Miramichi', 'Anmore', 'Hardwicke', 'Saint-Côme', 'Waskaganish', 'Twillingate', 'Saint-Quentin', 'Lebel-sur-Quévillon', 'Pilot Butte', 'Nanton', 'Pierreville', 'New-Wes-Valley', 'Pennfield Ridge', 'West Interlake', 'Biggar', 'Britannia No. 502', 'Kent', 'Wabana', 'Saint-Gilles', 'Wendake', 'Saint-Bernard', 'Sainte-Cécile-de-Milton', 'Saint-Roch-de-Richelieu', 'Saint-Nazaire', 'Saint-Elzéar', 'Hinchinbrooke', 'Saint-François-Xavier-de-Brompton', 'Papineauville', 'Prairie View', 'Cowichan Bay', 'Saint-Ignace-de-Loyola', 'Central Manitoulin', 'Maple Creek', 'Glovertown', 'Tofield', 'Madoc', 'Upton', 'Sainte-Anne-de-Sabrevois', 'Logan Lake', 'Sainte-Anne-de-la-Pérade', 'Saint-Damien-de-Buckland', 'Baker Lake', 'Saltair', 'Pouch Cove', 'Saint-Ferdinand', 'Port McNeill', 'Digby', 'Manouane', 'Saint-Gervais', 'Neebing', 'Redwater', 'Saint-Alexandre-de-Kamouraska', 'Saint-Marc-sur-Richelieu', 'Mandeville', 'Caplan', 'Point Edward', 'Allardville', 'Waterville', 'Saint-Damien', 'Lac-Nominingue', 'Obedjiwan', 'Rama', 'McCreary', 'Deloraine-Winchester', 'Oakland-Wawanesa', 'Brenda-Waskada', 'Russell-Binscarth', 'Ellice-Archie', 'Souris-Glenwood', 'Riverdale', 'Pembina', 'Wallace-Woodworth', 'Lorne', 'Ethelbert', 'Yellowhead', 'Swan Valley West', 'Grey', 'Gilbert Plains', 'Norfolk-Treherne', 'Hamiota', 'Emerson-Franklin', 'Sifton', 'Rossburn', 'Grand View', 'Grassland', 'Louise', 'Ste. Rose', 'Cartwright-Roblin', 'Mossey River', 'Lakeshore', 'Riding Mountain West', 'Clanwilliam-Erickson', 'Glenboro-South Cypress', 'North Norfolk', 'Reinland', 'Minitonas-Bowsman', 'Kippens', 'Blucher', 'Hatley', 'Saint-Gédéon', 'Kingsey Falls', 'Provost', 'Saint-Charles', 'Mattawa', 'Tumbler Ridge', 'Terrasse-Vaudreuil', "L'Ascension-de-Notre-Seigneur", 'Bow Island', 'Barraute', 'One Hundred Mile House', 'Kedgwick', 'Gambo', 'Saint-Liguori', 'Bonfield', 'Pointe-Lebel', 'Saint Mary', 'Saint-Patrice-de-Sherrington', 'Fox Creek', 'Dawn-Euphemia', 'Chapleau', 'Saint-Esprit', 'Westfield Beach', 'Montague', 'Mashteuiatsh', 'Saint-François-du-Lac', 'Eel River Crossing', 'Saint-Fulgence', 'Millet', 'Vallée-Jonction', 'Saint-Georges-de-Cacouna', 'Lumsden No. 189', 'Manitouwadge', 'Wellington', 'Swift Current No. 137', 'Tofino', 'Fort Qu’Appelle', 'Vulcan', 'Indian Head', 'Petit Rocher', 'Wabush', 'Saint-Fabien', 'Watrous', 'North Frontenac', 'Lac-Supérieur', 'Les Escoumins', 'Richibucto', 'Rivière-Beaudette', 'Saint-Barthélemy', "Nisga'a", 'Austin', 'Saint-Mathieu', "Saint-Paul-de-l'Île-aux-Noix", 'Orkney No. 244', 'Behchokò', 'Saint-Joseph-de-Coleraine', 'Saint-Cyprien-de-Napierville', 'Sayabec', 'Valleyview', 'Déléage', 'Potton', 'Sainte-Béatrix', 'Sainte-Justine', 'Eastman', 'Saint-Valérien-de-Milton', 'Saint-Cuthbert', 'Saint-Blaise-sur-Richelieu', 'Middleton', 'Maugerville', 'Dalmeny', 'Kamsack', 'Lumsden', 'Trinity Bay North', 'Saint-Michel-de-Bellechasse', 'Sainte-Angèle-de-Monnoir', 'Picture Butte', 'Sacré-Coeur-Saguenay', 'Saint-Louis', 'Victoria', 'Saint-Robert', 'Armstrong', "Saint-Pierre-de-l'Île-d'Orléans", 'La Guadeloupe', 'Saint Andrews', 'Burns Lake', 'Povungnituk', 'Manners Sutton', 'Gore', 'Deseronto', 'Lamont', 'Chambord', 'Dudswell', 'Wynyard', 'Cambridge Bay', 'Saint-Narcisse', 'Frontenac Islands', 'Waswanipi', 'Inukjuak', 'Piney', 'Komoka', 'Saint-Zacharie', 'Hemmingford', 'Shelburne', 'Saint-Clet', 'Carberry', 'Brighton', 'Saint-Antoine', 'Warfield', 'Northampton', 'Saint-Ours', 'Stephenville Crossing', 'Sainte-Anne-de-la-Pocatière', 'Ucluelet', 'Saint-Placide', 'Barrière', 'Fisher', 'Nipissing', 'Sainte-Clotilde', 'Shaunavon', 'Wicklow', 'Southesk', 'Nouvelle', 'Rosthern', 'Yamaska', 'Neguac', 'Flat Rock', 'Igloolik', 'Grunthal', 'Naramata', 'Saint-Élie-de-Caxton', 'Blumenort', 'Balmoral', 'Price', 'Rosedale', 'Saint-Jacques-le-Mineur', 'Huron Shores', 'Champlain', 'Whitehead', 'Saint-Antoine-sur-Richelieu', 'Saint-Pacôme', 'Saint-Stanislas-de-Kostka', 'Frontenac', 'Stuartburn', 'Yamaska-Est', "Sainte-Émélie-de-l'Énergie", 'Saint-Charles-sur-Richelieu', 'Saint-Joseph-de-Sorel', 'Nipigon', 'Rivière-Blanche', 'Sainte-Hélène-de-Bagot', 'Franklin Centre', 'Harbour Breton', 'Massey Drive', 'Mille-Isles', 'Wilton No. 472', 'Lyster', 'Oakview', 'Balgonie', 'Harrison Park', 'Kensington', 'Witless Bay', 'Pond Inlet', 'Royston', 'Sainte-Clotilde-de-Horton', 'Burford', 'Fossambault-sur-le-Lac', 'Saint-Benoît-Labre', 'Coombs', 'Terrace Bay', 'Chapais', 'Saint-Honoré-de-Shenley', 'Cleveland', 'Macdonald, Meredith and Aberdeen Additional', 'Messines', 'Saint-Jean-de-Dieu', 'Nakusp', 'Florenceville', 'Saint-Antoine-de-Tilly', 'Lakeview', 'Humbermouth', 'Fort St. James', 'Saint-François-de-la-Rivière-du-Sud', 'Saint-Jacques', 'Uashat', 'Perth', 'Eeyou Istchee Baie-James', 'Shellbrook No. 493', 'Shawville', 'Saint-Lucien', 'Lambton', "Saint-Laurent-de-l'Île-d'Orléans", 'Saint-Flavien', 'Grenville', 'Chute-aux-Outardes', 'Sainte-Marcelline-de-Kildare', 'Saint-Félix-de-Kingsey', 'Upper Island Cove', 'Glenelg', 'Sainte-Élisabeth', 'Ashcroft', 'Clarkes Beach', 'Saint-Bernard-de-Lacolle', 'Belledune', 'Saint-Guillaume', 'Venise-en-Québec', 'Maliotenam', 'Ripon', 'Hilliers', 'Saint-Joseph', 'Saint-Paulin', 'Bon Accord', 'Saint David', 'Saint-Albert', 'Matagami', 'Springfield', 'Amherst', 'Notre-Dame-du-Laus', 'St. George', 'Wembley', 'Victoria', 'Springbrook', 'Saint-Tite-des-Caps', 'Hudson Bay', 'Pinawa', 'Brudenell, Lyndoch and Raglan', 'Carlyle', 'Keremeos', 'Val-Joli', 'Gold River', 'Saint-Casimir', 'Bay Bulls', 'Langham', 'Frenchman Butte', 'Gordon', 'Kugluktuk', 'Saint-Malachie', 'Southampton', 'Salluit', 'Pangnirtung', 'Saint-Louis-de-Gonzague', 'Moosonee', 'Englehart', 'Saint-Urbain', 'Tring-Jonction', 'Nauwigewauk', 'Pointe-à-la-Croix', 'Denmark', 'Saint-Joachim', 'Torch River No. 488', "Saint-Théodore-d'Acton", 'Grindrod', 'L’ Îsle-Verte', 'Harrison Hot Springs', 'Palmarolle', 'Henryville', 'Sussex Corner', 'Saint-Odilon-de-Cranbourne', 'Pipestone', 'Laurierville', 'La Doré', 'Lac-au-Saumon', 'Wotton', 'Prairie Lakes', 'Elk Point', 'Shellbrook', 'Wemindji', 'Cape Dorset', 'Strong', 'Lappe', 'Rivière-Héva', 'Fort-Coulonge', 'Irishtown-Summerside', 'Godmanchester', 'Macklin', 'Armour', 'Saint-Simon', 'St. François Xavier', 'Tingwick', 'Saint-Aubert', 'Saint-Mathieu-du-Parc', 'Wabasca', 'Ragueneau', 'Notre-Dame-du-Bon-Conseil', 'Wasagamack', 'Saint-Ubalde', 'Creighton', 'Fortune', 'Faraday', 'Berthier-sur-Mer', 'Frampton', 'Magnetawan', 'New Carlisle', 'Laird No. 404', 'Petitcodiac', 'Popkum', 'Norton', 'Canwood No. 494', 'Wentworth-Nord', 'Bas Caraquet', 'Sainte-Ursule', 'Dawson', 'Nantes', 'Lac-aux-Sables', 'Stewiacke', 'Taylor', 'Rosser', 'Estevan No. 5', 'Falmouth', 'Vaudreuil-sur-le-Lac', 'Grahamdale', 'Cardwell', 'Two Hills', 'Spiritwood No. 496', 'Legal', 'Amulet', 'Hérouxville', 'Pointe-des-Cascades', 'Weldford', 'Reynolds', 'St. Laurent', 'Lions Bay', "L'Isle-aux-Allumettes", 'Emo', "Sainte-Brigide-d'Iberville", 'Les Éboulements', 'Dunsmuir', 'Pointe-aux-Outardes', 'Smooth Rock Falls', 'Oxbow', 'Telkwa', 'Gjoa Haven', 'Sainte-Barbe', 'Mayerthorpe', 'Saint-Louis-du-Ha! Ha!', 'Powerview-Pine Falls', 'Baie Verte', 'Saint-Édouard', 'Charlo', 'Hillsborough', 'Bruederheim', 'Burgeo', 'Wadena', 'Richmond', 'Swan Hills', 'Wilkie', 'Saint-Léonard', 'Rivière-Bleue', 'Noyan', 'Ile-à-la-Crosse', 'Landmark', 'Saint-Hugues', 'Chisholm', 'Sainte-Anne-du-Sault', 'La Conception', 'Saint-Valère', 'Sorrento', 'Lamèque', 'Thessalon', "L'Isle-aux-Coudres", 'Nobleford', 'Larouche', "South Qu'Appelle No. 157", 'Elton', 'Lorrainville', 'Conestogo', 'Upham', 'St.-Charles', 'Sainte-Lucie-des-Laurentides', 'Saint-Alexis', 'Gillam', 'Roxton Falls', 'Montcalm', 'Clarendon', 'Mervin No. 499', 'Saint-Ludger', 'Coldwell', 'Saint-Arsène', 'Racine', 'Saint-Majorique-de-Grantham', 'Saint-Zénon', 'Saint-Armand', 'Saint-Édouard-de-Lotbinière', 'Alonsa', 'Listuguj', 'Bowden', 'St. Joseph', 'Osler', 'Saint-Hubert-de-Rivière-du-Loup', 'Saint-Jude', 'Dildo', 'La Minerve', 'Lanigan', 'Lajord No. 128', 'Moonbeam', 'Notre-Dame-des-Pins', 'Saint-Alban', 'Saint-Pierre-les-Becquets', 'Arborg', 'Vauxhall', 'Bayfield', 'Beaver River', 'Irricana', 'Labrecque', 'New Bandon', 'Wemotaci', 'Sainte-Hénédine', "L'Anse-Saint-Jean", 'Bassano', 'Parrsboro', 'Kaleden', "St. George's", 'Fort Simpson', 'Akwesasne', 'L’Avenir', 'Ignace', 'Claremont', 'Teulon', 'Peel', 'Musquash', 'Notre-Dame-du-Portage', 'St. Lawrence', 'Oxford', 'Minto-Odanah', "St. Alban's", 'Saint James', "Saint-Norbert-d'Arthabaska", 'Manning', 'Glenella-Lansdowne', 'Saint-Hilarion', 'Saint-Siméon', 'Saint-Barnabé', 'Sainte-Félicité', 'Two Borders', 'Queensbury', 'Bury', 'Lac-Bouchette', 'Saint-Lazare-de-Bellechasse', 'Saint-Michel-du-Squatec', 'Saint-Joachim-de-Shefford', 'St-Pierre-Jolys', 'Grand-Remous', 'Saint-Gabriel-de-Rimouski', 'Armstrong', 'Rogersville', 'Langenburg', 'Sainte-Marie-Salomé', 'Moose Jaw No. 161', 'Saint-Cyprien', 'Maidstone', 'Très-Saint-Sacrement', 'Battle River No. 438', 'Miltonvale Park', 'McAdam', 'Saints-Anges', 'Saint-Urbain-Premier', 'Centreville-Wareham-Trinity', 'Alberton', 'Winnipeg Beach', 'Sainte-Agathe-de-Lotbinière', 'Salmo', 'Kipling', 'Sagamok', 'Trécesson', 'Tara', 'Grande-Vallée', 'Bertrand', 'Newcastle', 'Mont-Carmel', 'Saint Martins', 'Saint-Eugène', 'Notre-Dame-des-Neiges', 'Saint-André', 'Centreville', 'Roland', 'Saint-Léon-de-Standon', 'Saint-Modeste', 'Carnduff', 'Carling', 'Eckville', 'Nain', 'Hillsburgh', 'Foam Lake', 'Sainte-Sabine', 'Saint-Maxime-du-Mont-Louis', 'Blanc-Sablon', 'Cobalt', 'Gravelbourg', 'South River', 'Hudson Bay No. 394', 'McKellar', 'Frelighsburg', 'Buffalo Narrows', 'Ayer’s Cliff', 'Les Méchins', 'Sainte-Marguerite', 'Saint-Claude', 'Air Ronge', 'Chipman', 'Girardville', 'Saint-Bruno-de-Guigues', 'Grenfell', 'Dorchester', 'South Algonquin', 'Windermere', 'Saint-Narcisse-de-Beaurivage', 'Saint-René-de-Matane', "Sainte-Jeanne-d'Arc", 'Plaisance', 'Roxton-Sud', 'St. Louis No. 431', 'Youbou', 'Duchess', 'Saint-Frédéric', 'Viking', 'Sioux Narrows-Nestor Falls', 'Whitecourt', 'Repulse Bay', 'Montréal-Est', 'King', 'Regina Beach', 'Saint-Patrice-de-Beaurivage', 'Ootischenia', 'Hensall', 'Bentley', 'Durham', 'Sainte-Marthe', 'Notre-Dame-du-Nord', 'Pinehouse', 'Saint-Aimé-des-Lacs', 'Lac-Drolet', 'Preeceville', 'Maple Creek No. 111', "Harbour Main-Chapel's Cove-Lakeview", 'Saint-Wenceslas', 'Weyburn No. 67', 'Birch Hills', 'Wedgeport', 'Kerrobert', 'Havelock', 'Eston', 'Sainte-Geneviève-de-Batiscan', 'Saint-Justin', 'Saint-Norbert', 'Schreiber', 'Trochu', 'Botsford', 'Riviere-Ouelle', 'Greenwich', 'Stukely-Sud', 'Saint-Georges-de-Clarenceville', 'Sainte-Thérèse-de-Gaspé', 'Beachburg', 'Desbiens', 'Clyde River', 'La Macaza', 'Souris', 'Kindersley No. 290', 'Laird', 'Falher', 'Saint-Vallier', 'Coleraine', 'Melita', 'Noonan', 'Sainte-Pétronille', 'Delisle', 'Bristol', 'Mahone Bay', 'Waldheim', 'Saint-Sylvestre', 'Taloyoak', 'Onoway', 'Saint-Stanislas', 'Malpeque', 'Plantagenet', 'Longue-Rive', 'Argyle', 'Davidson', 'Plaster Rock', 'Wilmot', 'Valemount', 'Saint-Léonard-de-Portneuf', 'Alberta Beach', 'Saint-Narcisse-de-Rimouski', 'Saint-Bonaventure', 'Longlaketon No. 219', 'Papineau-Cameron', 'Assiginack', 'Brébeuf', 'Hudson Hope', 'Prince', 'Baie-du-Febvre', 'Durham-Sud', 'Melbourne', 'Nipawin No. 487', 'Duck Lake No. 463', 'Oyen', 'Nova Scotia']
    
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

    # print('tags_params_mapped', tags_params_mapped)
    # print('query_relaxation_tags', query_relaxation_tags)

    
    resQueryset = resQueryset.filter(Q(tags__name__in=tags_params_mapped) | Q(tags__name__in=query_relaxation_tags))



    # calculating tf-idf for tags
    tags = Tag.objects.filter(Q(approved="1") and ~Q(tag_category="Location") and ~Q(tag_category="Language")).values('id','name')
    all_tags = []

    for tag in tags:
        all_tags.append({
            'id':tag['id'],
            'value':tag['name']
        })

    def tf_idf(doc_array, words_arr):
        doc_token_counts = {}
        response = {}
        token_counter = {}
        for doc in doc_array:
            doc_id = doc['id']
            tokens = doc['value']
            t_counts = Counter(tokens)
            doc_token_counts[doc_id] = t_counts
            for word in words_arr:
                word_value = word['value']
                if t_counts[word_value]>0:
                    if word_value not in token_counter:
                        token_counter[word_value]=0
                    token_counter[word_value] +=1        

        for doc in doc_array:
            doc_id = doc['id']
            doc_value = doc['value']
            response[doc_id] = {}
            for word in words_arr:
                word_value = word['value']
                word_id = word['id']
                if word_value not in token_counter or token_counter[word_value]==0:
                    response[doc_id][word_id] = 0
                else:    
                    response[doc_id][word_id] = (doc_token_counts[doc_id][word_value])/math.log2(len(doc_array)/token_counter[word_value])
            
        for doc in doc_array:
            doc_id = doc['id']
            items = response[doc_id]
            topitems = heapq.nlargest(70, items.items(), key=itemgetter(1))
            topitemsasdict = dict(filter(lambda x: x[1]>0, topitems))
            response[doc_id] = topitemsasdict
        
        return response

    # resource_text = []
    # for resource in list(map(lambda x: [x.id,list(x.tags.all())], resQueryset)):
    #     tag_names = list(map(lambda x: x.name  ,resource[1]))
    #     resource_text.append({'id':resource[0], 'value':tag_names})

    
    # tfidf_res = tf_idf(resource_text, all_tags)
    

    query_relaxation_tags = Tag.objects.filter(name__in=query_relaxation_tags).values('id').all()
    query_relaxation_tags_id = list(map(lambda x: x['id'], query_relaxation_tags))

    #retrieve tag ids from tag names
    tags = Tag.objects.filter(name__in=tags_params_mapped).values('id').all()
    tags_id_list = list(map(lambda x: x['id'], tags))


    # scoring and ordering by scores
    resource_scores = {}
    res_counter = 0
    for resource in list(map(lambda x: [x.id,x.index,list(x.tags.all()), x.title, x.resource_type, x.definition], resQueryset)):
        resource_scores[resource[0]] = 0
        if resource[1] is None or resource[1]=='':
            continue

        index = json.loads(resource[1])
        original_tag_ids = list(map(lambda x: str(x.id), resource[2]))
        original_tag_categories = list(map(lambda x: str(x.tag_category), resource[2]))
        
        # print('tags_id_list', tags_id_list)
        # tags_id_list = tag ids
        for tag in tags_id_list:
            tag = str(tag)
            # print(tag, index, '\n')
            if tag in index:
                resource_scores[resource[0]] += index[tag]
                # print('check...')
            if tag in original_tag_ids:
                resource_scores[resource[0]] += 0.2
                # if resource[0] in tfidf_res and int(tag) in tfidf_res[resource[0]]:
                #     resource_scores[resource[0]] += (tfidf_res[resource[0]][int(tag)]*3)

                i = original_tag_ids.index(tag)

                if original_tag_categories[i] == 'City':
                    resource_scores[resource[0]] += 0.55
                elif original_tag_categories[i] == 'Health Issue':
                    resource_scores[resource[0]] += 0.1
                elif original_tag_categories[i] == 'Resource Type for Programs and Services':
                    resource_scores[resource[0]] += 0.1
                elif original_tag_categories[i] == 'Resource Type for Education/Informational':
                    resource_scores[resource[0]] += 0.1

        for original_tag_id in original_tag_ids:
            if original_tag_id in query_relaxation_tags_id:
                resource_scores[resource[0]] += 0.07 #for query relaxation


        # resource_scores[resource[0]] += cos(sentence_embeddings[0], sentence_embeddings[1+res_counter]).numpy()*0.7
        

        #tags_params_mapped = string value of tags
        for tag in tags_params_mapped:
            if len(tag)<2:
                continue

            if len(tag)<10 and tag[:-2].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.55
            
            if len(tag)>=10 and tag[:-4].lower() in resource[3].lower():
                resource_scores[resource[0]] += 0.55
            
            
            if (tag == 'information') and (resource[4] == 'RS' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 0.45
            elif (tag == 'program_services') and (resource[4] == 'SR' or resource[4] == 'BT'):
                resource_scores[resource[0]] += 0.45

            if (tag == 'definition') and (resource[5]):
                resource_scores[resource[0]] += 0.45

            sum_tag = ""
            for w in tag.replace("-", " ").split(" "):
                sum_tag += w[0]
            if (sum_tag.upper() != "") and (sum_tag.upper() in resource[3]):
                resource_scores[resource[0]] += 0.55
        
        res_counter+=1

    topitems = heapq.nlargest(25, resource_scores.items(), key=itemgetter(1))

    topitemsasdict = dict(topitems)

    if len(topitems) > 1:
        resQueryset = resQueryset.filter(id__in=topitemsasdict.keys())

        ######################## sentence transformer ########################
        ######################################################################

        # Sentences we want sentence embeddings for
        sentences = []
        resource_titles = []
        sentences.append((" ").join(tags_params_mapped))
        resource_titles.append('-')
        for res_title in list(map(lambda x: (x.title, x.organization_name), resQueryset)):
            resource_titles.append(res_title[0])
            if res_title[1][5:] not in res_title[0]:
                sentences.append(res_title[0])
            else:
                sentences.append(res_title[0][res_title[0].index(res_title[1][5:]):])

        # Tokenize sentences
        encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling
        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        ######################## sentence transformer ########################
        ######################################################################

        
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
                res_embedding_index = resource_titles.index(qs.title)
                bert_model_score = cos(sentence_embeddings[0], sentence_embeddings[res_embedding_index]).numpy()*0.7
                qs.score = topitemsasdict[qs.id] + bert_model_score

        return newQuerySet



    #  tags = Tag.objects.filter(name__in=tags_params).values('id').all()
    #  tagsList = list(map(lambda x: x.id, tags))
    # print(tagsList)
    
    # resQueryset = resQueryset.filter(tags__id__in=tagsList)
    # resQueryset = resQueryset.order_by('public_view_count')

    return resQueryset


def VerifyApprovedResources(query_params):
    resources = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved")).values('id', 'title', 'description', 'organization_description', 'website_meta_data_updated_at', 'url', 'organization_name', 'definition')

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

    result = Resource.objects.filter((Q(review_status="approved") & Q(review_status_2="approved")) | Q(review_status_3="approved")).filter(id__in=resource_ids_with_problems)

    return result


class VerifyApprovedResourcesView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get_queryset(self):
        return VerifyApprovedResources(self.request.query_params)

class HomepageResourceView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get_queryset(self):
        return ResourceViewQuerySet(self.request.query_params)


class ResourceByIntentEntityView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return ResourceByIntentEntityViewQuerySet(self.request.query_params)

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
