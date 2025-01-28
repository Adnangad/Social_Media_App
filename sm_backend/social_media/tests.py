from django.test import TestCase, Client
from django.urls import reverse
import json
from social_media.models import *
from datetime import datetime

class MyViewsTestCase(TestCase):
    """Tests the methods in the views modules"""
    def test_signup(self):
        """Tests the signup view method"""
        client = Client()
        url = reverse("signup")
        payload = {"name": "adnan", "email": "obuya@gmail.com", "location": "Nai",
                   "dob": datetime.now().date()}
        response = client.post(
            url,
            data=json.dumps(payload, indent=4, sort_keys=True, default=str),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success"})
    
    def test_signup_with_invalid_data(self):
        """Tests the signup method when invalid data is parsed"""
        client = Client()
        url = reverse("signup")
        payload = {"name": "bom", "email": "aollo@gmail.com",
                   "password": "abumi", "location": "Nai"}
        response = client.post(
            url, 
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
    
    def test_signup_with_image(self):
        """Tests the signup when an image is sent"""
        




class MyModelsTestCase(TestCase):
    """Contains tests on models"""
    def setUp(self):
        #creates test data
        x = datetime.now()
        person = People.objects.create(user_name="obuya", email='obuya@gmail.com',
                              password='testing', location='Kisumu',
                              date_of_birth=datetime.date(x))
        person2 = People.objects.create(user_name="adnan", email='adnan@gmail.com',
                              password='testing2', location='Nairobi',
                              date_of_birth=datetime.date(x))
        person3 = People.objects.create(user_name="gard", email='gard@gmail.com',
                              password='testing3', location='Bungoma',
                              date_of_birth=datetime.date(x))
        
        text = "Backend is better than frontend"
        text2 = "Fifa is the best game ever"
        comment = "No frontend is better"

        p1 = Posts.objects.create(user_id=person, text_post=text)
        Posts.objects.create(user_id=person2, text_post=text2)
        Comments.objects.create(post_id =p1, user_id=person3, text_comment=comment)
        
    def test_create_user(self):
        """Tests if a user is created"""
        obj = People.objects.get(email='gard@gmail.com')
        self.assertEqual(obj.user_name, 'gard')
    
    def test_create_post(self):
        """Tests whether a post is created"""
        obj = People.objects.get(email="obuya@gmail.com")
        pst = Posts.objects.get(user_id=obj)
        self.assertEqual(pst.text_post, "Backend is better than frontend")
    
    def test_following_features(self):
        """Tests the following features in the app"""
        obj1 = People.objects.get(email='obuya@gmail.com')
        obj2 = People.objects.get(email="adnan@gmail.com")
        obj2.follow(obj1)
        self.assertTrue(obj1.is_followed_by(obj2))
    
    def test_comment_features(self):
        """Tests the comment feature"""
        obj1 = People.objects.get(email='obuya@gmail.com')
        post = Posts.objects.get(user_id=obj1)
        obj3 = Comments.objects.get(post_id=post)
        self.assertEqual(obj3.text_comment, "No frontend is better")
        
