document.addEventListener("DOMContentLoaded",function(){
    document.querySelector(".txtAndImgBannerTxtP").addEventListener("click",function(){
        const recorder = document.querySelector(".recorder")
        const video = document.getElementById("video")
        let mediaRecorder;
        let recordedChunks = [];
        recorder.style.display = "" 

        navigator.mediaDevices.getUserMedia({video:true})
        .then((stream)=>{
            video.src = stream

            mediaRecorder = new MediaRecorder(stream)
            mediaRecorder.ondataavailable = (event)=>{
                if(event.data.size > 0)
                {
                    recordedChunks.append(event.data)
                }
            }
            mediaRecorder.onstop = ()=>{
                const blob = new Blob(recordedChunks, {type: "video/webm"})
                const url = url.createObjectURL(blob)

                video.src = url
            }
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });
    })
})