from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Member, TransactionRecord
from .serializers import BookSerializer, MemberSerializer, BorrowReturnActionSerializer


# --- 1. HTML Frontend View ---
def home(request):
    if request.method == "POST":
        action_type = request.POST.get("action_type")
        member_id = request.POST.get("member_id")
        book_id = request.POST.get("book_id")

        try:
            member = Member.objects.get(member_id=member_id)
            book = Book.objects.get(book_id=book_id)
        except (Member.DoesNotExist, Book.DoesNotExist):
            messages.error(request, "Invalid Member ID or Book ID.")
            return redirect("home")

        if action_type == "borrow":
            if not book.available:
                messages.error(request, f"'{book.title}' is already borrowed.")
            elif member.borrowed_books.count() >= 3:
                messages.error(request, "Borrow limit reached (maximum 3 books allowed).")
            else:
                with transaction.atomic():
                    member.borrowed_books.add(book)
                    book.available = False
                    book.save()
                    TransactionRecord.objects.create(member=member, book=book)
                messages.success(request, f"'{book.title}' borrowed successfully by {member.name}.")

        elif action_type == "return":
            if not member.borrowed_books.filter(pk=book.pk).exists():
                messages.error(request, f"{member.name} has not borrowed '{book.title}'.")
            else:
                late_days = int(request.POST.get("late_days", 0) or 0)
                fee = TransactionRecord.calculate_late_fee(late_days)
                with transaction.atomic():
                    member.borrowed_books.remove(book)
                    book.available = True
                    book.save()
                    record = TransactionRecord.objects.filter(
                        member=member, book=book, returned_at__isnull=True
                    ).order_by("-borrowed_at").first()
                    if record:
                        record.returned_at = timezone.now()
                        record.late_fee = fee
                        record.save()
                msg = f"'{book.title}' returned successfully."
                if fee > 0:
                    msg += f" Late fee charged: Rs. {fee} ({late_days} days late)."
                messages.success(request, msg)

        return redirect("home")

    books = Book.objects.all().order_by("book_id")
    members = Member.objects.prefetch_related("borrowed_books").all().order_by("member_id")
    available_books = Book.objects.filter(available=True)

    context = {
        "books": books,
        "members": members,
        "available_books": available_books,
    }
    return render(request, "home.html", context)


# --- 2. DRF API ViewSets ---
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.prefetch_related('borrowed_books').all()
    serializer_class = MemberSerializer


class LibraryViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow_book(self, request):
        serializer = BorrowReturnActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_id = serializer.validated_data['member_id']
        book_id = serializer.validated_data['book_id']

        try:
            member = Member.objects.get(member_id=member_id)
            book = Book.objects.get(book_id=book_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if not book.available:
            return Response({"error": "Book already borrowed."}, status=status.HTTP_400_BAD_REQUEST)
        if member.borrowed_books.count() >= 3:
            return Response({"error": "Max limit of 3 books reached."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            member.borrowed_books.add(book)
            book.available = False
            book.save()
            TransactionRecord.objects.create(member=member, book=book)

        return Response({"message": f"'{book.title}' borrowed successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='return-book')
    def return_book(self, request):
        serializer = BorrowReturnActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_id = serializer.validated_data['member_id']
        book_id = serializer.validated_data['book_id']
        late_days = serializer.validated_data.get('late_days', 0)

        try:
            member = Member.objects.get(member_id=member_id)
            book = Book.objects.get(book_id=book_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if not member.borrowed_books.filter(pk=book.pk).exists():
            return Response({"error": "Member has not borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        fee = TransactionRecord.calculate_late_fee(late_days)
        with transaction.atomic():
            member.borrowed_books.remove(book)
            book.available = True
            book.save()
            record = TransactionRecord.objects.filter(
                member=member, book=book, returned_at__isnull=True
            ).order_by("-borrowed_at").first()
            if record:
                record.returned_at = timezone.now()
                record.late_fee = fee
                record.save()

        return Response({
            "message": f"'{book.title}' returned successfully.",
            "late_days": late_days,
            "late_fee": fee
        }, status=status.HTTP_200_OK)