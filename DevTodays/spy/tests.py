from .models import SpyCat, Mission, Target
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class SpyCatTests(APITestCase):
    def setUp(self):
        self.spycat = SpyCat.objects.create(
            name="Whiskers", years_of_experience=3, breed="Siamese", salary=50000
        )
        self.spycat_url = reverse('spycat-detail', args=[self.spycat.pk])
        self.spycat_list_url = reverse('spycat-list')

    def test_get_spycat_list(self):
        response = self.client.get(self.spycat_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_spycat(self):
        data = {"name": "Mittens", "years_of_experience": 2, "breed": "Persian", "salary": 40000}
        response = self.client.post(self.spycat_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_spycat(self):
        response = self.client.get(self.spycat_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.spycat.name)

    def test_update_spycat(self):
        data = {"salary": "60000.00"}
        response = self.client.patch(self.spycat_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['salary'], "60000.00")

    def test_delete_spycat(self):
        response = self.client.delete(self.spycat_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SpyCat.objects.filter(pk=self.spycat.pk).exists())


class MissionTests(APITestCase):
    def setUp(self):
        self.spycat = SpyCat.objects.create(
            name="Whiskers", years_of_experience=3, breed="Siamese", salary=50000
        )
        self.mission = Mission.objects.create(cat=None, is_complete=False)
        self.mission_url = reverse('mission-detail', args=[self.mission.pk])
        self.mission_list_url = reverse('mission-list')

    def test_get_mission_list(self):
        response = self.client.get(self.mission_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_mission(self):
        data = {
            "cat": None,
            "targets": [{"name": "Target1", "country": "Country A", "notes": "", "is_complete": False}]
        }
        response = self.client.post(self.mission_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_mission(self):
        response = self.client.get(self.mission_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.mission.pk)

    def test_update_mission(self):
        data = {"is_complete": True}
        response = self.client.patch(self.mission_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_cat_to_mission(self):
        assign_url = reverse('mission-assign-cat', args=[self.mission.pk])
        response = self.client.post(assign_url, {"cat_id": self.spycat.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertEqual(self.mission.cat, self.spycat)

    def test_complete_mission(self):
        complete_url = reverse('mission-complete', args=[self.mission.pk])
        Target.objects.create(mission=self.mission, name="Target1", country="Country A", is_complete=True)
        response = self.client.post(complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertTrue(self.mission.is_complete)


class TargetTests(APITestCase):
    def setUp(self):
        self.spycat = SpyCat.objects.create(
            name="Whiskers", years_of_experience=3, breed="Siamese", salary=50000
        )
        self.mission = Mission.objects.create(cat=self.spycat)
        self.target = Target.objects.create(
            mission=self.mission, name="Target1", country="Country A", notes="", is_complete=False
        )
        self.target_url = reverse('target-detail', args=[self.target.pk])
        self.target_list_url = reverse('target-list')

    def test_get_target_list(self):
        response = self.client.get(self.target_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_target(self):
        response = self.client.get(self.target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.target.name)

    def test_update_target(self):
        data = {"notes": "Updated note"}
        response = self.client.patch(self.target_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], "Updated note")

    def test_complete_target(self):
        complete_url = reverse('target-complete', args=[self.target.pk])
        response = self.client.post(complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_complete)


class SpyCatBreedValidationTests(APITestCase):
    def test_create_spycat_with_valid_breed(self):
        data = {
            "name": "Whiskers",
            "years_of_experience": 2,
            "breed": "Siamese",
            "salary": 50000
        }
        url = reverse('spycat-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['breed'], "Siamese")

    def test_create_spycat_with_invalid_breed(self):
        data = {
            "name": "Shadow",
            "years_of_experience": 3,
            "breed": "Dragon",
            "salary": 55000
        }
        url = reverse('spycat-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('breed', response.data)
        self.assertEqual(
            response.data['breed'][0],
            "Invalid breed 'Dragon'."
        )
