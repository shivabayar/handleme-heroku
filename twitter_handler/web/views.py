import pdb

import operator

import twitter
from collections import Counter

from django.shortcuts import render
from rest_framework.views import APIView
from twitter import TwitterError

api = twitter.Api(consumer_key='YM7lZLIwUlaKh70kcMFuodMQl',
                  consumer_secret='bsFtG0RVgaSlYkVUy3at99JuIdOdtsfRpVWf4SBbxII0yK0zyK',
                  access_token_key='391498643-YrBYllBegsfTSPYslZHLpg86FiAsiFLTfd2HLDF7',
                  access_token_secret='LgAQ8qP3XFRJX4vfauxKr0SB1QHm3ZonKyZSoBuFLI79R')


def get_index_page(request):
    return render(request, 'search-box.html', {})


class TimeLineView(APIView):
    def get(self, request, handler):
        try:
            timeline = api.GetUserTimeline(screen_name=handler, exclude_replies=False,
                                           include_rts=True, count=100)

            user = api.GetUser(screen_name=handler)

            if user:
                profile_pic = str(user.profile_image_url)
                profile_pic = profile_pic.replace("normal", "200x200")
                banner_url = str(user.profile_banner_url)
                name = str(user.name)
                profile_url = str(user.url)
                response_dict = {'handler': handler,
                                 'profile_pic': profile_pic,
                                 'name': name,
                                 'profile_url': profile_url,
                                 'banner_url': banner_url,
                                 'timeline': timeline}

                return render(request, 'search-result.html', response_dict)
            else:
                return render(request, 'data-not-found.html', {})
        except TwitterError:
            return render(request, 'data-not-found.html', {})


class MostUsedHashTag(APIView):
    def get(self, request, handler):
        timeline = api.GetUserTimeline(screen_name=handler, count=200)
        hashtags = list()

        for time in timeline:
            hashes = time.hashtags
            if len(hashes) == 0:
                continue
            temp_hash = list()
            for hash_ in hashes:
                temp_hash.append(hash_.text)

            hashtags.extend(temp_hash)

        occurrances_of_hashtags = Counter(hashtags)
        sorted_x = sorted(occurrances_of_hashtags.items(), key=operator.itemgetter(1))

        return render(request, 'hashtags.html', {"hash_tags": reversed(sorted_x[-10:]), "screen_name": handler})
