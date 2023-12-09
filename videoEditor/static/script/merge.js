document.addEventListener('DOMContentLoaded',function(){
    videoTools = document.querySelector(".videoTools")
        videoTools.addEventListener("mouseover",function(){
            const videoTool = document.getElementById("videoToolsList")
            videoTool.style.display = ""

        })
        videoTools.addEventListener("mouseout",function(){
            const vidToolList = document.getElementById("videoToolsList")
            vidToolList.style.display = "none";
        })
        audioTools = document.querySelector(".audioTools")
        audioTools.addEventListener("mouseover",function(){
            const audioToolsList = document.getElementById("audioToolsList")
            audioToolsList.style.display = ""
        })
        audioTools.addEventListener("mouseout",function(){
            const audioToolsList = document.getElementById("audioToolsList")
            audioToolsList.style.display = "none"
        })
    bubbleMainP = document.getElementById("bubbleMainP")
    if (bubbleMainP){
        console.log("k2",bubbleMainP)
        bubbleMainP.addEventListener("click",function(){
            console.log("k1")
            const uploadVideo = document.getElementsByClassName("uploadVideo")
            const bubbleMain = document.getElementsByClassName("bubbleMain")

            bubbleMain[0].style.display="none"
            uploadVideo[0].style.display = ""

        })
    }
    bubbleVideoUploadH4 = document.getElementById("bubbleVideoUploadH4")
    if (bubbleVideoUploadH4){
        bubbleVideoUploadH4.addEventListener("click",function(){
            const uploadVideo = document.getElementsByClassName("uploadVideoBubble")

            uploadVideo[0].style.display = ""
            bubbleVideoUploadH4.style.display = "none"

        })
    }
    SaveOrCancelP = document.getElementById("SaveOrCancelP")
    if (SaveOrCancelP){
        SaveOrCancelP.addEventListener("click",function(){
            document.getElementById("cancelClick").click();
        })
    }
   
    cancelIc = document.getElementById("cancelIc")
    if (cancelIc){
        cancelIc.addEventListener("click",function(){
            document.getElementById("cancelClickImg").click();
        })
    // BubbleEditorr.style.display = "none"
    }
        
});