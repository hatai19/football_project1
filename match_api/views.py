from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from match.models import Match
from match.forms import CommentForm
from accounts.models import Profile
from .serializers import MatchSerializer, ProfileSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib import messages
import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UpdateUserSerializer, UpdateProfileSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login


class MatchList(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['place']
    search_fields = ['place']

    def get_queryset(self):
        now = timezone.now()
        return Match.objects.filter(date__gt=now)


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all().order_by('-goals')
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PastMatchListAPIView(ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        now = timezone.now()
        return Match.objects.filter(date__lt=now).order_by('-date')


class JoinMatchAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        profile = request.user.profile
        today = datetime.date.today()
        match_date = match.date.date()

        if profile in match.players.all():
            return Response({'message': 'Вы уже присоединились к этому матчу.'}, status=status.HTTP_400_BAD_REQUEST)
        elif match_date < today:
            return Response({'message': 'Матч уже прошел.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            match.players.add(profile)
            messages.success(request, 'Вы успешно присоединились к матчу.')
            return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)


class MatchCommentAPI(APIView):
    @staticmethod
    def post(request, match_id):
        match = get_object_or_404(Match, id=match_id)
        comment = None
        form = CommentForm(data=request.data)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.match = match
            comment.save()
            return Response({'message': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UpdateUserSerializer(request.user)
        profile_serializer = UpdateProfileSerializer(request.user.profile)
        return Response({'user': user_serializer.data, 'profile': profile_serializer.data})

    def put(self, request):
        user_serializer = UpdateUserSerializer(request.user, data=request.data.get('user', {}), partial=True)
        profile_serializer = UpdateProfileSerializer(request.user.profile, data=request.data.get('profile', {}), partial=True)
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            return Response({'user': user_serializer.data, 'profile': profile_serializer.data})
        return Response({'user': user_serializer.errors, 'profile': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            remember_me = serializer.validated_data.get('remember_me')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True
                return Response({'message': 'User authenticated'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
