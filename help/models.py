from django.db import models

# Create your models here.

class HelpArticle(models.Model):
	"""permet de définir un modèle d'article. Celui-ci peut être de deux sortes :
	 - soit il n'est qu'un lien vers un pdf, auquel cas il contient le nom de ce document qui se trouve
	 	dans help/guides
	 - soit il possède des paragraphes reliés qui permettent de construire une aide intégrée dans le site"""
	title = models.CharField(max_length=500, verbose_name='Titre')
	subtitle = models.TextField(null=True, blank=True, verbose_name='Description rapide')
	is_pdf = models.BooleanField(default=True) # décrit les deux cas d'utilisation ci-dessus
	filename = models.CharField(max_length=300, blank=True, null=True) #attention afin de préserver contre l'import de mauvais fichiers l'extension .pdf n'est pas contenue dans le filename

	def __str__(self):
		return self.title

	class Meta:
		unique_together = ('title',)
		ordering = ('title',)


	@models.permalink
	def get_article_url(self):
		"""retourne le lien vers la page de vision de l'article, que ce soit un
			pdf ou du html"""
		return ('help_article', [self.id])

	@models.permalink
	def get_pdf_url(self):
		"""retourne le lien vers la page de vision de l'article, uniquement pour un pdf"""
		return ('view_pdf', [self.filename])

	@models.permalink
	def delete_self_url(self):
		"""retourne le lien vers la page de vision de l'article, uniquement pour un pdf"""
		return ('delete_article', [self.filename])