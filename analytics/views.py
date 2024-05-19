from typing import Final

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing_extensions import assert_never

from analytics.models import BookingAnalytics


class BookingAnalyticsView(APIView):

    def __extract_request_data(self, request) -> dict:
        extracted_data = {}

        request_data: dict = request.data['data']['booking']
        extract_keys: Final[tuple[str, ...]] = ('amount', 'begin_date', 'end_date', 'realty_id')
        for extract_key in extract_keys:
            if extract_key in request_data:
                extracted_data[extract_key] = request_data[extract_key]
            else:
                extracted_data[extract_key] = None

        client_keys: Final[tuple[str, ...]] = ('email', 'fio', 'phone')
        if 'client' in request_data:
            client_request_data: dict = request_data['client']
            for key in client_keys:
                if key in client_request_data:
                    extracted_data[key] = client_request_data[key]
                else:
                    extracted_data[key] = None
        else:
            for key in client_keys:
                extracted_data[key] = None

        extracted_data['fullname'] = extracted_data['fio']
        del extracted_data['fio']

        extracted_data['apartment_id'] = extracted_data['realty_id']
        del extracted_data['realty_id']

        extracted_data['json_data'] = str(request.data).replace('\'', '"')

        return extracted_data

    def __create_booking_analytics(self, request: Request) -> None:
        new_record: BookingAnalytics = self.__extract_request_data(request)
        new_record.save()

    def __delete_booking_analytics(self, request: Request) -> None:
        pass

    def __update_booking_analytics(self, request: Request) -> None:
        pass

    def post(self, request):
        match request.data['action']:
            case 'create_booking':
                self.__create_booking_analytics(request)
            case 'delete_booking':
                self.__delete_booking_analytics(request)
            case 'update_booking':
                self.__update_booking_analytics(request)
            case _:
                return Response(status=400)

        return Response(status=200)
