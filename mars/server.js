const express = require("express");
const app = express();

app.use("/public", express.static(__dirname+"visual"))

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/visual/index.html");

})

app.listen(1336, () => {
  console.log("The server is up and running!");
});
