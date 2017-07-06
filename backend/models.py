from django.db import models

# obsolete
class ValidateEleve(models.Model):
	"""crée un modèle de stockage temporaire des
	utilisateurs importés en attendant d'être validés"""
	nom = models.CharField(max_length=100)
	prenom = models.CharField(max_length=100)
	promotion = models.CharField(max_length=4)
	username = models.CharField(max_length=100)
	password1 = models.CharField(max_length=100)
	password2 = models.CharField(max_length=100)