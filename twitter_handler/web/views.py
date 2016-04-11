import twitter
from django.shortcuts import render
from rest_framework.views import APIView

import pdb

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
        except Exception:
            return render(request, 'data-not-found.html', {})


class MostUsedHashTag(APIView):
    def get(self, request, handler):
        # pdb.set_trace()
        api.GetHomeTimeline(screen_name=handler)
        # api.GetUser()
        pass
