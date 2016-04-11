import pdb

import operator

import twitter
from collections import Counter

from django.shortcuts import render
from rest_framework.views import APIView
from twitter import TwitterError
import os


api = twitter.Api(consumer_key=os.environ.get('CONSUMER_KEY'),
                  consumer_secret=os.environ.get('CONSUMER_SECRET'),
                  access_token_key=os.environ.get('ACCESS_TOKEN_KEY'),
                  access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'))


def get_index_page(request):
    return render(request, 'search-box.html', {})


def get_check_it_page(request):
    return render(request, 'check-it.html', {})


class TimeLineView(APIView):
    @staticmethod
    def get_user_info(handler):
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
                             'banner_url': banner_url}

            return response_dict
        else:
            return None

    def get(self, request, handler):
        try:
            timeline = api.GetUserTimeline(screen_name=handler, exclude_replies=False,
                                           include_rts=True, count=100)

            response_dict = self.get_user_info(handler)

            if response_dict and timeline:
                response_dict['timeline'] = timeline
                return render(request, 'search-result.html', response_dict)
            else:
                return render(request, 'data-not-found.html', {})
        except TwitterError:
            return render(request, 'data-not-found.html', {})


class MostUsedHashTag(APIView):
    def get(self, request, handler):
        try:
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

            return render(request, 'hashtags.html',
                          {"hash_tags": reversed(sorted_x[-10:]), "screen_name": handler,
                           "length": len(sorted_x[-10:])})
        except TwitterError:
            return render(request, 'data-not-found.html', {})


class FavouriteTweets(TimeLineView):
    def get(self, request, handler):
        try:
            response_dict = self.get_user_info(handler)
            fav = api.GetFavorites(screen_name=handler, count=200)
            if response_dict and fav:
                response_dict['timeline'] = fav
                return render(request, 'search-result.html', response_dict)
            else:
                return render(request, 'data-not-found.html', {})
        except TwitterError:
            return render(request, 'data-not-found.html', {})
