# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# Configures the endpoint
config :search_server, SearchServer.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "vy7yqRvUYwq5wEyCS2a1OPxpL6DJHF9kbqrjuQ2FKI+8a6r4a6jHjFsyulFf+1t/",
  render_errors: [view: SearchServer.ErrorView, accepts: ~w(html json)],
  pubsub: [name: SearchServer.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
