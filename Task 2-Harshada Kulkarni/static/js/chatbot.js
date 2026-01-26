console.log("Chatbot JS loaded");

// ================== VOICE SETUP ==================
function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.rate = 1;
    speech.pitch = 1;
    speech.lang = "en-IN";
    window.speechSynthesis.speak(speech);
}

// ================== QUESTIONS ==================
const questions = [
    { id: "age", text: "What is your age?" },
    { id: "gender", text: "What is your gender?" },
    { id: "blood_group", text: "What is your blood group?" },
    { id: "weight", text: "What is your weight in kg?" },
    { id: "donated_before", text: "Have you donated blood before? (yes/no)" },
    { id: "donation_count", text: "How many times have you donated blood?" },
    { id: "last_donation", text: "When was your last blood donation? (days)" },
    { id: "chronic", text: "Do you have any chronic disease?" },
    { id: "surgery", text: "Have you had surgery in last 6 months?" },
    { id: "willing", text: "Are you willing to donate blood in future?" }
];


let currentQuestion = 0;
let answers = {};
let chatStarted = false;

// ================== TOGGLE CHAT ==================
function toggleChat() {
    console.log("Chat button clicked");

    const box = document.getElementById("chatbot-box");

    if (box.style.display === "block") {
        box.style.display = "none";
        return;
    }

    box.style.display = "block";

    if (!chatStarted) {
        addBotMessage("Hello! 😊 How can I help you today?");
        speak("Hello! How can I help you today?");
        setTimeout(() => askQuestion(), 1000);
        chatStarted = true;
    }
}

// ================== ASK QUESTION ==================
function askQuestion() {
    if (currentQuestion < questions.length) {
        const q = questions[currentQuestion].text;
        addBotMessage(q);
        speak(q);
    } else {
        finishChat();
    }
}


// ================== MESSAGE FUNCTIONS ==================
function addBotMessage(msg) {
    const chatBody = document.getElementById("chat-body");
    chatBody.innerHTML += `<div><b>Bot:</b> ${msg}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

function addUserMessage(msg) {
    const chatBody = document.getElementById("chat-body");
    chatBody.innerHTML += `<div><b>You:</b> ${msg}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

// ================== SEND MESSAGE ==================
function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim().toLowerCase();
    if (message === "") return;

    addUserMessage(message);
    const currentQ = questions[currentQuestion];
    answers[currentQ.id] = message;
    input.value = "";

    /* ===== CONDITIONAL LOGIC ===== */

    // AGE CHECK
    if (currentQ.id === "age") {
        if (parseInt(message) < 18) {
            addBotMessage("⚠️🩸 You are NOT eligible for blood donation (Age < 18) 😔");
            speak("You are not eligible for blood donation because age is less than eighteen");
        }
        currentQuestion++;
        return setTimeout(askQuestion, 800);
    }

    // DONATED BEFORE CHECK
    if (currentQ.id === "donated_before") {
        if (message === "no") {
            addBotMessage("Okay 👍 Skipping donation history questions.");
            speak("Okay, skipping donation history questions");
            currentQuestion += 3; // skip donation_count & last_donation
            return setTimeout(askQuestion, 800);
        }
    }

    // NORMAL FLOW
    currentQuestion++;
    setTimeout(askQuestion, 800);
}


// ================== FINAL RESPONSE ==================
function finishChat() {
    addBotMessage("Thank you for answering all questions ❤️");
    speak("Thank you for answering all questions");

    setTimeout(() => {
        if (parseInt(answers.age) < 18) {
            addBotMessage("❌🩸 Final Result: Not Eligible for Blood Donation 😔");
            speak("Final result. You are not eligible for blood donation");
        } else {
            addBotMessage("✅🩸 Final Result: You may be eligible for Blood Donation ❤️");
            speak("Final result. You may be eligible for blood donation");
        }
        console.log("User Answers:", answers);
    }, 1200);
}

