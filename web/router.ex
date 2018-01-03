defmodule SearchServer.Router do
  use SearchServer.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", SearchServer do
    pipe_through :browser # Use the default browser stack

    get "/", PageController, :index
    get "/search", PageController, :search
  end

  # Other scopes may use custom stacks.
  # scope "/api", SearchServer do
  #   pipe_through :api
  # end
end
