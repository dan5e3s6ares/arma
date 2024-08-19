ARMA documentation
==================

:::{div} sd-text-center sd-font-italic sd-text-primary
   ARMA, high performance, easy to learn, fast to code, ready for production
:::
## A Real Mock API


::::{div} sd-text-justify

ARMA is a set of packages for API mocking and contract testing with **OpenAPI v3.x**.

ARMA provides:

- **Mock Servers**: Life-like mock servers from any API specification document. {octicon}`alert-fill;1em;sd-text-info`Future!
- **Validation Proxy**: Contract Testing for API consumers and developers.
- **Comprehensive API Specification Support**: OpenAPI v3.1, OpenAPI v3.0.

## Mocking
The term "mock" for a lot of developers will have unit-testing connotations.
In unit-testing, a mock is a fake implementation of a class or function, which accepts the same arguments as the real thing.
It might return something pretty similar to expected output, and different test cases might even modify those returns to see how the code under test works.

This is almost exactly the concept here, just at a HTTP level instead.
This is done using a mock server, which will respond to the expected endpoints, error for non-existent endpoints, often even provide realistic validation errors if a client sends it an invalid request.

ARMA can be given an OpenAPI v3 description document, which is essentially a data source for all the decisions ARMA makes.

### Validation Proxy
Mocking helps when there is no real API and helps API consumers feel confident they're building applications that will work with the API.
Then, when the API has been built, ARMA can continue to help by sending proxy requests to the real server and reporting if anything is different.

Running ARMA on the CLI with ARMA proxy openapi.yml http://api.example.com/ will run a HTTP server similar to the mock, and it will use the same request validation logic as the mock server.

If the request is valid, it will make the same request to the upstream server provided in the CLI, and return its response. At this point, if the response is invalid against the API description provided, it can also error.

Basically, if the consumer makes an invalid request, or the server makes an invalid response, ARMA will let you know about it. It can log it, or blow up with errors, you decide which is useful for your use case.

Read more about this in the validation proxy guide.

Content Negotiation
ARMA provides strong support for mocking and validating REST APIs and most structured data types, such as JSON, XML, and URL-encoded forms.

The following content types aren't supported by ARMA:

Multipart requests and responses, such as multipart/form-data
Binary files, such as PDFs, image files, and zip archives
::::

```{toctree}
:maxdepth: 10
ways_to_use.md
mocking.md
scenarios.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
help.md
thanks.md
sponsor.md

```

