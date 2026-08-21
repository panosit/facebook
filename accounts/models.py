from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    RELATIONSHIP_CHOICES = [
        ('single', 'Single'),
        ('in_relationship', 'In a Relationship'),
        ('engaged', 'Engaged'),
        ('married', 'Married'),
    ]

    INTERESTED_IN_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('both', 'Both'),
    ]

    CLASS_YEAR_CHOICES = [
        (2004, '2004'),
        (2005, '2005'),
        (2006, '2006'),
        (2007, '2007'),
        (2008, '2008'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    concentration = models.CharField(max_length=100, blank=True, help_text='Major/Concentration')
    house = models.CharField(max_length=100, blank=True, help_text='Dorm/House')
    class_year = models.IntegerField(choices=CLASS_YEAR_CHOICES, blank=True, null=True)
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)
    interested_in = models.CharField(max_length=10, choices=INTERESTED_IN_CHOICES, blank=True)
    courses = models.CharField(max_length=255, blank=True, help_text='Courses this semester')
    about_me = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Poke(models.Model):
    from_user = models.ForeignKey(User, related_name='pokes_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='pokes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} poked {self.to_user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
