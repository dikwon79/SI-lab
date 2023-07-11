const express = require('express')
const app = express()
const port = 5003

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.get('/session/:id', (req, res)=> {
    console.log("SessionID : ", req.params.id)  
    res.send("You've been hacked")
})
app.listen(port, () => {
  console.log(`Backend app listening on port ${port}`)
})