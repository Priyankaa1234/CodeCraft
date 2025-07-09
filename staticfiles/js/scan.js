function scanDocument() {
  console.log("scanDocument function loaded")
  const token = document.getElementById("token").value.trim();
  const docId = document.getElementById("docId").value.trim();
  const result = document.getElementById("result");
  const pdfFrame = document.getElementById("pdfFrame");

  if (!token || !docId) {
    result.innerHTML = '<span style="color:red;">❌ Please enter both access token and document ID.</span>';
    return;
  }

  result.innerHTML = "Loading...";
  pdfFrame.style.display = "none";

  fetch(`http://127.0.0.1:8000/api/scan/${docId}/`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  })
    .then(response => response.json().then(data => ({ status: response.status, data })))
    .then(({ status, data }) => {
      if (status === 200) {
        const fileUrl = `http://127.0.0.1:8000${data.file}`;
        result.innerHTML = `
          <strong>Type:</strong> ${data.type}<br>
          <strong>Patient ID:</strong> ${data.patient}<br>
          <strong>Document:</strong> <a href="${fileUrl}" target="_blank">Open</a>
        `;
        if (data.file.endsWith(".pdf")) {
          pdfFrame.src = fileUrl;
          pdfFrame.style.display = "block";
        }
      } else {
        result.innerHTML = <span style="color:red;">❌ Error: ${data.error || data.detail}</span>;
      }
    })
    .catch(err => {
      result.innerHTML = <span style="color:red;">❌ Network error: ${err.message}</span>;
    });
}