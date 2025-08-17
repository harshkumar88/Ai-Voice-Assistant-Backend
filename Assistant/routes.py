from django.urls import re_path

from Assistant.Views.AiResponseView import AiResponseView
from Assistant.Views.GenerateQuestionsView import GenerateQuestionsView
from Assistant.Views.HealthCheckView import HealthCheckView
from Assistant.Views.VoiceBotView import VoiceBotView

urlpatterns = [
    re_path(r'^health/check/v(?P<version_id>\d+)/', HealthCheckView.as_view()),
    re_path(r'^generate/questions/v(?P<version_id>\d+)/', GenerateQuestionsView.as_view()),
    re_path(r'^voice/v(?P<version_id>\d+)/', VoiceBotView.as_view()),
    re_path(r'^generate/response/v(?P<version_id>\d+)/', AiResponseView.as_view()),

]
