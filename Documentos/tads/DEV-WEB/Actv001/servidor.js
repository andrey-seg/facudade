const express = require("express");
const app = express();
const path = require("path");

app.use(express.static(path.join(__dirname)));

const server = app.listen(3000, '0.0.0.0', function(){
    console.log("Servidor sendo executado em http://localhost:3000");
});

server.on('error', function(err){
    console.log("Erro:", err);
});

process.on('SIGINT', function(){
    console.log("Servidor encerrado");
    process.exit();
});