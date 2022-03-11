defmodule PydisSiteWeb.PageController do
  use PydisSiteWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
