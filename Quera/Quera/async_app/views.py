import asyncio
import json

import httpx
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Animal
from .serializers import AnimalSerializer


@csrf_exempt
async def create_animal(request):
    try:
        data = json.loads(request.body)
        animal = await Animal.objects.acreate(name=data['name'])
        return JsonResponse({'id': animal.pk})
    except asyncio.CancelledError:
        return JsonResponse({'error': 'Client Closed Request'}, status=499)


@csrf_exempt
async def get_animal(request):
    try:
        if request.method == 'GET':
            animal = await Animal.objects.aget(name=request.GET['name'])
            serializer = AnimalSerializer(animal)
            return JsonResponse(serializer.data, safe=False)
    except asyncio.CancelledError:
        return JsonResponse({'error': 'Client Closed Request'}, status=499)


class GetAnimal(View):
    async def get(self, request, *args, **kwargs):
        try:
            animal = await Animal.objects.aget(name=request.GET['name'])
            serializer = AnimalSerializer(animal)
            return JsonResponse(serializer.data, safe=False)
        except asyncio.CancelledError:
            return JsonResponse({'error': 'Client Closed Request'}, status=499)

    async def post(self, request, *args, **kwargs):
        try:
            await Animal.objects.acreate(name=request.data['name'])
        except asyncio.CancelledError:
            return JsonResponse({'error': 'Client Closed Request'}, status=499)


async def google_animal(request):
    return JsonResponse({'result': (await httpx.AsyncClient().get(f'https://www.google.com/?q={request.GET["name"]}')).text})

