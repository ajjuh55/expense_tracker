from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from expense.serializers import UserSerializer,ExpenseSerializer
from expense.models import Expenses
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone




class RegisterView(ViewSet):

    def create(self, request):
        dser = UserSerializer(data=request.data)

        if dser.is_valid():
            dser.save()
            return Response(
                data=dser.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=dser.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ExpenseView(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        expense_list=Expenses.objects.filter(owner=request.user)
        ser=ExpenseSerializer(expense_list,many=True)
        return Response(data=ser.data)
    def destroy(self,request,pk=0):
        Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"DELETED!"})
    def update(self,request,pk=0):
        expense_obj=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=expense_obj)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self,requset,pk=0):
        expense_obj=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=self.request.data,instance=expense_obj,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)    

class ExpenseSummeryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cur_date=timezone.now()
        print(cur_date)
        cur_mnth=cur_date.month
        cur_yr=cur_date.year
        print(cur_mnth,cur_yr)
        data=Expenses.objects.filter(owner=request.user,created_at__month=cur_mnth,created_at__year=cur_yr)
        category_summery=data.values('category').annotate(Sum('amount'))
        '''
        [
            {'categoty':'fuel','totel',3000},
            {'categoty':'bills','totel',12000},
        ]
        '''
        cate_summry=[summery for summery in category_summery]
        print(cate_summry)
        for i in category_summery:
            print(i)
        totel_expns=data.values('amount').aggregate(Sum('amount' ))
        print(totel_expns)
        # ser=ExpenseSerializer(qs,many=True)
        context={
            "totel_expense":totel_expns,
            "category_summery":cate_summry
        }
        return Response(data=context)

    