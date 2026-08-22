// Chrome loads this file when the extension popup opens.
// The popup is a normal HTML page, so we can access elements by their IDs.
const noticeText = document.getElementById("noticeText");
const fileUpload = document.getElementById("fileUpload");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");

// Show the selected file name. The File object is kept for a future API request.
fileUpload.addEventListener("change", () => {
  const selectedFile = fileUpload.files[0];
  fileName.textContent = selectedFile ? `Selected file: ${selectedFile.name}` : "";
});

// The Analyze button collects input and starts the frontend-only analysis flow.
analyzeBtn.addEventListener("click", analyzeNotice);

async function analyzeNotice() {
  // Read the current textarea value and optional selected File object.
  const text = noticeText.value.trim();
  const selectedFile = fileUpload.files[0];

  // A notice must be pasted or uploaded before analysis can begin.
  if (!text && !selectedFile) {
    showMessage("Please enter a notice or upload a PDF/image before analyzing.");
    return;
  }

  setLoading(true);
  result.hidden = true;

  try {
    // FUTURE FLASK API:
    // Replace the delay and dummyResponse below with a fetch call, for example:
    // const formData = new FormData();
    // formData.append("text", text);
    // if (selectedFile) formData.append("file", selectedFile);
    // const response = await fetch("http://localhost:5000/analyze", {
    //   method: "POST",
    //   body: formData
    // });
    // const apiResponse = await response.json();

    await delay(800);
    const dummyResponse = {
      verdict: "Fake",
      confidence: "High",
      reasons: ["Unofficial domain", "Urgent payment request", "Suspicious contact method"]
    };

    // The future Flask response uses the same verdict, confidence, and reasons fields.
    displayResult(dummyResponse);
  } catch (error) {
    console.error("Notice analysis failed:", error);
    showMessage("Unable to analyze the notice. Please try again.");
  } finally {
    setLoading(false);
  }
}

function setLoading(isLoading) {
  loading.hidden = !isLoading;
  analyzeBtn.disabled = isLoading;
  analyzeBtn.textContent = isLoading ? "Analyzing..." : "Analyze Notice";
}

function displayResult(analysis) {
  // This works for Fake, Suspicious, Likely Genuine, or any future verdict value.
  result.replaceChildren();

  const verdict = document.createElement("p");
  verdict.textContent = `Verdict: ${analysis.verdict}`;
  const confidence = document.createElement("p");
  confidence.textContent = `Confidence: ${analysis.confidence}`;
  const reasonsTitle = document.createElement("p");
  reasonsTitle.textContent = "Reasons:";
  const reasonsList = document.createElement("ul");

  analysis.reasons.forEach((reason) => {
    const item = document.createElement("li");
    item.textContent = reason;
    reasonsList.appendChild(item);
  });

  result.append(verdict, confidence, reasonsTitle, reasonsList);
  result.hidden = false;
}

function showMessage(message) {
  result.textContent = message;
  result.hidden = false;
}

function delay(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}
