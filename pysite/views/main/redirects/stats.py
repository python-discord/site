from pysite.base_route import RedirectView


class StatsView(RedirectView):
    path = "/stats"
    name = "stats"
    page = "https://p.datadoghq.com/sb/ac8680a8c-c01b556f01b96622fd4f57545b81d568"
