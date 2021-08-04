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

"""
WSGI config for ChatbotPortal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

#This is very bad, but the portal has been configuered wiered and it's the only way I can get wsgi to recognize things correctly
#this will need to change with every deployment
sys.path.append('/mnt/d/VAWork/GithubForkVer/MDSC-Portal/ChatbotPortal')
sys.path.append('/mnt/d/VAWork/GithubForkVer/MDSC-Portal/ChatbotPortal/resource/')
sys.path.append('/mnt/d/VAWork/GithubForkVer/MDSC-Portal/ChatbotPortal/review')
sys.path.append('/mnt/d/VAWork/GithubForkVer/MDSC-Portal/ChatbotPortal/frontend')
sys.path.append('/mnt/d/VAWork/GithubForkVer/MDSC-Portal/ChatbotPortal/chatbotPortal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbotPortal.settings')

application = get_wsgi_application()
