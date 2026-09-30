from django.contrib import admin
from .models import Book, Member, TransactionRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'available')
    list_filter = ('available',)
    search_fields = ('title', 'author', 'book_id')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'name')
    search_fields = ('name', 'member_id')
    filter_horizontal = ('borrowed_books',)

@admin.register(TransactionRecord)
class TransactionRecordAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'borrowed_at', 'returned_at', 'late_fee')
    list_filter = ('borrowed_at', 'returned_at')