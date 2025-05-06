from django.core.management.base import BaseCommand
from django.core.files import File
from campaigns.models import Campaign
import requests
import tempfile
import os

class Command(BaseCommand):
    help = 'Adds sample images to existing campaigns using placeholder images'

    def handle(self, *args, **kwargs):
        # List of placeholder image URLs (using placeholder.com for demo)
        image_urls = [
            'https://picsum.photos/800/600',  # Random image 1
            'https://picsum.photos/800/600',  # Random image 2
            'https://picsum.photos/800/600',  # Random image 3
            'https://picsum.photos/800/600',  # Random image 4
            'https://picsum.photos/800/600',  # Random image 5
            'https://picsum.photos/800/600',  # Random image 6
            'https://picsum.photos/800/600',  # Random image 7
            'https://picsum.photos/800/600',  # Random image 8
            'https://picsum.photos/800/600',  # Random image 9
            'https://picsum.photos/800/600',  # Random image 10
        ]

        campaigns = Campaign.objects.filter(image='')

        for i, campaign in enumerate(campaigns):
            if i < len(image_urls):
                try:
                    # Download image
                    response = requests.get(image_urls[i])
                    if response.status_code == 200:
                        # Create a temporary file
                        img_temp = tempfile.NamedTemporaryFile(delete=True)
                        img_temp.write(response.content)
                        img_temp.flush()

                        # Save the image to the campaign
                        filename = f'campaign_{campaign.id}.jpg'
                        campaign.image.save(filename, File(img_temp), save=True)
                        
                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully added image to campaign: {campaign.title}'
                        ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error adding image to campaign {campaign.title}: {str(e)}'
                    ))

        self.stdout.write(self.style.SUCCESS('Finished adding sample images'))