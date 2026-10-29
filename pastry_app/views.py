from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from pastry_app.models import PastryDb,OrderDb
from pastry_app.serializers import PastrySerializer,OrderSerializer
from datetime import time,datetime,timedelta
from rest_framework import serializers
# Create your views here.
class PastryCreateListView(APIView):

    def get(self,request):

        qs = PastryDb.objects.all()
        serializer_instance = PastrySerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data
        serializer_instance = PastrySerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class PastryRetrievalUpdateDeleteView(APIView):

    def get(self,request,pk):

        qs = get_object_or_404(PastryDb,id=pk)
        serializer_instance = PastrySerializer(qs)
        return Response(data = serializer_instance.data)
    
    def put(self,request,pk):

        form_data = request.data
        pastry_object = get_object_or_404(PastryDb,id=pk)
        serializer_instance = PastrySerializer(data=form_data,instance=pastry_object)

        if serializer_instance.is_valid():

            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):

        pastry_object = get_object_or_404(PastryDb,id=pk)
        pastry_object.delete()
        return Response({
            "Message":"pastry deleted successffully...."
        })
class OrderListCreateView(APIView):

    def get(self,request):

        qs = OrderDb.objects.all()
        serializer_instance = OrderSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data
        serializer_instance = OrderSerializer(data=form_data)

        if serializer_instance.is_valid():

            order_date = serializer_instance.validated_data.get("order_date")
            pastry_id = serializer_instance.validated_data.get("pastry_id")

            last_order = OrderDb.objects.filter(
                order_date=order_date,
                pastry_id=pastry_id
            ).order_by("-token").first()

            if last_order is None:

                form_data["token"] = 1
                form_data['pickup_time'] = time(11,0)

            else:

                form_data["token"] = last_order.token + 1
                current_time = datetime.combine(order_date,last_order.pickup_time)
                next_time = current_time + timedelta(minutes=30)

                if next_time.time() == time(12,30) :
                    next_time = datetime.combine(order_date,time(13,30))

                if next_time.time() == time(14,0) :
                    raise serializers.ValidationError("Shop closed...visit again thank you")
                
                form_data ["pickup_time"] = next_time.time() 

            
            
            form_data["status"] = "success"
            qs = OrderDb.objects.create(**form_data)
            serializer_instance = OrderSerializer(qs)
            return Response({
                     "Status":"booked successfully",
                     "Token" : form_data["token"],
                    "Pickup time" :form_data["pickup_time"]
                  })
        else:
            return Response(data = serializer_instance.errors)

