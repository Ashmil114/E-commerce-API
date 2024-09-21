from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import AllowAny, IsAuthenticated

from .utils import generate_otp
from datetime import datetime

from django.contrib.auth.models import User
from .models import tb_customer, tb_otp, tb_address
from .serializers import customer_serializer, address_serializer

from django_filters import rest_framework as filters
from .filter_set import AddressFilter


class test(APIView):
    def get(self, request):
        return Response("test")


class login_with_otp(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=customer_serializer)
    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response(
                {"error": "phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user_obj = User.objects.get(username=phone)
        except User.DoesNotExist:
            user_obj = User.objects.create(username=phone)

        try:
            tb_customer.objects.get(phone=phone, user=user_obj)
        except tb_customer.DoesNotExist:
            tb_customer.objects.create(phone=phone, user=user_obj)

        try:
            otp = tb_otp.objects.get(user=user_obj)
        except tb_otp.DoesNotExist:
            otp = tb_otp.objects.create(user=user_obj)

        if otp.number_of_time_try_to_otp == 0:
            wait_1_min = True

        else:
            last_otp_attempt_naive = otp.last_otp_attempt.replace(tzinfo=None)
            time_difference = datetime.now() - last_otp_attempt_naive
            wait_1_min = time_difference.total_seconds() > 60

        not_max_limit = otp.number_of_time_try_to_otp < int(settings.OTP_REPEAT_NUMBER)

        if not_max_limit:
            if wait_1_min:
                otp_code = generate_otp()
                otp.otp = otp_code
                otp.number_of_time_try_to_otp += 1
                otp.last_otp_attempt = datetime.now()
                otp.save()

                # TODO:  Add OTP Service Here
                # send_otp_email(email, otp_code)
                # send_otp_phone(phone_number, otp_code)

                return Response(
                    {
                        "message": "OTP will sent to your phone number shortly ",
                        "otp": otp_code,
                        "time": 60 * 1000,
                        "created_time": int(
                            otp.last_otp_attempt.replace(tzinfo=None).timestamp()
                        )
                        * 1000,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                if time_difference.total_seconds() <= 60:
                    time = 60 - time_difference.total_seconds()
                else:
                    time = 0
                return Response(
                    {
                        "message": "Try 1 min Later",
                        "time": int(time) * 1000,
                        "created_time": int(
                            otp.last_otp_attempt.replace(tzinfo=None).timestamp()
                        )
                        * 1000,
                    },
                    status=status.HTTP_200_OK,
                )  # noqa

        else:
            last_otp_attempt_naive = otp.last_otp_attempt.replace(tzinfo=None)
            time_difference = datetime.now() - last_otp_attempt_naive

            wait_2_hour = time_difference.total_seconds() > 7200
            if wait_2_hour:
                otp_code = generate_otp()
                otp.otp = otp_code
                otp.number_of_time_try_to_otp = 1
                otp.last_otp_attempt = datetime.now()
                otp.save()

                # TODO:  Add OTP Service Here
                # send_otp_email(email, otp_code)
                # send_otp_phone(phone_number, otp_code)

                return Response(
                    {
                        "message": "OTP will sent to your phone number shortly ",
                        "otp": otp_code,
                        "time": 60 * 1000,
                        "created_time": int(
                            otp.last_otp_attempt.replace(tzinfo=None).timestamp()
                        )
                        * 1000,
                    },
                    status=status.HTTP_200_OK,
                )
            if time_difference.total_seconds() <= 7200:
                time = 7200 - time_difference.total_seconds()
            else:
                time = 0
            return Response(
                {
                    "message": "MAX OTP LIMIT IS OVER, Try 2 Hours Later",
                    "time": int(time) * 1000,
                    "created_time": int(
                        otp.last_otp_attempt.replace(tzinfo=None).timestamp()
                    )
                    * 1000,
                },
                status=status.HTTP_200_OK,
            )  # noqa


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class validate_otp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp_code = request.data.get("otp")

        try:
            user_obj = User.objects.get(username=phone)
            otp = tb_otp.objects.get(user=user_obj)
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        otp_exp_10_min = (
            datetime.now().time().minute - otp.last_otp_attempt.time().minute < 10
        )

        if otp.otp == otp_code and otp_exp_10_min:
            token = get_tokens_for_user(user_obj)
            otp.otp = None
            otp.last_otp_attempt = None
            otp.number_of_time_try_to_otp = 0
            otp.save()

            return Response({"token": token}, status=status.HTTP_200_OK)
        else:

            return Response(
                {"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST
            )


class logout(APIView):
    def post(self, request):
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()
            return Response(
                {"message": "Logged out successfully."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": f"Error while logging out: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class user(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = tb_customer.objects.get(user=request.user)
            serializer = customer_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except tb_customer.DoesNotExist:
            return Response(
                {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        try:
            user = tb_customer.objects.get(user=request.user)
            serializer = customer_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except tb_customer.DoesNotExist:
            return Response(
                {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )


class create_address(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "alt_phone": {"type": "string"},
                    "city_or_town": {"type": "string"},
                    "pin": {"type": "string"},
                    "district": {"type": "string"},
                    "landmark": {"type": "string"},
                },
                "required": [
                    "name",
                    "phone",
                    "city_or_town",
                    "pin",
                    "district",
                    "landmark",
                ],
            }
        },
        responses={
            201: {"type": "object", "properties": {"message": {"type": "string"}}}
        },
    )
    def post(self, request):
        name = request.data.get("name")
        phone = request.data.get("phone")
        alt_phone = request.data.get("alt_phone")
        city_or_town = request.data.get("city_or_town")
        pin = request.data.get("pin")
        district = request.data.get("district")
        landmark = request.data.get("landmark")
        try:
            customer = tb_customer.objects.get(user=request.user)
        except tb_customer.DoesNotExist:
            return Response(
                {"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            tb_address.objects.create(
                customer=customer,
                name=name,
                phone=phone,
                alt_phone=alt_phone,
                city_or_town=city_or_town,
                pin=pin,
                district=district,
                landmark=landmark,
            )
            return Response(
                {"message": "Address Added Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class address_update_delete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = address_serializer
    queryset = tb_address.objects.all()


class address_list(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tb_address.objects.all()
    serializer_class = address_serializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AddressFilter

    def get_queryset(self):
        return tb_address.objects.filter(customer__user=self.request.user)
