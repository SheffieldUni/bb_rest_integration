First try at a Flask integration layer between SITS and MOLE. Translates SITS's XML into JSON and handles OAuth2 authorization.

Runs under Python 3.5+ and Flask. 

Currently requires a separate Redis installation for caching OAuth2 access tokens, but other caches are supported by the underlying Flask code.
