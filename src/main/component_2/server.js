const express = require('express');
const {ApolloServer, gql} = require('apollo-server-express');
const fs = require('fs');

const port = 4000;
const path = '/graphql';

const app = express();

const typeDefs = gql(fs.readFileSync('./schema.graphql', {encoding: 'utf8'}));

const resolvers = require('./resolvers');

// let server = null;

async function startServer() {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
  });

  await server.start();
  server.applyMiddleware({app, path});
}

startServer();

app.listen(port, () => console.info(`Server started on port ${port}`));
