from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import time
from operator import itemgetter
from django.db.models import Count
import steamapi
import urllib2
import re
import base64
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import itertools
from .tools import compare_images, to_grayscale
import cStringIO
from fuzzywuzzy import fuzz


# Create your views here.


def index(request):
    if request.method == 'POST':
        steamid = str(request.POST['steamid'])
        steamidencoded = base64.b64encode(steamid)
        return HttpResponseRedirect(reverse('smurffinder:smurflist', args=(steamidencoded,)))
    return render(request, 'smurffinder/index.html')


def smurfproxy(request):
    if request.method == 'POST':
        steamid_friend = str(request.POST['steamid_friend'])
        steamid_smurf = str(request.POST['steamid_smurf'])
        steamidencoded_friend = base64.b64encode(steamid_friend)
        steamidencoded_smurf = base64.b64encode(steamid_smurf)

        return HttpResponseRedirect(reverse('smurffinder:smurfproxylist', args=(steamidencoded_smurf, steamidencoded_friend,)))
    return render(request, 'smurffinder/proxyindex.html')


# '<span class="historyDash">-</span>\s*([^<]+)\s*</div>'
def smurflist(request, steamid):
    steamid_decoded = base64.b64decode(steamid)
    if steamid_decoded.endswith('/'):
        steamid_decoded = steamid_decoded[:-1]
    steamapi.core.APIConnection(api_key=settings.STEAM_API_KEY)
    urllist = steamid_decoded.split("/")
    userid = urllist[len(urllist) - 1]
    matching_friends = []
    identical_name_matches = []
    identical_avatar_matches = []
    partial_name_matches = []
    partial_avatar_matches = []
    user = steamapi.user.SteamUser(userurl="officials1mple")
    if "/id/" in steamid_decoded:
        user = steamapi.user.SteamUser(userurl=userid)
    elif "/profiles/" in steamid_decoded:
        user = steamapi.user.SteamUser(userid)
    else:
        error_message = "sif"
        return render(request, 'smurffinder/smurf.html', {'error_message': error_message})

    user_history_page = user.profile_url + "namehistory"
    page = urllib2.urlopen(user_history_page)
    html = page.read()

    namelist = re.findall('<span class="historyDash">-</span>\s*([^<]+)\s*</div>', html)
    # utf_list = [str(x) for x in namelist]
    stripped_list = map(str.strip, namelist)
    # stripped_list.append(str(user.name))
    unicode_list = [x.decode('utf-8') for x in stripped_list]
    unicode_list.append(user.name)

    useravatar = user.avatar_full
    avfile1 = cStringIO.StringIO(urllib2.urlopen(useravatar).read())
    img1 = to_grayscale(imread(avfile1).astype(float))
    for friend in user.friends:
        friend_history_page = friend.profile_url + "namehistory"
        friend_page = urllib2.urlopen(friend_history_page)
        friend_html = friend_page.read()

        friend_namelist = re.findall('<span class="historyDash">-</span>\s*([^<]+)\s*</div>', friend_html)
        # friend_decoded_list = [str(x) for x in friend_namelist]
        friend_stripped_list = map(str.strip, friend_namelist)
        # friend_stripped_list.append(str(friend.name))
        friend_unicode_list = [x.decode('utf-8') for x in friend_stripped_list]
        friend_unicode_list.append(friend.name)

        matches = set(stripped_list).intersection(friend_stripped_list)
        if len(matches) > 0:
            identical_name_matches.append((friend, ', '.join(matches)))

        fuzzmatches = list((i1, i2, fuzz.ratio(i1, i2)) for i1, i2 in itertools.product(unicode_list, friend_unicode_list) if
                            fuzz.ratio(i1, i2) >= 57)

        if len(fuzzmatches) > 0:
            partial_name_matches.append((friend, fuzzmatches))
        friendavatar = friend.avatar_full
        avfile2 = cStringIO.StringIO(urllib2.urlopen(friendavatar).read())
        img2 = to_grayscale(imread(avfile2).astype(float))
        n_m, n_0 = compare_images(img1, img2)
        if n_0 == 0:
            identical_avatar_matches.append((friend, "Identical avatar"))
        elif n_m/img1.size < 15:
            partial_avatar_matches.append((friend, "Partial avatar match"))
        # if user.real_name == friend.real_name:
        #    matching_friends.append((friend, "Real name match"))

    return render(request, 'smurffinder/smurf.html', {'identical_name_matches': identical_name_matches,
                                                      'partial_name_matches': partial_name_matches,
                                                      'identical_avatar_matches': identical_avatar_matches,
                                                      'partial_avatar_matches': partial_avatar_matches,
                                                      'user': user})


def smurfproxylist(request, steamid_smurf, steamid_friend):
    steamidsmurf_decoded = base64.b64decode(steamid_smurf)
    steamidfriend_decoded = base64.b64decode(steamid_friend)
    if steamidsmurf_decoded.endswith('/'):
        steamidsmurf_decoded = steamidsmurf_decoded[:-1]
    if steamidfriend_decoded.endswith('/'):
        steamidfriend_decoded = steamidfriend_decoded[:-1]
    steamapi.core.APIConnection(api_key=settings.STEAM_API_KEY)
    urllist = steamidsmurf_decoded.split("/")
    userid = urllist[len(urllist) - 1]
    matching_friends = []
    identical_name_matches = []
    identical_avatar_matches = []
    partial_name_matches = []
    partial_avatar_matches = []
    user = steamapi.user.SteamUser(userurl="officials1mple")
    if "/id/" in steamidsmurf_decoded:
        user = steamapi.user.SteamUser(userurl=userid)
    elif "/profiles/" in steamidsmurf_decoded:
        user = steamapi.user.SteamUser(userid)
    else:
        error_message = "sif"
        return render(request, 'smurffinder/smurf.html', {'error_message': error_message})

    user_history_page = user.profile_url + "namehistory"
    page = urllib2.urlopen(user_history_page)
    html = page.read()

    namelist = re.findall('<span class="historyDash">-</span>\s*([^<]+)\s*</div>', html)
    # utf_list = [str(x) for x in namelist]
    stripped_list = map(str.strip, namelist)
    # stripped_list.append(str(user.name))
    unicode_list = [x.decode('utf-8') for x in stripped_list]
    unicode_list.append(user.name)

    useravatar = user.avatar_full
    avfile1 = cStringIO.StringIO(urllib2.urlopen(useravatar).read())
    img1 = to_grayscale(imread(avfile1).astype(float))
    urllist = steamidfriend_decoded.split("/")
    userid = urllist[len(urllist) - 1]
    user2 = steamapi.user.SteamUser(userurl="officials1mple")
    if "/id/" in steamidfriend_decoded:
        user2 = steamapi.user.SteamUser(userurl=userid)
    elif "/profiles/" in steamidfriend_decoded:
        user2 = steamapi.user.SteamUser(userid)
    else:
        error_message = "sif"
        return render(request, 'smurffinder/smurf.html', {'error_message': error_message})

    for friend in user2.friends:
        friend_history_page = friend.profile_url + "namehistory"
        friend_page = urllib2.urlopen(friend_history_page)
        friend_html = friend_page.read()

        friend_namelist = re.findall('<span class="historyDash">-</span>\s*([^<]+)\s*</div>', friend_html)
        # friend_decoded_list = [str(x) for x in friend_namelist]
        friend_stripped_list = map(str.strip, friend_namelist)
        # friend_stripped_list.append(str(friend.name))
        friend_unicode_list = [x.decode('utf-8') for x in friend_stripped_list]
        friend_unicode_list.append(friend.name)

        matches = set(stripped_list).intersection(friend_stripped_list)
        if len(matches) > 0:
            identical_name_matches.append((friend, ', '.join(matches)))
        fuzzmatches = list((i1, i2, fuzz.ratio(i1, i2)) for i1, i2 in itertools.product(unicode_list, friend_unicode_list) if
                            fuzz.ratio(i1, i2) >= 57)

        if len(fuzzmatches) > 0:
            partial_name_matches.append((friend, fuzzmatches))
        friendavatar = friend.avatar_full
        avfile2 = cStringIO.StringIO(urllib2.urlopen(friendavatar).read())
        img2 = to_grayscale(imread(avfile2).astype(float))
        n_m, n_0 = compare_images(img1, img2)
        if n_0 == 0:
            identical_avatar_matches.append((friend, "Identical avatar"))
        elif n_m/img1.size < 15:
            partial_avatar_matches.append((friend, "Partial avatar match"))
        # if user.real_name == friend.real_name:
        #    matching_friends.append((friend, "Real name match"))

    return render(request, 'smurffinder/smurf.html', {'identical_name_matches': identical_name_matches,
                                                      'partial_name_matches': partial_name_matches,
                                                      'identical_avatar_matches': identical_avatar_matches,
                                                      'partial_avatar_matches': partial_avatar_matches,
                                                      'user': user})

