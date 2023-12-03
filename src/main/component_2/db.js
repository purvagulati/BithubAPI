const persons =[{
  id: "user001",
  username: "alice@script.com",
  age: 34,
  name: "Alice"
 },{
  id: "user002",
  username: "makky@try.com",
  age: 31,
  name: "Makky"
 }]
const posts = [{
  id: "01",
  userID: "user001",
  name: "An introduction to GraphQL"
 },{
  id: "012",
  userID: "user002",
  name: "Javascript for beginners"
 },{
  id: "03",
  userID: "user001",
  name: "Modular GraphQL"
 },{
  id: "055",
  userID: "user002",
  name: "Learn Reactjs"
 },{
  id: "0123",
  userID: "user002",
  name: "Angular vs Reactjs"
}]


module.exports = {
persons,
posts
}
