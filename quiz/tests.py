# Create your tests here.
import json
from django import views
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class hello(APITestCase):
    
    def test_hello(self):
        response = self.client.get(reverse('hello'))
        print(response)
        print(response.data)
            
        #self.assertEqual(response.status_code,status.HTTP_200_OK)
        
''' 
class cafe(APITestCase):
    
    def test_cafe(self):
       
        #response = self.client.get(reverse('cafe'),{'count': '4'})
        #response = self.client.get('/quiz/cafe/', {'count': '4'})
        
        #print(response)
            
        #self.assertEqual(response.status_code,status.HTTP_200_OK)
'''