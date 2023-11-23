document.addEventListener('DOMContentLoaded',function(){
    const trimVideoTagOpenFile = document.getElementById('trimVideoTagOpenFile')
    if (trimVideoTagOpenFile)
    {
        trimVideoTagOpenFile.addEventListener('click',()=>{
            const uploadVideo = document.getElementsByClassName('uploadVideo');
            const trimVideoTag = document.getElementsByClassName("trimVideoTag")

            console.log(uploadVideo[0])
            uploadVideo[0].style.display = ""
            trimVideoTag[0].style.display = "none"
            
        })
    }
    const trimPlayButton = document.getElementsByClassName("trimPlayButton")
    console.log("1",trimPlayButton)
    if(trimPlayButton)
    {
        trimPlayButton[0].addEventListener('click',()=>{
            console.log("2")
            const players = document.getElementById("videoPlayer")
            const trimDurationStartSec = document.getElementById("trimDurationStartSec")
            const startSec = trimDurationStartSec.value
            const trimDurationStopSec = document.getElementById("trimDurationStopSec")
            const stopSec = trimDurationStopSec.value

            var videoSource = players.querySelector("source");

            // Now, you can access the src attribute
            var videoSrc = videoSource.getAttribute("src");

            console.log(startSec)
            console.log(stopSec)

            fetch(videoSrc)
            .then(response => response.blob())
            .then(blob => {
                // Create an object URL from the Blob
                var blobUrl = URL.createObjectURL(blob);

                // Set the object URL as the source for the video element
                videoSource.src = blobUrl;
                console.log("123",videoSource.src)
                  trimmer();
            })
            .catch(error => {
                console.error("Error fetching video:", error);
            });



            function trimmer(){
            const player = document.getElementById("videoPlayer")
            var videoSource = videoPlayer.querySelector("source");

            // Now, you can access the src attribute
            var videoSrc = videoSource.getAttribute("src");

            // players.addEventListener("canplaythrough", function() {
            console.log("yes")
            console.log(videoSrc)
            player.currentTime = startSec
            player.play()
            //   });

            player.addEventListener("timeupdate", function() {
                if (player.currentTime >= stopSec) {
                  player.pause();
                }
              });
            }
        })
    }
    const output_trim = document.getElementById("output_trim");
    if (output_trim)
    {
        console.log("trim download")
        output_trim.click();
    }
    const cancelIc = document.getElementById("cancelIc")
    if (cancelIc)
    {
        cancelIc.addEventListener("click",()=>{
            document.getElementById("cancelClick").click();
        });
    }
});