from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer
from django.shortcuts import get_object_or_404


class SpyCatList(APIView):
    def get(self, request):
        spycats = SpyCat.objects.all()
        serializer = SpyCatSerializer(spycats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpyCatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpyCatDetail(APIView):
    def get(self, request, pk):
        spycat = get_object_or_404(SpyCat, pk=pk)
        serializer = SpyCatSerializer(spycat)
        return Response(serializer.data)

    def patch(self, request, pk):
        spycat = get_object_or_404(SpyCat, pk=pk)
        serializer = SpyCatSerializer(spycat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        spycat = get_object_or_404(SpyCat, pk=pk)
        spycat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MissionList(APIView):
    def get(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissionDetail(APIView):
    def get(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        serializer = MissionSerializer(mission)
        return Response(serializer.data)

    def patch(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        serializer = MissionSerializer(mission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        if mission.cat is not None:
            return Response(
                {"error": "Cannot delete a mission assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        mission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MissionAssignCat(APIView):
    def post(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        if mission.is_complete:
            return Response(
                {"error": "Cannot assign a cat to a completed mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        cat_id = request.data.get('cat_id')
        if not cat_id:
            return Response({"error": "cat_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        cat = get_object_or_404(SpyCat, pk=cat_id)
        if Mission.objects.filter(cat=cat, is_complete=False).exists():
            return Response(
                {"error": "Cat is already assigned to an active mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        mission.cat = cat
        mission.save()
        return Response({"status": "Cat assigned to mission."}, status=status.HTTP_200_OK)


class MissionComplete(APIView):
    def post(self, request, pk):
        mission = get_object_or_404(Mission, pk=pk)
        if mission.is_complete:
            return Response(
                {"error": "Mission is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        incomplete_targets = mission.targets.filter(is_complete=False)
        if incomplete_targets.exists():
            return Response(
                {"error": "All targets must be completed before completing the mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        mission.is_complete = True
        mission.save()
        return Response({"status": "Mission marked as complete."}, status=status.HTTP_200_OK)


class TargetList(APIView):
    def get(self, request):
        targets = Target.objects.all()
        serializer = TargetSerializer(targets, many=True)
        return Response(serializer.data)


class TargetDetail(APIView):
    def get(self, request, pk):
        target = get_object_or_404(Target, pk=pk)
        serializer = TargetSerializer(target)
        return Response(serializer.data)

    def patch(self, request, pk):
        target = get_object_or_404(Target, pk=pk)
        serializer = TargetSerializer(target, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TargetComplete(APIView):
    def post(self, request, pk):
        target = get_object_or_404(Target, pk=pk)
        if target.is_complete:
            return Response(
                {"error": "Target is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if target.mission.is_complete:
            return Response(
                {"error": "Cannot complete a target of a completed mission."},
                status=status.HTTP_400_BAD_REQUEST
            )
        target.is_complete = True
        target.save()
        return Response({"status": "Target marked as complete."}, status=status.HTTP_200_OK)
