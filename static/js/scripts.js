// Bunny Chatbot
document.addEventListener("DOMContentLoaded", function() {
    const questions = [
        "Did you follow your diet plan today? 🥗",
        "Did you sleep on time yesterday? 😴",
        "Did you take time to relax your mind? 🧘‍♀️",
        "Did you avoid screens before bed? 📵"
    ];

    let currentQuestion = 0;

    const bunny = document.createElement('img');
    bunny.src = "/static/img/cute_bunny.png";
    bunny.alt = "Bunny";
    bunny.style.width = "150px";
    bunny.style.position = "fixed";
    bunny.style.bottom = "20px";
    bunny.style.right = "20px";
    document.body.appendChild(bunny);

    const messageBox = document.createElement('div');
    messageBox.style.position = "fixed";
    messageBox.style.bottom = "190px";
    messageBox.style.right = "20px";
    messageBox.style.background = "#fff8dc";
    messageBox.style.padding = "15px";
    messageBox.style.borderRadius = "10px";
    messageBox.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
    messageBox.style.fontFamily = "Poppins, sans-serif";
    messageBox.innerHTML = questions[currentQuestion];
    document.body.appendChild(messageBox);

    const nextBtn = document.createElement('button');
    nextBtn.innerText = "Next ➡️";
    nextBtn.style.marginTop = "10px";
    nextBtn.style.backgroundColor = "#ffb6b9";
    nextBtn.style.border = "none";
    nextBtn.style.padding = "10px";
    nextBtn.style.borderRadius = "5px";
    nextBtn.style.cursor = "pointer";
    messageBox.appendChild(document.createElement("br"));
    messageBox.appendChild(nextBtn);

    nextBtn.addEventListener("click", function() {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            messageBox.innerHTML = questions[currentQuestion];
            messageBox.appendChild(document.createElement("br"));
            messageBox.appendChild(nextBtn);
        } else {
            messageBox.innerHTML = "🎉 Great job! Keep it up! 🎉";
        }
    });
});
