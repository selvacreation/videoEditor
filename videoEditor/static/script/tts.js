document.addEventListener("DOMContentLoaded",function(){
    var audioPlayer = document.getElementById('APBAudio');
    var audioBase64 = "{{ audio_base64 }}";
    audioPlayer.src = "data:audio/mp3;base64," + audioBase64;

    const Accent = document.querySelector(".Accent");
    Accent.addEventListener("mouseover",function(){
        const AccentList = document.getElementsByClassName("AccentList")
        const AmericanAL = document.getElementById("AmericanAL")
        const BritishAL = document.getElementById("BritishAL")
        const IndianAL = document.getElementById("IndianAL")
        const SpanishAL = document.getElementById("SpanishAL")
        const AccentP = document.querySelector(".AccentP")

        AccentList[0].style.display = ""
        AmericanAL.addEventListener("click",function(){
            AccentP.textContent = AmericanAL.textContent;
            AccentList[0].style.display = "none"
        })
        BritishAL.addEventListener("click",function(){
            AccentP.textContent = BritishAL.textContent;
            AccentList[0].style.display = "none"
        })
        IndianAL.addEventListener("click",function(){
            AccentP.textContent = IndianAL.textContent;
            AccentList[0].style.display = "none"
        })
        SpanishAL.addEventListener("click",function(){
            AccentP.textContent = SpanishAL.textContent;
            AccentList[0].style.display = "none"
        })
    })
    Accent.addEventListener("mouseout",function(){
        const AccentList = document.getElementsByClassName("AccentList")
        AccentList[0].style.display = "none"
    })

    const gender = document.querySelector(".gender");
    gender.addEventListener("mouseover",function(){
        const genderList = document.getElementsByClassName("genderList")
        const Male = document.getElementById("Male")
        const Female = document.getElementById("Female")
        const genderP = document.querySelector(".genderP")

        genderList[0].style.display = ""
        Male.addEventListener("click",function(){
            genderP.textContent = Male.textContent;
            genderList[0].style.display = "none"
        })
        Female.addEventListener("click",function(){
            genderP.textContent = Female.textContent;
            genderList[0].style.display = "none"
        })
    })
    gender.addEventListener("mouseout",function(){
        const genderList = document.getElementsByClassName("genderList")
        genderList[0].style.display = "none"
    })
    document.getElementById("GenerateButton").addEventListener("click",function(event){
        const genderP = document.querySelector(".genderP")
        const AccentP = document.querySelector(".AccentP")
        const Spam = document.getElementById("Spam")
        const GenerateTagAccent = document.getElementById("GenerateTagAccent")
        const GenerateTagGender = document.getElementById("GenerateTagGender")
        const GenerateTagText = document.getElementById("GenerateTagText")
        const InputlapBanner = document.getElementById("InputlapBanner")

        if(genderP.textContent == "Choose Gender" || AccentP.textContent == "Choose Accent"){
            console.log("yess!!")
            const APBAudio = document.getElementById("APBAudio")
            Spam.style.display = ""
            event.preventDefault();
            APBAudio.style.marginTop = "0px"
        }
        else{
            GenerateTagAccent.value = AccentP.textContent
            GenerateTagGender.value = genderP.textContent
            GenerateTagText.value = InputlapBanner.value
            console.log("GenerateTagText",GenerateTagText.value)
        }
    })
})