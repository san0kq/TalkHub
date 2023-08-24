from core.models import Config, Notification, NotificationType, Rating, Retweet, Tag, Tweet, TweetRating
from django.contrib import admin

admin.site.register(NotificationType)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Retweet)
admin.site.register(Tag)
admin.site.register(TweetRating)
admin.site.register(Tweet)
admin.site.register(Config)
