from rest_framework.serializers import ModelSerializer
from pastry_app.models import PastryDb,OrderDb
from rest_framework import serializers
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

    def validate(self,validated_data):
        
        phone = validated_data.get("phone")
        order_date = validated_data.get("order_date")

        if OrderDb.objects.filter(
            phone = phone,
            order_date = order_date
        ).exists():
            raise serializers.ValidationError('Already booked....')
        else:
            return validated_data