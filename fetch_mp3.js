const puppeteer = require('puppeteer');
const fs = require('fs');
const https = require('https');

(async () => {
    // This is the direct CDN link to a public domain marching brass track similar to Indy
    const url = "https://cdn.pixabay.com/download/audio/2023/10/24/audio_33af640700.mp3?filename=heroic-demise-172733.mp3";
    const file = fs.createWriteStream("/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers/indy.mp3");
    
    https.get(url, function(response) {
      response.pipe(file);
      file.on('finish', function() {
        file.close();  
        console.log("Downloaded Indy!");
      });
    });
})();
