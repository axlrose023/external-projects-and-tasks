# region				-----External Imports-----
import typing
import fastapi
import math
from django.db import models as django_models
from fastapi.exceptions import HTTPException

# endregion


class APIViewMixin:
    queryset = None
    lookup_field = "pk"

    async def get_queryset(self) -> django_models.QuerySet:
        return self.queryset.all()

    async def filter_queryset(
        self, queryset: django_models.QuerySet, filter_params: django_models.Q
    ) -> django_models.QuerySet:
        return queryset.filter(filter_params)

    async def get_object(
        self, lookup_value: typing.Any
    ) -> typing.Type[django_models.Model]:
        queryset = await self.get_queryset()
        obj = await queryset.filter(**{self.lookup_field: lookup_value}).afirst()

        if obj is None:
            raise HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Not found."
            )

        return obj

    async def create_object(self, **kwargs) -> typing.Type[django_models.Model]:
        return await self.queryset.model.objects.acreate(**kwargs)

    async def update_object(
        self, lookup_value: typing.Any, data: dict
    ) -> typing.Type[django_models.Model]:
        queryset = await self.get_queryset()
        queryset = queryset.filter(**{self.lookup_field: lookup_value})

        if not await queryset.aexists():
            raise HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Not found."
            )

        await queryset.aupdate(**data)

        return await queryset.afirst()

    async def delete_object(
        self, lookup_value: typing.Any
    ) -> typing.Type[django_models.Model]:
        queryset = await self.get_queryset()
        queryset = queryset.filter(**{self.lookup_field: lookup_value})

        if not await queryset.aexists():
            raise HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Not found."
            )

        return await queryset.adelete()
