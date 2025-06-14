from django.db import models
import csv


class Voter(models.Model):
    voter_id = models.CharField(max_length=100, default='UNKNOWN')
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=10)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.voter_id}"
    
def load_data():
    with open('newton_voters.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                voter_id=row['Voter ID Number'],
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row.get('Residential Address - Apartment Number') or None,
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=row['Date of Birth'],
                date_of_registration=row['Date of Registration'],
                party_affiliation=row['Party Affiliation'].strip(),
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'].upper() == 'TRUE',
                v21town=row['v21town'].upper() == 'TRUE',
                v21primary=row['v21primary'].upper() == 'TRUE',
                v22general=row['v22general'].upper() == 'TRUE',
                v23town=row['v23town'].upper() == 'TRUE',
                voter_score=int(row['voter_score'])
            )