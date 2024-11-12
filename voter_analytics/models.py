from django.db import models

class Voter(models.Model):
    '''Store/represent the data from one voter in Newton'''
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()

    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.CharField(max_length=6, default="")
    zip_code = models.IntegerField()
    
    date_of_birth = models.DateField()
    date_of_reg = models.DateField()

    party = models.TextField()
    precinct_num = models.TextField()
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voterscore = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}, ({self.street_num} {self.street_name}) {self.zip_code}, score: {self.voterscore}'
    
    def save(self, *args, **kwargs):
        # list of fields to apply title case
        fields_to_titlecase = ['first_name', 'last_name', 'street_name', 'apt_num']
        
        for field in fields_to_titlecase:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.title())
        super().save(*args, **kwargs)
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = '/Users/19149/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    for line in f:
        fields = line.split(',').strip()
        
        data = {
            'voter_id': fields[0],
            'last_name': fields[1],
            'first_name': fields[2],
            'street_num': fields[3],
            'street_name': fields[4],
            'apt_num': fields[5],
            'zip_code': fields[6],
            'date_of_birth': fields[7],
            'date_of_reg': fields[8],
            'party': fields[9],
            'precinct_num': fields[10],
            'voterscore': fields[16]
        }

        # Mapping of boolean fields to their CSV indices
        boolean_fields = {
            'v20state': 11, 'v21town': 12, 'v21primary': 13, 'v22general': 14, 'v23town': 15
        }

        # convert "TRUE"/"FALSE" to True/False for boolean fields
        for field_name, index in boolean_fields.items():
            data[field_name] = fields[index] == "TRUE"
        
        # Create a new voter instance with data
        voter = Voter(**data)
        voter.save()  # Commit to database
        # print(f'Created voter: {voter}')

    print(f'Done. Created {len(Voter.objects.all())} Voters.')
    