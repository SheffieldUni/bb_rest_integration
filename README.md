Experimental Flask integration layer between Blackboard and systems that can't handle OAuth2 token generation/caching or emitting JSON. Translates XML into JSON and transparently handles OAuth2 authorization.

Runs under Python 3.5+.

Currently requires a separate Redis installation for caching OAuth2 access tokens, but other caches are supported by the underlying Flask code.
