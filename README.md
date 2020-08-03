# Aiven Coding Challenge

## Setup

The easiest way to run the project would be on a Linux OS with `docker` and `docker-compose` installed.

There are some manual steps for setting up the environment:

- Create copies of the relevant `*.sample` environment files (`.env.sample` in the root, as well as the `.env.*.sample` files in the `env` folder)
- Set the proper values for the Kafka, Zookeeper, and PostgreSQL instances
- Set the proper parameters for the producer in the `docker-compose.prod.yml` file
- Start both the producer and consumer with:

```bash
make run
```

Alternatively, use `make run-producer` or `make run-consumer` to start either of them separately.

Check out the `Makefile` for other recipes.

## Design decisions

I was trying to satisfy the following criteria (among others):

- Producer and Consumer components, able to run on separate systems
- The database writer should be able to handle a reasonable amount of checks over a longer period of time
- Tests included
- No ORM libraries, use raw SQL queries

Taking this into account, I made the following choices:

- A single code base that can be used either for the producer or the consumer. For this particular task it simplified the development somewhat, allowing to use the same ORM-related code, and easier writing of the integration tests. However, for production, I would consider separate code bases, while putting the common code, or infrastructure into packages.
- I included a Dead Letter Queue Handler -- a simple class that stores messages from failed attempts to write to the database, and periodically tries to re-insert them.
- I dedicated a bit too much effort to the ORM related code. This was possibly a mistake, but I was surprised by the "no ORM" constraint, and I really don't like raw SQL queries around the code. I decided to use `pydantic` "dataclasses" for the models, and added a bit of boilerplate code to generate the SQL queries. However, in production I would definitely suggest to use an ORM, like SQLALchemy or something similar.

## Known Issues or Shortcommings

Here are the current TODOs:

- TODO: xdist doesn't play nice with session scoped fixtures
- TODO: combine the usage descriptions for all parsers in the root parser
- TODO: would have been nice to have these as class properties (instead of methods)
- TODO: the reason for the extra `description` is because `constr` could not be
- TODO: doesn't work when one of the tests fails
- TODO: write the test with a DLH
- TODO: write "end-to-end" tests

- Some of them are because of the hacky ORM-like code that I decided to use. I could have definitely written a bit simpler model with hardcoded SQL queries, but I liked the possibility to have some dynamic generation.
- I didn't write all the tests that I wanted to. I hit some unexpected bumps, mostly with docker-compose, and this took me more time than I expected. Still, I hope that the tests that are already there, showcase my skills and testing style sufficiently.
- The setup/teardown mechanism with pytest and the database does not work 100% smoothly, when it comes to parallelized testing, and when tests are failing. I would definitely look into this some more, If I've had the time.

## Final Note

In general, I had fun working on this task. I do think it's a bit on the more challenging side, especially with the wide range of requirements (probing a website with a regex, both a producer and a consumer, and writing to a database, plus tests and deployment in your platform) and the "no ORM" constraint. I haven't worked with Kafka before, so that was also a drawback in my case, but I'm happy about the opportunity, and I consider this as a decent crash-course into it.
