from rest_framework.serializers import ModelSerializer
from pastry_app.models import PastryDb,OrderDb

class PastrySerializer(ModelSerializer):

    class Meta:
        model = PastryDb
        fields = '__all__'
        read_only_field =['id']

class OrderSerializer(ModelSerializer):

    class Meta:
        model = OrderDb
        fields = '__all__'
        read_only_field = ['id']