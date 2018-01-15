defmodule SearchServer.PageController do
  use SearchServer.Web, :controller

  def index(conn, _params) do
    render conn, "index.html"
  end

  def search(conn, _params) do
    phrase = conn.params["phrase"]
    resc = conn.params["resc"]
    use_noise_reduction? = conn.params["noise_reduction"] |> String.to_existing_atom()
    case run_search(phrase, resc, use_noise_reduction?) do
      {:error, msg} ->
        json conn, %{is_correct: false, error_msg: msg}
      results ->
        json conn, %{is_correct: true, results: results |> Enum.map(fn(x) -> result_to_map(x) end)}
    end
  end


  def run_search(phrase, count, false) do
    {res_string, exit_code} = System.cmd("python3", ["priv/engine/search.py", phrase, count])
    case exit_code do
      0 ->
        res_string |> form_result()
      24 ->
        {:error, "Indices are not generated"}
    end
  end
  def run_search(phrase, count, true) do
    {res_string, exit_code} = System.cmd("python3", ["priv/engine/search.py", phrase, count, "--use-noise-reduction-indices"])
    case exit_code do
      0 ->
        res_string |> form_result()
      24 ->
        {:error, "Indices are not generated"}
    end
  end

  def form_result(res_string) do
    res_string |>
        String.trim("\n") |>
        String.split("#") |>
        Enum.map(fn(x) -> split_single_result(x) end) |>
        Enum.drop(-1) |> #At the end empty string, so dropping it
        Enum.map(fn ({file, corr}) -> {change_contents_for_html(file), corr} end)
  end

  def change_contents_for_html(file) do
    file 
    |> String.replace("/contents/", "/htmls/")
    |> String.replace(".txt", ".html")
  end

  def split_single_result(s) do
    [h | t] = String.split(s, "$")
    {h, t}
  end

  def result_to_map({path, [corr]}) do
    {corrf, ""} = Float.parse(corr)
    [filename] = path |> String.split("/")
         |> Enum.take(-1)
    [id] = filename
         |> String.split(".")
         |> Enum.take(1)
    {idint, ""} = Integer.parse(id)
    %{correctness: corrf, path: path |> make_relative(), pageid: idint}
  end

  def make_relative(s) do
    {_, path} = s |> String.split_at(13)
    path
  end


end
