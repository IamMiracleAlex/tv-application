from django.db import models


class Quote(models.Model):
	author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=250, default='')
	body = models.TextField()
	make_public = models.BooleanField(default=False)
	views = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.title