from django.db import models



class AuthorStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    RETIRED = 'retired', 'Retired'
    DECEASED = 'deceased', 'Deceased'

class Genre(models.TextChoices):
    FICTION = 'fiction', 'Fiction'
    NONFICTION = 'nonfiction', 'Non-fiction'
    SCIFI = 'sci-fi', 'Sci-Fi'
    FANTASY = 'fantasy', 'Fantasy'
    MYSTERY = 'mystery', 'Mystery'

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=10,
        choices=AuthorStatus.choices,
        default=AuthorStatus.ACTIVE,
    )

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    genre = models.CharField(
        max_length=20,
        choices=Genre.choices,
        default=Genre.FICTION,
    )
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
