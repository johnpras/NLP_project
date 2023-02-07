const express = require('express');
const app = express();
const path = require('path');
const WebSocket = require('ws');
const http = require('http');
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static(path.join(__dirname, 'main')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'main/index.html'));
});

app.get('/sum', (req, res) => {
  res.sendFile(path.join(__dirname, 'main/indexsum.html'));
});

app.get('/sen', (req, res) => {
  res.sendFile(path.join(__dirname, 'main/indexsen.html'));
});

app.get('/par', (req, res) => {
  res.sendFile(path.join(__dirname, 'main/indexpar.html'));
});

let pythonProcess;

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    console.log(`Text received: ${message}`);

    const messageJson = JSON.parse(message);
    const text = messageJson.text;
    const scriptName = messageJson.scriptName;

    console.log(`Text received: ${text} ,from ${scriptName}`);

    const fs = require('fs');
    fs.writeFile("inputforpy.txt", text, (err) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log("Text saved to file.");
    });


    const spawn = require('child_process').spawn;

    switch (scriptName) {
        case 'summary':
          pythonProcess = spawn('/usr/bin/python3', ['summary.py', 'inputforpy.txt', 'output.txt']);
          break;
        case 'sentiment':
          pythonProcess = spawn('/usr/bin/python3', ['sentiment.py', 'inputforpy.txt', 'output2.txt']);
          break;
        case 'paraphrase':
          pythonProcess = spawn('/usr/bin/python3', ['paraphrase.py', 'inputforpy.txt', 'output3.txt']);
          break;
        default:
            console.error(`Unknown script name: ${scriptName}`);
            return;

      }

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Output from Python script: ${data}`);
      console.log(`Done.`);
    });


    pythonProcess.on('close', function (code, signal) {

      // Read the contents of the appropriate output file
      let outputFileName;
      switch (scriptName) {
        case 'summary':
          outputFileName = 'output.txt';
          break;
        case 'sentiment':
          outputFileName = 'output2.txt';
          break;
        case 'paraphrase':
          outputFileName = 'output3.txt';
          break;
        default:
          console.error(`Unknown script name: ${scriptName}`);
          return;
      }

      // Read the contents of the output file
      fs.readFile(outputFileName, 'utf8', function (err, data) {
        if (err) {
          console.error(err);
          return;
        }

        // Send the contents of the file to the HTML page
        ws.send(data);
      });
    });
  });

  ws.on('close', () => {
    console.log('Client disconnected');
    pythonProcess.kill('SIGINT');
  });
  
});




server.listen(8000, () => {
  console.log('Server started on http://localhost:8000');
});
