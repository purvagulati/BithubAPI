[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/kTiXaL2K)
# API Design - Final Project

## Setup for GraphQL

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
