from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from core.models import EmailAccount, EmailAccountParsedData
from core.serializers import EmailAccountSerializer, EmailAccountParsedDataSerializer
from lib.custom.api_views import ListCreateRetrieveViewSet
from lib.custom.exceptions import BadRequest
from lib.custom.paginations import PageNumberPagination
from service.gmail_parser.fetch_emails import ParseGmail
from core.tasks import extract_content_from_gmail_task


class EmailAccountViewSet(ListCreateRetrieveViewSet):
    queryset = EmailAccount.objects.all()
    serializer_class = EmailAccountSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        mandatory_attrs = ["user", "password", "sender"]
        for attr in mandatory_attrs:
            if not request.data.get(attr):
                raise BadRequest({"error": f"{attr} is required."})
        parsed_data = ParseGmail(request.data['user'], request.data['password'], request.data['sender']).parse()
        if parsed_data:
            parsed_data_new = [item for item in parsed_data if
                           item.get("message_id") and not EmailAccountParsedData.objects.filter(
                               message_id=item.get("message_id"), account__sender=request.data['sender'],
                               account__user=request.data["user"]).exists()]
            if parsed_data_new:
                with transaction.atomic():
                    if self.queryset.filter(user=request.data["user"], sender=request.data["sender"]).exists():
                        account = self.queryset.filter(user=request.data["user"], sender=request.data["sender"]).latest()
                    else:
                        serializer = self.get_serializer(data={
                            "user": request.data["user"],
                            "sender": request.data["sender"]
                        }
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        account = serializer.instance

                    # create parsed data
                    pd_obj_ids = []
                    for data in parsed_data_new:
                        data["account"] = account.id
                        parsed_data_serializer = EmailAccountParsedDataSerializer(data=data)
                        parsed_data_serializer.is_valid(raise_exception=True)
                        parsed_data_serializer.save()
                        pd_obj_ids.append(parsed_data_serializer.instance.id)

                extract_content_from_gmail_task.delay(pd_obj_ids)
                return Response(self.serializer_class(account, expand="parsed_data").data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No New Record Found."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Record Found."}, status=status.HTTP_200_OK)