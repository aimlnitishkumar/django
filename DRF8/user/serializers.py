from rest_framework import serializers
from .models import Book, Member, TransactionRecord

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'available']


class MemberSerializer(serializers.ModelSerializer):
    borrowed_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ['member_id', 'name', 'borrowed_books']


class BorrowReturnActionSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)
    late_days = serializers.IntegerField(required=False, default=0, min_value=0)