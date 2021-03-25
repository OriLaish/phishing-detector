from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class client_submission_data:

    def __init__(self, url, features, is_phishing, uid):
        self.url = url
        self.features = features
        self.is_phishing = is_phishing
        self.uid = uid


def features_validator(features):
    return True

class client_submission_data_serializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    features = serializers.CharField(required=True, validators=[features_validator])
    is_phishing = serializers.BooleanField(required=True)
    uid = serializers.CharField(required=True)

    def restore_object(self, attrs, instance=None):
        if instance is client_submission_data :
            instance.url = attrs.get('url', instance.url)
            instance.features = attrs.get('features', instance.features)
            instance.is_phishing = attrs.get('is_phishing', instance.is_phishing)
            instance.uid = attrs.get('uid', instance.uid)
        return client_submission_data(**attrs)

    def create(self, validated_data):
        return client_submission_data(**validated_data)
