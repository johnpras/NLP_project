//load navigation bar
fetch('navigation.html')
.then(response => response.text())
.then(content => {
    document.getElementById('navigation-bar').innerHTML = content;
});

function updateIndex(obj) {
    var name = obj.id;
    
    if(name == "body1-left-button"){
        location.replace('/indexsum.html');
    }

    if(name == "body2-left-button"){
        location.replace('/indexsen.html');
    }

    if(name == "body3-left-button"){
        location.replace('/indexpar.html');
    }
}

function summarysend(){

    //loader while waiting for the data
    document.getElementsByClassName("loader")[0].style.display = "block";
    var elms = document.getElementsByClassName('collapsible-boxes-wrapper')[0];
    elms.style.opacity = "0";
    document.getElementById("getresults_button_sum").disabled = true;

    const text = document.getElementById('input_text_area_sum').value;
    console.log(text);
    if (!text) {
        alert("Please enter some text to continue.");
        document.getElementsByClassName("loader")[0].style.display = "none";
		return false;
	}

    const socket = new WebSocket('ws://localhost:8000');

    var itemstosend = {
        "text": text,
        "scriptName": "summary"
    }
    socket.onopen = () => {
        socket.send(JSON.stringify(itemstosend));
    };

    socket.onmessage = function (event) {
        
        console.log(event.data);

        //keywords
        const json = JSON.parse(event.data);
        const extractKeywords = json.extract_keywords;

        var list = document.createElement("ul");

        extractKeywords.forEach(keyword => {
        const item = document.createElement("li");
        item.textContent = keyword;
        list.appendChild(item);
        });

        list.style.listStyleType = "circle";
        list.style.color="white"
        list.style.fontSize="24px";
        list.style.margin="10px 0;"

        const listBoxes = document.querySelectorAll('.list-box');
        document.getElementsByClassName('list-box')[0].appendChild(list);

        //keypoints
        const extractkeypoints = json.extract_keypoints;

        list = document.createElement("ul");

        extractkeypoints.forEach(keyword => {
        const item = document.createElement("li");
        item.textContent = keyword;
        list.appendChild(item);
        });

        list.style.listStyleType = "circle";
        list.style.color="white"
        list.style.fontSize="24px";
        list.style.margin="10px";

        document.getElementsByClassName('list-box')[1].appendChild(list);

        //summary
        const extractsummary = json.extract_summary;

        const paragr = document.createElement("p");
        paragr.style.color="white"
        paragr.style.fontSize="24px";
        paragr.textContent = extractsummary;
        document.getElementsByClassName('list-box')[2].appendChild(paragr);

        listBoxes[2].querySelector('p').style.display="none";


        //click behavior
        listBoxes[0].querySelector('h2').addEventListener('click', function() {
            listBoxes[0].querySelector('ul').classList.toggle('show');
        });
        listBoxes[1].querySelector('h2').addEventListener('click', function() {
            listBoxes[1].querySelector('ul').classList.toggle('show');
        });
        listBoxes[2].querySelector('h2').addEventListener('click', function() {
            listBoxes[2].querySelector('p').style.display = listBoxes[2].querySelector('p').style.display === 'none' ? 'block' : 'none';
        });

        //release the button, remove the loader, display the data
        document.getElementById("getresults_button_sum").disabled = false;
        document.getElementsByClassName("loader")[0].style.display = "none";
        elms.style.opacity = "1";
      };
}

function sentimentsend(){

    document.getElementsByClassName("loader")[0].style.display = "block";
    document.getElementById("getresults_button_sen").disabled = true;
    const text = document.getElementById('input_text_area_sen').value;
    document.getElementById("resultstext").innerHTML = "";
    document.getElementById("divsentavg").innerHTML = "";

    console.log(text);

    if (!text) {
        alert("Please enter some text to continue.");
        document.getElementsByClassName("loader")[0].style.display = "none";
		return false;
	}

    const socket = new WebSocket('ws://localhost:8000');

    var itemstosend = {
        "text": text,
        "scriptName": "sentiment"
    }

    socket.onopen = () => {
        socket.send(JSON.stringify(itemstosend));
    };

    socket.onmessage = function (event) {
        
        console.log(event.data);
        const json = JSON.parse(event.data);

        const sentences = [];
        const sentimentlist = json.sentimentlist;
        const extractsentences = json.sentences;

        for (let i = 0; i < sentimentlist.length; i++) {
        let color;
        if (sentimentlist[i] === "positive") {
            color = "green";
        } else if (sentimentlist[i] === "neutral") {
            color = "grey";
        } else {
            color = "red";
        }
        sentences.push({
            text: extractsentences[i],
            color: color
        });
        }
          
        const container = document.createElement("div");

        sentences.forEach(sentence => {
        const sentenceElement = document.createElement("span");
        sentenceElement.innerText = sentence.text;
        sentenceElement.style.color = sentence.color;
        container.appendChild(sentenceElement);
        });


        document.getElementById("resultstext").innerHTML = "Here's a detailed view of the text's sentiment: <br><br>"
        document.getElementById("resultstext").appendChild(container);

        let positiveCount = 0;
        let negativeCount = 0;
        let neutralCount = 0;

        for (let sentiment of sentimentlist) {
        switch (sentiment) {
            case "positive":
            positiveCount++;
            break;
            case "negative":
            negativeCount++;
            break;
            case "neutral":
            neutralCount++;
            break;
            default:
            break;
        }
        }

        const totalCount = positiveCount + negativeCount + neutralCount;
        const averageSentiment = (positiveCount - negativeCount) / totalCount;

        console.log(averageSentiment);

        var sentintext;
        if (averageSentiment >= -1 && averageSentiment < -0.7) {
            sentintext= "<strong>Negative Sentiment</strong> <br>This text is composed of negative sentiment.";
        } else if (averageSentiment >= -0.7 && averageSentiment < -0.4) {
            sentintext= "<strong>Slightly Negative Sentiment</strong> <br>This text has a slight negative sentiment.";
        } else if (averageSentiment >= -0.4 && averageSentiment <= 0.4) {
            sentintext= "<strong>Neutral Sentiment</strong> <br>This text has a neutral sentiment.";
        } else if (averageSentiment > 0.4 && averageSentiment <= 0.7) {
            sentintext= "<strong>Slightly Positive Sentiment</strong> <br>This text has a slight positive sentiment.";
        } else if (averageSentiment > 0.7 && averageSentiment <= 1) {
            sentintext= "<strong>Positive Sentiment</strong> <br>This text is composed of positive sentiment.";
        }

        document.getElementById("divsentavg").innerHTML += sentintext;

        document.getElementById("divsentavg").style.width="fit-content"; 
        document.getElementById("divsentavg").style.padding="10px"; 
        document.getElementById("divsentavg").style.textAlign = "center";
        document.getElementById("divsentavg").style.fontSize = "18px";
        document.getElementById("divsentavg").style.fontFamily = "sans-serif";
        document.getElementById("divsentavg").style.borderRadius = "10px";
        document.getElementById("divsentavg").style.backgroundColor = "white";
        document.getElementById("divsentavg").style.color = "black";
        document.getElementById("divsentavg").style.marginLeft = "auto";
        document.getElementById("divsentavg").style.marginRight = "auto";
    
        document.getElementById("getresults_button_sen").disabled = false;
        document.getElementsByClassName("loader")[0].style.display = "none";
    };
}

//clear textarea (sentiment)
function clearres(){
    document.getElementById("input_text_area_sen").value = "";
}

//clear textarea (paraphrase)
function clearrespar(){
    document.getElementById("input_text_area_par").value = "";
}

function paraphrasesend(){

    document.getElementsByClassName("loader")[0].style.display = "block";
    document.getElementById("getresults_button_par").disabled = true;
    const text = document.getElementById('input_text_area_par').value;
    document.getElementById("divtextarea").style.opacity = "0";

    console.log(text);

    if (!text) {
        alert("Please enter some text to continue.");
        document.getElementsByClassName("loader")[0].style.display = "none";
		return false;
	}

    const socket = new WebSocket('ws://localhost:8000');

    var itemstosend = {
        "text": text,
        "scriptName": "paraphrase"
    }

    socket.onopen = () => {
        socket.send(JSON.stringify(itemstosend));
    };

    socket.onmessage = function (event) {
        
        console.log(event.data);
        const json = JSON.parse(event.data);
        const paraphrasedtext = json.paraphrased_text;

        document.getElementById("results_text_area_par").value = paraphrasedtext;

        document.getElementById("getresults_button_par").disabled = false;
        document.getElementsByClassName("loader")[0].style.display = "none";
        document.getElementById("divtextarea").style.opacity = "1";
    };
}

