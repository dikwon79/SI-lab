const targetURL = "http://127.0.0.1:8080" //DVWA is running on this port
const attackerServer = "http://127.0.0.1:5003" //server.js in backend is running on this port
const Levels = {
    low : "Low",
    medium : "Medium",
    high : "High",
    impossible : "Impossible"
}

module.exports ={targetURL, attackerServer, Levels}