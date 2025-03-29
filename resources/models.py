from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    # Ensure unique slugs
    def save(self):
        if not self.slug:
            self.slug = self.title.replace(" ", "-").lower()
        base_slug = self.slug
        counter = 1
        while Post.objects.filter(slug=self.slug).exists():
            self.slug = f"{base_slug}-{counter}"
            counter += 1

        super(Post, self).save()
