# SearchServer

To start your Phoenix app:

  * Install dependencies with `mix deps.get`
  * Install Node.js dependencies with `npm install`
  * Start Phoenix endpoint with `mix phoenix.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](http://www.phoenixframework.org/docs/deployment).

## Creating indices

Before running server you have to create indices. For the server to be useful you should create at least one kind of indices.
 To do so:
 * Go to project root
 * Type `python3 priv/engine/indexing.py [amount of documents to index] [--noise-reduction]`
 It will save those indices and then use them when user aqcquires search results
 
 ## Documents' location
 Documents should be placed in priv/static/

## Learn more

  * Official website: http://www.phoenixframework.org/
  * Guides: http://phoenixframework.org/docs/overview
  * Docs: https://hexdocs.pm/phoenix
  * Mailing list: http://groups.google.com/group/phoenix-talk
  * Source: https://github.com/phoenixframework/phoenix
