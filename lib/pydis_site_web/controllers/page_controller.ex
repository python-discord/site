defmodule PydisSiteWeb.PageController do
  use PydisSiteWeb, :controller

  @repos [
    %{
      name: "bot",
      description: "The community bot for the Python Discord community",
      stargazers: 836,
      forks: 435,
      language: "Python"
    },
    %{
      name: "king-arthur",
      description: "King Arthur is the DevOps helper bot for Python Discord",
      stargazers: 8,
      forks: 4,
      language: "Python"
    },
    %{
      name: "metricity",
      description: "Advanced metric collection for the Python Discord server",
      stargazers: 28,
      forks: 13,
      language: "Python"
    },
    %{
      name: "sir-lancebot",
      description: "A Discord bot started as a community project for Hacktoberfest 2018, later evolved into an introductory project for aspiring new developers starting out with open source development.",
      stargazers: 174,
      forks: 216,
      language: "Python"
    },
    %{
      name: "site",
      description: "pythondiscord.com - A Phoenix and Bulma web application.",
      stargazers: 600,
      forks: 115,
      language: "Elixir"
    },
    %{
      name: "snekbox",
      description: "Easy, safe evaluation of arbitrary Python code",
      stargazers: 130,
      forks: 28,
      language: "Python"
    }
  ]

  def index(conn, _params) do
    conn
    |> assign(:repos, @repos)
    |> render("index.html")
  end
end
