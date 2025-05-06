from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from campaigns.models import Category, Campaign
from donations.models import Donation
from decimal import Decimal
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates sample data for the CharitySpark demo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories = [
            {'name': 'Education', 'description': 'Support educational initiatives and students'},
            {'name': 'Healthcare', 'description': 'Medical support and healthcare initiatives'},
            {'name': 'Environment', 'description': 'Environmental conservation and sustainability'},
            {'name': 'Animal Welfare', 'description': 'Support for animals and wildlife'},
            {'name': 'Disaster Relief', 'description': 'Emergency response and recovery'},
            {'name': 'Arts & Culture', 'description': 'Support for arts, culture, and heritage'},
        ]

        created_categories = []
        for cat in categories:
            category, created = Category.objects.get_or_create(
                name=cat['name'],
                defaults={'description': cat['description']}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create test users
        test_users = [
            {'username': 'john_donor', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Donor'},
            {'username': 'mary_creator', 'email': 'mary@example.com', 'first_name': 'Mary', 'last_name': 'Creator'},
            {'username': 'peter_supporter', 'email': 'peter@example.com', 'first_name': 'Peter', 'last_name': 'Supporter'},
        ]

        created_users = []
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            created_users.append(user)

        # Create sample campaigns
        campaign_titles = [
            'School Building Project',
            'Save the Rainforest',
            'Emergency Medical Fund',
            'Animal Shelter Support',
            'Clean Water Initiative',
            'Arts Education Program',
            'Disaster Relief Fund',
            'Youth Sports Program',
            'Community Garden Project',
            'Historic Theater Restoration'
        ]

        for title in campaign_titles:
            creator = random.choice(created_users)
            category = random.choice(created_categories)
            goal_amount = random.randint(5000, 50000)
            current_amount = random.randint(0, goal_amount)
            days_duration = random.randint(30, 90)
            
            campaign, created = Campaign.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'This is a sample campaign for {title}. Support this initiative to make a difference!',
                    'creator': creator,
                    'category': category,
                    'goal_amount': goal_amount,
                    'current_amount': current_amount,
                    'end_date': timezone.now().date() + timedelta(days=days_duration),
                    'is_featured': random.choice([True, False]),
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created campaign: {campaign.title}')
                
                # Create some donations for this campaign
                for _ in range(random.randint(3, 8)):
                    donor = random.choice(created_users)
                    amount = Decimal(random.randint(10, 1000))
                    
                    Donation.objects.create(
                        campaign=campaign,
                        donor=donor,
                        amount=amount,
                        message=f'Supporting {campaign.title}! Good luck!',
                        anonymous=random.choice([True, False]),
                        simulated_payment_status='completed'
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data'))