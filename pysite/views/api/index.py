from pysite.base_route import APIView
from pysite.constants import ErrorCodes


class IndexView(APIView):
    path = "/"
    name = "api.index"

    def get(self):
        return self.error(ErrorCodes.unknown_route)
