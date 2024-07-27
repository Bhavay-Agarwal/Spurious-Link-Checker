const labels = document.querySelectorAll(".form-control label");

labels.forEach((label) => {
  label.innerHTML = label.innerText
    .split("")
    .map(
      (letter, idx) =>
        `<span style="transition-delay: ${idx * 50}ms">${letter}</span>`
    )
    .join("");
});

// Handle different views and api calls

const baseURL = "http://localhost:9000/check/";
const URL_REGEX = /^https:\/\/[0-9A-z.]+.[0-9A-z.]+.[a-z]+$/i;

const showSearching = () => {
  const searchingElement = document.createElement("div");
  searchingElement.classList.add("searching");
  searchingElement.textContent = "Searching...";
  document.body.appendChild(searchingElement);
};

const showSuccess = (message) => {
  const successElement = document.createElement("div");
  successElement.classList.add("success");
  successElement.textContent = message;
  
  const closeButton = document.createElement("button");
  closeButton.textContent = "Close";
  closeButton.addEventListener("click", () => {
    successElement.remove();
  });
  
  successElement.appendChild(closeButton);
  document.body.appendChild(successElement);
};

const showError = (message) => {
  const errorElement = document.createElement("div");
  errorElement.classList.add("error");
  errorElement.textContent = message;
  
  const closeButton = document.createElement("button");
  closeButton.textContent = "Close";
  closeButton.addEventListener("click", () => {
    errorElement.remove();
  });
  
  errorElement.appendChild(closeButton);
  document.body.appendChild(errorElement);
};

const removeWaitingState = () => {
  const waitingElement = document.querySelector(".searching");
  if (waitingElement) {
    waitingElement.remove();
  }
};

const crossOutWindows = () => {
  const windows = document.querySelectorAll(".success, .error");
  windows.forEach((window) => {
    window.style.textDecoration = "line-through";
  });
};

document
  .getElementById("urlForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const { url, selectBox: scanType } = Object.fromEntries(
      new FormData(e.target)
    );

    showSearching();

    const data = await fetch(`${baseURL}${scanType}?url=${url}`).catch(
      () => {}
    );
    if (!data) {
      showError(data.message);
      removeWaitingState();
      return;
    }

    showSuccess(data.result);
    removeWaitingState();
    crossOutWindows();
    return;
  });
