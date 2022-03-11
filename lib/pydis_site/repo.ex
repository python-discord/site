defmodule PydisSite.Repo do
  use Ecto.Repo,
    otp_app: :pydis_site,
    adapter: Ecto.Adapters.Postgres
end
