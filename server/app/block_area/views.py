from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tb_block_district, tb_block_pincode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class test(APIView):
    def get(self, request):
        return Response("Block area test pong")


class check_block_area(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        district = request.GET.get("district")
        pincode = request.GET.get("pincode")
        data = {
            "is_blocked": False,
            "reason": "",
        }
        try:
            try:
                if district:
                    district_obj = tb_block_district.objects.get(
                        district__iexact=district.lower()
                    )
                    data["is_blocked"] = True
                    data["reason"] = "District is Blocked : " + district_obj.reason
                    return Response({"message": data}, status=status.HTTP_200_OK)
            except tb_block_district.DoesNotExist:
                data["is_blocked"] = False
                data["reason"] = ""
            try:
                if pincode:
                    pincode_obj = tb_block_pincode.objects.get(pincode__iexact=pincode)
                    data["is_blocked"] = True
                    data["reason"] = "Pincode is Blocked : " + pincode_obj.reason
                    return Response({"message": data}, status=status.HTTP_200_OK)

            except tb_block_pincode.DoesNotExist:
                data["is_blocked"] = False
                data["reason"] = ""

            return Response({"message": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
