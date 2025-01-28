from django.db import models
from sqlalchemy.orm.exc import NoResultFound


class People(models.Model):
    """Creates a users table"""
    user_name = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    location = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    profile_pic = models.ImageField(default='fallback.jpg', blank=True)

    def follow(self, other_user):
        """Enables the following of another user"""
        if self != other_user:
            Following.objects.get_or_create(follower=self, following=other_user)
    
    def is_following(self, other_user):
        return Following.objects.filter(follower=self, following=other_user).exists()
    
    def unfollow(self, other_user):
        Following.objects.filter(follower=self, following=other_user).delete()
    
    def is_followed_by(self, other_user):
        return Following.objects.filter(follower=other_user, following=self).exists()

class Posts(models.Model):
    """Creates a Posts table"""
    user_id = models.ForeignKey(People, on_delete=models.CASCADE)
    text_post = models.TextField(null=True)
    image_post = models.ImageField(blank=True)
    date_posted = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    """Creates a comments table"""
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(People, on_delete=models.CASCADE)
    text_comment = models.TextField(null=True)
    image_comment = models.ImageField(blank=True)
    date_comment = models.DateTimeField(auto_now=True)

class Following(models.Model):
    """Creates a following table"""
    follower = models.ForeignKey(People, related_name="followers", on_delete=models.CASCADE)
    following = models.ForeignKey(People, related_name="following", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')