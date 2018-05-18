from pysite.base_route import RouteView


class JamsSignupView(RouteView):
    path = "/jams/signup"
    name = "jams.signup"

    def get(self):
        return self.render("main/jams/signup.html")
