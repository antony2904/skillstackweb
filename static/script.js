function toggleChat() {
  let box = document.getElementById("chatbot");
  box.style.display = (box.style.display === "none") ? "flex" : "none";
}

async function sendMessage() {
  let input = document.getElementById("chat-input");
  let message = input.value;
  if (!message) return;

  let chatBox = document.getElementById("chat-messages");
  chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`;
  input.value = "";

  let response = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: message})
  });

  let data = await response.json();
  chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}