<p align="center">
    <em>ARMA, high performance, easy to learn, fast to code, ready for production</em>
</p>

# A Real Mock API

ARMA is a set of packages for API mocking and contract testing with **OpenAPI v3.x**.

ARMA provides:

- **Mock Servers**: Life-like mock servers from any API specification document.
- **Validation Proxy**: Contract Testing for API consumers and developers.
- **Comprehensive API Specification Support**: OpenAPI v3.1, OpenAPI v3.0.

## Ways to Use ARMA

### Self-hosted ARMA

ARMA is an open-source HTTP server run from the command-line. It provides mocking, request validation, and content negotiation. Use it standalone tool or in continuous integration.

### Start Self-hosted ARMA

Update a_real_settings.json
```json
{
 "mock_api_swaggerUrl": "https//www.apitomock.com/doc/swagger.json",
 "update_on_start": true,
}
```

ARMA requires

- Docker-Compose >= 2.29.1

```bash
make arma/start
```
<p>
<p>
<p>


------
### [Click here to Full Documentation](https://dan5e3s6ares.github.io/arma/)
------



### 🏁 Help Others Utilize ARMA

If you're using ARMA for an interesting use case, [contact us](mailto:daniel@soaresmartins.com) for a case study. We'll add it to a list here. Spread the goodness 🎉

### 👏 Contributing

If you are interested in contributing to ARMA itself, check out our [contributing docs ⇗][contributing] and [code of conduct ⇗][code_of_conduct] to get started.

### 🎉 Thanks

ARMA is built on top of lots of excellent packages, and here are a few we'd like to say a special thanks to.

- [rocketry](https://rocketry.readthedocs.io/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
- [jsf](https://github.com/ghandic/jsf)
- [ruamel-yaml](https://yaml.readthedocs.io/en/latest/)
- [fastapi](https://fastapi.tiangolo.com/)

Check these projects out!

### 🌲 Sponsor ARMA by Planting a Tree

If you would like to thank us for creating ARMA, we ask that you [**buy the world a tree**](https://ecologi.com/stoplightinc).

[code_of_conduct]: CODE_OF_CONDUCT.md
[contributing]: CONTRIBUTING.md
[download-release]: https://github.com/stoplightio/prism/releases/latest
