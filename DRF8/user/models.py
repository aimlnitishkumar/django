from django.db import models

class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.book_id})"


class Member(models.Model):
    member_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    borrowed_books = models.ManyToManyField(Book, blank=True, related_name="borrowed_by")

    def __str__(self):
        return f"{self.name} (ID: {self.member_id})"


class TransactionRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    @staticmethod
    def calculate_late_fee(late_days):
        return late_days * 10

    def __str__(self):
        return f"{self.member.name} - {self.book.title}"