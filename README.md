[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/kTiXaL2K)
# API Design - Final Project

## Installation & Setup
To get started, you will need to have Python 3.12.0 installed on your machine. If you don't have them installed, you can download them from the official website: https://www.python.org/downloads/

## Pytest installation
Use pip to install pytest and pytest-cov.

```bash
pip install pytest pytest-cov
```
## Setup for ApolloServer (GraphQL)

const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');
const fs = require('fs');

const port = 4000;
const path = '/graphql';

const app = express();

const typeDefs = gql(fs.readFileSync('./schema.graphql', { encoding: 'utf8' }));

const resolvers = require('./resolvers');

async function startServer() {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    formatError: (error) => ({
      message: error.message
    }),
  });

  await server.start();
  server.applyMiddleware({ app, path });
}

startServer();

app.listen(port, () => console.info(`Server started on port ${port}`));
=======
## Installation & Setup
To get started, you will need to have Python 3.12.0 installed on your machine. If you don't have them installed, you can download them from the official website: https://www.python.org/downloads/

## Pytest installation
Use pip to install pytest and pytest-cov.

```bash
pip install pytest pytest-cov
```
>>>>>>> main

