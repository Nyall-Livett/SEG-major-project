from django.contrib.auth.mixins import LoginRequiredMixin
from clubs.enums import MomentType
from clubs.models import Moment
from django.views import View
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json


class CreateMomentView(LoginRequiredMixin, View):
    """docstring for CreateMomentView."""

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            moment_body = json.loads(request.POST.get('moment_body'))
            new_moment = Moment(
                body=moment_body,
                type=MomentType.CUSTOM,
                user=request.user
            )

            try:
                new_moment.full_clean()
                new_moment.save()
                json_username = json.dumps(new_moment.user.username)
                json_body = json.dumps(new_moment.body)
                return JsonResponse(
                {
                    'username': json_username,
                    'body': json_body,
                }, status=200)

            except ValidationError as e:
                return JsonResponse({}, status=400)
        raise PermissionDenied()
