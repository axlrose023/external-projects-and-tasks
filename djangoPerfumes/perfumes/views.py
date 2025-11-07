from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from perfumes.models import Perfume, Brand, Offer, Review, Category, ReviewReply
from perfumes.serializers import PerfumeSerializer, BrandSerializer, OfferSerializer, ReviewSerializer, \
    CategorySerializer, ReviewReplySerializer


@api_view(['GET'])
def perfume_list(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        brand_id = request.GET.get('brand_id')
        gender_id = request.GET.get('gender_id')

        # Start with all perfumes
        perfumes = Perfume.objects.all()

        # Apply filters as needed
        if category_id:
            perfumes = perfumes.filter(category__id=category_id)
        if brand_id:
            perfumes = perfumes.filter(brand__id=brand_id)
        if gender_id:
            perfumes = perfumes.filter(gender__id=gender_id)

        serializer = PerfumeSerializer(perfumes, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def perfume_detail(request, pk):
    """
    Retrieve, update or delete a perfume instance.
    """
    try:
        perfume = Perfume.objects.get(pk=pk)
    except Perfume.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PerfumeSerializer(perfume)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PerfumeSerializer(perfume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        perfume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def brand_list(request):
    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


class OfferAPIView(APIView):
    def get(self, request, perfume_id):
        perfume = get_object_or_404(Perfume, pk=perfume_id)
        offers = Offer.objects.filter(perfume=perfume)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        permission_classes([IsAuthenticated])
        serializer = OfferSerializer(data=request.data)
        user = Account.objects.get(email=request.data['seller'])
        if serializer.is_valid():
            offer = serializer.save(seller=user)

            # Send email notification
            subject = 'Your Offer Has Been Created'
            html_content = render_to_string('emails/email_offer_created.html', {'offer': offer})
            send_mail(
                subject,
                'An offer has been created.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                html_message=html_content,
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, offer_id):

        offer = Offer.objects.filter(pk=offer_id).first()

        if not offer:
            return Response({'detail': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def put(self, request, offer_id):
        user = request.user
        offer = Offer.objects.filter(seller=user, pk=offer_id).first()

        if not offer:
            return Response({'detail': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSerializer(offer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, offer_id):
        user = request.user
        offer = Offer.objects.filter(seller=user, pk=offer_id).first()

        if not offer:
            return Response({'detail': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def review_list_create(request, perfume_id, review_id=None):
    if request.method == 'GET':
        reviews = Review.objects.filter(perfume=perfume_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        permission_classes([IsAuthenticated])
        data = request.data.copy()
        review_data = data.pop('review', {})
        data.update(review_data)
        data['perfume'] = perfume_id
        print(data)
        serializer = ReviewSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        permission_classes([IsAuthenticated])
        review = get_object_or_404(Review, id=review_id, perfume=perfume_id)
        if request.user == review.user or request.user.is_staff:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to delete this review.'},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'DELETE'])
def review_replies(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'GET':
        replies = ReviewReply.objects.filter(review=review)
        serializer = ReviewReplySerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        permission_classes([IsAuthenticated])
        data_with_review = {**request.data, 'review': review_id}
        serializer = ReviewReplySerializer(data=data_with_review, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        permission_classes([IsAuthenticated])
        reply_id = request.query_params.get('reply_id')
        if not reply_id:
            return Response({'error': 'Missing reply_id query parameter'}, status=status.HTTP_400_BAD_REQUEST)

        reply = get_object_or_404(ReviewReply, id=reply_id, review=review)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
