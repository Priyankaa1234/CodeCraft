async function scanDocument() {
  const qrToken = document.getElementById("qrToken").value;
  const docId = document.getElementById("docId").value;
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Loading...";

  try {
    const response = await fetch("/api/verify-document/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ qr_token: qrToken, doc_id: docId })
    });

    const data = await response.json();
    if (data.success) {
      resultDiv.innerHTML = `<h3 class='font-semibold text-lg text-green-700 mb-2'>${data.file_name} (${data.type})</h3>
      <iframe src="${data.file_url}" class="w-full border rounded" height="500"></iframe>`;
    } else {
      resultDiv.innerHTML = <p class='text-red-600 font-medium'>${data.error}</p>;
    }
  } catch (err) {
    resultDiv.innerHTML = <p class='text-red-600 font-medium'>Request failed: ${err.message}</p>;
  }
}